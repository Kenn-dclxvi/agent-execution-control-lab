import copy
import json
from pathlib import Path

import jsonschema
import pytest

from scripts import general_chat_agentic_worker_trace_probe_r5 as probe


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZATION = ROOT / "docs/general-chat-agentic-worker-trace-probe-r5-authorization.json"
SCHEMA = ROOT / "docs/general-chat-agentic-worker-trace-probe-r5-authorization.schema.json"


def write_jsonl(path: Path, values: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(value, ensure_ascii=False) for value in values) + "\n", encoding="utf-8")


def test_authorized_identity_matches_write_once_lifecycle() -> None:
    result = probe.prepare(AUTHORIZATION, SCHEMA)
    assert result["authorization_state"] == "authorized_not_issued"
    assert result["model_invocations"] == 0 and result["probe_issues"] == 0
    if result["identity_available"]:
        assert result["existing_records"] == [] and result["dispatch_state"] == "allowed"
    else:
        assert result["existing_records"] == list(probe.RECORD_NAMES) and result["dispatch_state"] == "denied"


@pytest.mark.parametrize(("field", "value"), [("retry", True), ("overwrite", True), ("max_issues", 2)])
def test_authorization_rejects_issue_policy_drift(field: str, value: object) -> None:
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    mutated = copy.deepcopy(authorization)
    mutated["issuance_policy"][field] = value
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(mutated)


def synthetic_private_root(tmp_path: Path, *, include_spawn_output: bool = True) -> Path:
    root_id, child_id = "root-r5", "child-r5"
    write_jsonl(tmp_path / "stdout.jsonl", [{"type": "thread.started", "thread_id": root_id}])
    usage = {"input_tokens": 10, "cached_input_tokens": 2, "output_tokens": 3, "total_tokens": 13}
    root_items = [
        {"type": "session_meta", "payload": {"id": root_id, "parent_thread_id": None}},
        {"type": "response_item", "payload": {"type": "function_call", "name": "spawn_agent", "call_id": "spawn-r5", "arguments": json.dumps({"task_name": probe.TASK_NAME, "fork_turns": "none", "message": json.dumps(probe.EXPECTED_PACKET, ensure_ascii=False, separators=(",", ":"))}, ensure_ascii=False)}},
    ]
    if include_spawn_output:
        root_items.append({"type": "response_item", "payload": {"type": "function_call_output", "call_id": "spawn-r5", "output": json.dumps({"child_thread_id": child_id, "task_name": probe.TASK_NAME})}})
    root_items.append({"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": usage}}})
    child_items = [
        {"type": "session_meta", "payload": {"id": child_id, "parent_thread_id": root_id, "source": {"subagent": {"thread_spawn": {"agent_path": "/root/parking_fact_check"}}}}},
        {"type": "event_msg", "payload": {"type": "task_complete", "last_agent_message": "土曜日は18時まで駐車できる。利用時間は18時30分までです。"}},
        {"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": usage}}},
    ]
    write_jsonl(tmp_path / "codex-home" / "sessions" / "root.jsonl", root_items)
    write_jsonl(tmp_path / "codex-home" / "sessions" / "child.jsonl", child_items)
    (tmp_path / "final.txt").write_text(probe.EXPECTED_FINAL + "\n", encoding="utf-8")
    (tmp_path / "stderr.txt").write_text("", encoding="utf-8")
    return tmp_path


def test_synthetic_three_way_binding_satisfies_all_criteria(tmp_path: Path) -> None:
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    receipt = probe.build_receipt(authorization, synthetic_private_root(tmp_path), 100, 200, 0)
    assert receipt["terminal_state"] == "worker_trace_available"
    assert set(receipt["criteria"].values()) == {"satisfied"}
    schema = json.loads((ROOT / "docs/general-chat-agentic-worker-trace-probe-r5-receipt.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(receipt)


def test_agent_path_does_not_replace_missing_runtime_spawn_result(tmp_path: Path) -> None:
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    receipt = probe.build_receipt(authorization, synthetic_private_root(tmp_path, include_spawn_output=False), 100, 200, 0)
    assert receipt["criteria"]["runtime_spawn_result"] == "unobserved"
    assert receipt["criteria"]["child_session_binding"] == "unobserved"
    assert receipt["terminal_state"] == "worker_trace_unavailable"


def test_write_once_rejects_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "record.json"
    probe.write_once(target, {"value": 1})
    with pytest.raises(FileExistsError):
        probe.write_once(target, {"value": 2})
