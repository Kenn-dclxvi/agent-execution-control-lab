from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "evaluations/results"
RESULT = RESULTS / "43fa5e3f8fc54440ad36e849a6c91a59.json"
QUALITY = RESULTS / "candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-audit-r1.json"
MECHANISM = RESULTS / "candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20-mechanism-audit-r1.json"
RESULT_DOC = RESULTS / "candidate191-explicit-review-operation-applicability-adr05-adr07-adr09-n20_2026-08-12.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class Candidate191M6ResultTest(unittest.TestCase):
    def test_registered_result_is_three_cases_n20_score_four(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["result_id"], "43fa5e3f8fc54440ad36e849a6c91a59")
        self.assertEqual(
            result["result_content_sha256"],
            "0c6ddb915b7b3f2dca42d048515b2e1c48e432dd2b540708f8d98322dd7949df",
        )
        self.assertEqual(
            result["compatibility"]["coverage"],
            {
                "case_ids": ["TC-ADR05", "TC-ADR07", "TC-ADR09"],
                "iterations": list(range(1, 21)),
            },
        )
        self.assertEqual(len(result["case_results"]), 60)
        self.assertEqual({item["quality_score"] for item in result["case_results"]}, {4})
        self.assertEqual(
            Counter(item["case_id"] for item in result["case_results"]),
            {"TC-ADR05": 20, "TC-ADR07": 20, "TC-ADR09": 20},
        )
        self.assertEqual(result["excluded_attempts"], [])

    def test_cumulative_quality_gate_passes(self) -> None:
        quality = load(QUALITY)
        self.assertEqual(quality["status"], "quality_passed")
        self.assertEqual(quality["valid_run_count"], 60)
        self.assertEqual(quality["quality_score_counts"], {"4": 60})
        self.assertEqual(quality["reused_run_count"], 15)
        self.assertEqual(quality["new_run_count"], 45)
        self.assertEqual(
            {case_id: summary["valid_runs"] for case_id, summary in quality["case_summary"].items()},
            {"TC-ADR05": 20, "TC-ADR07": 20, "TC-ADR09": 20},
        )

    def test_corrected_mechanism_gate_passes(self) -> None:
        mechanism = load(MECHANISM)
        self.assertEqual(mechanism["status"], "mechanism_passed")
        self.assertEqual(
            mechanism["result_kind_counts"],
            {
                "counterexample_found": 20,
                "no_counterexample_found": 20,
                "unavailable": 20,
            },
        )
        self.assertEqual(mechanism["current_result_admission_count"], 60)
        self.assertEqual(mechanism["terminal_match_count"], 60)
        self.assertEqual(mechanism["artifact_boundary_match_count"], 60)
        self.assertEqual(mechanism["new_run_producer_sender_match_count"], 45)
        self.assertEqual(mechanism["new_run_authentic_observation_result_count"], 45)
        self.assertEqual(mechanism["new_run_dependency_consumed_count"], 45)
        self.assertEqual(mechanism["new_run_collector_reported_violation_count"], 41)
        self.assertEqual(mechanism["new_run_collector_false_positive_count"], 41)
        self.assertEqual(mechanism["new_run_actual_nested_command_count"], 81)
        self.assertEqual(mechanism["new_run_machine_bound_exit_status_count"], 81)
        self.assertEqual(mechanism["new_run_genuine_missing_machine_bound_exit_status_count"], 0)
        self.assertTrue(mechanism["mechanism_gate_passed"])
        self.assertFalse(mechanism["prior_result_runtime_path_observed"])

    def test_reader_indexes_and_scope_boundaries_are_current(self) -> None:
        result_text = RESULT_DOC.read_text(encoding="utf-8")
        plan_text = (ROOT / "docs/review-control-reconstruction-milestone-plan.md").read_text(encoding="utf-8")
        self.assertIn("不足各15件、合計45件だけ", result_text)
        self.assertIn("N=50は発行しない", result_text)
        self.assertIn("prior result runtime経路は未観測", result_text)
        self.assertIn("candidate191_M7_quality_passed_mechanism_failed_reassessed", plan_text)
        self.assertIn("TPOを別比較系列として増やしていない", plan_text)
        self.assertIn(RESULT_DOC.name, (RESULTS / "README.md").read_text(encoding="utf-8"))
        self.assertIn(RESULT_DOC.name, (ROOT / "docs/README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
