#!/usr/bin/env python3
"""Validate the general-chat agentic capability ticket without invoking a model."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TICKET = ROOT / "docs/general-chat-agentic-capability-preflight-ticket-r1.json"
DEFAULT_TICKET_SCHEMA = ROOT / "docs/general-chat-agentic-capability-preflight-ticket.schema.json"
DEFAULT_NEGATIVE_FIXTURES = ROOT / "docs/general-chat-agentic-capability-negative-fixtures-r1.json"
DEFAULT_ISSUANCE_ROOT = ROOT / "artifacts/capability-preflight-issuance"
VALIDATION_RECEIPT_SCHEMA = "general-chat-agentic-capability-static-validation/v1"
ISSUANCE_RECORD_NAMES = ("reservation.json", "issued.json", "receipt.json")


class PreflightError(Exception):
    """The static validator could not load or interpret its fixed inputs."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PreflightError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise PreflightError(f"JSON value must be an object: {path}")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def static_runtime_rejection(ticket: dict[str, Any]) -> str | None:
    runtime = ticket.get("runtime")
    if not isinstance(runtime, dict):
        return "SCHEMA_INVALID"
    trace = runtime.get("trace_capabilities")
    if not isinstance(trace, dict):
        return "SCHEMA_INVALID"
    isolation = runtime.get("instruction_isolation")
    if not isinstance(isolation, dict):
        return "SCHEMA_INVALID"

    ordered_checks = (
        (runtime.get("executable") == "codex", "RUNTIME_EXECUTABLE_MISMATCH"),
        (runtime.get("version") == "0.146.0", "RUNTIME_VERSION_MISMATCH"),
        (runtime.get("model") == "gpt-5.6-sol", "MODEL_MISMATCH"),
        (runtime.get("reasoning_effort") == "medium", "REASONING_MISMATCH"),
        (runtime.get("sandbox_mode") == "workspace-write", "SANDBOX_MISMATCH"),
        (runtime.get("approval_policy") == "never", "APPROVAL_POLICY_MISMATCH"),
        (runtime.get("multi_agent") is True, "MULTI_AGENT_DISABLED"),
        (
            isinstance(runtime.get("agents_max_threads"), int)
            and not isinstance(runtime.get("agents_max_threads"), bool)
            and 2 <= runtime["agents_max_threads"] <= 4,
            "INSUFFICIENT_AGENT_THREADS",
        ),
        (runtime.get("persist_session") is True, "PERSISTED_SESSION_REQUIRED"),
        (runtime.get("descendant_rollout_export") is True, "DESCENDANT_EXPORT_UNAVAILABLE"),
        (trace.get("parent_thread_identity") is True, "PARENT_THREAD_IDENTITY_UNAVAILABLE"),
        (trace.get("task_identity") is True, "TASK_IDENTITY_UNAVAILABLE"),
        (trace.get("terminal_sender") is True, "TERMINAL_SENDER_UNAVAILABLE"),
        (trace.get("all_agent_final_usage") is True, "ALL_AGENT_USAGE_UNAVAILABLE"),
        (trace.get("tool_call_result_identity") is True, "TOOL_IDENTITY_UNAVAILABLE"),
        (trace.get("safe_packet_projection") is True, "SAFE_PACKET_PROJECTION_UNAVAILABLE"),
        (
            isolation
            == {
                "user_config": False,
                "user_rules": False,
                "memories": False,
                "apps": False,
                "plugins": False,
                "plugin_sharing": False,
            },
            "INSTRUCTION_ISOLATION_MISMATCH",
        ),
        (runtime.get("codex_home_scope") == "per_probe_persisted_temporary", "CODEX_HOME_SCOPE_MISMATCH"),
    )
    for passed, code in ordered_checks:
        if not passed:
            return code
    return None


def schema_rejection(ticket: dict[str, Any], schema: dict[str, Any]) -> str | None:
    validator = jsonschema.Draft202012Validator(schema)
    return "SCHEMA_INVALID" if next(validator.iter_errors(ticket), None) is not None else None


