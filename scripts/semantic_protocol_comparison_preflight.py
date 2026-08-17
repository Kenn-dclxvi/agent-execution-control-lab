#!/usr/bin/env python3
"""Preflight two semantic-protocol prompt conditions without repository refs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


class PreflightError(Exception):
    pass


SCHEMA_VERSION = "portable-instruction-semantic-comparison-condition/v1"
RECEIPT_VERSION = "portable-instruction-semantic-comparison-preflight/v1"
REQUIRED_FIELDS = {
    "schema_version",
    "prompt_set_identity",
    "target_subject_ref",
    "runtime_ref",
    "task_spec_ref",
    "case_ref",
    "rating_ref",
    "repetition_condition",
}


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PreflightError(f"cannot load condition: {path}") from error
    if not isinstance(value, dict):
        raise PreflightError(f"condition must be an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def contains_unbound(value: Any) -> bool:
    if value is None or value == "unbound":
        return True
    if isinstance(value, dict):
        return any(contains_unbound(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_unbound(item) for item in value)
    return False


def nested_keys(value: Any) -> set[str]:
    if isinstance(value, dict):
        result = set(value)
        for item in value.values():
            result.update(nested_keys(item))
        return result
    if isinstance(value, list):
        result: set[str] = set()
        for item in value:
            result.update(nested_keys(item))
        return result
    return set()


def validate_condition(value: dict[str, Any], label: str) -> None:
    if set(value) != REQUIRED_FIELDS:
        raise PreflightError(f"{label} fields differ from contract: {sorted(value)}")
    if value.get("schema_version") != SCHEMA_VERSION:
        raise PreflightError(f"{label} schema version mismatch")
    if contains_unbound(value):
        raise PreflightError(f"{label} contains unbound value")
    if "target_repository_ref" in nested_keys(value):
        raise PreflightError(f"{label} contains forbidden target_repository_ref")

    subject = value.get("target_subject_ref")
    if not isinstance(subject, dict) or subject.get("kind") != "semantic_protocol":
        raise PreflightError(f"{label} target subject is not semantic_protocol")
    required_subject = {"kind", "protocol_id", "protocol_revision", "interaction_mode", "response_schema_sha256"}
    if set(subject) != required_subject:
        raise PreflightError(f"{label} target subject fields mismatch")

    runtime = value.get("runtime_ref")
    required_runtime = {
        "runtime",
        "version",
        "model",
        "reasoning_effort",
        "token_accounting",
        "session_mode",
        "instruction_isolation",
        "permission",
        "capability_catalog",
        "elapsed_boundary",
    }
    if not isinstance(runtime, dict) or set(runtime) != required_runtime:
        raise PreflightError(f"{label} runtime fields mismatch")
    token_accounting = runtime.get("token_accounting")
    if token_accounting != {
        "scope": "all_agents",
        "revision": "v1",
        "source": "codex_rollout_final_usage_by_workspace",
    }:
        raise PreflightError(f"{label} token accounting is unsupported")
    if runtime.get("elapsed_boundary") != "adapter_start_to_terminal_process_result_monotonic":
        raise PreflightError(f"{label} elapsed boundary is unsupported")
    if runtime.get("session_mode") == "ephemeral":
        raise PreflightError(f"{label} ephemeral session cannot satisfy transcript token accounting")


def comparison_payload(value: dict[str, Any]) -> dict[str, Any]:
    return {key: value[key] for key in sorted(REQUIRED_FIELDS - {"prompt_set_identity"})}


def mismatch_paths(left: Any, right: Any, prefix: str = "") -> list[str]:
    if type(left) is not type(right):
        return [prefix or "$"]
    if isinstance(left, dict):
        paths = []
        for key in sorted(set(left) | set(right)):
            path = f"{prefix}.{key}" if prefix else key
            if key not in left or key not in right:
                paths.append(path)
            else:
                paths.extend(mismatch_paths(left[key], right[key], path))
        return paths
    if isinstance(left, list):
        if len(left) != len(right):
            return [prefix]
        paths = []
        for index, (left_item, right_item) in enumerate(zip(left, right, strict=True)):
            paths.extend(mismatch_paths(left_item, right_item, f"{prefix}[{index}]"))
        return paths
    return [] if left == right else [prefix]


def preflight(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    validate_condition(left, "left")
    validate_condition(right, "right")
    if left["prompt_set_identity"] == right["prompt_set_identity"]:
        raise PreflightError("prompt identities must differ")
    left_payload = comparison_payload(left)
    right_payload = comparison_payload(right)
    mismatches = mismatch_paths(left_payload, right_payload)
    return {
        "schema_version": RECEIPT_VERSION,
        "compatible": not mismatches,
        "changed_axis": "prompt_set_identity",
        "left_prompt_set_identity": left["prompt_set_identity"],
        "right_prompt_set_identity": right["prompt_set_identity"],
        "non_prompt_conditions_sha256": hashlib.sha256(canonical_bytes(left_payload)).hexdigest() if not mismatches else None,
        "mismatch_paths": mismatches,
        "dispatch_allowed": not mismatches,
    }


def write_once(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
    except FileExistsError as error:
        raise PreflightError(f"refusing to overwrite: {path}") from error


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--left", type=Path, required=True)
    parser.add_argument("--right", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        left_path = args.left.resolve()
        right_path = args.right.resolve()
        receipt = preflight(load_object(left_path), load_object(right_path))
        receipt["source_sha256"] = {"left": sha256_file(left_path), "right": sha256_file(right_path)}
        write_once(args.output.resolve(), receipt)
    except PreflightError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0 if receipt["dispatch_allowed"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
