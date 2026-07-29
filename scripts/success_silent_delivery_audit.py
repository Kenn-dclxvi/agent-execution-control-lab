#!/usr/bin/env python3
"""Audit success-only output suppression in a Codex rollout."""

from __future__ import annotations

import argparse
import hashlib
import json
import shlex
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "the-caption-prompt.success-delivery-audit/v1"
RAW_SUCCESS_MARKERS = (
    "test session starts",
    "============================= test session",
    "collecting ...",
)
MAX_VALIDATION_RECEIPT_BYTES = 4096
MAX_INTERMEDIATE_MESSAGES = 2
MAX_INTERMEDIATE_MESSAGE_BYTES = 1024


class SuccessSilentDeliveryAuditError(Exception):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def message_text(payload: dict[str, Any]) -> str:
    content = payload.get("content")
    if not isinstance(content, list):
        return ""
    return "".join(
        item.get("text", "")
        for item in content
        if isinstance(item, dict) and isinstance(item.get("text"), str)
    )


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def audit_local_evidence(
    evidence_dir: Path | None,
    allowed_commands: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    if allowed_commands is None:
        return {
            "required": False,
            "passed": True,
            "expected_count": 0,
            "observed_count": 0,
            "failures": [],
        }
    failures: list[str] = []
    expected = [entry.get("argv") for entry in allowed_commands]
    observed: list[list[str]] = []
    metadata_files = [] if evidence_dir is None else sorted(evidence_dir.glob("*.json"))
    for metadata_path in metadata_files:
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            failures.append(f"invalid_metadata:{metadata_path.name}")
            continue
        evidence_id = metadata.get("evidence_id")
        argv = metadata.get("argv")
        if not isinstance(evidence_id, str) or not isinstance(argv, list):
            failures.append(f"invalid_identity:{metadata_path.name}")
            continue
        observed.append(argv)
        if metadata.get("exit_code") != 0:
            failures.append(f"nonzero_evidence:{evidence_id}")
        for stream in ("stdout", "stderr"):
            path = metadata_path.with_name(f"{evidence_id}.{stream}.bin")
            if not path.is_file():
                failures.append(f"missing_{stream}:{evidence_id}")
                continue
            value = path.read_bytes()
            if metadata.get(f"{stream}_bytes") != len(value):
                failures.append(f"{stream}_size_mismatch:{evidence_id}")
            if metadata.get(f"{stream}_sha256") != sha256(value):
                failures.append(f"{stream}_sha256_mismatch:{evidence_id}")
    if sorted(observed) != sorted(expected):
        failures.append("exact_argv_set_mismatch")
    return {
        "required": True,
        "passed": not failures,
        "expected_count": len(expected),
        "observed_count": len(metadata_files),
        "failures": failures,
    }


def audit(
    rollout: Path,
    required_command_groups: list[list[str]],
    allowed_commands: list[dict[str, Any]] | None = None,
    raw_evidence_dir: Path | None = None,
) -> dict[str, Any]:
    try:
        lines = rollout.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise SuccessSilentDeliveryAuditError(f"missing rollout: {rollout}") from exc

    assistant_messages: list[str] = []
    calls: dict[str, str] = {}
    outputs: dict[str, Any] = {}
    for line_number, raw_line in enumerate(lines, start=1):
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise SuccessSilentDeliveryAuditError(
                f"invalid rollout JSON at line {line_number}"
            ) from exc
        if not isinstance(event, dict) or event.get("type") != "response_item":
            continue
        payload = event.get("payload")
        if not isinstance(payload, dict):
            continue
        item_type = payload.get("type")
        if item_type == "message" and payload.get("role") == "assistant":
            assistant_messages.append(message_text(payload))
        elif item_type == "custom_tool_call" and payload.get("name") == "exec":
            call_id = payload.get("call_id")
            call_input = payload.get("input")
            if isinstance(call_id, str) and isinstance(call_input, str):
                calls[call_id] = call_input
        elif item_type == "custom_tool_call_output":
            call_id = payload.get("call_id")
            if isinstance(call_id, str):
                outputs[call_id] = payload.get("output")

    if allowed_commands is None:
        command_needles = [
            item for group in required_command_groups for item in group if item
        ]
        validation_call_ids = [
            call_id
            for call_id, call_input in calls.items()
            if command_needles and all(needle in call_input for needle in command_needles)
        ]
    else:
        exact_commands = [entry["argv"] for entry in allowed_commands]
        validation_call_ids = [
            call_id
            for call_id, call_input in calls.items()
            if call_input.count("success_silent_command.py") >= len(exact_commands)
            and all(shlex.join(argv) in call_input for argv in exact_commands)
        ]
    visible_validation_outputs = [
        outputs[call_id] for call_id in validation_call_ids if call_id in outputs
    ]
    validation_output_bytes = sum(
        len(canonical_json(output)) for output in visible_validation_outputs
    )
    validation_text = "\n".join(
        str(output) for output in visible_validation_outputs
    ).casefold()
    raw_success_markers = [
        marker for marker in RAW_SUCCESS_MARKERS if marker in validation_text
    ]
    intermediate_messages = assistant_messages[:-1] if assistant_messages else []
    intermediate_message_bytes = sum(
        len(value.encode("utf-8")) for value in intermediate_messages
    )

    validation_success_silent_passed = (
        len(validation_call_ids) == 1
        and len(visible_validation_outputs) == 1
        and validation_output_bytes <= MAX_VALIDATION_RECEIPT_BYTES
        and not raw_success_markers
    )
    status_suppression_passed = (
        len(intermediate_messages) <= MAX_INTERMEDIATE_MESSAGES
        and intermediate_message_bytes <= MAX_INTERMEDIATE_MESSAGE_BYTES
    )
    local_evidence = audit_local_evidence(raw_evidence_dir, allowed_commands)
    return {
        "schema_version": SCHEMA_VERSION,
        "rollout": str(rollout.resolve()),
        "mechanism_passed": (
            validation_success_silent_passed
            and status_suppression_passed
            and local_evidence["passed"]
        ),
        "validation_success_silent_passed": validation_success_silent_passed,
        "status_suppression_passed": status_suppression_passed,
        "validation_wave_call_count": len(validation_call_ids),
        "validation_wave_output_count": len(visible_validation_outputs),
        "validation_model_visible_bytes": validation_output_bytes,
        "validation_raw_success_markers": raw_success_markers,
        "intermediate_message_count": len(intermediate_messages),
        "intermediate_message_bytes": intermediate_message_bytes,
        "local_raw_evidence": local_evidence,
        "limits": {
            "validation_receipt_bytes": MAX_VALIDATION_RECEIPT_BYTES,
            "intermediate_messages": MAX_INTERMEDIATE_MESSAGES,
            "intermediate_message_bytes": MAX_INTERMEDIATE_MESSAGE_BYTES,
        },
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--rollout", required=True)
    value.add_argument("--required-command-groups", required=True)
    value.add_argument("--command-policy")
    value.add_argument("--raw-evidence-dir")
    value.add_argument("--output", required=True)
    return value


def main() -> int:
    args = parser().parse_args()
    groups = json.loads(Path(args.required_command_groups).read_text(encoding="utf-8"))
    if not isinstance(groups, list):
        raise SuccessSilentDeliveryAuditError("required command groups must be an array")
    allowed_commands = None
    if args.command_policy:
        policy = json.loads(Path(args.command_policy).read_text(encoding="utf-8"))
        commands = policy.get("commands") if isinstance(policy, dict) else None
        if not isinstance(commands, list):
            raise SuccessSilentDeliveryAuditError("command policy has no commands")
        allowed_commands = commands
    raw_evidence_dir = Path(args.raw_evidence_dir) if args.raw_evidence_dir else None
    if (allowed_commands is None) != (raw_evidence_dir is None):
        raise SuccessSilentDeliveryAuditError(
            "command policy and raw evidence directory must be provided together"
        )
    result = audit(
        Path(args.rollout),
        groups,
        allowed_commands,
        raw_evidence_dir,
    )
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":"), sort_keys=True))
    return 0 if result["mechanism_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
