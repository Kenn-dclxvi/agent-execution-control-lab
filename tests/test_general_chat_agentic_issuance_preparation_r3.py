from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import jsonschema
import pytest

from scripts.general_chat_agentic_issuance_preparation_r3 import (
    DEFAULT_NEGATIVE_FIXTURES,
    DEFAULT_SCHEMA,
    DEFAULT_TICKET,
    ROOT,
    issuance_rejection,
    load_object,
    semantic_rejection,
    validate_negative_fixtures,
    validate_ticket_path,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def test_fixed_r3_ticket_remains_unmodified_after_identity_is_used() -> None:
    receipt = validate_ticket_path(DEFAULT_TICKET, DEFAULT_SCHEMA, ROOT)
    assert receipt == {
        "schema_version": "general-chat-agentic-issuance-preparation/v1",
        "probe_id": "general-chat-agentic-capability-preflight-r3",
        "ticket_sha256": sha256(DEFAULT_TICKET),
        "direct_predecessor": "general-chat-agentic-capability-preflight-r2",
        "composition_id": "general-chat-agentic-composition-preflight-r2",
        "runtime_identity_state": "verified",
        "adapter_technical_state": "shadow_verified",
        "real_trace_observed": False,
        "identity_available": False,
        "issuance_authority": "not_authorized",
        "preparation_state": "unavailable",
        "dispatch_state": "denied",
        "reason": "PROBE_IDENTITY_ALREADY_USED",
        "model_invocations": 0,
        "real_trace_reads": 0,
        "probe_issues": 0,
    }


def test_fixed_ticket_and_historical_ready_output_schema_remain_valid() -> None:
    ticket = load_object(DEFAULT_TICKET)
    ticket_schema = load_object(DEFAULT_SCHEMA)
    jsonschema.Draft202012Validator.check_schema(ticket_schema)
    jsonschema.Draft202012Validator(ticket_schema).validate(ticket)
    receipt = validate_ticket_path(DEFAULT_TICKET, DEFAULT_SCHEMA, ROOT)
    output_schema = load_object(ROOT / ticket["preparation_output_schema"]["path"])
    jsonschema.Draft202012Validator.check_schema(output_schema)
    assert receipt["reason"] == "PROBE_IDENTITY_ALREADY_USED"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(output_schema).validate(receipt)


def test_fourteen_negative_fixtures_fail_by_fixed_reason() -> None:
    result = validate_negative_fixtures(
        DEFAULT_TICKET, DEFAULT_SCHEMA, DEFAULT_NEGATIVE_FIXTURES, ROOT
    )
    assert result["case_count"] == 14
    assert result["passed"] is True
    assert result["model_invocations"] == 0
    assert result["real_trace_reads"] == 0
    assert result["probe_issues"] == 0
    assert all(case["passed"] for case in result["cases"])


def test_authority_cannot_be_changed_inside_fixed_r3_ticket() -> None:
    ticket = copy.deepcopy(load_object(DEFAULT_TICKET))
    ticket["issuance_authority"] = "authorized_not_issued"
    assert semantic_rejection(ticket) == "ISSUANCE_AUTHORITY_NOT_FIXED"


def test_existing_record_makes_probe_identity_unavailable(tmp_path: Path) -> None:
    ticket = load_object(DEFAULT_TICKET)
    identity_root = (
        tmp_path
        / ticket["issuance_records"]["root"]
        / ticket["probe_id"]
    )
    write_json(identity_root / "reservation.json", {"reserved": True})
    rejection, available = issuance_rejection(ticket, tmp_path)
    assert rejection == "PROBE_IDENTITY_ALREADY_USED"
    assert available is False


def test_no_record_leaves_identity_available_but_authority_denied(tmp_path: Path) -> None:
    rejection, available = issuance_rejection(load_object(DEFAULT_TICKET), tmp_path)
    assert rejection == "ISSUANCE_NOT_AUTHORIZED"
    assert available is True


def test_issuance_root_escape_is_rejected(tmp_path: Path) -> None:
    ticket = copy.deepcopy(load_object(DEFAULT_TICKET))
    ticket["issuance_records"]["root"] = "../outside"
    rejection, available = issuance_rejection(ticket, tmp_path)
    assert rejection == "ISSUANCE_ROOT_OUTSIDE_REPOSITORY"
    assert available is False


def test_static_validation_creates_no_issuance_record() -> None:
    ticket = load_object(DEFAULT_TICKET)
    identity_root = ROOT / ticket["issuance_records"]["root"] / ticket["probe_id"]
    before = [path.name for path in identity_root.iterdir()] if identity_root.is_dir() else []
    validate_ticket_path(DEFAULT_TICKET, DEFAULT_SCHEMA, ROOT)
    after = [path.name for path in identity_root.iterdir()] if identity_root.is_dir() else []
    assert after == before


def test_issuance_record_root_is_ignored_by_git() -> None:
    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert "artifacts/capability-preflight-issuance/" in ignored
