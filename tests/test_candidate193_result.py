from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "evaluations/results/9630f826932c4abc91cc2a4598ca318d.json"
QUALITY = ROOT / "evaluations/results/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-audit-r2.json"
MECHANISM = ROOT / "evaluations/results/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-mechanism-audit-r2.json"
REASSESSMENT = ROOT / "evaluations/results/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5-mechanism-reassessment-r3.json"
REPORT = ROOT / "evaluations/results/candidate193-frontier-bound-dispatch-transition-adr9-r2-n5_2026-08-12.md"


class Candidate193ResultTest(unittest.TestCase):
    def test_registered_result_and_failure_gates_are_preserved(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))

        self.assertEqual(result["result_id"], "9630f826932c4abc91cc2a4598ca318d")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(sum(item["quality_score"] == 4 for item in result["case_results"]), 43)
        self.assertEqual(sum(item["quality_score"] == 1 for item in result["case_results"]), 2)
        self.assertEqual(quality["status"], "quality_failed_stopped")
        self.assertEqual(quality["terminal_match_count"], 43)
        self.assertEqual(quality["collector_false_positive_count"], 171)
        self.assertEqual(quality["genuine_missing_machine_bound_exit_status_count"], 0)
        self.assertEqual(mechanism["status"], "mechanism_failed_stopped")
        self.assertEqual(mechanism["initial_frontier_match_count"], 17)
        self.assertEqual(mechanism["initial_coissuance_count"], 28)
        self.assertTrue(mechanism["command_evidence_gate_passed"])
        self.assertFalse(mechanism["dispatch_trace_gate_passed"])
        self.assertFalse(mechanism["mechanism_gate_passed"])

    def test_reassessment_preserves_partial_effect_and_audit_limitations(self) -> None:
        reassessment = json.loads(REASSESSMENT.read_text(encoding="utf-8"))

        self.assertEqual(reassessment["new_run_count"], 0)
        self.assertEqual(reassessment["candidate191"]["identity_read_coissuance_count"], 36)
        self.assertEqual(reassessment["candidate193"]["identity_read_coissuance_count"], 28)
        self.assertEqual(reassessment["direct_parent_delta"]["correct_initial_separation_count"], 8)
        self.assertEqual(
            reassessment["diagnostic_only_noncausal_context"]["candidate147"]["compatibility"],
            "not_compatible_with_r2_comparison",
        )
        self.assertEqual(
            reassessment["prior_r2_audit_limitations"]["stale_quality_fields"],
            ["TC-ADR06_iteration_2", "TC-ADR06_iteration_3"],
        )
        self.assertIn("dispatch_frontier", reassessment["classification"]["pending"])
        self.assertNotIn("dispatch_frontier", reassessment["classification"]["reject"])

    def test_reader_facing_status_stops_before_m6_and_standard14(self) -> None:
        report = REPORT.read_text(encoding="utf-8")
        plan = (ROOT / "docs/review-control-reconstruction-milestone-plan.md").read_text(encoding="utf-8")
        results_index = (ROOT / "evaluations/results/README.md").read_text(encoding="utf-8")
        docs_index = (ROOT / "docs/README.md").read_text(encoding="utf-8")
        candidate_index = (ROOT / "prompts/candidates/README.md").read_text(encoding="utf-8")

        self.assertIn("Score 4 = 43 / Score 1 = 2", report)
        self.assertIn("dispatch_dependency_crossing_28", report)
        self.assertIn("M1_reopened_for_candidate193_quality_and_dispatch_failures", plan)
        self.assertIn(REPORT.name, results_index)
        self.assertIn("Candidate147〜Candidate193", results_index)
        self.assertIn(REPORT.name, docs_index)
        self.assertIn(
            "adr9_r2_n5_evaluated / quality_failed / mechanism_failed / stopped",
            candidate_index,
        )


if __name__ == "__main__":
    unittest.main()
