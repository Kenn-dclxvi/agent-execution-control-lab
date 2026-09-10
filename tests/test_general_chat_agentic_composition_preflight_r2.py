from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.general_chat_agentic_composition_preflight_r2 import (
    CompositionR2Error,
    DEFAULT_INPUT,
    DEFAULT_SCHEMA,
    ROOT,
    compose,
    load_object,
    validate,
)


def input_value() -> dict:
    value = load_object(DEFAULT_INPUT, "TEST_INPUT_UNAVAILABLE")
    validate(
        value,
        load_object(DEFAULT_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"),
        "TEST_INPUT_SCHEMA_INVALID",
    )
    return value


def runtime_available() -> bool:
    value = input_value()
    ticket = load_object(ROOT / value["runtime"]["ticket"]["path"], "TEST_TICKET_UNAVAILABLE")
    runtime = ticket["runtime_ref"]
    return Path(runtime["alias"]["path"]).is_file() and Path(runtime["manifest"]["path"]).is_file()


def test_fixed_r2_input_is_schema_valid_and_delta_is_narrow() -> None:
    value = input_value()
    assert value["lineage"]["direct_predecessor"] == "general-chat-agentic-composition-preflight-r1"
    assert value["lineage"]["allowed_delta"] == "synthetic_adapter_to_private_trace_shadow"
    assert value["mode"] == "model_free_private_trace_shadow_composition"
    assert value["expected"]["dispatch_state"] == "denied"
    assert value["expected"]["real_trace_reads"] == 0


@pytest.mark.skipif(not runtime_available(), reason="host-local exact Codex 0.146.0 registry is unavailable")
def test_exact_runtime_and_private_shadow_compose_without_dispatch() -> None:
    receipt = compose(input_value())
    assert receipt["runtime_identity_state"] == "verified"
    assert receipt["adapter_state"] == "private_trace_shadow_verified"
    assert receipt["trace_origin"] == "synthetic_shadow"
    assert receipt["projection_state"] == "synthetic_shadow_verified"
    assert receipt["binding_admission"] == "agentic_runtime_capability_unavailable"
    assert receipt["ticket_real_trace_adapter_ready"] is False
    assert receipt["issuance_authority"] == "not_authorized"
    assert receipt["dispatch_state"] == "denied"
    assert receipt["reasons"] == ["REAL_TRACE_ADAPTER_NOT_READY", "ISSUANCE_NOT_AUTHORIZED"]
    assert receipt["model_invocations"] == 0
    assert receipt["real_trace_reads"] == 0
    assert receipt["probe_issues"] == 0
    assert receipt["mutation_performed"] is False
    assert receipt["raw_path_count"] == 0
    rendered = json.dumps(receipt, ensure_ascii=False, sort_keys=True)
    assert "/Users/" not in rendered
    assert "agent_path" not in rendered


@pytest.mark.parametrize(
    ("section", "field"),
    [
        ("lineage", "artifact"),
        ("adapter", "validator"),
        ("adapter", "normalizer"),
        ("adapter", "synthetic_adapter_dependency"),
    ],
)
def test_bound_dependency_hash_drift_fails_closed(section: str, field: str) -> None:
    value = input_value()
    value[section][field]["sha256"] = "0" * 64
    with pytest.raises(CompositionR2Error, match="COMPOSITION_FILE_HASH_MISMATCH"):
        compose(value)


def test_cross_artifact_normalized_schema_mismatch_fails_closed() -> None:
    value = input_value()
    value["adapter"]["normalized_schema"] = copy.deepcopy(value["adapter"]["input_schema"])
    with pytest.raises(CompositionR2Error, match="COMPOSITION_IDENTITY_RELATION_MISMATCH"):
        compose(value)


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("runtime_identity_state", "unavailable"),
        ("adapter_state", "issued_probe_verified"),
        ("trace_origin", "issued_probe"),
        ("binding_admission", "agentic_runtime_capability_available"),
        ("dispatch_state", "allowed"),
        ("model_invocations", 1),
        ("real_trace_reads", 1),
        ("probe_issues", 1),
        ("mutation_performed", True),
        ("raw_path_count", 1),
    ],
)
def test_schema_rejects_r2_state_escalation(field: str, replacement: object) -> None:
    value = input_value()
    value["expected"][field] = replacement
    with pytest.raises(CompositionR2Error, match="COMPOSITION_INPUT_SCHEMA_INVALID"):
        validate(
            value,
            load_object(DEFAULT_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"),
            "COMPOSITION_INPUT_SCHEMA_INVALID",
        )


def test_schema_rejects_shadow_root_drift() -> None:
    value = input_value()
    value["adapter"]["shadow_root"] = "docs/other-shadow"
    with pytest.raises(CompositionR2Error, match="COMPOSITION_INPUT_SCHEMA_INVALID"):
        validate(
            value,
            load_object(DEFAULT_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"),
            "COMPOSITION_INPUT_SCHEMA_INVALID",
        )
