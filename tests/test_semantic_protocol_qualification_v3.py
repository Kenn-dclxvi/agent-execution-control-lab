import json
from pathlib import Path

import pytest

from scripts.run_semantic_protocol_qualification_v3 import (
    QualificationGateError,
    bind_existing_iteration_result,
    generate_plan,
)


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/portable-instruction-semantic-conformance"
TARGET = TARGET_ROOT / "target.json"


@pytest.mark.parametrize(
    ("profile_name", "bundle_name", "result_name"),
    [
        (
            "portable-semantic-c147-reference-heldout-r3-codex-cli0146-sol-medium-n5-r1.json",
            "baselines/portable-semantic-c147-full-agent-reference-r1",
            "portable-semantic-c147-reference-heldout-r3-n1-qualification-r1.json",
        ),
        (
            "portable-semantic-c147-portable-full-agent-heldout-r3-codex-cli0146-sol-medium-n5-r1.json",
            "candidates/portable-semantic-c147-portable-full-agent-r1",
            "portable-semantic-c147-portable-full-agent-heldout-r3-n1-qualification-r1.json",
        ),
    ],
)
def test_n5_plan_reuses_i001_and_dispatches_only_i002_through_i005(
    profile_name: str, bundle_name: str, result_name: str
) -> None:
    plan = generate_plan(
        repository_root=ROOT,
        profile_path=TARGET_ROOT / "profiles" / profile_name,
        target_path=TARGET,
        bundle_path=TARGET_ROOT / "prompts" / bundle_name,
    )
    assert len(plan["slots"]) == 56
    assert {slot["iteration"] for slot in plan["slots"]} == {2, 3, 4, 5}
    assert plan["authorized_slot_count"] == 56
    binding = bind_existing_iteration_result(
        reference_result_path=TARGET_ROOT / "results" / result_name,
        plan=plan,
        repository_root=ROOT,
    )
    assert binding["reused_slot_count"] == 14
    assert {slot["iteration"] for slot in binding["reused_slots"]} == {1}


def test_n5_reference_binding_rejects_other_prompt_result() -> None:
    plan = generate_plan(
        repository_root=ROOT,
        profile_path=TARGET_ROOT
        / "profiles/portable-semantic-c147-portable-full-agent-heldout-r3-codex-cli0146-sol-medium-n5-r1.json",
        target_path=TARGET,
        bundle_path=TARGET_ROOT
        / "prompts/candidates/portable-semantic-c147-portable-full-agent-r1",
    )
    with pytest.raises(QualificationGateError, match="incompatible"):
        bind_existing_iteration_result(
            reference_result_path=TARGET_ROOT
            / "results/portable-semantic-c147-reference-heldout-r3-n1-qualification-r1.json",
            plan=plan,
            repository_root=ROOT,
        )


def test_n5_profiles_keep_execution_gate_and_make_missing_iterations_explicit() -> None:
    for path in sorted((TARGET_ROOT / "profiles").glob("*heldout-r3*medium-n5-r1.json")):
        profile = json.loads(path.read_text())
        assert profile["execution"] == {
            "max_workers": 24,
            "schedule_policy": "global_queue",
            "max_attempts_per_slot": 1,
            "dispatch_gate": "adapter_entrypoint_and_preflight_required",
        }
        assert profile["dispatch_iterations"] == [2, 3, 4, 5]


def test_registered_n5_results_have_exact_case_iteration_coverage() -> None:
    results = [
        json.loads(path.read_text())
        for path in sorted((TARGET_ROOT / "results").glob("*heldout-r3-n5-qualification-r1.json"))
    ]
    assert len(results) == 2
    for result in results:
        assert len(result["cases"]) == 70
        assert result["summary"]["reused_slots"] == 14
        assert result["summary"]["newly_authorized_slots"] == 56
        by_case: dict[str, set[int]] = {}
        for row in result["cases"]:
            by_case.setdefault(row["slot"]["case_id"], set()).add(row["slot"]["iteration"])
        assert len(by_case) == 14
        assert all(iterations == {1, 2, 3, 4, 5} for iterations in by_case.values())
        assert len(result["excluded_attempts"]) == result["summary"]["excluded_attempts"]


def test_n5_quality_difference_is_preserved_without_rerun() -> None:
    reference = json.loads(
        (
            TARGET_ROOT
            / "results/portable-semantic-c147-reference-heldout-r3-n5-qualification-r1.json"
        ).read_text()
    )
    portable = json.loads(
        (
            TARGET_ROOT
            / "results/portable-semantic-c147-portable-full-agent-heldout-r3-n5-qualification-r1.json"
        ).read_text()
    )
    assert reference["summary"]["score4_results"] == 69
    failed = [row for row in reference["cases"] if row["quality_score"] != 4]
    assert [row["slot"]["slot_id"] for row in failed] == ["PIC-H17-i002"]
    assert portable["summary"]["score4_results"] == 70
