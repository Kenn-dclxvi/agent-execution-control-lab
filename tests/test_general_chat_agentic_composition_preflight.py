from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.general_chat_agentic_composition_preflight import (
    CompositionError,
    DEFAULT_INPUT,
    DEFAULT_SCHEMA,
    ROOT,
    compose,
    load_object,
    validate_input,
)


def input_value() -> dict:
    value = load_object(DEFAULT_INPUT, "TEST_INPUT_UNAVAILABLE")
    validate_input(value, load_object(DEFAULT_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"))
    return value


def runtime_available() -> bool:
    value = input_value()
    ticket = load_object(ROOT / value["runtime"]["ticket"]["path"], "TEST_TICKET_UNAVAILABLE")
    runtime = ticket["runtime_ref"]
    return Path(runtime["alias"]["path"]).is_file() and Path(runtime["manifest"]["path"]).is_file()


def test_fixed_composition_input_is_schema_valid() -> None:
    value = input_value()
    assert value["mode"] == "model_free_synthetic_composition"
    assert value["output_schema"]["path"].endswith("composition-preflight-output.schema.json")
    assert value["expected"]["dispatch_state"] == "denied"
    assert value["expected"]["model_invocations"] == 0
    assert value["expected"]["real_trace_reads"] == 0
    assert value["expected"]["probe_issues"] == 0


@pytest.mark.skipif(not runtime_available(), reason="host-local exact Codex 0.146.0 registry is unavailable")
def test_exact_runtime_and_synthetic_adapter_compose_without_dispatch() -> None:
    receipt = compose(input_value())
    assert receipt["runtime_identity_state"] == "verified"
    assert receipt["adapter_state"] == "synthetic_verified"
    assert receipt["adapter_input_mode"] == "synthetic_repository_fixture"
    assert receipt["binding_admission"] == "agentic_runtime_capability_unavailable"
    assert receipt["ticket_real_trace_adapter_ready"] is False
    assert receipt["issuance_authority"] == "not_authorized"
    assert receipt["dispatch_state"] == "denied"
    assert receipt["reasons"] == ["REAL_TRACE_ADAPTER_NOT_READY", "ISSUANCE_NOT_AUTHORIZED"]
    assert receipt["model_invocations"] == 0
    assert receipt["real_trace_reads"] == 0
    assert receipt["probe_issues"] == 0
    rendered = json.dumps(receipt, ensure_ascii=False, sort_keys=True)
    assert "agent_path" not in rendered
    assert "/Users/" not in rendered


def test_dependency_hash_drift_fails_before_composition() -> None:
    value = input_value()
    value["adapter"]["validator"]["sha256"] = "0" * 64
    with pytest.raises(CompositionError, match="COMPOSITION_FILE_HASH_MISMATCH"):
        compose(value)


def test_cross_artifact_schema_identity_mismatch_fails_closed() -> None:
    value = input_value()
    value["adapter"]["normalized_schema"] = copy.deepcopy(value["adapter"]["packet_schema"])
    with pytest.raises(CompositionError, match="COMPOSITION_IDENTITY_RELATION_MISMATCH"):
        compose(value)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("runtime_identity_state", "unavailable"),
        ("adapter_state", "real_trace_verified"),
        ("binding_admission", "agentic_runtime_capability_available"),
        ("dispatch_state", "allowed"),
        ("model_invocations", 1),
        ("real_trace_reads", 1),
        ("probe_issues", 1),
    ],
)
def test_schema_rejects_composition_state_escalation(field: str, value: object) -> None:
    candidate = input_value()
    candidate["expected"][field] = value
    with pytest.raises(CompositionError, match="COMPOSITION_INPUT_SCHEMA_INVALID"):
        validate_input(candidate, load_object(DEFAULT_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"))


def test_schema_rejects_path_escape() -> None:
    value = input_value()
    value["binding"]["fixture"]["path"] = "docs/../outside.json"
    with pytest.raises(CompositionError, match="COMPOSITION_INPUT_SCHEMA_INVALID"):
        validate_input(value, load_object(DEFAULT_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"))
