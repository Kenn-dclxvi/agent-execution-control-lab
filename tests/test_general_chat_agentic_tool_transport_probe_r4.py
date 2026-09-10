import copy
import json
from pathlib import Path

import jsonschema
import pytest

from scripts import general_chat_agentic_branch_tool_server_r4 as server
from scripts import general_chat_agentic_tool_transport_probe_r4 as probe


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZATION = ROOT / "docs/general-chat-agentic-tool-transport-probe-r4-authorization.json"
SCHEMA = ROOT / "docs/general-chat-agentic-tool-transport-probe-r4-authorization.schema.json"


def test_authorized_identity_matches_write_once_lifecycle() -> None:
    result = probe.prepare(AUTHORIZATION, SCHEMA)
    assert result["authorization_state"] == "authorized_not_issued"
    assert result["model_invocations"] == 0
    assert result["probe_issues"] == 0
    if result["identity_available"]:
        assert result["existing_records"] == []
        assert result["dispatch_state"] == "allowed"
    else:
        assert result["existing_records"] == list(probe.RECORD_NAMES)
        assert result["dispatch_state"] == "denied"


@pytest.mark.parametrize(("pointer", "replacement"), [("retry", True), ("overwrite", True), ("max_issues", 2)])
def test_authorization_rejects_issue_policy_drift(pointer: str, replacement: object) -> None:
    value = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    mutated = copy.deepcopy(value)
    mutated["issuance_policy"][pointer] = replacement
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(mutated)


def test_server_audits_handshake_list_and_one_fixed_call(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    audit = tmp_path / "audit.jsonl"
    monkeypatch.setenv("GENERAL_CHAT_BRANCH_TOOL_AUDIT", str(audit))
    initialized = server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})
    server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"})
    listed = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    called = server.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": server.TOOL_NAME, "arguments": server.ALLOWED_INPUT}})
    assert initialized["result"]["protocolVersion"] == "2025-06-18"
    assert listed["result"]["tools"][0]["name"] == server.TOOL_NAME
    assert called["result"]["structuredContent"] == server.TERMINAL_RESULT
    events = [json.loads(line)["event"] for line in audit.read_text(encoding="utf-8").splitlines()]
    assert events == ["initialize", "initialized", "tools_list", "tools_call"]


def test_server_rejects_other_input_without_result(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    audit = tmp_path / "audit.jsonl"
    monkeypatch.setenv("GENERAL_CHAT_BRANCH_TOOL_AUDIT", str(audit))
    result = server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": server.TOOL_NAME, "arguments": {"record_id": "other"}}})
    assert "error" in result
    assert json.loads(audit.read_text(encoding="utf-8"))["event"] == "rejected_call"


def test_write_once_rejects_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "record.json"
    probe.write_once(target, {"value": 1})
    with pytest.raises(FileExistsError):
        probe.write_once(target, {"value": 2})


def test_synthetic_terminal_projection_satisfies_all_criteria(tmp_path: Path) -> None:
    root_id = "root-r4"
    (tmp_path / "codex-home" / "sessions").mkdir(parents=True)
    (tmp_path / "stdout.jsonl").write_text(json.dumps({"type": "thread.started", "thread_id": root_id}) + "\n", encoding="utf-8")
    rollout = [
        {"type": "session_meta", "payload": {"id": root_id, "parent_thread_id": None}},
        {"type": "response_item", "payload": {"type": "function_call", "name": "mcp__branch_hours__fetch_branch_counter_hours", "call_id": "call-r4", "arguments": json.dumps(server.ALLOWED_INPUT)}},
        {"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": 10, "cached_input_tokens": 2, "output_tokens": 3, "total_tokens": 13}}}},
    ]
    (tmp_path / "codex-home" / "sessions" / "root.jsonl").write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in rollout) + "\n", encoding="utf-8")
    audit = [
        {"event": "initialize", "protocol_version": "2025-06-18"},
        {"event": "initialized"},
        {"event": "tools_list"},
        {"event": "tools_call", "tool_id": server.TOOL_NAME, "input": server.ALLOWED_INPUT, "result": server.TERMINAL_RESULT},
    ]
    (tmp_path / "tool-audit.jsonl").write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in audit) + "\n", encoding="utf-8")
    (tmp_path / "final.txt").write_text(probe.EXPECTED_FINAL + "\n", encoding="utf-8")
    (tmp_path / "stderr.txt").write_text("", encoding="utf-8")
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    receipt = probe.build_receipt(authorization, tmp_path, 100, 200, 0)
    assert receipt["terminal_state"] == "tool_transport_available"
    assert set(receipt["criteria"].values()) == {"satisfied"}
    schema = json.loads((ROOT / "docs/general-chat-agentic-tool-transport-probe-r4-receipt.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(receipt)
