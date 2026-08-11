from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "evaluations/profiles/candidate187-review-admission-proof-obligation-adr9-r2-medium-m24-n5-cli0146.json"
REFERENCE = ROOT / "evaluations/profiles/candidate186-review-decision-record-totality-adr9-r2-medium-m24-n5-cli0146.json"
DESIGN = ROOT / "docs/candidate187-review-admission-proof-obligation-adr9-r2-n5-evaluation-design.md"
RESULT = ROOT / "evaluations/results/c6434276d81b437b9331fb0202aaa34d.json"
REFERENCE_RESULT = ROOT / "evaluations/results/c05a481ec7d24be691649b2135aecbe4.json"
AUDIT = ROOT / "evaluations/results/candidate187-review-admission-proof-obligation-adr9-r2-subset-n5-audit-r1.json"
RESULT_DOC = ROOT / "evaluations/results/candidate187-review-admission-proof-obligation-adr9-r2-subset-n5_2026-08-12.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class Candidate187Adr9ProfileTest(unittest.TestCase):
    def test_subset_keeps_compatible_reference_conditions(self) -> None:
        profile = load(PROFILE)
        reference = load(REFERENCE)
        self.assertEqual(profile["evaluation_set"], reference["evaluation_set"])
        self.assertEqual(
            [item["id"] for item in profile["cases"]],
            ["TC-ADR01", "TC-ADR02", "TC-ADR05", "TC-ADR07", "TC-ADR08", "TC-ADR09"],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["comparison_conditions"], reference["comparison_conditions"])
        self.assertEqual(profile["execution"], reference["execution"])
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-review-admission-proof-obligation-r1",
                "revision": "r1",
                "bundle_sha256": "189a7a11615511a3341646e24ecbffb61bb278fc6652c2db492648515d797fbd",
            },
        )

    def test_design_issues_only_candidate187_thirty(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        for required in (
            "比較相手は新規実行しない",
            "Candidate187のADR9 atomic runは0件",
            "30件だけを発行",
            "30 / 30 validかつScore 4",
            "Standard14",
        ):
            self.assertIn(required, design)

    def test_registered_result_keeps_subset_compatibility(self) -> None:
        result = load(RESULT)
        reference_result = load(REFERENCE_RESULT)
        self.assertEqual(result["result_id"], "c6434276d81b437b9331fb0202aaa34d")
        self.assertEqual(
            result["compatibility_key"],
            "2924c0c9e86ee6288530499ea1d055f7c6d6ce785110387f3d853ef7d2c3d572",
        )
        self.assertEqual(result["compatibility_key"], reference_result["compatibility_key"])
        self.assertEqual(len(reference_result["case_results"]), 30)
        self.assertEqual(result["source_selection"]["selection_id"], "8b00da5906c04e219d3f0b304967baaf")
        self.assertEqual(len(result["case_results"]), 30)
        self.assertEqual({item["case_id"] for item in result["case_results"]}, {
            "TC-ADR01", "TC-ADR02", "TC-ADR05", "TC-ADR07", "TC-ADR08", "TC-ADR09",
        })

    def test_failed_gate_is_preserved_without_rerun(self) -> None:
        audit = load(AUDIT)
        self.assertEqual(audit["valid_run_count"], 30)
        self.assertEqual(audit["excluded_attempt_count"], 0)
        self.assertEqual(audit["quality_score_counts"], {"1": 12, "4": 18})
        self.assertEqual(audit["mechanism_failure_count"], 12)
        self.assertFalse(audit["targeted_gate_passed"])
        self.assertEqual(audit["status"], "quality_failed_mechanism_failed_stopped")
        result_doc = RESULT_DOC.read_text(encoding="utf-8")
        self.assertIn("失敗した12件は適格な観測結果として保持し、再実行しない", result_doc)
        self.assertIn("Standard14へ進めない", result_doc)


if __name__ == "__main__":
    unittest.main()
