#!/usr/bin/env python3
"""Project an externally selected private trace without discovery or mutation."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

try:
    from scripts.general_chat_agentic_raw_normalizer import normalize_known_fields
    from scripts.general_chat_agentic_real_trace_adapter import (
        AdapterError,
        project_known_session_events,
        project_root_events,
        verify_session_graph,
    )
except ModuleNotFoundError:  # direct script execution puts scripts/ on sys.path
    from general_chat_agentic_raw_normalizer import normalize_known_fields
    from general_chat_agentic_real_trace_adapter import (
        AdapterError,
        project_known_session_events,
        project_root_events,
        verify_session_graph,
    )


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "docs/general-chat-agentic-private-trace-shadow-packet-r1.json"
DEFAULT_INPUT_SCHEMA = ROOT / "docs/general-chat-agentic-private-trace-adapter-input.schema.json"
DEFAULT_OUTPUT_SCHEMA = ROOT / "docs/general-chat-agentic-private-trace-adapter-output.schema.json"
DEFAULT_SHADOW_ROOT = ROOT / "docs/general-chat-agentic-private-trace-shadow"
EXPECTED_NORMALIZED_SCHEMA = {
    "path": "docs/general-chat-agentic-binding-extractor-input-r2.schema.json",
    "sha256": "42a85185964df04ea0b085c25b13d155c06658d758c76f95f617e69730c167e8",
    "bytes": 4917,
}
OUTPUT_SCHEMA_VERSION = "general-chat-agentic-private-trace-projection/v1"


class PrivateTraceAdapterError(Exception):
    """The externally selected trace did not satisfy the private boundary."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def load_object(path: Path, code: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PrivateTraceAdapterError(code) from error
    if not isinstance(value, dict):
        raise PrivateTraceAdapterError(code)
    return value


def validate(value: dict[str, Any], schema: dict[str, Any], code: str) -> None:
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(value)
    except (jsonschema.SchemaError, jsonschema.ValidationError) as error:
        raise PrivateTraceAdapterError(code) from error


def verified_file(root: Path, identity: dict[str, Any]) -> tuple[Path, bytes]:
    canonical_root = root.resolve()
    relative = Path(identity["path"])
    cursor = canonical_root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise PrivateTraceAdapterError("TRACE_SYMLINK_FORBIDDEN")
    path = (canonical_root / relative).resolve()
    try:
        path.relative_to(canonical_root)
    except ValueError as error:
        raise PrivateTraceAdapterError("TRACE_PATH_OUTSIDE_ROOT") from error
    if not path.is_file():
        raise PrivateTraceAdapterError("TRACE_FILE_UNAVAILABLE")
    try:
        data = path.read_bytes()
    except OSError as error:
        raise PrivateTraceAdapterError("TRACE_FILE_UNAVAILABLE") from error
    if len(data) != identity["bytes"]:
        raise PrivateTraceAdapterError("TRACE_FILE_BYTES_MISMATCH")
    if hashlib.sha256(data).hexdigest() != identity["sha256"]:
        raise PrivateTraceAdapterError("TRACE_FILE_HASH_MISMATCH")
    return path, data


def parse_json_lines(data: bytes) -> list[dict[str, Any]]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PrivateTraceAdapterError("TRACE_JSONL_INVALID") from error
    events = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise PrivateTraceAdapterError("TRACE_JSONL_INVALID") from error
        if not isinstance(event, dict):
            raise PrivateTraceAdapterError("TRACE_JSONL_INVALID")
        events.append(event)
    return events


def verify_root_mode(packet: dict[str, Any], trace_root: Path, repository_root: Path) -> None:
    root = trace_root.resolve()
    repository = repository_root.resolve()
    if not root.is_dir():
        raise PrivateTraceAdapterError("TRACE_ROOT_UNAVAILABLE")
    inside_repository = root.is_relative_to(repository)
    if packet["trace_root_kind"] == "repository_shadow" and not inside_repository:
        raise PrivateTraceAdapterError("SHADOW_ROOT_OUTSIDE_REPOSITORY")
    if packet["trace_root_kind"] == "private_temporary" and inside_repository:
        raise PrivateTraceAdapterError("PRIVATE_ROOT_INSIDE_REPOSITORY")


