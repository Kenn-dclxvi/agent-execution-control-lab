import copy
import json
from pathlib import Path

import jsonschema
import pytest

from scripts import general_chat_agentic_capability_probe_r8 as probe
from scripts import general_chat_agentic_branch_tool_server_r4 as server


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZATION = ROOT / "docs/general-chat-agentic-capability-probe-r8-authorization.json"
SCHEMA = ROOT / "docs/general-chat-agentic-capability-probe-r8-authorization.schema.json"


def write_jsonl(path: Path, values: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(value, ensure_ascii=False) for value in values) + "\n", encoding="utf-8")


def test_authorized_identity_matches_lifecycle() -> None:
    result = probe.prepare()
    assert result["authorization_state"] == "authorized_not_issued"
    assert result["model_invocations"] == 0 and result["probe_issues"] == 0
    assert (result["identity_available"], result["existing_records"]) in ((True, []), (False, list(probe.RECORD_NAMES)))


@pytest.mark.parametrize(("field", "value"), [("retry", True), ("overwrite", True), ("max_issues", 2)])
def test_authorization_rejects_issue_policy_drift(field: str, value: object) -> None:
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8")); schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    mutated = copy.deepcopy(authorization); mutated["issuance_policy"][field] = value
    with pytest.raises(jsonschema.ValidationError): jsonschema.Draft202012Validator(schema).validate(mutated)


def test_packet_carrier_accepts_path_without_answer_values() -> None:
    message = f"{probe.FIXTURE_RELATIVE}だけを読み、18時まで駐車できるか終了時刻とともに一文で答える"
    assert probe.packet_state(message) == "satisfied"


def test_packet_carrier_rejects_answer_or_tool_record_leak() -> None:
    message = f"{probe.FIXTURE_RELATIVE}を読み、18時まで駐車できるか終了時刻を一文で答える。18時30分"
    assert probe.packet_state(message) == "unsatisfied"


def test_root_model_input_does_not_contain_hidden_results() -> None:
    text = (ROOT / "docs/general-chat-agentic-capability-probe-r8-model-input.txt").read_text(encoding="utf-8")
    assert "18時30分" not in text
    assert "17時" not in text
    assert "9時00分" not in text


def test_synthetic_combined_normal_route_satisfies_all_criteria(tmp_path: Path) -> None:
    root_id, child_id = "root-r8", "child-r8"
    write_jsonl(tmp_path / "stdout.jsonl", [{"type": "thread.started", "thread_id": root_id}])
    usage = {"input_tokens": 10, "cached_input_tokens": 2, "output_tokens": 3, "total_tokens": 13}
    packet = f"{probe.FIXTURE_RELATIVE}だけを読み、18時まで駐車できるか終了時刻とともに一文で答える"
    root_events = [
        {"type": "session_meta", "payload": {"id": root_id, "parent_thread_id": None}},
        {"type": "response_item", "payload": {"type": "function_call", "name": "spawn_agent", "call_id": "spawn", "arguments": json.dumps({"task_name": "parking_fact_check", "fork_turns": "none", "message": packet}, ensure_ascii=False)}},
        {"type": "event_msg", "payload": {"type": "sub_agent_activity", "agent_thread_id": child_id, "agent_path": "/root/parking_fact_check"}},
        {"type": "response_item", "payload": {"type": "mcp_tool_call", "name": probe.FULL_TOOL_ID, "call_id": "tool", "arguments": json.dumps(server.ALLOWED_INPUT)}},
        {"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": usage}}},
    ]
    child_events = [
        {"type": "session_meta", "payload": {"id": child_id, "parent_thread_id": root_id, "source": {"subagent": {"thread_spawn": {"agent_path": "/root/parking_fact_check"}}}}},
        {"type": "response_item", "payload": {"type": "custom_tool_call", "name": "exec", "call_id": "read", "input": {"cmd": f"sed -n 1p {probe.FIXTURE_RELATIVE}"}}},
        {"type": "event_msg", "payload": {"type": "task_complete", "last_agent_message": "土曜日は18時まで駐車できる。利用時間は18時30分までです。"}},
        {"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": usage}}},
    ]
    write_jsonl(tmp_path / "codex-home" / "sessions" / "root.jsonl", root_events)
    write_jsonl(tmp_path / "codex-home" / "sessions" / "child.jsonl", child_events)
    audits = [{"event": "initialize"}, {"event": "initialized"}, {"event": "tools_list"}, {"event": "tools_call", "tool_id": server.TOOL_NAME, "input": server.ALLOWED_INPUT, "result": server.TERMINAL_RESULT}]
    write_jsonl(tmp_path / "tool-audit.jsonl", audits)
    (tmp_path / "stderr.txt").write_text("", encoding="utf-8")
    (tmp_path / "final.txt").write_text(probe.EXPECTED_FINAL + "\n", encoding="utf-8")
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    receipt = probe.build_receipt(authorization, tmp_path, 100, 200, 0)
    assert receipt["terminal_state"] == "agentic_runtime_capability_available"
    assert set(receipt["criteria"].values()) == {"satisfied"}
    schema = json.loads((ROOT / "docs/general-chat-agentic-capability-probe-r8-receipt.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(receipt)
