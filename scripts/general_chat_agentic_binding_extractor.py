#!/usr/bin/env python3
"""Evaluate a normalized synthetic agentic trace without reading raw runtime transcripts."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema
from referencing import Registry, Resource


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "docs/general-chat-agentic-capability-preflight-fixture-r1.json"
DEFAULT_INPUT_SCHEMA = ROOT / "docs/general-chat-agentic-binding-extractor-input.schema.json"
DEFAULT_OUTPUT_SCHEMA = ROOT / "docs/general-chat-agentic-binding-extractor-output.schema.json"
DEFAULT_RECEIPT_SCHEMA = ROOT / "docs/general-chat-agentic-capability-preflight-receipt.schema.json"
OUTPUT_SCHEMA_VERSION = "general-chat-agentic-binding-extraction/v1"
EXPECTED_TASK_IDENTITY = "parking_fact_check"
CRITERION_NAMES = (
    "root_thread_identity",
    "spawn_call_and_task_identity",
    "worker_packet_projection",
    "descendant_parent_and_task_binding",
    "descendant_terminal_sender_and_result",
    "root_tool_call_and_terminal_result",
    "final_response_direct_binding",
    "all_agent_final_usage",
    "monotonic_elapsed",
    "safe_projection_without_raw_transcript",
)


class ExtractionError(Exception):
    """A normalized synthetic input or schema could not be read."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ExtractionError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise ExtractionError(f"JSON value must be an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_value(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def state_for_cardinality(values: list[Any]) -> str | None:
    if not values:
        return "unobserved"
    if len(values) != 1:
        return "unsatisfied"
    return None


def expected_packet(fixture: dict[str, Any]) -> dict[str, Any]:
    worker = fixture["worker_material"]
    return {
        "task_identity": EXPECTED_TASK_IDENTITY,
        "record_id": worker["allowed_record_id"],
        "record": worker["allowed_record"],
        "required_result_shape": worker["required_result_shape"],
    }


def empty_usage(thread_id: str | None = None) -> dict[str, Any]:
    return {
        "thread_id": thread_id,
        "input_tokens": None,
        "cached_input_tokens": None,
        "output_tokens": None,
        "total_tokens": None,
    }


def projected_usage(session: dict[str, Any]) -> dict[str, Any]:
    return {
        "thread_id": session.get("thread_id"),
        "input_tokens": session.get("input_tokens"),
        "cached_input_tokens": session.get("cached_input_tokens"),
        "output_tokens": session.get("output_tokens"),
        "total_tokens": session.get("total_tokens"),
    }


def split_sentences(value: str) -> list[str]:
    return [item for item in value.split("。") if item]


def extract(trace: dict[str, Any], fixture: dict[str, Any]) -> dict[str, Any]:
    criteria = {name: "unobserved" for name in CRITERION_NAMES}
    root = trace["root"]
    usage_input = trace["usage"]
    raw_transcript_required = trace["projection"]["raw_transcript_required"]

    root_ids = root["thread_started"]
    root_id = root_ids[0] if len(root_ids) == 1 else None
    if not root_ids:
        criteria["root_thread_identity"] = "unobserved"
    elif len(root_ids) != 1 or root_id != usage_input.get("root_thread_id"):
        criteria["root_thread_identity"] = "unsatisfied"
    else:
        criteria["root_thread_identity"] = "satisfied"

    spawn_binding = {
        "call_id": None,
        "requested_task_identity": None,
        "returned_task_identity": None,
        "child_thread_id": None,
    }
    calls = root["spawn_calls"]
    results = root["spawn_results"]
    spawn_cardinality = state_for_cardinality(calls) or state_for_cardinality(results)
    if calls:
        spawn_binding["call_id"] = calls[0].get("call_id")
        spawn_binding["requested_task_identity"] = calls[0].get("requested_task_identity")
    if results:
        spawn_binding["returned_task_identity"] = results[0].get("returned_task_identity")
        spawn_binding["child_thread_id"] = results[0].get("child_thread_id")
    if spawn_cardinality is not None:
        criteria["spawn_call_and_task_identity"] = spawn_cardinality
    else:
        call = calls[0]
        result = results[0]
        required = (
            call.get("call_id"),
            call.get("requested_task_identity"),
            result.get("call_id"),
            result.get("returned_task_identity"),
            result.get("child_thread_id"),
        )
        if not all(isinstance(item, str) and item for item in required):
            criteria["spawn_call_and_task_identity"] = "unobserved"
        elif (
            call["call_id"] == result["call_id"]
            and call["requested_task_identity"] == EXPECTED_TASK_IDENTITY
            and result["returned_task_identity"] == EXPECTED_TASK_IDENTITY
        ):
            criteria["spawn_call_and_task_identity"] = "satisfied"
        else:
            criteria["spawn_call_and_task_identity"] = "unsatisfied"

    packet = calls[0].get("packet") if len(calls) == 1 else None
    expected = expected_packet(fixture)
    allowed_keys = set(expected)
    packet_projection = None
    packet_sha256 = sha256_value(packet) if isinstance(packet, dict) else None
    forbidden_count = 0
    if isinstance(packet, dict):
        packet_projection = {key: packet[key] for key in expected if key in packet}
        forbidden_count = len(set(packet) - allowed_keys)
        encoded = json.dumps(packet, ensure_ascii=False, sort_keys=True)
        forbidden_count += sum(encoded.count(value) for value in fixture["worker_material"]["forbidden_record_ids"])
    if raw_transcript_required:
        packet_projection = None
        criteria["worker_packet_projection"] = "unobserved"
        criteria["safe_projection_without_raw_transcript"] = "unsatisfied"
    else:
        criteria["safe_projection_without_raw_transcript"] = "satisfied"
        if packet is None:
            criteria["worker_packet_projection"] = "unobserved"
        elif not isinstance(packet, dict) or packet != expected or forbidden_count:
            criteria["worker_packet_projection"] = "unsatisfied"
        else:
            criteria["worker_packet_projection"] = "satisfied"
    packet_binding = {
        "sha256": packet_sha256,
        "canonical_projection": packet_projection,
        "forbidden_field_count": forbidden_count,
        "raw_transcript_required": raw_transcript_required,
    }

    descendant_binding = {
        "thread_id": None,
        "parent_thread_id": None,
        "task_identity": None,
        "terminal_sender": None,
        "terminal_result_sha256": None,
    }
    descendant = None
    if criteria["spawn_call_and_task_identity"] == "satisfied":
        matching = [
            item for item in trace["descendants"]
            if item.get("thread_id") == spawn_binding["child_thread_id"]
        ]
        cardinality = state_for_cardinality(matching)
        if cardinality is not None:
            criteria["descendant_parent_and_task_binding"] = cardinality
        else:
            descendant = matching[0]
            for name in ("thread_id", "parent_thread_id", "task_identity"):
                descendant_binding[name] = descendant.get(name)
            identity_values = (
                descendant.get("thread_id"), descendant.get("parent_thread_id"), descendant.get("task_identity")
            )
            if not all(isinstance(item, str) and item for item in identity_values) or root_id is None:
                criteria["descendant_parent_and_task_binding"] = "unobserved"
            elif (
                descendant["thread_id"] == spawn_binding["child_thread_id"]
                and descendant["parent_thread_id"] == root_id
                and descendant["task_identity"] == EXPECTED_TASK_IDENTITY
            ):
                criteria["descendant_parent_and_task_binding"] = "satisfied"
            else:
                criteria["descendant_parent_and_task_binding"] = "unsatisfied"

    terminal_result = None
    if criteria["descendant_parent_and_task_binding"] == "satisfied" and descendant is not None:
        terminals = descendant["terminal_events"]
        terminal_cardinality = state_for_cardinality(terminals)
        if terminal_cardinality is not None:
            criteria["descendant_terminal_sender_and_result"] = terminal_cardinality
        else:
            terminal = terminals[0]
            sender = terminal.get("sender")
            terminal_result = terminal.get("result")
            descendant_binding["terminal_sender"] = sender
            if isinstance(terminal_result, str) and terminal_result:
                descendant_binding["terminal_result_sha256"] = hashlib.sha256(terminal_result.encode("utf-8")).hexdigest()
            if not isinstance(sender, str) or not sender or not isinstance(terminal_result, str) or not terminal_result:
                criteria["descendant_terminal_sender_and_result"] = "unobserved"
            elif sender != EXPECTED_TASK_IDENTITY or not all(
                value in terminal_result for value in fixture["worker_material"]["required_result_shape"]["must_include"]
            ):
                criteria["descendant_terminal_sender_and_result"] = "unsatisfied"
            else:
                criteria["descendant_terminal_sender_and_result"] = "satisfied"

    root_tool_binding = {
        "tool_id": None,
        "call_id": None,
        "input_sha256": None,
        "terminal_status": None,
        "result_sha256": None,
    }
    tool_calls = root["tool_calls"]
    tool_results = root["tool_results"]
    tool_cardinality = state_for_cardinality(tool_calls) or state_for_cardinality(tool_results)
    if tool_calls:
        root_tool_binding["tool_id"] = tool_calls[0].get("tool_id")
        root_tool_binding["call_id"] = tool_calls[0].get("call_id")
        if isinstance(tool_calls[0].get("input"), dict):
            root_tool_binding["input_sha256"] = sha256_value(tool_calls[0]["input"])
    if tool_results:
        root_tool_binding["terminal_status"] = tool_results[0].get("terminal_status")
        if isinstance(tool_results[0].get("result"), dict):
            root_tool_binding["result_sha256"] = sha256_value(tool_results[0]["result"])
    if tool_cardinality is not None:
        criteria["root_tool_call_and_terminal_result"] = tool_cardinality
    else:
        call = tool_calls[0]
        result = tool_results[0]
        required_values = (call.get("call_id"), call.get("tool_id"), call.get("input"), result.get("call_id"), result.get("terminal_status"), result.get("result"))
        if any(item is None for item in required_values):
            criteria["root_tool_call_and_terminal_result"] = "unobserved"
        elif (
            call["call_id"] == result["call_id"]
            and call["tool_id"] == fixture["root_tool"]["tool_id"]
            and call["input"] == fixture["root_tool"]["allowed_input"]
            and result["terminal_status"] == "success"
            and result["result"] == fixture["root_tool"]["terminal_result"]
        ):
            criteria["root_tool_call_and_terminal_result"] = "satisfied"
        else:
            criteria["root_tool_call_and_terminal_result"] = "unsatisfied"

    final_binding = {
        "sha256": None,
        "worker_result_directly_carried": False,
        "root_tool_result_directly_carried": False,
    }
    finals = root["final_responses"]
    final_cardinality = state_for_cardinality(finals)
    if final_cardinality is not None:
        criteria["final_response_direct_binding"] = final_cardinality
    elif (
        criteria["descendant_terminal_sender_and_result"] != "satisfied"
        or criteria["root_tool_call_and_terminal_result"] != "satisfied"
    ):
        criteria["final_response_direct_binding"] = "unobserved"
    else:
        final = finals[0]
        final_binding["sha256"] = hashlib.sha256(final.encode("utf-8")).hexdigest()
        sentences = split_sentences(final)
        worker_values = fixture["final_response_oracle"]["sentence_1_must_include"]
        tool_values = fixture["final_response_oracle"]["sentence_2_must_include"]
        worker_carried = len(sentences) == 2 and all(value in sentences[0] for value in worker_values)
        tool_carried = len(sentences) == 2 and all(value in sentences[1] for value in tool_values)
        final_binding["worker_result_directly_carried"] = worker_carried
        final_binding["root_tool_result_directly_carried"] = tool_carried
        criteria["final_response_direct_binding"] = "satisfied" if worker_carried and tool_carried else "unsatisfied"

    sessions = usage_input["sessions"]
    thread_ids = [item.get("thread_id") for item in sessions if isinstance(item.get("thread_id"), str)]
    duplicate_count = len(thread_ids) - len(set(thread_ids))
    root_sessions = [item for item in sessions if item.get("thread_id") == usage_input.get("root_thread_id")]
    descendant_sessions = [item for item in sessions if item.get("thread_id") != usage_input.get("root_thread_id")]
    token_fields = ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")
    complete = (
        len(root_sessions) == 1
        and duplicate_count == 0
        and all(all(isinstance(item.get(field), int) and not isinstance(item.get(field), bool) for field in token_fields) for item in sessions)
        and all(item.get("parent_thread_id") == usage_input.get("root_thread_id") for item in descendant_sessions)
    )
    if not sessions:
        criteria["all_agent_final_usage"] = "unobserved"
    else:
        criteria["all_agent_final_usage"] = "satisfied" if complete else "unsatisfied"
    projected_sessions = [projected_usage(item) for item in sessions]
    root_usage = projected_usage(root_sessions[0]) if root_sessions else empty_usage(usage_input.get("root_thread_id"))
    projected_descendants = [projected_usage(item) for item in descendant_sessions]
    total_usage = empty_usage("all-agent-total")
    if complete:
        for field in token_fields:
            total_usage[field] = sum(item[field] for item in projected_sessions)
    usage = {
        "root": root_usage,
        "descendants": projected_descendants,
        "all_agent_total": total_usage,
        "complete": complete,
        "duplicate_session_count": duplicate_count,
    }

    started = trace["monotonic"].get("started_ms")
    ended = trace["monotonic"].get("ended_ms")
    elapsed_ms = None
    if not isinstance(started, int) or isinstance(started, bool) or not isinstance(ended, int) or isinstance(ended, bool):
        criteria["monotonic_elapsed"] = "unobserved"
    elif ended < started:
        criteria["monotonic_elapsed"] = "unsatisfied"
    else:
        elapsed_ms = ended - started
        criteria["monotonic_elapsed"] = "satisfied"

    admission = (
        "agentic_runtime_capability_available"
        if all(value == "satisfied" for value in criteria.values())
        else "agentic_runtime_capability_unavailable"
    )
    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "probe_id": trace["probe_id"],
        "synthetic_input": True,
        "bindings": {
            "spawn": spawn_binding,
            "packet": packet_binding,
            "descendant": descendant_binding,
            "root_tool": root_tool_binding,
            "final_response": final_binding,
        },
        "usage": usage,
        "elapsed_ms": elapsed_ms,
        "criteria": criteria,
        "admission": admission,
        "sensitive_material_saved": False,
    }