def artifact_rejection(ticket: dict[str, Any], repo_root: Path) -> str | None:
    artifacts = ticket.get("artifacts")
    if not isinstance(artifacts, dict):
        return "SCHEMA_INVALID"
    resolved_root = repo_root.resolve()
    for name in ("task", "fixture"):
        identity = artifacts.get(name)
        if not isinstance(identity, dict) or not isinstance(identity.get("path"), str):
            return f"{name.upper()}_IDENTITY_INVALID"
        path = (resolved_root / identity["path"]).resolve()
        if not path.is_relative_to(resolved_root) or not path.is_file():
            return f"{name.upper()}_PATH_INVALID"
        try:
            value = path.read_bytes()
        except OSError:
            return f"{name.upper()}_UNREADABLE"
        if len(value) != identity.get("bytes"):
            return f"{name.upper()}_BYTES_MISMATCH"
        if hashlib.sha256(value).hexdigest() != identity.get("sha256"):
            return f"{name.upper()}_SHA256_MISMATCH"
    return None


def contract_rejection_code(
    ticket: dict[str, Any], schema: dict[str, Any], repo_root: Path
) -> str | None:
    rejection = static_runtime_rejection(ticket)
    if rejection is not None:
        return rejection
    rejection = schema_rejection(ticket, schema)
    if rejection is not None:
        return rejection
    return artifact_rejection(ticket, repo_root)


def issuance_rejection(ticket: dict[str, Any], repo_root: Path, issuance_root: Path) -> str | None:
    resolved_root = repo_root.resolve()
    resolved_issuance = issuance_root.resolve()
    if not resolved_issuance.is_relative_to(resolved_root):
        return "ISSUANCE_ROOT_OUTSIDE_REPOSITORY"
    probe_id = ticket.get("probe_id")
    if not isinstance(probe_id, str):
        return "SCHEMA_INVALID"
    identity_root = resolved_issuance / probe_id
    if any((identity_root / name).exists() for name in ISSUANCE_RECORD_NAMES):
        return "PROBE_IDENTITY_ALREADY_USED"
    if ticket.get("issuance_authority") != "authorized_not_issued":
        return "ISSUANCE_NOT_AUTHORIZED"
    return None


