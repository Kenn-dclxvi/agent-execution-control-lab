from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "evaluations/results/candidate191-explicit-review-operation-applicability-m8-complexity-efficiency-audit-r1.json"
PLAN = ROOT / "docs/review-control-reconstruction-milestone-plan.md"
REPORT = ROOT / "docs/candidate191-complexity-efficiency-evaluation.md"
DOCS_INDEX = ROOT / "docs/README.md"
RESULTS_INDEX = ROOT / "evaluations/results/README.md"
CANDIDATE_INDEX = ROOT / "prompts/candidates/README.md"


class Candidate191M8ResultTest(unittest.TestCase):
    def test_static_complexity_and_decision_are_fixed(self) -> None:
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))

        self.assertEqual(audit["status"], "m8_completed_reassessed_m9_not_ready")
        self.assertEqual(audit["measurement_policy"]["new_evaluation_runs_issued"], 0)
        self.assertFalse(audit["measurement_policy"]["candidate_content_changed"])
        self.assertEqual(
            audit["static_complexity"]["candidate147"],
            {
                "characters": 7090,
                "utf8_bytes": 10772,
                "top_level_clauses": 13,
                "named_definitions": 9,
                "explicit_state_domains": 1,
                "state_literal_occurrences": 3,
            },
        )
        self.assertEqual(audit["static_complexity"]["candidate191"]["utf8_bytes"], 17989)
        self.assertEqual(audit["static_complexity"]["candidate191"]["top_level_clauses"], 19)
        self.assertAlmostEqual(
            audit["static_complexity"]["candidate191_minus_candidate147"]["utf8_bytes_percent"],
            66.99777200148533,
        )
        responsibility = audit["static_complexity"]["responsibility_audit"]
        self.assertEqual(responsibility["conflicting_transition_owner_count"], 0)
        self.assertEqual(responsibility["unsafe_duplicate_deletion_candidate_count"], 0)

        decision = audit["decision"]
        self.assertEqual(decision["quality_status"], "passed_before_m8")
        self.assertEqual(decision["mechanism_status"], "standard14_failed_after_cost_trace_reassessment")
        self.assertFalse(decision["optimization_required_before_m9"])
        self.assertFalse(decision["m9_ready"])

    def test_candidate191_kpis_are_bound_to_registered_results(self) -> None:
        audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        expected = {
            "adr9_r2_full_n5": ("e599690689294c658b52a6a9e301697f", 45, 100.0, 1410389, 921.6695667080094),
            "adr05_adr07_adr09_n20": ("43fa5e3f8fc54440ad36e849a6c91a59", 60, 100.0, 550016.5, 373.549701583499),
            "standard14_full_n5": ("da6ada84ac07426d8c66dddddcb08fdc", 70, 100.0, 1875286, 932.7256169989923),
        }
        for key, values in expected.items():
            with self.subTest(key=key):
                kpi = audit["candidate191_kpi"][key]
                self.assertEqual(
                    (
                        kpi["result_id"],
                        kpi["run_count"],
                        kpi["quality_score_median"],
                        kpi["all_agent_total_tokens_median"],
                        kpi["elapsed_seconds_median"],
                    ),
                    values,
                )
                self.assertEqual(kpi["genuine_command_protocol_violation_count"], 0)
                self.assertEqual(kpi["environment_recovery_count"], 0)

    def test_m8_report_and_indexes_point_to_the_audit(self) -> None:
        plan = PLAN.read_text(encoding="utf-8")
        report = REPORT.read_text(encoding="utf-8")
        docs_index = DOCS_INDEX.read_text(encoding="utf-8")
        results_index = RESULTS_INDEX.read_text(encoding="utf-8")
        candidate_index = CANDIDATE_INDEX.read_text(encoding="utf-8")

        self.assertIn("Candidate193 ADR9 r2品質・発行遷移機序不通過／M1原因分析再開", plan)
        self.assertIn("candidate193_M5_valid_45_score4_43_score1_2", plan)
        self.assertIn("M9_not_ready", plan)
        self.assertNotIn("M8_not_started", plan)
        self.assertIn("candidate191-explicit-review-operation-applicability-m8-complexity-efficiency-audit-r1.json", report)
        self.assertIn("candidate191-complexity-efficiency-evaluation.md", docs_index)
        self.assertIn("candidate191-explicit-review-operation-applicability-m8-complexity-efficiency-audit-r1.json", results_index)
        self.assertIn("candidate191-standard14-cost-mechanism-reassessment.md", candidate_index)
        self.assertIn("mechanism_failed_reassessed", candidate_index)

    def test_standard14_cost_reassessment_blocks_m9(self) -> None:
        reassessment = json.loads(
            (ROOT / "evaluations/results/candidate191-standard14-cost-mechanism-reassessment-r1.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(reassessment["status"], "mechanism_failed_reassessed")
        self.assertEqual(reassessment["mechanism_failure"]["affected_case_count"], 9)
        self.assertEqual(reassessment["mechanism_failure"]["candidate191_run_count_with_extra_prechange_step"], 44)
        self.assertAlmostEqual(
            reassessment["token_totals"]["affected_nine_cases_share_of_total_delta_percent"],
            86.74156311487195,
        )
        self.assertFalse(reassessment["decision"]["m9_ready"])


if __name__ == "__main__":
    unittest.main()
