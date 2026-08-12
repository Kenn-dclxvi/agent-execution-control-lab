from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "evaluations/results/2d8c2500cab64220ab1fe76b7e87adac.json"
QUALITY = ROOT / "evaluations/results/candidate190-current-prior-review-result-admission-adr9-r2-n5-audit-r1.json"
MECHANISM = ROOT / "evaluations/results/candidate190-current-prior-review-result-admission-adr9-r2-n5-mechanism-audit-r2.json"
RESULT_DOC = ROOT / "evaluations/results/candidate190-current-prior-review-result-admission-adr9-r2-n5_2026-08-12.md"


class Candidate190Adr9ResultTest(unittest.TestCase):
    def test_registered_result_is_compatible_six_case_score4_n5(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "2d8c2500cab64220ab1fe76b7e87adac")
        self.assertEqual(result["compatibility_key"], "d09c57a94101d4e2682efbf93a44a456a04e9378556859726d58af872edb6152")
        self.assertEqual(len(result["case_results"]), 30)
        self.assertEqual({item["quality_score"] for item in result["case_results"]}, {4})
        self.assertEqual(
            sorted({item["case_id"] for item in result["case_results"]}),
            ["TC-ADR03", "TC-ADR04", "TC-ADR05", "TC-ADR06", "TC-ADR07", "TC-ADR09"],
        )

    def test_quality_and_mechanism_gates_pass_without_prior_runtime_claim(self) -> None:
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(quality["quality_score_counts"], {"4": 30})
        self.assertTrue(quality["targeted_gate_passed"])
        self.assertTrue(mechanism["mechanism_gate_passed"])
        self.assertEqual(mechanism["current_result_admission_count"], 30)
        self.assertEqual(mechanism["terminal_match_count"], 30)
        self.assertEqual(mechanism["forbidden_canary_delivery_count"], 0)
        self.assertFalse(mechanism["prior_result_runtime_path_observed"])

    def test_result_document_preserves_scope_boundaries(self) -> None:
        text = RESULT_DOC.read_text(encoding="utf-8")
        for required in (
            "TPOを別系列へ追加していない",
            "prior result runtime経路",
            "Standard14",
            "文字列表現の完全一致を真正性の代用にしていない",
        ):
            self.assertIn(required, text)


if __name__ == "__main__":
    unittest.main()