def observe_cli_version(executable: str) -> str | None:
    try:
        completed = subprocess.run(
            [executable, "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if completed.returncode != 0:
        return None
    value = completed.stdout.strip()
    return value or None


def runtime_inventory_rejection(ticket: dict[str, Any], observed_cli_version: str | None) -> str | None:
    if observed_cli_version is None:
        return "RUNTIME_VERSION_UNAVAILABLE"
    runtime = ticket.get("runtime")
    if not isinstance(runtime, dict):
        return "SCHEMA_INVALID"
    if observed_cli_version != f"codex-cli {runtime.get('version')}":
        return "RUNTIME_VERSION_MISMATCH"
    return None


def validate_ticket(
    ticket_path: Path,
    schema_path: Path,
    repo_root: Path,
    issuance_root: Path,
    observed_cli_version: str | None,
) -> dict[str, Any]:
    ticket = load_object(ticket_path)
    schema = load_object(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    rejection = contract_rejection_code(ticket, schema, repo_root)
    if rejection is None:
        rejection = runtime_inventory_rejection(ticket, observed_cli_version)
    if rejection is None:
        rejection = issuance_rejection(ticket, repo_root, issuance_root)
    return {
        "schema_version": VALIDATION_RECEIPT_SCHEMA,
        "operation": "validate-ticket",
        "probe_id": ticket.get("probe_id"),
        "ticket_sha256": sha256_file(ticket_path),
        "observed_cli_version": observed_cli_version,
        "model_invocations": 0,
        "dispatch_state": "allowed" if rejection is None else "denied",
        "reason": rejection,
    }


def replace_json_pointer(value: dict[str, Any], pointer: str, replacement: Any) -> None:
    if not pointer.startswith("/"):
        raise PreflightError(f"invalid JSON Pointer: {pointer}")
    parts = [item.replace("~1", "/").replace("~0", "~") for item in pointer[1:].split("/")]
    target: Any = value
    for part in parts[:-1]:
        if not isinstance(target, dict) or part not in target:
            raise PreflightError(f"JSON Pointer does not exist: {pointer}")
        target = target[part]
    if not isinstance(target, dict) or not parts or parts[-1] not in target:
        raise PreflightError(f"JSON Pointer does not exist: {pointer}")
    target[parts[-1]] = replacement


def validate_negative_fixtures(
    ticket_path: Path,
    schema_path: Path,
    fixtures_path: Path,
    repo_root: Path,
) -> dict[str, Any]:
    ticket = load_object(ticket_path)
    schema = load_object(schema_path)
    fixtures = load_object(fixtures_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    base = fixtures.get("base_ticket")
    if not isinstance(base, dict) or base.get("sha256") != sha256_file(ticket_path):
        raise PreflightError("negative fixture base ticket identity mismatch")
    if fixtures.get("mutation_format") != "single_json_pointer_replace":
        raise PreflightError("unsupported negative fixture mutation format")
    cases = fixtures.get("cases")
    if not isinstance(cases, list):
        raise PreflightError("negative fixture cases must be an array")

    case_receipts = []
    seen: set[str] = set()
    for case in cases:
        if not isinstance(case, dict) or set(case) != {"case_id", "pointer", "value", "expected_rejection"}:
            raise PreflightError("negative fixture case fields mismatch")
        case_id = case["case_id"]
        if not isinstance(case_id, str) or case_id in seen:
            raise PreflightError(f"duplicate or invalid negative fixture identity: {case_id}")
        seen.add(case_id)
        mutated = copy.deepcopy(ticket)
        replace_json_pointer(mutated, case["pointer"], case["value"])
        observed = contract_rejection_code(mutated, schema, repo_root)
        passed = observed == case["expected_rejection"]
        case_receipts.append(
            {
                "case_id": case_id,
                "expected_rejection": case["expected_rejection"],
                "observed_rejection": observed,
                "passed": passed,
            }
        )
    return {
        "schema_version": VALIDATION_RECEIPT_SCHEMA,
        "operation": "validate-negative-fixtures",
        "probe_id": ticket.get("probe_id"),
        "ticket_sha256": sha256_file(ticket_path),
        "fixtures_sha256": sha256_file(fixtures_path),
        "model_invocations": 0,
        "case_count": len(case_receipts),
        "passed": bool(case_receipts) and all(item["passed"] for item in case_receipts),
        "cases": case_receipts,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    subparsers = value.add_subparsers(dest="operation", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--ticket", type=Path, default=DEFAULT_TICKET)
    common.add_argument("--schema", type=Path, default=DEFAULT_TICKET_SCHEMA)
    common.add_argument("--repo-root", type=Path, default=ROOT)

    ticket = subparsers.add_parser("validate-ticket", parents=[common])
    ticket.add_argument("--issuance-root", type=Path, default=DEFAULT_ISSUANCE_ROOT)

    negative = subparsers.add_parser("validate-negative-fixtures", parents=[common])
    negative.add_argument("--fixtures", type=Path, default=DEFAULT_NEGATIVE_FIXTURES)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        if args.operation == "validate-ticket":
            ticket = load_object(args.ticket.resolve())
            runtime = ticket.get("runtime") if isinstance(ticket.get("runtime"), dict) else {}
            executable = runtime.get("executable") if isinstance(runtime.get("executable"), str) else "codex"
            receipt = validate_ticket(
                args.ticket.resolve(),
                args.schema.resolve(),
                args.repo_root.resolve(),
                args.issuance_root.resolve(),
                observe_cli_version(executable),
            )
        else:
            receipt = validate_negative_fixtures(
                args.ticket.resolve(), args.schema.resolve(), args.fixtures.resolve(), args.repo_root.resolve()
            )
    except (PreflightError, jsonschema.SchemaError) as error:
        print(json.dumps({"schema_version": VALIDATION_RECEIPT_SCHEMA, "status": "validator_error", "error": str(error)}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    if args.operation == "validate-negative-fixtures" and not receipt["passed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
