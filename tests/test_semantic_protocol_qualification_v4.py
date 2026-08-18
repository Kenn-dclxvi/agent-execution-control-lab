import hashlib
import json
from pathlib import Path

import pytest

from scripts.run_semantic_protocol_qualification_v4 import (
    QualificationGateError,
    bind_existing_iteration_result,
    generate_plan,
)


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/portable-instruction-semantic-conformance"
TARGET = TARGET_ROOT / "target.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize(
    ("profile_name", "bundle_name", "result_name"),
    [
        (
            "portable-semantic-c147-reference-heldout-r3-codex-cli0146-sol-medium-n20-r1.json",
            "baselines/portable-semantic-c147-full-agent-reference-r1",
            "portable-semantic-c147-reference-heldout-r3-n5-qualification-r1.json",
        ),
        (
            "portable-semantic-c147-portable-full-agent-heldout-r3-codex-cli0146-sol-medium-n20-r1.json",
            "candidates/portable-semantic-c147-portable-full-agent-r1",
            "portable-semantic-c147-portable-full-agent-heldout-r3-n5-qualification-r1.json",
        ),
    ],
)
def test_n20_plan_reuses_n5_and_dispatches_only_i006_through_i020(
    profile_name: str, bundle_name: str, result_name: str
) -> None:
    plan = generate_plan(
        repository_root=ROOT,
        profile_path=TARGET_ROOT / "profiles" / profile_name,
        target_path=TARGET,
        bundle_path=TARGET_ROOT / "prompts" / bundle_name,
    )
    assert len(plan["slots"]) == 210
    assert {slot["iteration"] for slot in plan["slots"]} == set(range(6, 21))
    binding = bind_existing_iteration_result(
        reference_result_path=TARGET_ROOT / "results" / result_name,
        plan=plan,
        repository_root=ROOT,
    )
    assert binding["reused_slot_count"] == 70
    assert {slot["iteration"] for slot in binding["reused_slots"]} == set(range(1, 6))


def test_n20_reference_binding_rejects_other_prompt_result() -> None:
    plan = generate_plan(
        repository_root=ROOT,
        profile_path=TARGET_ROOT
        / "profiles/portable-semantic-c147-portable-full-agent-heldout-r3-codex-cli0146-sol-medium-n20-r1.json",
        target_path=TARGET,
        bundle_path=TARGET_ROOT
        / "prompts/candidates/portable-semantic-c147-portable-full-agent-r1",
    )
    with pytest.raises(QualificationGateError, match="incompatible"):
        bind_existing_iteration_result(
            reference_result_path=TARGET_ROOT
            / "results/portable-semantic-c147-reference-heldout-r3-n5-qualification-r1.json",
            plan=plan,
            repository_root=ROOT,
        )


def test_n20_profiles_keep_fixed_execution_gate() -> None:
    paths = sorted((TARGET_ROOT / "profiles").glob("*heldout-r3*medium-n20-r1.json"))
    assert len(paths) == 2
    for path in paths:
        profile = json.loads(path.read_text())
        assert profile["execution"] == {
            "max_workers": 24,
            "schedule_policy": "global_queue",
            "max_attempts_per_slot": 1,
            "dispatch_gate": "adapter_entrypoint_and_preflight_required",
        }
        assert profile["dispatch_iterations"] == list(range(6, 21))


def test_n5_preflights_still_bind_unchanged_v3_runner() -> None:
    runner = ROOT / "scripts/run_semantic_protocol_qualification_v3.py"
    for path in (TARGET_ROOT / "plans").glob("*heldout-r3-n5-preflight-r1.json"):
        receipt = json.loads(path.read_text())
        assert receipt["execution_code"]["runner"]["sha256"] == sha256(runner)


def test_registered_n20_results_have_exact_coverage_and_preserve_quality() -> None:
    results = [
        json.loads(path.read_text())
        for path in sorted((TARGET_ROOT / "results").glob("*heldout-r3-n20-qualification-r1.json"))
    ]
    assert len(results) == 2
    for result in results:
        assert len(result["cases"]) == 280
        assert result["summary"]["reused_slots"] == 70
        assert result["summary"]["newly_authorized_slots"] == 210
        by_case: dict[str, set[int]] = {}
        for row in result["cases"]:
            by_case.setdefault(row["slot"]["case_id"], set()).add(row["slot"]["iteration"])
        assert len(by_case) == 14
        assert all(iterations == set(range(1, 21)) for iterations in by_case.values())
        assert len(result["excluded_attempts"]) == 6
    assert results[0]["summary"]["score4_results"] == 280
    assert results[1]["summary"]["score4_results"] == 275
