from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "evaluations/profiles"
RESULTS = ROOT / "evaluations/results"
REFERENCE = PROFILES / "candidate190-current-prior-review-result-admission-adr05-adr07-adr09-reference-n5-medium-m24-cli0146.json"
EXPANDED = PROFILES / "candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-medium-m24-cli0146.json"
RESULT = RESULTS / "d3b75f599f024ab8802595311920a00e.json"
QUALITY = RESULTS / "candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-audit-r1.json"
MECHANISM = RESULTS / "candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20-mechanism-audit-r1.json"
RESULT_DOC = RESULTS / "candidate190-current-prior-review-result-admission-adr05-adr07-adr09-n20_2026-08-12.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class Candidate190M6ResultTest(unittest.TestCase):
    def test_reference_and_expanded_profiles_change_only_coverage(self) -> None:
        reference = load(REFERENCE)
        expanded = load(EXPANDED)
        expected_cases = [
            {"id": case_id, "revision": "adversarial-design-review-r2"}
            for case_id in ("TC-ADR05", "TC-ADR07", "TC-ADR09")
        ]
        self.assertEqual(reference["cases"], expected_cases)
        self.assertEqual(expanded["cases"], expected_cases)
        self.assertEqual(reference["iterations"], 5)
        self.assertEqual(expanded["iterations"], 20)
        self.assertEqual(reference["prompt_set_identity"], expanded["prompt_set_identity"])
        reference_conditions = reference["comparison_conditions"]
        expanded_conditions = expanded["comparison_conditions"]
        reference_conditions["repetition_condition"]["iterations"] = 20
        self.assertEqual(reference_conditions, expanded_conditions)
        self.assertEqual(reference["execution"]["max_workers"], 24)
        self.assertEqual(expanded["execution"]["max_workers"], 24)

    def test_registered_result_is_three_cases_n20_score_four(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["result_id"], "d3b75f599f024ab8802595311920a00e")
        self.assertEqual(
            result["compatibility"]["coverage"],
            {
                "case_ids": ["TC-ADR05", "TC-ADR07", "TC-ADR09"],
                "iterations": list(range(1, 21)),
            },
        )
        self.assertEqual(len(result["case_results"]), 60)
        self.assertEqual({item["quality_score"] for item in result["case_results"]}, {4})
        self.assertEqual(result["excluded_attempts"], [])

    def test_cumulative_quality_and_mechanism_gates_pass(self) -> None:
        quality = load(QUALITY)
        mechanism = load(MECHANISM)
        self.assertEqual(quality["status"], "quality_passed")
        self.assertEqual(quality["valid_run_count"], 60)
        self.assertEqual(quality["quality_score_counts"], {"4": 60})
        self.assertEqual(quality["reused_run_count"], 15)
        self.assertEqual(quality["new_run_count"], 45)
        self.assertEqual(mechanism["status"], "mechanism_passed")
        self.assertEqual(mechanism["result_kind_counts"], {
            "counterexample_found": 20,
            "no_counterexample_found": 20,
            "unavailable": 20,
        })
        self.assertEqual(mechanism["current_result_admission_count"], 60)
        self.assertEqual(mechanism["terminal_match_count"], 60)
        self.assertEqual(mechanism["artifact_boundary_match_count"], 60)
        self.assertTrue(mechanism["mechanism_gate_passed"])

    def test_result_and_plan_keep_scope_boundaries(self) -> None:
        text = RESULT_DOC.read_text(encoding="utf-8")
        self.assertIn("不足各15件、合計45件だけ", text)
        self.assertIn("TPOを別比較系列として増やしていない", (ROOT / "docs/review-control-reconstruction-milestone-plan.md").read_text(encoding="utf-8"))
        self.assertIn("prior result runtime経路は未観測", text)
        self.assertIn("Standard14_not_started", text)
        self.assertIn(RESULT_DOC.name, (RESULTS / "README.md").read_text(encoding="utf-8"))
        self.assertIn(RESULT_DOC.name, (ROOT / "docs/README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
