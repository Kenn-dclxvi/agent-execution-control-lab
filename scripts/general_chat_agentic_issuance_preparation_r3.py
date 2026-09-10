#!/usr/bin/env python3
"""Validate one-issue preparation without invoking or authorizing a probe."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib
import json
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TICKET = ROOT / "docs/general-chat-agentic-capability-preflight-ticket-r3.json"
DEFAULT_SCHEMA = ROOT / "docs/general-chat-agentic-capability-preflight-ticket-r3.schema.json"
DEFAULT_NEGATIVE_FIXTURES = ROOT / "docs/general-chat-agentic-issuance-preparation-negative-fixtures-r3.json"
RECEIPT_SCHEMA_VERSION = "general-chat-agentic-issuance-preparation/v1"
EXPECTED_RECORD_NAMES = ("reservation.json", "issued.json", "receipt.json")


class IssuancePreparationError(Exception):
    """The issuance preparation input could not be loaded or interpreted."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise IssuancePreparationError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise IssuancePreparationError(f"JSON value must be an object: {path}")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_rejection(ticket: dict[str, Any]) -> str | None:
    adapter = ticket.get("private_trace_adapter") or {}
    policy = ticket.get("issuance_policy") or {}
    records = ticket.get("issuance_records") or {}
    storage = ticket.get("storage_policy") or {}
    checks = (
        (ticket.get("issuance_authority") == "not_authorized", "ISSUANCE_AUTHORITY_NOT_FIXED"),
        (adapter.get("technical_state") == "shadow_verified", "ADAPTER_TECHNICAL_STATE_MISMATCH"),
        (adapter.get("real_trace_observed") is False, "REAL_TRACE_OBSERVED_UNEXPECTED"),
        (adapter.get("discovery_allowed") is False, "ADAPTER_DISCOVERY_ENABLED"),
        (policy.get("max_issues") == 1, "MAX_ISSUES_MISMATCH"),
        (policy.get("retry") is False, "RETRY_ENABLED"),
        (policy.get("overwrite") is False, "OVERWRITE_ENABLED"),
        (records.get("root") == "artifacts/capability-preflight-issuance", "ISSUANCE_ROOT_MISMATCH"),
        (records.get("names") == list(EXPECTED_RECORD_NAMES), "ISSUANCE_RECORD_NAMES_MISMATCH"),
        (records.get("write_once") is True, "ISSUANCE_RECORD_WRITE_ONCE_DISABLED"),
        (records.get("commit_allowed") is False, "ISSUANCE_RECORD_COMMIT_ENABLED"),
        (
            storage.get("cleanup_terminal") == "receipt_sealed_or_terminal_failure",
            "CLEANUP_TERMINAL_MISMATCH",
        ),
    )
    for passed, reason in checks:
        if not passed:
            return reason
    return None


def schema_rejection(ticket: dict[str, Any], schema: dict[str, Any]) -> str | None:
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
    except jsonschema.SchemaError:
        return "TICKET_SCHEMA_INVALID"
    error = next(jsonschema.Draft202012Validator(schema).iter_errors(ticket), None)
    return "TICKET_SCHEMA_INVALID" if error is not None else None


def identity_rejection(
    repository_root: Path, identity: dict[str, Any], label: str
) -> tuple[str | None, Path | None]:
    root = repository_root.resolve()
    if not isinstance(identity, dict) or not isinstance(identity.get("path"), str):
        return f"{label}_IDENTITY_INVALID", None
    path = (root / identity["path"]).resolve()
    try:
        path.relative_to(root)
    except ValueError:
        return f"{label}_PATH_INVALID", None
    if not path.is_file():
        return f"{label}_PATH_INVALID", None
    try:
        data = path.read_bytes()
    except OSError:
        return f"{label}_UNREADABLE", None
    if len(data) != identity.get("bytes"):
        return f"{label}_BYTES_MISMATCH", None
    if hashlib.sha256(data).hexdigest() != identity.get("sha256"):
        return f"{label}_SHA256_MISMATCH", None
    return None, path


