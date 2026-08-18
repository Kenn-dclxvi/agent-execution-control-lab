#!/usr/bin/env python3
"""Target-specific materialization and grading for validation-carrier cases."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tempfile
from typing import Any, Iterable

import jsonschema


ADAPTER_SCHEMA_VERSION = "codex-validation-carrier-runtime-adapter/v1"
MATERIALIZATION_SCHEMA_VERSION = "codex-validation-carrier-materialization/v1"
GRADE_SCHEMA_VERSION = "codex-validation-carrier-grade/v1"
TRACE_SCHEMA_VERSION = "codex-validation-carrier-trace-diagnostic/v1"
REQUIRED_CAPABILITIES = (
    "single_admission",
    "ordered_individual_execution",
    "local_result_check",
    "fail_fast_control",
    "intermediate_ingress_denial",
    "terminal_projection",
    "continuation_identity",
)


class ValidationCarrierRuntimeError(Exception):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8") + b"\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationCarrierRuntimeError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise ValidationCarrierRuntimeError(f"JSON root is not an object: {path}")
    return value


def _select_case(document: dict[str, Any], case_id: str) -> dict[str, Any]:
    matches = [item for item in document.get("cases", []) if item.get("case_id") == case_id]
    if len(matches) != 1:
        raise ValidationCarrierRuntimeError(f"case identity is not unique: {case_id}")
    return matches[0]


def _contained_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise ValidationCarrierRuntimeError("relative path is unbound")
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as error:
        raise ValidationCarrierRuntimeError(f"path escapes target root: {relative}") from error
    return candidate


def capability_preflight(runtime_contract: dict[str, Any]) -> dict[str, Any]:
    capabilities = runtime_contract.get("carrier_capabilities")
    missing = (list(REQUIRED_CAPABILITIES) if not isinstance(capabilities, dict) else [name for name in REQUIRED_CAPABILITIES if capabilities.get(name) is not True])
    if missing:
        state, reason = "denied", "carrier_capability_set_incomplete"
    elif not isinstance(runtime_contract.get("continuation_identity_field"), str):
        state, reason = "denied", "continuation_identity_unbound"
    elif not isinstance(runtime_contract.get("terminal_status_field"), str):
        state, reason = "denied", "required_terminal_field_unbound"
    else:
        state, reason = "allowed", None
    return {
        "schema_version": "codex-validation-carrier-capability-preflight/v1",
        "dispatch_state": state,
        "reason": reason,
        "required_capabilities": list(REQUIRED_CAPABILITIES),
        "missing_capabilities": missing,
        "continuation_identity_field": runtime_contract.get("continuation_identity_field"),
        "terminal_status_field": runtime_contract.get("terminal_status_field"),
    }


def materialize_case(target_root: Path, case_id: str, destination: Path) -> dict[str, Any]:
    target_root = target_root.resolve()
    destination = destination.resolve()
    if destination.exists():
        raise ValidationCarrierRuntimeError(f"refusing to overwrite materialization: {destination}")
    case_root = target_root / "cases/heldout-r1"
    cases = load_object(case_root / "input-cases.json")
    case = _select_case(cases, case_id)
    preflight = capability_preflight(cases.get("runtime_contract") or {})
    if preflight["dispatch_state"] != "allowed":
        raise ValidationCarrierRuntimeError(f"capability preflight denied: {preflight['reason']}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}.", dir=destination.parent))
    try:
        workspace = temporary / "workspace"
        model_visible = temporary / "model-visible"
        private = temporary / "private"
        workspace.mkdir(mode=0o700)
        model_visible.mkdir(mode=0o700)
        private.mkdir(mode=0o700)
        fixture_root = _contained_path(case_root, case["fixture"]["root"])
        copied: list[dict[str, Any]] = []
        for entry in case["fixture"]["files"]:
            source = _contained_path(fixture_root, entry["path"])
            target = _contained_path(workspace, entry["path"])
            if not source.is_file() or source.is_symlink():
                raise ValidationCarrierRuntimeError(f"fixture source is not a regular file: {source}")
            if sha256_file(source) != entry["sha256"]:
                raise ValidationCarrierRuntimeError(f"fixture hash mismatch: {source}")
            source_mode = f"100{stat.S_IMODE(source.stat().st_mode):03o}"
            if source_mode != entry["mode"]:
                raise ValidationCarrierRuntimeError(f"fixture mode mismatch: {source}")
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target, follow_symlinks=False)
            os.chmod(target, int(entry["mode"][-3:], 8))
            copied.append({"path": entry["path"], "mode": entry["mode"], "sha256": entry["sha256"]})
        packet = {
            "schema_version": "codex-validation-carrier-model-packet/v1",
            "case_id": case["case_id"],
            "case_revision": case["case_revision"],
            "required_action": case["required_action"],
            "validation_plan": case["validation_plan"],
            "required_terminal_state": case["required_terminal_state"],
            "runtime_contract": cases["runtime_contract"],
            "response_schema": cases["response_schema"],
        }
        packet_path = model_visible / "input.json"
        packet_path.write_bytes(canonical_bytes(packet))
        os.chmod(packet_path, 0o600)
        receipt = {
            "schema_version": MATERIALIZATION_SCHEMA_VERSION,
            "adapter_schema_version": ADAPTER_SCHEMA_VERSION,
            "case_id": case_id,
            "case_revision": case["case_revision"],
            "fixture_files": copied,
            "model_packet_sha256": sha256_file(packet_path),
            "capability_preflight": preflight,
            "oracle_materialized": False,
        }
        receipt_path = private / "materialization-receipt.json"
        receipt_path.write_bytes(canonical_bytes(receipt))
        os.chmod(receipt_path, 0o600)
        temporary.replace(destination)
        return receipt
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise


def render_model_input(template_path: Path, packet_path: Path) -> bytes:
    template = template_path.read_text(encoding="utf-8")
    if template.count("{{MODEL_PACKET_JSON}}") != 1:
        raise ValidationCarrierRuntimeError("TaskSpec template must contain one packet placeholder")
    packet = load_object(packet_path)
    rendered = json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True)
    return template.replace("{{MODEL_PACKET_JSON}}", rendered).encode("utf-8")


def _jsonl_objects(path: Path) -> Iterable[dict[str, Any]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ValidationCarrierRuntimeError(f"cannot read rollout: {path}") from error
    for number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise ValidationCarrierRuntimeError(f"invalid rollout JSONL line {number}") from error
        if isinstance(value, dict):
            yield value


def _payload_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(_payload_text(item) for item in value)
    if isinstance(value, dict):
        return "\n".join(_payload_text(item) for item in value.values())
    return ""


def analyze_rollout(
    rollout_path: Path,
    validation_plan: list[dict[str, Any]],
    forbidden_output_substrings: list[str] | None = None,
) -> dict[str, Any]:
    response_items = [item["payload"] for item in _jsonl_objects(rollout_path) if item.get("type") == "response_item" and isinstance(item.get("payload"), dict)]
    calls: dict[str, dict[str, Any]] = {}
    outputs: dict[str, list[tuple[int, Any]]] = {}
    for index, payload in enumerate(response_items):
        item_type = payload.get("type")
        call_id = payload.get("call_id")
        if item_type in {"custom_tool_call", "function_call"} and payload.get("name") == "exec":
            source = payload.get("input", payload.get("arguments"))
            if isinstance(call_id, str) and isinstance(source, str):
                calls[call_id] = {"index": index, "source": source}
        elif item_type in {"custom_tool_call_output", "function_call_output"} and isinstance(call_id, str):
            outputs.setdefault(call_id, []).append((index, payload.get("output")))
    if not validation_plan:
        return {
            "schema_version": TRACE_SCHEMA_VERSION, "carrier_expected": False,
            "mechanism_passed": True, "outer_call_id": None, "terminal_projection_count": 0,
            "model_visible_responses_between_validation_results": 0,
            "continuation_identity_preserved": None, "raw_output_bytes": 0,
            "interposed_model_item_types": [], "carrier_route": "not_required",
            "nested_invocation_count": 0, "continuation_count": 0,
            "forbidden_terminal_output_substrings": [],
        }
    required_groups = [[str(token) for token in item["argv"]] for item in validation_plan]
    matching = sorted(call_id for call_id, call in calls.items() if all(all(token in call["source"] for token in group) for group in required_groups))
    outer_id = matching[0] if len(matching) == 1 else None
    projected = [] if outer_id is None else outputs.get(outer_id, [])
    interposed: list[str] = []
    source = "" if outer_id is None else calls[outer_id]["source"]
    if outer_id is not None and len(projected) == 1:
        start, end = calls[outer_id]["index"], projected[0][0]
        interposed = [str(item.get("type")) for item in response_items[start + 1 : end] if item.get("type") != "reasoning"]
    terminal_text = "" if len(projected) != 1 else _payload_text(projected[0][1])
    continuation_required = any(item["validation_id"] == "v-indigo" for item in validation_plan)
    continuation_preserved = (("write_stdin" in source and "session_id" in source) if continuation_required else None)
    forbidden_projection = [token for token in (forbidden_output_substrings or []) if token in terminal_text]
    mechanism_passed = (
        outer_id is not None and len(projected) == 1 and not interposed
        and (not continuation_required or continuation_preserved is True)
        and not forbidden_projection
    )
    return {
        "schema_version": TRACE_SCHEMA_VERSION, "carrier_expected": True,
        "mechanism_passed": mechanism_passed, "outer_call_id": outer_id,
        "terminal_projection_count": len(projected),
        "model_visible_responses_between_validation_results": 0 if mechanism_passed else None,
        "continuation_identity_preserved": continuation_preserved,
        "raw_output_bytes": len(terminal_text.encode("utf-8")),
        "interposed_model_item_types": interposed,
        "carrier_route": "programmatic_carrier" if outer_id is not None else "unobserved",
        "nested_invocation_count": source.count("tools.exec_command"),
        "continuation_count": source.count("write_stdin"),
        "forbidden_terminal_output_substrings": forbidden_projection,
    }


def _event_lines(workspace: Path) -> list[str]:
    path = workspace / ".carrier-events.log"
    return [] if not path.exists() else path.read_text(encoding="utf-8").splitlines()


def _response_without_evidence(response: dict[str, Any]) -> dict[str, Any]:
    reduced = json.loads(json.dumps(response))
    for result in reduced.get("validation_results", []):
        result.pop("evidence", None)
    reduced.pop("unstarted_validation_ids", None)
    return reduced


def grade_case(*, target_root: Path, case_id: str, materialized_root: Path, final_response_path: Path, rollout_path: Path) -> dict[str, Any]:
    target_root = target_root.resolve()
    case_root = target_root / "cases/heldout-r1"
    case = _select_case(load_object(case_root / "input-cases.json"), case_id)
    oracle = _select_case(load_object(case_root / "oracle.json"), case_id)
    schema = load_object(target_root / "schemas/response.schema.json")
    workspace = materialized_root.resolve() / "workspace"
    action_path = _contained_path(workspace, case["required_action"]["path"])
    action_matches = action_path.is_file() and sha256_file(action_path) == case["required_action"]["expected_sha256"]
    events = _event_lines(workspace)
    expected_events_exact = events == oracle["expected_event_lines"]
    forbidden_events = [line for line in events if line in oracle["forbidden_event_lines"]]
    response_schema_valid, response, raw_response = False, {}, b""
    try:
        raw_response = final_response_path.read_bytes()
        response = json.loads(raw_response)
        if not isinstance(response, dict):
            raise ValueError("response is not an object")
        jsonschema.Draft202012Validator(schema).validate(response)
        response_schema_valid = True
    except (OSError, json.JSONDecodeError, jsonschema.ValidationError, ValueError):
        pass
    expected_response = oracle["expected_response"]
    response_exact = response_schema_valid and response == expected_response
    forbidden_tokens = oracle.get("forbidden_terminal_output_substrings", [])
    terminal_state_matches = response_schema_valid and response.get("validation_plan_state") == expected_response["validation_plan_state"]
    try:
        evidence_subset = all(set(actual.get("evidence", [])) <= set(expected.get("evidence", [])) for actual, expected in zip(response.get("validation_results", []), expected_response["validation_results"], strict=True))
    except ValueError:
        evidence_subset = False
    only_non_destructive_omission = (
        response_schema_valid and _response_without_evidence(response) == _response_without_evidence(expected_response)
        and evidence_subset and set(response.get("unstarted_validation_ids", [])) <= set(expected_response["unstarted_validation_ids"])
    )
    false_success = response_schema_valid and expected_response["validation_plan_state"] in {"failed", "unavailable"} and response.get("validation_plan_state") == "succeeded"
    trace = analyze_rollout(rollout_path, case["validation_plan"], forbidden_tokens)
    forbidden_output = sorted(set(
        [token for token in forbidden_tokens if token.encode("utf-8") in raw_response]
        + trace["forbidden_terminal_output_substrings"]
    ))
    if action_matches and expected_events_exact and not forbidden_events and response_exact and not forbidden_output:
        quality_score = 4
    elif action_matches and expected_events_exact and not forbidden_events and terminal_state_matches and only_non_destructive_omission and not forbidden_output:
        quality_score = 3
    elif not action_matches or not response_schema_valid or not expected_events_exact or forbidden_events or forbidden_output or false_success:
        quality_score = 1
    else:
        quality_score = 2
    return {
        "schema_version": GRADE_SCHEMA_VERSION, "adapter_schema_version": ADAPTER_SCHEMA_VERSION,
        "case_id": case_id, "quality_score": quality_score,
        "quality_checks": {
            "action_matches": action_matches, "expected_events_exact": expected_events_exact,
            "forbidden_events": forbidden_events, "response_schema_valid": response_schema_valid,
            "terminal_state_matches": terminal_state_matches, "response_exact": response_exact,
            "forbidden_terminal_output_substrings": forbidden_output, "false_success": false_success,
        },
        "trace_diagnostics": trace, "mechanism_passed": trace["mechanism_passed"],
    }


def adapter_contract() -> dict[str, Any]:
    return {
        "schema_version": ADAPTER_SCHEMA_VERSION, "target_id": "codex-validation-carrier-conformance",
        "materializer": MATERIALIZATION_SCHEMA_VERSION, "grader": GRADE_SCHEMA_VERSION,
        "trace_diagnostic": TRACE_SCHEMA_VERSION, "quality_kpis": ["quality_score"],
        "diagnostics_not_kpis": ["mechanism_passed", "model_visible_responses_between_validation_results", "terminal_projection_count", "continuation_identity_preserved", "raw_output_bytes"],
        "qualification_entrypoint_enabled": True, "formal_evaluation_entrypoint_enabled": False,
        "qualification_state": "implemented_not_qualified",
    }
