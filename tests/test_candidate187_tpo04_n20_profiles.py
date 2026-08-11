from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILES = ROOT / "evaluations/profiles"
REFERENCE = PROFILES / "candidate187-review-admission-proof-obligation-tpo04-reference-n5-medium-m24-cli0146.json"
EXPANDED = PROFILES / "candidate187-review-admission-proof-obligation-tpo04-n20-medium-m24-cli0146.json"
SOURCE = PROFILES / "candidate187-review-admission-proof-obligation-targeted-r1-medium-m24-n5-cli0146.json"
DESIGN = ROOT / "docs/candidate187-review-admission-proof-obligation-tpo04-n20-evaluation-design.md"
RESULT = ROOT / "evaluations/results/e5a454fa221048199bf5f08c35f0b3af.json"
AUDIT = ROOT / "evaluations/results/candidate187-review-admission-proof-obligation-tpo04-n20-audit.json"
RESULT_DOC = ROOT / "evaluations/results/candidate187-review-admission-proof-obligation-tpo04-n20_2026-08-12.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class Candidate187Tpo04N20ProfilesTest(unittest.TestCase):
    def test_reference_and_expanded_profiles_change_only_coverage(self) -> None:
        source = load(SOURCE)
        reference = load(REFERENCE)
        expanded = load(EXPANDED)

        expected_case = [{"id": "TC-TPO04", "revision": "review-terminal-proof-obligation-r1"}]
        self.assertEqual(reference["cases"], expected_case)
        self.assertEqual(expanded["cases"], expected_case)
        self.assertEqual(reference["iterations"], 5)
        self.assertEqual(expanded["iterations"], 20)
        self.assertEqual(reference["prompt_set_identity"], source["prompt_set_identity"])
        self.assertEqual(expanded["prompt_set_identity"], source["prompt_set_identity"])
        self.assertEqual(reference["comparison_conditions"], source["comparison_conditions"])
        expected_expanded_conditions = load(SOURCE)["comparison_conditions"]
        expected_expanded_conditions["repetition_condition"]["iterations"] = 20
        self.assertEqual(expanded["comparison_conditions"], expected_expanded_conditions)
        self.assertEqual(reference["execution"]["max_workers"], 24)
        self.assertEqual(expanded["execution"]["max_workers"], 24)

    def test_design_reuses_five_and_issues_only_fifteen(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        for required in (
            "既存5 atomic runを再利用",
            "不足15件だけを新規発行",
            "`TC-TPO04`だけ",
            "one-case pool",
            "20 / 20 valid、Score `4 = 20 / 20`",
            "誤経路が0 / 20件",
            "15 ready slotへ合わせて変更しない",
        ):
            self.assertIn(required, design)

    def test_registered_result_is_exactly_tpo04_n20_score_four(self) -> None:
        result = load(RESULT)
        self.assertEqual(result["result_id"], "e5a454fa221048199bf5f08c35f0b3af")
        self.assertEqual(result["compatibility"]["coverage"]["case_ids"], ["TC-TPO04"])
        self.assertEqual(result["compatibility"]["coverage"]["iterations"], list(range(1, 21)))
        self.assertEqual(len(result["case_results"]), 20)
        self.assertEqual(
            [(item["case_id"], item["iteration"], item["quality_score"]) for item in result["case_results"]],
            [("TC-TPO04", iteration, 4) for iteration in range(1, 21)],
        )
        self.assertEqual(result["excluded_attempts"], [])
        self.assertEqual(result["median"]["total_tokens"], 183382.0)
        self.assertAlmostEqual(result["median"]["elapsed_seconds"], 88.03827402050047)

    def test_cumulative_audit_closes_target_error_route(self) -> None:
        audit = load(AUDIT)
        self.assertEqual(audit["status"], "quality_passed_mechanism_passed")
        self.assertEqual(audit["run_count"], 20)
        self.assertEqual(audit["score_counts"], {"4": 20})
        self.assertEqual(audit["mechanism"]["reviewer_count_pass_count"], 20)
        self.assertEqual(audit["mechanism"]["review_disposition_pass_count"], 20)
        self.assertEqual(audit["mechanism"]["mechanism_failure_count"], 0)
        self.assertEqual(audit["mechanism"]["target_error_route_count"], 0)
        self.assertEqual(audit["gate"]["standard14_adoption"], "not_evaluated")

    def test_result_is_linked_from_reader_indexes(self) -> None:
        self.assertTrue(RESULT_DOC.is_file())
        self.assertIn(RESULT.name, (ROOT / "evaluations/results/README.md").read_text(encoding="utf-8"))
        self.assertIn(RESULT_DOC.name, (ROOT / "evaluations/profiles/README.md").read_text(encoding="utf-8"))
        self.assertIn(RESULT_DOC.name, (ROOT / "docs/README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
