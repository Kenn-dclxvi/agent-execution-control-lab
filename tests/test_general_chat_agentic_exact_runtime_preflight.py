from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import jsonschema
import pytest

from scripts.general_chat_agentic_exact_runtime_preflight import (
    DEFAULT_SCHEMA,
    DEFAULT_TICKET,
    ROOT,
    load_object,
    validate_ticket,
    verify_ticket,
)


NEGATIVE_FIXTURES = ROOT / "docs/general-chat-agentic-exact-runtime-negative-fixtures-r2.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def set_json_pointer(value: dict, pointer: str, replacement: object) -> None:
    parts = [item.replace("~1", "/").replace("~0", "~") for item in pointer[1:].split("/")]
    target: object = value
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    if isinstance(target, list):
        target[int(parts[-1])] = replacement
    else:
        target[parts[-1]] = replacement


def runtime_available() -> bool:
    ticket = load_object(DEFAULT_TICKET)
    runtime = ticket["runtime_ref"]
    return Path(runtime["alias"]["path"]).is_file() and Path(runtime["manifest"]["path"]).is_file()


def test_r2_ticket_and_negative_fixture_base_are_schema_valid() -> None:
    ticket = load_object(DEFAULT_TICKET)
    schema = load_object(DEFAULT_SCHEMA)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(schema).validate(ticket)
    fixtures = load_object(NEGATIVE_FIXTURES)
    assert fixtures["base_ticket"] == {
        "path": "docs/general-chat-agentic-capability-preflight-ticket-r2.json",
        "sha256": sha256(DEFAULT_TICKET),
    }


@pytest.mark.skipif(not runtime_available(), reason="host-local exact Codex 0.146.0 registry is unavailable")
def test_exact_runtime_is_verified_but_dispatch_remains_denied() -> None:
    receipt = validate_ticket(DEFAULT_TICKET, DEFAULT_SCHEMA, ROOT)
    assert receipt["runtime_identity_state"] == "verified"
    assert receipt["entrypoint"].endswith("/bundle/bin/codex")
    assert receipt["dispatch_state"] == "denied"
    assert receipt["reasons"] == ["REAL_TRACE_ADAPTER_NOT_READY", "ISSUANCE_NOT_AUTHORIZED"]
    assert receipt["model_invocations"] == 0


@pytest.mark.skipif(not runtime_available(), reason="host-local exact Codex 0.146.0 registry is unavailable")
def test_six_exact_runtime_negative_fixtures_fail_by_fixed_reason() -> None:
    ticket = load_object(DEFAULT_TICKET)
    schema = load_object(DEFAULT_SCHEMA)
    fixtures = load_object(NEGATIVE_FIXTURES)
    seen = set()
    for case in fixtures["cases"]:
        assert case["case_id"] not in seen
        seen.add(case["case_id"])
        mutated = copy.deepcopy(ticket)
        set_json_pointer(mutated, case["pointer"], case["value"])
        receipt = verify_ticket(mutated, schema, ROOT)
        assert receipt["runtime_identity_state"] == "unavailable", case["case_id"]
        assert receipt["dispatch_state"] == "denied", case["case_id"]
        assert receipt["reasons"] == [case["expected_rejection"]], case["case_id"]
        assert receipt["model_invocations"] == 0
    assert len(seen) == 6
