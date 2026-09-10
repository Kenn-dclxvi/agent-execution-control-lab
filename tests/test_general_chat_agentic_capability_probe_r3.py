import copy
import json
from pathlib import Path

import jsonschema
import pytest

from scripts import general_chat_agentic_capability_probe_r3 as probe


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZATION = ROOT / "docs/general-chat-agentic-capability-preflight-authorization-r1.json"
SCHEMA = ROOT / "docs/general-chat-agentic-capability-preflight-authorization-r1.schema.json"


def test_authorization_schema_and_bound_artifacts() -> None:
    result = probe.prepare(AUTHORIZATION, SCHEMA)
    assert result["authorization_state"] == "authorized_not_issued"
    assert result["model_invocations"] == 0
    assert result["probe_issues"] == 0


def test_authorization_rejects_retry() -> None:
    value = json.loads(AUTHORIZATION.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    mutated = copy.deepcopy(value)
    mutated["issuance_policy"]["retry"] = True
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(mutated)


def test_write_once_rejects_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "record.json"
    probe.write_once(target, {"value": 1})
    with pytest.raises(FileExistsError):
        probe.write_once(target, {"value": 2})


def test_fixed_tool_contract(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from scripts import general_chat_agentic_branch_tool_server as server

    audit = tmp_path / "audit.jsonl"
    monkeypatch.setenv("GENERAL_CHAT_BRANCH_TOOL_AUDIT", str(audit))
    response = server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": server.TOOL_NAME, "arguments": server.ALLOWED_INPUT}})
    assert response is not None
    assert response["result"]["structuredContent"] == server.TERMINAL_RESULT
    assert len(audit.read_text(encoding="utf-8").splitlines()) == 1


def test_fixed_tool_rejects_other_record(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from scripts import general_chat_agentic_branch_tool_server as server

    monkeypatch.setenv("GENERAL_CHAT_BRANCH_TOOL_AUDIT", str(tmp_path / "audit.jsonl"))
    response = server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": server.TOOL_NAME, "arguments": {"record_id": "other"}}})
    assert response is not None and "error" in response
    assert not (tmp_path / "audit.jsonl").exists()