def validate_input(value: dict[str, Any], schema: dict[str, Any]) -> None:
    jsonschema.Draft202012Validator(schema).validate(value)


def validate_output(value: dict[str, Any], schema: dict[str, Any], receipt_schema: dict[str, Any]) -> None:
    resource = Resource.from_contents(receipt_schema)
    registry = Registry().with_resource(receipt_schema["$id"], resource)
    jsonschema.Draft202012Validator(schema, registry=registry).validate(value)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--synthetic-trace", type=Path, required=True)
    value.add_argument("--fixture", type=Path, default=DEFAULT_FIXTURE)
    value.add_argument("--input-schema", type=Path, default=DEFAULT_INPUT_SCHEMA)
    value.add_argument("--output-schema", type=Path, default=DEFAULT_OUTPUT_SCHEMA)
    value.add_argument("--receipt-schema", type=Path, default=DEFAULT_RECEIPT_SCHEMA)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        trace = load_object(args.synthetic_trace.resolve())
        fixture = load_object(args.fixture.resolve())
        input_schema = load_object(args.input_schema.resolve())
        output_schema = load_object(args.output_schema.resolve())
        receipt_schema = load_object(args.receipt_schema.resolve())
        validate_input(trace, input_schema)
        result = extract(trace, fixture)
        validate_output(result, output_schema, receipt_schema)
    except (ExtractionError, jsonschema.ValidationError, jsonschema.SchemaError) as error:
        print(json.dumps({"schema_version": OUTPUT_SCHEMA_VERSION, "status": "extractor_error", "error": str(error)}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
