import json
from pathlib import Path

from scripts.register_semantic_protocol_qualification import (
    collect_qualification,
    quality_gate_result,
    result_identity,
)


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "evaluations/targets/portable-instruction-semantic-conformance"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_collect_qualification_keeps_low_quality_valid_result(tmp_path: Path) -> None:
    inputs = load(TARGET / "cases/heldout-r1/input-cases.json")
    oracle = load(TARGET / "cases/heldout-r1/oracle.json")
    schema = load(TARGET / "cases/heldout-r1/response.schema.json")
    slot = {"slot_id": "PIC-H01-i001", "case_id": "PIC-H01", "case_revision": "r1", "iteration": 1}
    private = tmp_path / slot["slot_id"] / "private"
    private.mkdir(parents=True)
    response = dict(oracle["cases"][0]["expected_response"])
    response["unavailable_operation_ids"] = ["op-inspect-storage"]
    response_path = private / "final-response.json"
    response_path.write_text(json.dumps(response), encoding="utf-8")
    observation = {
        "slot": slot,
        "status": "executor_complete_unrated",
        "elapsed_seconds": 1.25,
        "token_accounting": {"all_agent_total_tokens": 100, "session_count": 1},
    }
    observation_path = private / "execution-observation.json"
    observation_path.write_text(json.dumps(observation), encoding="utf-8")
    rows = collect_qualification(
        plan={"slots": [slot]},
        output_root=tmp_path,
        inputs=inputs,
        oracle=oracle,
        response_schema=schema,
    )
    assert len(rows) == 1
    assert rows[0]["status"] == "valid"
    assert rows[0]["quality_score"] < 4
    assert rows[0]["mechanism_passed"] is False


def test_result_identity_is_bound_to_dispatch_series() -> None:
    assert result_identity({"plan_id": "portable-full-agent-heldout-r1-n1-dispatch-r1"}) == (
        "portable-full-agent-heldout-r1-n1-qualification-r1"
    )


def test_control_free_quality_is_descriptive_but_candidate_requires_all_score4() -> None:
    control = {
        "prompt_set_identity": {"name": "portable-semantic-a544769-control-free-r1"}
    }
    candidate = {
        "prompt_set_identity": {"name": "portable-semantic-c147-portable-full-agent-r1"}
    }
    assert quality_gate_result(control, [1] * 14)["quality_gate"] == (
        "descriptive_not_an_admission_gate"
    )
    assert quality_gate_result(candidate, [4] * 14) == {
        "quality_gate": "passed",
        "quality_gate_contract": "exact_all_14_score4",
        "comparison_reference": "authorized_after_quality_gate",
    }
    assert quality_gate_result(candidate, [4] * 13 + [3])["comparison_reference"] == (
        "not_authorized"
    )