def bound_paths(
    ticket: dict[str, Any], repository_root: Path
) -> tuple[str | None, dict[str, Path]]:
    identities = {
        "PREPARATION_OUTPUT_SCHEMA": ticket.get("preparation_output_schema"),
        "LINEAGE": (ticket.get("lineage") or {}).get("artifact"),
        "COMPOSITION_INPUT": (ticket.get("composition_readiness") or {}).get("input"),
        "COMPOSITION_INPUT_SCHEMA": (ticket.get("composition_readiness") or {}).get("input_schema"),
        "COMPOSITION_OUTPUT_SCHEMA": (ticket.get("composition_readiness") or {}).get("output_schema"),
        "COMPOSITION_VALIDATOR": (ticket.get("composition_readiness") or {}).get("validator"),
        "ADAPTER_VALIDATOR": (ticket.get("private_trace_adapter") or {}).get("validator"),
        "ADAPTER_INPUT_SCHEMA": (ticket.get("private_trace_adapter") or {}).get("input_schema"),
        "ADAPTER_OUTPUT_SCHEMA": (ticket.get("private_trace_adapter") or {}).get("output_schema"),
        "TASK": (ticket.get("artifacts") or {}).get("task"),
        "FIXTURE": (ticket.get("artifacts") or {}).get("fixture"),
    }
    paths = {}
    for label, identity in identities.items():
        rejection, path = identity_rejection(repository_root, identity, label)
        if rejection is not None or path is None:
            return rejection, {}
        paths[label] = path
    return None, paths


def composition_rejection(
    ticket: dict[str, Any], paths: dict[str, Path], repository_root: Path
) -> tuple[str | None, dict[str, Any] | None]:
    lineage = load_object(paths["LINEAGE"])
    composition_input = load_object(paths["COMPOSITION_INPUT"])
    readiness = ticket["composition_readiness"]
    if (
        lineage.get("probe_id") != readiness.get("required_state", {}).get("probe_id", lineage.get("probe_id"))
        or lineage.get("probe_id") != "general-chat-agentic-capability-preflight-r2"
        or composition_input.get("composition_id") != readiness.get("composition_id")
        or composition_input.get("probe_id") != lineage.get("probe_id")
    ):
        return "READINESS_RELATION_MISMATCH", None
    try:
        try:
            module = importlib.import_module("scripts.general_chat_agentic_composition_preflight_r2")
        except ModuleNotFoundError:
            module = importlib.import_module("general_chat_agentic_composition_preflight_r2")
        schema = load_object(paths["COMPOSITION_INPUT_SCHEMA"])
        module.validate(composition_input, schema, "COMPOSITION_INPUT_SCHEMA_INVALID")
        receipt = module.compose(composition_input, repository_root)
    except Exception:
        return "COMPOSITION_READINESS_UNAVAILABLE", None
    required = readiness["required_state"]
    observed = {key: receipt.get(key) for key in required}
    if observed != required:
        return "COMPOSITION_REQUIRED_STATE_MISMATCH", None
    return None, receipt


def issuance_rejection(ticket: dict[str, Any], repository_root: Path) -> tuple[str | None, bool]:
    root = repository_root.resolve()
    issuance_root = (root / ticket["issuance_records"]["root"]).resolve()
    try:
        issuance_root.relative_to(root)
    except ValueError:
        return "ISSUANCE_ROOT_OUTSIDE_REPOSITORY", False
    identity_root = issuance_root / ticket["probe_id"]
    if any((identity_root / name).exists() for name in EXPECTED_RECORD_NAMES):
        return "PROBE_IDENTITY_ALREADY_USED", False
    if ticket["issuance_authority"] != "authorized_not_issued":
        return "ISSUANCE_NOT_AUTHORIZED", True
    return None, True


def validate_ticket(
    ticket: dict[str, Any], schema: dict[str, Any], repository_root: Path
) -> dict[str, Any]:
    rejection = semantic_rejection(ticket)
    paths: dict[str, Path] = {}
    composition_receipt = None
    if rejection is None:
        rejection = schema_rejection(ticket, schema)
    if rejection is None:
        rejection, paths = bound_paths(ticket, repository_root)
    if rejection is None:
        rejection, composition_receipt = composition_rejection(ticket, paths, repository_root)
    identity_available = False
    if rejection is None:
        rejection, identity_available = issuance_rejection(ticket, repository_root)
    readiness = ticket.get("composition_readiness") or {}
    adapter = ticket.get("private_trace_adapter") or {}
    return {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "probe_id": ticket.get("probe_id"),
        "ticket_sha256": None,
        "direct_predecessor": (ticket.get("lineage") or {}).get("direct_predecessor"),
        "composition_id": readiness.get("composition_id"),
        "runtime_identity_state": (
            composition_receipt.get("runtime_identity_state") if composition_receipt is not None else "unobserved"
        ),
        "adapter_technical_state": adapter.get("technical_state"),
        "real_trace_observed": adapter.get("real_trace_observed"),
        "identity_available": identity_available,
        "issuance_authority": ticket.get("issuance_authority"),
        "preparation_state": "ready_not_authorized" if rejection == "ISSUANCE_NOT_AUTHORIZED" else "unavailable",
        "dispatch_state": "allowed" if rejection is None else "denied",
        "reason": rejection,
        "model_invocations": 0,
        "real_trace_reads": 0,
        "probe_issues": 0,
    }


