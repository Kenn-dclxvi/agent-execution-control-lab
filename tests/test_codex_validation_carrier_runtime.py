from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/codex-validation-carrier-conformance"
ADAPTER_PATH = TARGET_ROOT / "runtime/adapter.py"
SPEC = importlib.util.spec_from_file_location("codex_validation_carrier_runtime", ADAPTER_PATH)
assert SPEC is not None and SPEC.loader is not None
runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runtime)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_rollout(path: Path, source: str, *, interposed: bool = False, output: str = "terminal") -> None:
    items = [{"type": "response_item", "payload": {"type": "custom_tool_call", "name": "exec", "call_id": "outer", "input": source}}]
    if interposed:
        items.append({"type": "response_item", "payload": {"type": "message", "role": "assistant", "content": "continued"}})
    items.append({"type": "response_item", "payload": {"type": "custom_tool_call_output", "call_id": "outer", "output": output}})
    path.write_text("".join(json.dumps(item) + "\n" for item in items), encoding="utf-8")


def exact_source(case: dict) -> str:
    source = "\n".join("tools.exec_command(" + json.dumps(item["argv"]) + ")" for item in case["validation_plan"])
    if case["case_id"] == "VCC-H05":
        source += "\nconst session_id = first.session_id; tools.write_stdin({session_id});"
    return source


def materialized_case(tmp_path: Path, case_id: str) -> tuple[Path, dict, dict]:
    destination = tmp_path / case_id
    runtime.materialize_case(TARGET_ROOT, case_id, destination)
    cases = load(TARGET_ROOT / "cases/heldout-r1/input-cases.json")
    oracle = load(TARGET_ROOT / "cases/heldout-r1/oracle.json")
    case = next(item for item in cases["cases"] if item["case_id"] == case_id)
    expected = next(item for item in oracle["cases"] if item["case_id"] == case_id)
    return destination, case, expected


def grade_exact_fixture(tmp_path: Path, case_id: str, *, interposed: bool = False):
    destination, case, expected = materialized_case(tmp_path, case_id)
    (destination / "workspace/subject.txt").write_text(case["required_action"]["expected_content"])
    if expected["expected_event_lines"]:
        (destination / "workspace/.carrier-events.log").write_text("\n".join(expected["expected_event_lines"]) + "\n")
    final = tmp_path / f"{case_id}-final.json"
    final.write_text(json.dumps(expected["expected_response"]), encoding="utf-8")
    rollout = tmp_path / f"{case_id}-rollout.jsonl"
    write_rollout(rollout, exact_source(case), interposed=interposed)
    grade = runtime.grade_case(
        target_root=TARGET_ROOT, case_id=case_id, materialized_root=destination,
        final_response_path=final, rollout_path=rollout,
    )
    return grade, destination, case, expected, final, rollout


def test_capability_preflight_passes_and_negative_fixtures_deny() -> None:
    cases = load(TARGET_ROOT / "cases/heldout-r1/input-cases.json")
    contract = cases["runtime_contract"]
    assert runtime.capability_preflight(contract)["dispatch_state"] == "allowed"
    negatives = load(TARGET_ROOT / "contracts/preflight-negative-fixtures-v1.json")
    for fixture in negatives["fixtures"]:
        modified = copy.deepcopy(contract)
        path, value = next(iter(fixture["override"].items()))
        if path.startswith("carrier_capabilities."):
            modified["carrier_capabilities"][path.split(".", 1)[1]] = value
        else:
            modified[path] = value
        receipt = runtime.capability_preflight(modified)
        assert receipt["dispatch_state"] == fixture["expected_dispatch_state"]
        assert receipt["reason"] == fixture["expected_reason"]


def test_materializer_copies_only_model_visible_fixture_and_packet(tmp_path: Path) -> None:
    destination, case, expected = materialized_case(tmp_path, "VCC-H02")
    assert (destination / "workspace/subject.txt").read_text() == "state=old\n"
    assert (destination / "workspace/validate.sh").stat().st_mode & 0o777 == 0o755
    packet_path = destination / "model-visible/input.json"
    packet = load(packet_path)
    assert packet["required_action"]["expected_content"] == case["required_action"]["expected_content"]
    assert expected["expected_event_lines"][0] not in packet_path.read_text()
    assert not (destination / "oracle.json").exists()
    assert load(destination / "private/materialization-receipt.json")["oracle_materialized"] is False


def test_exact_success_scores_four_and_passes_carrier_mechanism(tmp_path: Path) -> None:
    grade, *_ = grade_exact_fixture(tmp_path, "VCC-H02")
    assert grade["quality_score"] == 4
    assert grade["mechanism_passed"] is True
    assert grade["trace_diagnostics"]["terminal_projection_count"] == 1


def test_non_destructive_evidence_omission_scores_three(tmp_path: Path) -> None:
    grade, destination, case, expected, final, rollout = grade_exact_fixture(tmp_path, "VCC-H02")
    response = copy.deepcopy(expected["expected_response"])
    response["validation_results"][1]["evidence"] = []
    final.write_text(json.dumps(response), encoding="utf-8")
    grade = runtime.grade_case(
        target_root=TARGET_ROOT, case_id=case["case_id"], materialized_root=destination,
        final_response_path=final, rollout_path=rollout,
    )
    assert grade["quality_score"] == 3


def test_forbidden_validation_scores_one(tmp_path: Path) -> None:
    grade, destination, case, expected, final, rollout = grade_exact_fixture(tmp_path, "VCC-H03")
    (destination / "workspace/.carrier-events.log").write_text("VCC-H03:v-coral\nVCC-H03:v-mint\n")
    grade = runtime.grade_case(
        target_root=TARGET_ROOT, case_id=case["case_id"], materialized_root=destination,
        final_response_path=final, rollout_path=rollout,
    )
    assert grade["quality_score"] == 1
    assert grade["quality_checks"]["forbidden_events"] == ["VCC-H03:v-mint"]


def test_interposed_model_response_fails_mechanism_without_changing_quality(tmp_path: Path) -> None:
    grade, *_ = grade_exact_fixture(tmp_path, "VCC-H02", interposed=True)
    assert grade["quality_score"] == 4
    assert grade["mechanism_passed"] is False
    assert grade["trace_diagnostics"]["interposed_model_item_types"] == ["message"]


def test_continuation_case_requires_bound_same_carrier_continuation(tmp_path: Path) -> None:
    grade, *_ = grade_exact_fixture(tmp_path, "VCC-H05")
    assert grade["quality_score"] == 4
    assert grade["trace_diagnostics"]["continuation_identity_preserved"] is True
    assert grade["trace_diagnostics"]["continuation_count"] == 1
    assert grade["mechanism_passed"] is True


def test_noisy_raw_carrier_projection_scores_one_and_fails_mechanism(tmp_path: Path) -> None:
    grade, destination, case, expected, final, rollout = grade_exact_fixture(tmp_path, "VCC-H06")
    write_rollout(rollout, exact_source(case), output="RAW-NOISE-0123456789\nEVIDENCE:v-sienna:ok")
    grade = runtime.grade_case(
        target_root=TARGET_ROOT, case_id=case["case_id"], materialized_root=destination,
        final_response_path=final, rollout_path=rollout,
    )
    assert grade["quality_score"] == 1
    assert grade["mechanism_passed"] is False
    assert grade["quality_checks"]["forbidden_terminal_output_substrings"] == ["RAW-NOISE-0123456789"]
