from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
TARGET_ROOT = ROOT / "evaluations/targets/codex-validation-carrier-conformance"
REGISTER_PATH = ROOT / "evaluations/targets/codex-validation-carrier-conformance/runtime/register_qualification.py"
SPEC = importlib.util.spec_from_file_location("codex_validation_carrier_register", REGISTER_PATH)
assert SPEC is not None and SPEC.loader is not None
register = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(register)


def row(score: int, mechanism: bool, tokens: int, elapsed: float) -> dict:
    return {
        "status": "valid", "quality_score": score, "mechanism_passed": mechanism,
        "all_agent_total_tokens": tokens, "elapsed_seconds": elapsed,
    }


def test_summary_keeps_low_quality_and_reports_three_kpis() -> None:
    rows = [
        row(4, True, 25850, 16.6860815), row(4, False, 39367, 21.42902775),
        row(1, False, 56848, 23.024141042), row(4, False, 66322, 24.6311765),
        row(4, False, 66190, 27.749217), row(2, False, 95942, 36.874568375),
    ]
    summary = register.summarize(rows)
    assert summary["quality_score_distribution"] == {"1": 1, "2": 1, "4": 4}
    assert summary["mechanism_passed"] == 1
    assert summary["mechanism_failed"] == 5
    assert summary["all_agent_total_tokens_sum"] == 350519
    assert summary["all_agent_total_tokens_median"] == 61519
    assert summary["elapsed_seconds_sum"] == pytest.approx(150.394212167)
    assert summary["elapsed_seconds_median"] == pytest.approx(23.827658771)


def test_summary_rejects_incomplete_qualification() -> None:
    with pytest.raises(register.runner.RuntimeGateError, match="six valid rows"):
        register.summarize([row(4, True, 1, 1.0)])


def test_published_result_and_append_only_registration_are_consistent() -> None:
    result_path = TARGET_ROOT / "results/codex-validation-carrier-control-free-heldout-r1-n1-qualification-r1.json"
    result = register.runner.adapter.load_object(result_path)
    assert result["result_sha256"] == register.runner.content_identity(result, "result_sha256")
    assert result["summary"]["valid_results"] == 6
    assert result["summary"]["external_failures"] == 0
    assert result["qualification"]["all_cases_have_three_kpis"] is True
    registration = register.runner.adapter.load_object(
        TARGET_ROOT / "registrations/heldout-r1-runtime-registration-r1.json"
    )
    assert registration["qualification_result"]["sha256"] == register.runner.sha256_file(result_path)
    assert registration["qualification_result"]["result_sha256"] == result["result_sha256"]
    assert registration["allowed_next_profile_class"] == "candidate_only_p002_gate"
    assert "p001_p002_paired_comparison_before_candidate_gate" in registration["forbidden_profile_classes"]
