import copy
import json
from pathlib import Path

import jsonschema
import pytest

from scripts import general_chat_agentic_worker_trace_probe_r5 as r5
from scripts import general_chat_agentic_worker_trace_probe_r6 as r6


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZATION = ROOT / "docs/general-chat-agentic-worker-trace-probe-r6-authorization.json"
SCHEMA = ROOT / "docs/general-chat-agentic-worker-trace-probe-r6-authorization.schema.json"


def test_authorized_identity_matches_lifecycle() -> None:
    result = r6.prepare()
    assert result["authorization_state"] == "authorized_not_issued"
    assert result["model_invocations"] == 0 and result["probe_issues"] == 0
    assert (result["identity_available"], result["existing_records"]) in ((True, []), (False, list(r6.RECORD_NAMES)))


@pytest.mark.parametrize(("field", "value"), [("retry", True), ("overwrite", True), ("max_issues", 2)])
def test_authorization_rejects_issue_policy_drift(field: str, value: object) -> None:
    authorization = json.loads(AUTHORIZATION.read_text(encoding="utf-8")); schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    mutated = copy.deepcopy(authorization); mutated["issuance_policy"][field] = value
    with pytest.raises(jsonschema.ValidationError): jsonschema.Draft202012Validator(schema).validate(mutated)


def test_bounded_packet_projection_accepts_one_embedded_packet() -> None:
    message = "このJSONだけを使う: " + json.dumps(r5.EXPECTED_PACKET, ensure_ascii=False, separators=(",", ":"))
    assert r6.exact_packet_from_message(message) == r5.EXPECTED_PACKET


def test_bounded_packet_projection_rejects_forbidden_record() -> None:
    message = json.dumps(r5.EXPECTED_PACKET, ensure_ascii=False) + " parking-weekday-r1"
    assert r6.exact_packet_from_message(message) is None


def test_nested_spawn_result_requires_one_unique_binding() -> None:
    outputs = [{"call_id": "one", "raw": {"content": [{"text": json.dumps({"agent_id": "child", "task_name": r5.TASK_NAME})}]}}]
    assert r6.spawn_result("one", outputs) == {"child_thread_id": "child", "task_name": r5.TASK_NAME}
    outputs.append({"call_id": "one", "raw": {"agent_id": "other", "task_name": r5.TASK_NAME}})
    assert r6.spawn_result("one", outputs) is None


def test_write_once_rejects_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "record.json"; r5.write_once(target, {"value": 1})
    with pytest.raises(FileExistsError): r5.write_once(target, {"value": 2})
