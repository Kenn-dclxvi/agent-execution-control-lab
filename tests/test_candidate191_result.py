from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STANDARD_RESULT = ROOT / "evaluations/results/6cbac394f6dc46aea5da398c867df2f5.json"
STANDARD_QUALITY = ROOT / "evaluations/results/candidate191-explicit-review-operation-applicability-standard14-f02-f03-f04-n5-audit-r1.json"
STANDARD_MECHANISM = ROOT / "evaluations/results/candidate191-explicit-review-operation-applicability-standard14-f02-f03-f04-n5-mechanism-audit-r1.json"
ADR_RESULT = ROOT / "evaluations/results/b71bcb211b064977900bce9aa0132cd4.json"
ADR_QUALITY = ROOT / "evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-n5-audit-r1.json"
ADR_MECHANISM_R2 = ROOT / "evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-n5-mechanism-audit-r2.json"
ADR_MECHANISM_R3 = ROOT / "evaluations/results/candidate191-explicit-review-operation-applicability-adr9-r2-n5-mechanism-audit-r3.json"
C147_REASSESSMENT = ROOT / "evaluations/results/candidate147-result-effect-scope-adr9-r2-n50-mechanism-reassessment-r2.json"
C176_REASSESSMENT = ROOT / "evaluations/results/candidate176-decision-premise-counterexample-mechanism-reassessment-r2.json"


class Candidate191ResultTest(unittest.TestCase):
    def test_targeted_standard14_regression_gate_passes(self) -> None:
        result = json.loads(STANDARD_RESULT.read_text(encoding="utf-8"))
        quality = json.loads(STANDARD_QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(STANDARD_MECHANISM.read_text(encoding="utf-8"))

        self.assertEqual(result["result_id"], "6cbac394f6dc46aea5da398c867df2f5")
        self.assertEqual(result["compatibility_key"], "ccf1d2b5d84aaec45f2960a048a80c77d69ce69fca15a0546e86b368f799ba54")
        self.assertEqual(len(result["case_results"]), 15)
        self.assertEqual({item["quality_score"] for item in result["case_results"]}, {4})
        self.assertEqual(quality["score_counts"], {"4": 15})
        self.assertEqual(mechanism["unwanted_review_producer_run_count"], 0)
        self.assertEqual(mechanism["child_agent_run_count"], 0)
        self.assertEqual(mechanism["command_protocol_violation_count"], 0)
        self.assertTrue(mechanism["mechanism_gate_passed"])

    def test_adr9_reassessment_uses_raw_wrapper_results(self) -> None:
        result = json.loads(ADR_RESULT.read_text(encoding="utf-8"))
        quality = json.loads(ADR_QUALITY.read_text(encoding="utf-8"))
        historical = json.loads(ADR_MECHANISM_R2.read_text(encoding="utf-8"))
        mechanism = json.loads(ADR_MECHANISM_R3.read_text(encoding="utf-8"))

        self.assertEqual(result["result_id"], "b71bcb211b064977900bce9aa0132cd4")
        self.assertEqual(result["compatibility_key"], "d09c57a94101d4e2682efbf93a44a456a04e9378556859726d58af872edb6152")
        self.assertEqual(len(result["case_results"]), 30)
        self.assertEqual({item["quality_score"] for item in result["case_results"]}, {4})
        self.assertEqual(Counter(item["case_id"] for item in result["case_results"]), Counter({case: 5 for case in result["compatibility"]["coverage"]["case_ids"]}))
        self.assertEqual(quality["quality_score_counts"], {"4": 30})
        self.assertTrue(quality["targeted_gate_passed"])
        self.assertEqual(historical["command_protocol_violation_count"], 83)
        self.assertEqual(historical["status"], "mechanism_failed_stopped")
        self.assertEqual(mechanism["current_result_admission_count"], 30)
        self.assertEqual(mechanism["terminal_match_count"], 30)
        self.assertEqual(mechanism["authentic_observation_result_count"], 30)
        self.assertEqual(mechanism["collector_reported_violation_count"], 83)
        self.assertEqual(mechanism["collector_false_positive_count"], 83)
        self.assertEqual(mechanism["actual_nested_command_count"], 43)
        self.assertEqual(mechanism["machine_bound_exit_code_count"], 43)
        self.assertEqual(mechanism["genuine_missing_machine_bound_exit_code_count"], 0)
        self.assertEqual(mechanism["affected_run_count"], len(mechanism["affected_run_ids"]))
        self.assertLessEqual(
            set(mechanism["affected_run_ids"]),
            {item["run_id"] for item in result["case_results"]},
        )
        self.assertTrue(mechanism["mechanism_gate_passed"])
        self.assertEqual(mechanism["status"], "mechanism_passed_reassessed")

    def test_future_comparison_binds_corrected_mechanism_audits(self) -> None:
        c147 = json.loads(C147_REASSESSMENT.read_text(encoding="utf-8"))
        c176 = json.loads(C176_REASSESSMENT.read_text(encoding="utf-8"))

        self.assertEqual(c147["collector_reported_violation_count"], 44)
        self.assertEqual(c147["collector_false_positive_count"], 20)
        self.assertEqual(c147["genuine_missing_machine_bound_exit_code_count"], 24)
        self.assertEqual(c147["genuine_affected_run_count"], 21)
        self.assertFalse(c147["mechanism_gate_passed"])
        self.assertEqual(c147["future_comparison_binding"], "registered_result_plus_this_reassessment")

        self.assertEqual(c176["scopes"]["adr9_r2_n5"]["reassessed_status"], "mechanism_failed")
        self.assertEqual(c176["scopes"]["targeted_adr9_n20_additional_runs"]["genuine_missing_machine_bound_exit_code_count"], 2)
        self.assertEqual(c176["scopes"]["targeted_adr9_n50_additional_runs"]["independent_terminal_failure_run_id"], "79302c5e76874014bbcdf8f5d3304031")
        self.assertFalse(c176["mechanism_gate_passed"])
        self.assertEqual(c176["future_comparison_binding"], "registered_result_selection_plus_this_reassessment")


if __name__ == "__main__":
    unittest.main()
