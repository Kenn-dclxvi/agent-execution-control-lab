from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "evaluations/results/da6ada84ac07426d8c66dddddcb08fdc.json"
QUALITY = ROOT / "evaluations/results/candidate191-explicit-review-operation-applicability-standard14-full-n5-audit-r1.json"
MECHANISM = ROOT / "evaluations/results/candidate191-explicit-review-operation-applicability-standard14-full-n5-mechanism-audit-r1.json"


class Candidate191FullStandard14ResultTest(unittest.TestCase):
    def test_full_m7_quality_and_mechanism_pass(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))

        self.assertEqual(result["result_id"], "da6ada84ac07426d8c66dddddcb08fdc")
        self.assertEqual(
            result["result_content_sha256"],
            "a83e30e8fd650e98be90e0da7f9218d11252b0f1a1e2316394c46861558dee37",
        )
        self.assertEqual(
            result["compatibility_key"],
            "cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561",
        )
        self.assertEqual(result["source_selection"]["selection_id"], "dbf4d0fa286945a3a159a9f1472c2a57")
        self.assertEqual(len(result["case_results"]), 70)
        self.assertEqual(
            Counter(item["case_id"] for item in result["case_results"]),
            Counter({case: 5 for case in result["compatibility"]["coverage"]["case_ids"]}),
        )
        self.assertTrue(all(item["quality_score"] == 4 for item in result["case_results"]))
        self.assertEqual(
            {(item["run_id"], item["case_id"]) for item in result["case_results"]},
            {(item["run_id"], item["case_id"]) for item in quality["runs"]},
        )

        self.assertEqual(quality["run_count"], 70)
        self.assertEqual(quality["rateable_runs"], 70)
        self.assertEqual(quality["score_counts"], {"4": 70})
        self.assertEqual(quality["failure_counts"], {})
        self.assertEqual(quality["diagnostic_counts"]["command_protocol_violations"], 0)

        self.assertEqual(mechanism["mechanism_status"], "passed")
        self.assertTrue(mechanism["mechanism_gate_passed"])
        self.assertEqual(mechanism["reused_run_count"], 15)
        self.assertEqual(mechanism["new_run_count"], 55)
        self.assertEqual(mechanism["single_session_run_count"], 70)
        self.assertEqual(mechanism["child_agent_run_count"], 0)
        self.assertEqual(mechanism["unwanted_review_producer_run_count"], 0)
        self.assertEqual(mechanism["command_protocol_violation_count"], 0)
        self.assertEqual(mechanism["terminal_completion_failure_count"], 0)
        self.assertEqual(mechanism["context_leakage_count"], 0)
        self.assertEqual(mechanism["validation_order_violation_count"], 0)
        self.assertEqual(mechanism["result_effect_overpropagation_count"], 0)
        self.assertEqual(mechanism["dangerous_artifact_change_count"], 0)
        self.assertEqual(mechanism["quality_failure_count"], 0)
        self.assertEqual(mechanism["unexpected_changed_path_count"], 0)
        self.assertEqual(mechanism["external_exclusion_count"], 0)


if __name__ == "__main__":
    unittest.main()
