import copy
import json
from pathlib import Path

import jsonschema
import pytest

from scripts import general_chat_agentic_worker_trace_probe_r7 as probe


ROOT = Path(__file__).resolve().parents[1]
AUTHORIZATION = ROOT / "docs/general-chat-agentic-worker-trace-probe-r7-authorization.json"
SCHEMA = ROOT / "docs/general-chat-agentic-worker-trace-probe-r7-authorization.schema.json"


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


def test_activity_binding_uses_dedicated_fields() -> None:
    events = [{"type": "event_msg", "payload": {"type": "sub_agent_activity", "agent_thread_id": "child", "agent_path": "/root/parking_fact_check"}}]
    assert probe.activity_bindings(events) == [{"child_thread_id": "child", "agent_path": "/root/parking_fact_check"}]


def test_activity_binding_rejects_multiple_identities() -> None:
    events = [{"type": "event_msg", "payload": {"type": "sub_agent_activity", "agent_thread_id": child, "agent_path": "/root/parking_fact_check"}} for child in ("one", "two")]
    assert probe.activity_bindings(events) == []


def test_packet_material_accepts_required_only() -> None:
    message = " ".join(probe.REQUIRED_PACKET_STRINGS)
    assert probe.packet_material_state(message) == "satisfied"


def test_packet_material_rejects_forbidden_record() -> None:
    message = " ".join(probe.REQUIRED_PACKET_STRINGS + ("parking-weekday-r1",))
    assert probe.packet_material_state(message) == "unsatisfied"
