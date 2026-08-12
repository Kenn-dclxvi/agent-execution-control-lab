from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "evaluations/results/70652de440184e20bf54dea88b058c94.json"
AUDIT = ROOT / "evaluations/results/candidate189-self-contained-review-control-adr9-r2-n5-audit-r1.json"
RESULT_DOC = ROOT / "evaluations/results/candidate189-self-contained-review-control-adr9-r2-n5_2026-08-12.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class Candidate189Adr9ResultTest(unittest.TestCase):
    def test_registered_result_keeps_reference_compatibility(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["result_id"], "70652de440184e20bf54dea88b058c94")
        self.assertEqual(result["compatibility_key"], "1543a80108418ce1f2436f5f1945f6e680cf75378cc308d21adee22fcf0f11d3")
        self.assertEqual(
            load(AUDIT)["provenance"]["reference_result_id"],
            "d3e91302f0d14350906075676c5a2791",
        )
        self.assertEqual(len(result["case_results"]), 45)

    def test_failed_gate_is_preserved_without_rerun(self) -> None:
        audit = load(AUDIT)
        self.assertEqual(audit["valid_run_count"], 45)
        self.assertEqual(audit["excluded_attempt_count"], 0)
        self.assertEqual(audit["quality_score_counts"], {"1": 1, "4": 44})
        self.assertFalse(audit["targeted_gate_passed"])
        self.assertFalse(audit["mechanism_gate_passed"])
        self.assertEqual(audit["status"], "quality_failed_mechanism_failed_stopped")
        self.assertEqual(len(audit["failing_runs"]), 1)
        self.assertEqual(audit["failing_runs"][0]["run_id"], "4000b36892f5445c98b27d24e7d6d68c")
        result_doc = RESULT_DOC.read_text(encoding="utf-8")
        self.assertIn("再実行で置き換えない", result_doc)
        self.assertIn("M6とStandard14へ進まない", result_doc)

    def test_case_mechanisms_keep_expected_routes(self) -> None:
        summary = load(AUDIT)["case_summary"]
        self.assertEqual(summary["TC-ADR01"]["reviewer_count"], 0)
        self.assertEqual(summary["TC-ADR02"]["reviewer_count"], 0)
        for case in ("TC-ADR03", "TC-ADR04", "TC-ADR05", "TC-ADR06", "TC-ADR07", "TC-ADR09"):
            self.assertEqual(summary[case]["reviewer_count"], 5)
        self.assertEqual(summary["TC-ADR08"]["reviewer_count"], 0)
        self.assertEqual(summary["TC-ADR06"]["canary_delivery_count"], 0)
        self.assertEqual(summary["TC-ADR07"]["terminal_counts"], {"completion_ready": 4, "unavailable": 1})


if __name__ == "__main__":
    unittest.main()
