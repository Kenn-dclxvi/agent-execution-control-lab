from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema
import pytest

from scripts.general_chat_agentic_binding_extractor import (
    DEFAULT_FIXTURE,
    DEFAULT_INPUT_SCHEMA,
    DEFAULT_OUTPUT_SCHEMA,
    DEFAULT_RECEIPT_SCHEMA,
    extract,
    load_object,
    validate_input,
    validate_output,
)


ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC_FIXTURES = ROOT / "docs/general-chat-agentic-binding-synthetic-traces-r1.json"


def set_json_pointer(value: dict, pointer: str, replacement: object) -> None:
    parts = [item.replace("~1", "/").replace("~0", "~") for item in pointer[1:].split("/")]
    target: object = value
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    if isinstance(target, list):
        target[int(parts[-1])] = replacement
    else:
        target[parts[-1]] = replacement


def schemas() -> tuple[dict, dict, dict]:
    return load_object(DEFAULT_INPUT_SCHEMA), load_object(DEFAULT_OUTPUT_SCHEMA), load_object(DEFAULT_RECEIPT_SCHEMA)


def test_normalized_synthetic_trace_and_twelve_counterexamples_match_contract() -> None:
    fixtures = load_object(SYNTHETIC_FIXTURES)
    fixture = load_object(DEFAULT_FIXTURE)
    input_schema, output_schema, receipt_schema = schemas()
    seen = set()
    for case in fixtures["cases"]:
        assert case["case_id"] not in seen
        seen.add(case["case_id"])
        trace = copy.deepcopy(fixtures["base_trace"])
        mutation = case["mutation"]
        if mutation is not None:
            set_json_pointer(trace, mutation["pointer"], mutation["value"])
        validate_input(trace, input_schema)
        result = extract(trace, fixture)
        validate_output(result, output_schema, receipt_schema)
        expected = {**fixtures["base_expected_criteria"], **case["expected_overrides"]}
        assert result["criteria"] == expected, case["case_id"]
        assert result["admission"] == case["expected_admission"], case["case_id"]
        assert result["synthetic_input"] is True
        assert result["sensitive_material_saved"] is False
    assert len(seen) == 13
    assert len([item for item in seen if "-N" in item]) == 12


def test_success_projection_contains_bindings_but_not_raw_terminal_text() -> None:
    fixtures = load_object(SYNTHETIC_FIXTURES)
    result = extract(fixtures["base_trace"], load_object(DEFAULT_FIXTURE))
    rendered = json.dumps(result, ensure_ascii=False, sort_keys=True)
    assert result["admission"] == "agentic_runtime_capability_available"
    assert result["bindings"]["spawn"]["requested_task_identity"] == "parking_fact_check"
    assert result["bindings"]["descendant"]["terminal_result_sha256"] is not None
    assert result["bindings"]["final_response"]["sha256"] is not None
    assert "土曜日は18時まで駐車できる（利用時間は18時30分まで）。" not in rendered
    assert "支店窓口は17時に終了します" not in rendered


def test_output_schema_rejects_available_label_with_missing_criterion() -> None:
    fixtures = load_object(SYNTHETIC_FIXTURES)
    result = extract(fixtures["base_trace"], load_object(DEFAULT_FIXTURE))
    result["criteria"]["worker_packet_projection"] = "unobserved"
    _, output_schema, receipt_schema = schemas()
    with pytest.raises(jsonschema.ValidationError):
        validate_output(result, output_schema, receipt_schema)


def test_input_schema_rejects_raw_rollout_field() -> None:
    fixtures = load_object(SYNTHETIC_FIXTURES)
    trace = copy.deepcopy(fixtures["base_trace"])
    trace["raw_rollout"] = "not allowed"
    input_schema, _, _ = schemas()
    with pytest.raises(jsonschema.ValidationError):
        validate_input(trace, input_schema)


def test_usage_is_summed_only_when_every_session_has_final_usage() -> None:
    fixtures = load_object(SYNTHETIC_FIXTURES)
    fixture = load_object(DEFAULT_FIXTURE)
    passed = extract(fixtures["base_trace"], fixture)
    assert passed["usage"]["all_agent_total"] == {
        "thread_id": "all-agent-total",
        "input_tokens": 150,
        "cached_input_tokens": 30,
        "output_tokens": 30,
        "total_tokens": 180,
    }
    incomplete = copy.deepcopy(fixtures["base_trace"])
    incomplete["usage"]["sessions"][1]["total_tokens"] = None
    failed = extract(incomplete, fixture)
    assert failed["usage"]["complete"] is False
    assert failed["usage"]["all_agent_total"]["total_tokens"] is None
    assert failed["criteria"]["all_agent_final_usage"] == "unsatisfied"
