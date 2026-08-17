import json
from pathlib import Path

from scripts.register_semantic_protocol_qualification import collect_qualification


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
