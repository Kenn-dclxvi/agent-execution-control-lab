from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import jsonschema
import pytest

from scripts.general_chat_agentic_binding_extractor import extract
from scripts.general_chat_agentic_real_trace_adapter import (
    AdapterError,
    DEFAULT_PACKET,
    DEFAULT_PACKET_SCHEMA,
    adapt_packet,
    load_json_object,
    validate_packet,
)


ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_FIXTURE = ROOT / "docs/general-chat-agentic-capability-preflight-fixture-r1.json"
R1_NORMALIZED_SCHEMA = ROOT / "docs/general-chat-agentic-binding-extractor-input.schema.json"
R2_NORMALIZED_SCHEMA = ROOT / "docs/general-chat-agentic-binding-extractor-input-r2.schema.json"


def packet() -> dict:
    value = load_json_object(DEFAULT_PACKET, "TEST_PACKET_UNAVAILABLE")
    validate_packet(value, load_json_object(DEFAULT_PACKET_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"))
    return value


def bind_bytes(identity: dict, data: bytes) -> None:
    identity["bytes"] = len(data)
    identity["sha256"] = hashlib.sha256(data).hexdigest()


def materialize_repository(tmp_path: Path, value: dict) -> None:
    identities = [value["root_events"], value["normalized_output_schema"]]
    identities.extend(session["file"] for session in value["sessions"])
    for identity in identities:
        source = ROOT / identity["path"]
        target = tmp_path / identity["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())


def test_fixed_synthetic_packet_projects_only_confirmed_r2_fields() -> None:
    normalized = adapt_packet(packet())
    assert normalized["probe_id"] == "general-chat-agentic-capability-preflight-r2"
    assert normalized["root"]["thread_started"] == ["root-thread-r2"]
    assert normalized["root"]["spawn_calls"] == []
    assert normalized["root"]["spawn_results"] == []
    assert normalized["root"]["tool_calls"] == []
    assert normalized["root"]["tool_results"] == []
    assert normalized["root"]["final_responses"] == []
    assert normalized["descendants"] == [
        {
            "thread_id": "child-thread-r2",
            "parent_thread_id": "root-thread-r2",
            "task_identity": None,
            "terminal_events": [
                {
                    "sender": None,
                    "result": "土曜日は18時まで駐車できる（利用時間は18時30分まで）。",
                }
            ],
        }
    ]
    assert [item["total_tokens"] for item in normalized["usage"]["sessions"]] == [120, 60]
    assert normalized["monotonic"] == {"started_ms": 2000, "ended_ms": 2450}
    rendered = json.dumps(normalized, ensure_ascii=False, sort_keys=True)
    for forbidden in ('"source"', '"agent_path"', '"path"', "synthetic ignored"):
        assert forbidden not in rendered


def test_projection_remains_unavailable_for_unobserved_agentic_bindings() -> None:
    normalized = adapt_packet(packet())
    fixture = load_json_object(CAPABILITY_FIXTURE, "TEST_FIXTURE_UNAVAILABLE")
    result = extract(normalized, fixture)
    assert result["criteria"] == {
        "root_thread_identity": "satisfied",
        "spawn_call_and_task_identity": "unobserved",
        "worker_packet_projection": "unobserved",
        "descendant_parent_and_task_binding": "unobserved",
        "descendant_terminal_sender_and_result": "unobserved",
        "root_tool_call_and_terminal_result": "unobserved",
        "final_response_direct_binding": "unobserved",
        "all_agent_final_usage": "satisfied",
        "monotonic_elapsed": "satisfied",
        "safe_projection_without_raw_transcript": "satisfied",
    }
    assert result["admission"] == "agentic_runtime_capability_unavailable"


def test_r1_and_r2_normalized_schemas_coexist() -> None:
    normalized = adapt_packet(packet())
    r1 = load_json_object(R1_NORMALIZED_SCHEMA, "TEST_SCHEMA_UNAVAILABLE")
    r2 = load_json_object(R2_NORMALIZED_SCHEMA, "TEST_SCHEMA_UNAVAILABLE")
    jsonschema.Draft202012Validator(r2).validate(normalized)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(r1).validate(normalized)


def test_bound_file_hash_mismatch_fails_closed() -> None:
    value = packet()
    value["root_events"]["sha256"] = "0" * 64
    with pytest.raises(AdapterError, match="BOUND_FILE_HASH_MISMATCH"):
        adapt_packet(value)


def test_root_event_thread_drift_fails_closed(tmp_path: Path) -> None:
    value = packet()
    materialize_repository(tmp_path, value)
    data = b'{"type":"thread.started","thread_id":"other-root"}\n'
    target = tmp_path / value["root_events"]["path"]
    target.write_bytes(data)
    bind_bytes(value["root_events"], data)
    with pytest.raises(AdapterError, match="ROOT_THREAD_ID_MISMATCH"):
        adapt_packet(value, tmp_path)


@pytest.mark.parametrize(
    ("field", "replacement", "reason"),
    [
        ("id", "other-child", "SESSION_THREAD_ID_MISMATCH"),
        ("parent_thread_id", "outside-root", "SESSION_PARENT_ID_MISMATCH"),
        ("cwd", "/different/workspace", "SESSION_WORKSPACE_MISMATCH"),
    ],
)
def test_session_metadata_drift_fails_closed(
    tmp_path: Path, field: str, replacement: str, reason: str
) -> None:
    value = packet()
    materialize_repository(tmp_path, value)
    identity = value["sessions"][1]["file"]
    target = tmp_path / identity["path"]
    lines = target.read_text(encoding="utf-8").splitlines()
    meta = json.loads(lines[0])
    meta["payload"][field] = replacement
    lines[0] = json.dumps(meta, ensure_ascii=False, separators=(",", ":"))
    data = ("\n".join(lines) + "\n").encode("utf-8")
    target.write_bytes(data)
    bind_bytes(identity, data)
    with pytest.raises(AdapterError, match=reason):
        adapt_packet(value, tmp_path)


def test_duplicate_thread_and_file_bindings_fail_closed() -> None:
    duplicate_thread = packet()
    duplicate_thread["sessions"][1]["thread_id"] = "root-thread-r2"
    with pytest.raises(AdapterError, match="DUPLICATE_SESSION_THREAD"):
        adapt_packet(duplicate_thread)

    duplicate_file = packet()
    duplicate_file["sessions"][1]["file"] = copy.deepcopy(duplicate_file["sessions"][0]["file"])
    with pytest.raises(AdapterError, match="DUPLICATE_SESSION_FILE"):
        adapt_packet(duplicate_file)


def test_parent_outside_bound_session_graph_fails_closed() -> None:
    value = packet()
    value["sessions"][1]["parent_thread_id"] = "outside-root"
    with pytest.raises(AdapterError, match="SESSION_PARENT_CHAIN_INVALID"):
        adapt_packet(value)


@pytest.mark.parametrize("path", ["/absolute/session.jsonl", "docs/../session.jsonl"])
def test_packet_schema_rejects_non_relative_or_parent_traversal_paths(path: str) -> None:
    value = packet()
    value["root_events"]["path"] = path
    with pytest.raises(AdapterError, match="PACKET_SCHEMA_INVALID"):
        validate_packet(value, load_json_object(DEFAULT_PACKET_SCHEMA, "TEST_SCHEMA_UNAVAILABLE"))