def project_session(
    packet: dict[str, Any], session_identity: dict[str, Any], trace_root: Path
) -> dict[str, Any]:
    _, data = verified_file(trace_root, session_identity["file"])
    events = parse_json_lines(data)
    if not events or events[0].get("type") != "session_meta" or not isinstance(events[0].get("payload"), dict):
        raise PrivateTraceAdapterError("SESSION_META_MISSING")
    payload = events[0]["payload"]
    if payload.get("id") != session_identity["thread_id"]:
        raise PrivateTraceAdapterError("SESSION_THREAD_ID_MISMATCH")
    if payload.get("parent_thread_id") != session_identity["parent_thread_id"]:
        raise PrivateTraceAdapterError("SESSION_PARENT_ID_MISMATCH")
    if payload.get("cwd") != packet["workspace"]:
        raise PrivateTraceAdapterError("SESSION_WORKSPACE_MISMATCH")
    safe_meta = {
        "type": "session_meta",
        "payload": {
            "id": payload["id"],
            "cwd": payload["cwd"],
            "parent_thread_id": payload["parent_thread_id"],
        },
    }
    try:
        known = project_known_session_events(events[1:])
    except AdapterError as error:
        raise PrivateTraceAdapterError(error.code) from error
    return {"session_meta": safe_meta, "events": known}


def adapt_private_trace(
    packet: dict[str, Any], trace_root: Path, repository_root: Path = ROOT
) -> dict[str, Any]:
    verify_root_mode(packet, trace_root, repository_root)
    if packet["normalized_output_schema"] != EXPECTED_NORMALIZED_SCHEMA:
        raise PrivateTraceAdapterError("NORMALIZED_SCHEMA_IDENTITY_MISMATCH")
    if packet["monotonic"]["ended_ms"] < packet["monotonic"]["started_ms"]:
        raise PrivateTraceAdapterError("MONOTONIC_RANGE_INVALID")
    selection = packet["selection"]
    graph_packet = {
        "root_thread_id": selection["root_thread_id"],
        "sessions": selection["sessions"],
    }
    try:
        verify_session_graph(graph_packet)
    except AdapterError as error:
        raise PrivateTraceAdapterError(error.code) from error
    _, root_data = verified_file(trace_root, selection["root_events"])
    try:
        root_events = project_root_events(parse_json_lines(root_data), selection["root_thread_id"])
    except AdapterError as error:
        raise PrivateTraceAdapterError(error.code) from error
    sessions = [project_session(packet, session, trace_root) for session in selection["sessions"]]
    normalized = normalize_known_fields(
        {
            "probe_id": packet["probe_id"],
            "root_events": root_events,
            "sessions": sessions,
            "monotonic": packet["monotonic"],
        }
    )
    normalized_schema_path, _ = verified_file(repository_root, packet["normalized_output_schema"])
    validate(
        normalized,
        load_object(normalized_schema_path, "NORMALIZED_SCHEMA_INVALID"),
        "NORMALIZED_OUTPUT_INVALID",
    )
    state = (
        "synthetic_shadow_verified"
        if packet["trace_origin"] == "synthetic_shadow"
        else "issued_probe_projected"
    )
    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "probe_id": packet["probe_id"],
        "runtime_id": packet["runtime_id"],
        "trace_origin": packet["trace_origin"],
        "projection_state": state,
        "normalized_trace": normalized,
        "trace_file_count": 1 + len(selection["sessions"]),
        "raw_path_count": 0,
        "model_invocations": 0,
        "probe_issues": 0,
        "mutation_performed": False,
        "cleanup_responsibility": packet["lifecycle"]["trace_root_owner"],
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    value.add_argument("--input-schema", type=Path, default=DEFAULT_INPUT_SCHEMA)
    value.add_argument("--output-schema", type=Path, default=DEFAULT_OUTPUT_SCHEMA)
    value.add_argument("--trace-root", type=Path, default=DEFAULT_SHADOW_ROOT)
    value.add_argument("--repository-root", type=Path, default=ROOT)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        packet = load_object(args.packet.resolve(), "PRIVATE_TRACE_PACKET_UNAVAILABLE")
        input_schema = load_object(args.input_schema.resolve(), "PRIVATE_TRACE_INPUT_SCHEMA_UNAVAILABLE")
        output_schema = load_object(args.output_schema.resolve(), "PRIVATE_TRACE_OUTPUT_SCHEMA_UNAVAILABLE")
        validate(packet, input_schema, "PRIVATE_TRACE_PACKET_SCHEMA_INVALID")
        result = adapt_private_trace(packet, args.trace_root.resolve(), args.repository_root.resolve())
        validate(result, output_schema, "PRIVATE_TRACE_OUTPUT_SCHEMA_INVALID")
    except PrivateTraceAdapterError as error:
        print(
            json.dumps(
                {"schema_version": OUTPUT_SCHEMA_VERSION, "status": "adapter_error", "reason": error.code},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
