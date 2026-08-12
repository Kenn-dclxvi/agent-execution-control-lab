from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "evaluations/results/333508e7f37545218bea8f71fc9d3d1c.json"
QUALITY = ROOT / "evaluations/results/candidate190-current-prior-review-result-admission-standard14-n5-audit-r1.json"
MECHANISM = ROOT / "evaluations/results/candidate190-current-prior-review-result-admission-standard14-n5-mechanism-audit-r1.json"


class Candidate190M7ResultTest(unittest.TestCase):
    def test_quality_pass_and_mechanism_failure_are_not_collapsed(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))

        self.assertEqual(result["result_id"], "333508e7f37545218bea8f71fc9d3d1c")
        self.assertEqual(
            result["result_content_sha256"],
            "2cf13bb1d861558fda31922456608f7fbccd7063c9a32af6717553bb1faadaf1",
        )
        self.assertEqual(result["compatibility_key"], "cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561")
        self.assertEqual(result["source_selection"]["selection_id"], "df044c8c441443ecb025d5156c771a09")
        self.assertEqual(len(result["case_results"]), 70)
        self.assertEqual(Counter(item["case_id"] for item in result["case_results"]), Counter({case: 5 for case in result["compatibility"]["coverage"]["case_ids"]}))
        self.assertTrue(all(item["quality_score"] == 4 for item in result["case_results"]))

        self.assertEqual(quality["run_count"], 70)
        self.assertEqual(quality["rateable_runs"], 70)
        self.assertEqual(quality["score_counts"], {"4": 70})
        self.assertEqual(quality["failure_counts"], {})
        self.assertEqual(quality["diagnostic_counts"]["command_protocol_violations"], 37)

        self.assertEqual(mechanism["mechanism_status"], "failed")
        self.assertEqual(mechanism["unwanted_review_producer_run_count"], 8)
        self.assertEqual(mechanism["command_protocol_violation_count"], 37)
        self.assertEqual(mechanism["quality_failure_count"], 0)
        self.assertEqual(mechanism["unexpected_changed_path_count"], 0)


if __name__ == "__main__":
    unittest.main()
