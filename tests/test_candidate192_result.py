from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT_ID = "f53d1494b2ec45d083fdd199ec04a14d"
RESULT = ROOT / f"evaluations/results/{RESULT_ID}.json"
QUALITY = ROOT / "evaluations/results/candidate192-consumer-bound-coissuance-standard14-targeted-n5-audit-r1.json"
MECHANISM = ROOT / "evaluations/results/candidate192-consumer-bound-coissuance-standard14-targeted-n5-mechanism-audit-r1.json"
REPORT = ROOT / "evaluations/results/candidate192-consumer-bound-coissuance-standard14-targeted-n5_2026-08-12.md"


class Candidate192ResultTest(unittest.TestCase):
    def test_quality_passes_but_dispatch_mechanism_fails(self) -> None:
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))

        self.assertEqual(quality["run_count"], 50)
        self.assertEqual(quality["rateable_runs"], 50)
        self.assertEqual(quality["score_counts"], {"4": 50})
        self.assertEqual(quality["failure_counts"], {})
        self.assertEqual(quality["diagnostic_counts"]["command_protocol_violations"], 0)

        self.assertTrue(mechanism["quality_gate_passed"])
        self.assertFalse(mechanism["mechanism_gate_passed"])
        self.assertEqual(
            mechanism["failure_class"],
            "dispatch_admission_not_behaviorally_binding",
        )
        self.assertEqual(
            mechanism["a01_consumerless_start_identity_zero_gate"],
            {"passed": False, "passed_runs": 3, "run_count": 5},
        )
        self.assertEqual(
            mechanism["affected8_identity_read_coissuance_gate"],
            {"passed": False, "passed_runs": 1, "run_count": 40},
        )
        self.assertEqual(
            mechanism["regressed9_no_added_prechange_round_gate"],
            {"passed": False, "passed_runs": 4, "run_count": 45},
        )

    def test_registered_result_and_indexes_are_bound(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], RESULT_ID)
        self.assertEqual(
            result["compatibility_key"],
            "58c8563e60f397402b8b6d07f6636273f1836ddc88e0e51ad9df900b8f2719b3",
        )
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(
            mechanism["reference_result_id"],
            "4b3fcabe4a004d9a945f6d1bcbdecfdc",
        )
        self.assertEqual(len(result["case_results"]), 50)
        self.assertEqual({item["quality_score"] for item in result["case_results"]}, {4})

        report = REPORT.read_text(encoding="utf-8")
        results_index = (ROOT / "evaluations/results/README.md").read_text(encoding="utf-8")
        candidate_index = (ROOT / "prompts/candidates/README.md").read_text(encoding="utf-8")
        plan = (ROOT / "docs/review-control-reconstruction-milestone-plan.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(RESULT_ID, report)
        self.assertIn(REPORT.name, results_index)
        self.assertIn("quality_passed / mechanism_failed / stopped", candidate_index)
        self.assertIn("candidate192_targeted_standard14_quality_passed_mechanism_failed", plan)
        self.assertIn("candidate192_remaining_standard14_not_issued", plan)
        self.assertIn("candidate192_ADR9_not_issued", plan)

    def test_case_kpis_use_compatible_candidate191_reference(self) -> None:
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        rows = {item["case_id"]: item for item in mechanism["case_summary"]}
        self.assertAlmostEqual(rows["TC-A01-LATENT-MODE-POLICY"]["token_delta_percent"], -49.65)
        self.assertAlmostEqual(rows["TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING"]["token_delta_percent"], 28.28)
        self.assertAlmostEqual(rows["TC-F04-WEB-AUDIT-COLUMN-VISIBILITY"]["token_delta_percent"], 29.91)
        self.assertEqual(mechanism["control_f04"]["dependency_crossing_runs"], 0)


if __name__ == "__main__":
    unittest.main()
