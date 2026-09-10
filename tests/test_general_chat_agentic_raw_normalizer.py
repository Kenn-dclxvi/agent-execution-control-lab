from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema
import pytest

from scripts.general_chat_agentic_binding_extractor import extract
from scripts.general_chat_agentic_raw_normalizer import (
    DEFAULT_INPUT_SCHEMA,
    DEFAULT_OUTPUT_SCHEMA,
    load_object,
    normalize_known_fields,
    validate,
)


ROOT = Path(__file__).resolve().parents[1]
SYNTHETIC = ROOT / "docs/general-chat-agentic-raw-normalizer-synthetic-r1.json"
CAPABILITY_FIXTURE = ROOT / "docs/general-chat-agentic-capability-preflight-fixture-r1.json"


def fixture() -> dict:
    return load_object(SYNTHETIC)


def test_normalize_known_fields_matches_fixed_fail_closed_projection() -> None:
    value = fixture()
    raw_schema = load_object(DEFAULT_INPUT_SCHEMA)
    normalized_schema = load_object(DEFAULT_OUTPUT_SCHEMA)
    validate(value["raw_trace"], raw_schema)
    normalized = normalize_known_fields(value["raw_trace"])
    validate(normalized, normalized_schema)
    assert normalized == value["expected_normalized_trace"]


def test_normalized_projection_produces_fixed_unavailable_binding_result() -> None:
    value = fixture()
    normalized = normalize_known_fields(value["raw_trace"])
    result = extract(normalized, load_object(CAPABILITY_FIXTURE))
    assert result["criteria"] == value["expected_binding_result"]["criteria"]
    assert result["admission"] == "agentic_runtime_capability_unavailable"


def test_agent_path_does_not_become_task_identity_sender_or_spawn_result() -> None:
    raw = copy.deepcopy(fixture()["raw_trace"])
    raw["sessions"][1]["session_meta"]["payload"]["source"]["subagent"]["thread_spawn"][
        "agent_path"
    ] = "parking_fact_check"
    normalized = normalize_known_fields(raw)
    assert normalized["root"]["spawn_calls"] == []
    assert normalized["root"]["spawn_results"] == []
    assert normalized["descendants"][0]["task_identity"] is None
    assert normalized["descendants"][0]["terminal_events"][0]["sender"] is None


def test_descendant_terminal_result_is_not_reconstructed_as_root_final() -> None:
    normalized = normalize_known_fields(fixture()["raw_trace"])
    assert normalized["descendants"][0]["terminal_events"][0]["result"]
    assert normalized["root"]["final_responses"] == []


def test_last_final_usage_is_used_without_token_estimation() -> None:
    raw = copy.deepcopy(fixture()["raw_trace"])
    raw["sessions"][0]["events"].append(
        {
            "type": "event_msg",
            "payload": {
                "type": "token_count",
                "info": {
                    "total_token_usage": {
                        "input_tokens": 200,
                        "cached_input_tokens": 40,
                        "output_tokens": 30,
                        "total_tokens": 230,
                    }
                },
            },
        }
    )
    normalized = normalize_known_fields(raw)
    assert normalized["usage"]["sessions"][0]["total_tokens"] == 230

    raw["sessions"][0]["events"] = []
    normalized = normalize_known_fields(raw)
    root_usage = normalized["usage"]["sessions"][0]
    assert root_usage == {
        "thread_id": "root-thread-r1",
        "parent_thread_id": None,
        "input_tokens": None,
        "cached_input_tokens": None,
        "output_tokens": None,
        "total_tokens": None,
    }


def test_multiple_root_identities_are_preserved_and_not_selected() -> None:
    raw = copy.deepcopy(fixture()["raw_trace"])
    raw["root_events"].append({"type": "thread.started", "thread_id": "other-root"})
    normalized = normalize_known_fields(raw)
    assert normalized["root"]["thread_started"] == ["root-thread-r1", "other-root"]
    assert normalized["usage"]["root_thread_id"] is None


@pytest.mark.parametrize("field", ["auth", "raw_transcript", "request_headers", "tool_output"])
def test_raw_schema_rejects_forbidden_top_level_fields(field: str) -> None:
    raw = copy.deepcopy(fixture()["raw_trace"])
    raw[field] = "forbidden"
    with pytest.raises(jsonschema.ValidationError):
        validate(raw, load_object(DEFAULT_INPUT_SCHEMA))


def test_normalized_output_does_not_expose_source_or_agent_path() -> None:
    normalized = normalize_known_fields(fixture()["raw_trace"])
    rendered = json.dumps(normalized, ensure_ascii=False, sort_keys=True)
    assert '"source"' not in rendered
    assert '"agent_path"' not in rendered