def validate_ticket_path(ticket_path: Path, schema_path: Path, repository_root: Path) -> dict[str, Any]:
    ticket = load_object(ticket_path)
    schema = load_object(schema_path)
    receipt = validate_ticket(ticket, schema, repository_root)
    receipt["ticket_sha256"] = sha256_file(ticket_path)
    if receipt["preparation_state"] == "ready_not_authorized":
        output_schema_path = (repository_root / ticket["preparation_output_schema"]["path"]).resolve()
        output_schema = load_object(output_schema_path)
        jsonschema.Draft202012Validator.check_schema(output_schema)
        jsonschema.Draft202012Validator(output_schema).validate(receipt)
    return receipt


def replace_json_pointer(value: dict[str, Any], pointer: str, replacement: Any) -> None:
    parts = [item.replace("~1", "/").replace("~0", "~") for item in pointer[1:].split("/")]
    target: Any = value
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    if isinstance(target, list):
        target[int(parts[-1])] = replacement
    else:
        target[parts[-1]] = replacement


def validate_negative_fixtures(
    ticket_path: Path, schema_path: Path, fixtures_path: Path, repository_root: Path
) -> dict[str, Any]:
    ticket = load_object(ticket_path)
    schema = load_object(schema_path)
    fixtures = load_object(fixtures_path)
    if fixtures.get("base_ticket") != {
        "path": ticket_path.relative_to(repository_root).as_posix(),
        "sha256": sha256_file(ticket_path),
    }:
        raise IssuancePreparationError("negative fixture base identity mismatch")
    cases = []
    for case in fixtures["cases"]:
        mutated = copy.deepcopy(ticket)
        replace_json_pointer(mutated, case["pointer"], case["value"])
        receipt = validate_ticket(mutated, schema, repository_root)
        observed = receipt["reason"]
        cases.append(
            {
                "case_id": case["case_id"],
                "expected_rejection": case["expected_rejection"],
                "observed_rejection": observed,
                "passed": observed == case["expected_rejection"],
            }
        )
    return {
        "schema_version": "general-chat-agentic-issuance-preparation-negative-result/v1",
        "case_count": len(cases),
        "passed": all(case["passed"] for case in cases),
        "model_invocations": 0,
        "real_trace_reads": 0,
        "probe_issues": 0,
        "cases": cases,
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    subparsers = value.add_subparsers(dest="operation", required=True)
    ticket = subparsers.add_parser("validate-ticket")
    ticket.add_argument("--ticket", type=Path, default=DEFAULT_TICKET)
    ticket.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    ticket.add_argument("--repository-root", type=Path, default=ROOT)
    negative = subparsers.add_parser("validate-negative-fixtures")
    negative.add_argument("--ticket", type=Path, default=DEFAULT_TICKET)
    negative.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    negative.add_argument("--fixtures", type=Path, default=DEFAULT_NEGATIVE_FIXTURES)
    negative.add_argument("--repository-root", type=Path, default=ROOT)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        if args.operation == "validate-ticket":
            result = validate_ticket_path(
                args.ticket.resolve(), args.schema.resolve(), args.repository_root.resolve()
            )
        else:
            result = validate_negative_fixtures(
                args.ticket.resolve(),
                args.schema.resolve(),
                args.fixtures.resolve(),
                args.repository_root.resolve(),
            )
    except (IssuancePreparationError, jsonschema.SchemaError, jsonschema.ValidationError) as error:
        print(
            json.dumps(
                {"schema_version": RECEIPT_SCHEMA_VERSION, "status": "validator_error", "error": str(error)},
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
