from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from scripts.general_chat_agentic_capability_preflight import (
    DEFAULT_ISSUANCE_ROOT,
    DEFAULT_NEGATIVE_FIXTURES,
    DEFAULT_TICKET,
    DEFAULT_TICKET_SCHEMA,
    ROOT,
    contract_rejection_code,
    load_object,
    runtime_inventory_rejection,
    validate_negative_fixtures,
    validate_ticket,
)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def materialize_ticket(tmp_path: Path, *, authority: str = "not_authorized") -> tuple[Path, Path]:
    ticket = load_object(DEFAULT_TICKET)
    ticket["issuance_authority"] = authority
    for name, identity in ticket["artifacts"].items():
        source = ROOT / identity["path"]
        destination = tmp_path / identity["path"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
        assert sha256(destination) == identity["sha256"], name
    ticket_path = tmp_path / "ticket.json"
    write_json(ticket_path, ticket)
    return ticket_path, tmp_path / "issuance"


def test_fixed_ticket_is_valid_but_not_authorized_to_issue() -> None:
    receipt = validate_ticket(
        DEFAULT_TICKET, DEFAULT_TICKET_SCHEMA, ROOT, DEFAULT_ISSUANCE_ROOT, "codex-cli 0.146.0"
    )
    assert receipt == {
        "schema_version": "general-chat-agentic-capability-static-validation/v1",
        "operation": "validate-ticket",
        "probe_id": "general-chat-agentic-capability-preflight-r1",
        "ticket_sha256": sha256(DEFAULT_TICKET),
        "observed_cli_version": "codex-cli 0.146.0",
        "model_invocations": 0,
        "dispatch_state": "denied",
        "reason": "ISSUANCE_NOT_AUTHORIZED",
    }


def test_all_fixed_negative_fixtures_are_rejected_by_exact_reason() -> None:
    receipt = validate_negative_fixtures(
        DEFAULT_TICKET, DEFAULT_TICKET_SCHEMA, DEFAULT_NEGATIVE_FIXTURES, ROOT
    )
    assert receipt["model_invocations"] == 0
    assert receipt["case_count"] == 16
    assert receipt["passed"] is True
    assert all(item["passed"] for item in receipt["cases"])
    assert all(item["observed_rejection"] == item["expected_rejection"] for item in receipt["cases"])


def test_authorized_ticket_allows_dispatch_only_without_prior_identity(tmp_path: Path) -> None:
    ticket_path, issuance_root = materialize_ticket(tmp_path, authority="authorized_not_issued")
    receipt = validate_ticket(
        ticket_path, DEFAULT_TICKET_SCHEMA, tmp_path, issuance_root, "codex-cli 0.146.0"
    )
    assert receipt["dispatch_state"] == "allowed"
    assert receipt["reason"] is None
    assert receipt["model_invocations"] == 0


def test_existing_reservation_denies_authorized_ticket(tmp_path: Path) -> None:
    ticket_path, issuance_root = materialize_ticket(tmp_path, authority="authorized_not_issued")
    identity_root = issuance_root / "general-chat-agentic-capability-preflight-r1"
    write_json(identity_root / "reservation.json", {"reserved": True})
    receipt = validate_ticket(
        ticket_path, DEFAULT_TICKET_SCHEMA, tmp_path, issuance_root, "codex-cli 0.146.0"
    )
    assert receipt["dispatch_state"] == "denied"
    assert receipt["reason"] == "PROBE_IDENTITY_ALREADY_USED"


def test_artifact_drift_is_terminal_before_issuance(tmp_path: Path) -> None:
    ticket_path, issuance_root = materialize_ticket(tmp_path, authority="authorized_not_issued")
    task = tmp_path / load_object(ticket_path)["artifacts"]["task"]["path"]
    task.write_text(task.read_text(encoding="utf-8") + "drift\n", encoding="utf-8")
    receipt = validate_ticket(
        ticket_path, DEFAULT_TICKET_SCHEMA, tmp_path, issuance_root, "codex-cli 0.146.0"
    )
    assert receipt["dispatch_state"] == "denied"
    assert receipt["reason"] == "TASK_BYTES_MISMATCH"


def test_schema_drift_not_named_by_runtime_checks_is_rejected() -> None:
    ticket = copy.deepcopy(load_object(DEFAULT_TICKET))
    ticket["unexpected"] = True
    schema = load_object(DEFAULT_TICKET_SCHEMA)
    assert contract_rejection_code(ticket, schema, ROOT) == "SCHEMA_INVALID"


def test_issuance_root_outside_repository_is_rejected(tmp_path: Path) -> None:
    receipt = validate_ticket(
        DEFAULT_TICKET, DEFAULT_TICKET_SCHEMA, ROOT, tmp_path, "codex-cli 0.146.0"
    )
    assert receipt["dispatch_state"] == "denied"
    assert receipt["reason"] == "ISSUANCE_ROOT_OUTSIDE_REPOSITORY"


def test_runtime_inventory_drift_precedes_issuance_authority() -> None:
    ticket = load_object(DEFAULT_TICKET)
    assert runtime_inventory_rejection(ticket, "codex-cli 0.148.0") == "RUNTIME_VERSION_MISMATCH"
    receipt = validate_ticket(
        DEFAULT_TICKET, DEFAULT_TICKET_SCHEMA, ROOT, DEFAULT_ISSUANCE_ROOT, "codex-cli 0.148.0"
    )
    assert receipt["dispatch_state"] == "denied"
    assert receipt["reason"] == "RUNTIME_VERSION_MISMATCH"
    assert receipt["observed_cli_version"] == "codex-cli 0.148.0"
    assert receipt["model_invocations"] == 0


def test_unavailable_runtime_inventory_denies_dispatch() -> None:
    ticket = load_object(DEFAULT_TICKET)
    assert runtime_inventory_rejection(ticket, None) == "RUNTIME_VERSION_UNAVAILABLE"
