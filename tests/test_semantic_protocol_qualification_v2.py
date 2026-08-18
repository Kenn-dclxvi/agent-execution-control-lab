import json
from pathlib import Path

from scripts.run_semantic_protocol_qualification import generate_plan as generate_legacy_plan
from scripts.run_semantic_protocol_qualification_v2 import generate_plan as generate_v2_plan


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/portable-instruction-semantic-conformance"
TARGET = TARGET_ROOT / "target.json"
C147_BUNDLE = TARGET_ROOT / "prompts/baselines/portable-semantic-c147-full-agent-reference-r1"
CONTROL_BUNDLE = TARGET_ROOT / "prompts/baselines/portable-semantic-a544769-control-free-r1"


def test_v2_plan_binds_explicit_registration_and_heldout_artifacts() -> None:
    profile = (
        TARGET_ROOT
        / "profiles/portable-semantic-c147-reference-heldout-r2-codex-cli0146-sol-medium-n1-r1.json"
    )
    plan = generate_v2_plan(
        repository_root=ROOT,
        profile_path=profile,
        target_path=TARGET,
        bundle_path=C147_BUNDLE,
    )
    assert plan["target_registration"]["path"].endswith(
        "registrations/heldout-r2-registration-r1.json"
    )
    assert plan["qualification_artifacts"]["cases"]["path"].endswith(
        "cases/heldout-r2/input-cases.json"
    )
    assert plan["qualification_artifacts"]["oracle"]["path"].endswith(
        "cases/heldout-r2/oracle.json"
    )
    assert [slot["case_id"] for slot in plan["slots"]] == [
        f"PIC-H{number:02d}" for number in range(15, 29)
    ]


def test_legacy_plan_keeps_implicit_registration_and_no_v2_field() -> None:
    profile = (
        TARGET_ROOT
        / "profiles/portable-semantic-control-free-codex-cli0146-sol-medium-heldout-r1-n1-r1.json"
    )
    plan = generate_legacy_plan(
        repository_root=ROOT,
        profile_path=profile,
        target_path=TARGET,
        bundle_path=CONTROL_BUNDLE,
    )
    assert plan["target_registration"]["path"].endswith(
        "portable-instruction-semantic-conformance/registration.json"
    )
    assert "qualification_artifacts" not in plan


def test_heldout_r2_oracle_is_private_and_self_consistent() -> None:
    cases = json.loads((TARGET_ROOT / "cases/heldout-r2/input-cases.json").read_text())
    oracle = json.loads((TARGET_ROOT / "cases/heldout-r2/oracle.json").read_text())
    assert {case["case_id"] for case in cases["cases"]} == {
        f"PIC-H{number:02d}" for number in range(15, 29)
    }
    assert [case["case_id"] for case in oracle["cases"]] == [
        case["case_id"] for case in cases["cases"]
    ]
    assert "expected_response" not in json.dumps(cases, ensure_ascii=False)
