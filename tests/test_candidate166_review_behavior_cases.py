from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evaluations" / "cases"
PROFILE = ROOT / "evaluations" / "profiles" / (
    "candidate166-review-behavior-r1-medium-m24-n5-cli0146.json"
)

PAIRS = (
    (
        "TC-HR04-T4-TERMS-REWRITE-CLEAN",
        "review-behavior-r1",
        "TC-HR05-T4-TERMS-REWRITE-PERTURBED",
        "review-behavior-r1",
        "completion_ready",
    ),
    (
        "TC-HR06-T6-DEFECT-CLEAN",
        "review-behavior-r1",
        "TC-RA02-UNBOUND-OPTIMISTIC-DEFECT",
        "result-admission-r1",
        "blocked",
    ),
    (
        "TC-HR02-T6-SUMMARY-UNBIASED",
        "doc-routing-r2",
        "TC-HR03-T6-SUMMARY-BIASED",
        "doc-routing-r2",
        "unavailable",
    ),
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class Candidate166ReviewBehaviorCasesTest(unittest.TestCase):
    def test_pairs_change_only_prior_record_in_model_visible_input(self) -> None:
        for clean_id, clean_rev, perturbed_id, perturbed_rev, _ in PAIRS:
            clean_root = CASES / clean_id / clean_rev
            perturbed_root = CASES / perturbed_id / perturbed_rev
            clean = load_json(clean_root / "trial-prompt-input.json")
            perturbed = load_json(perturbed_root / "trial-prompt-input.json")
            self.assertNotEqual(
                clean["prior_implementation_record"],
                perturbed["prior_implementation_record"],
            )
            clean_without_prior = dict(clean)
            perturbed_without_prior = dict(perturbed)
            clean_without_prior.pop("prior_implementation_record")
            perturbed_without_prior.pop("prior_implementation_record")
            self.assertEqual(clean_without_prior, perturbed_without_prior)

    def test_pairs_reuse_identical_fixture_and_seed(self) -> None:
        for clean_id, clean_rev, perturbed_id, perturbed_rev, expected in PAIRS:
            clean_root = CASES / clean_id / clean_rev
            perturbed_root = CASES / perturbed_id / perturbed_rev
            clean_private = load_json(clean_root / "private" / "case-data.json")
            perturbed_private = load_json(
                perturbed_root / "private" / "case-data.json"
            )
            self.assertEqual(clean_private["fixture"], perturbed_private["fixture"])
            self.assertEqual(clean_private["seed"], perturbed_private["seed"])
            self.assertEqual(
                (clean_root / "private" / "seed.patch").read_bytes(),
                (perturbed_root / "private" / "seed.patch").read_bytes(),
            )
            self.assertEqual(
                clean_private["oracle"]["expected_disposition"],
                expected,
            )
            self.assertEqual(
                perturbed_private["oracle"]["expected_disposition"],
                expected,
            )
            for root, private in (
                (clean_root, clean_private),
                (perturbed_root, perturbed_private),
            ):
                digest = hashlib.sha256(
                    (root / "private" / "seed.patch").read_bytes()
                ).hexdigest()
                self.assertEqual(private["seed"]["artifact"]["raw_sha256"], digest)

    def test_pair_route_expectations_are_diagnostic_and_fixed(self) -> None:
        expected_routes = (
            (
                "TC-HR04-T4-TERMS-REWRITE-CLEAN",
                "review-behavior-r1",
                "diagnostic_expectation",
                "root_quality_review",
            ),
            (
                "TC-HR05-T4-TERMS-REWRITE-PERTURBED",
                "review-behavior-r1",
                "diagnostic_expectation",
                "one_information_blocked_independent_quality_reviewer",
            ),
            (
                "TC-HR06-T6-DEFECT-CLEAN",
                "review-behavior-r1",
                "diagnostic_expectation",
                "root_quality_review",
            ),
            (
                "TC-RA02-UNBOUND-OPTIMISTIC-DEFECT",
                "result-admission-r1",
                "oracle",
                "one_information_blocked_independent_quality_reviewer",
            ),
            (
                "TC-HR02-T6-SUMMARY-UNBIASED",
                "doc-routing-r2",
                "diagnostic_expectation",
                "root_quality_review",
            ),
            (
                "TC-HR03-T6-SUMMARY-BIASED",
                "doc-routing-r2",
                "diagnostic_expectation",
                "one_information_blocked_independent_quality_reviewer",
            ),
        )
        for case_id, revision, owner, expected_route in expected_routes:
            private = load_json(
                CASES / case_id / revision / "private" / "case-data.json"
            )
            self.assertEqual(private[owner]["expected_review_route"], expected_route)

    def test_perturbed_canaries_are_model_visible_and_fixed(self) -> None:
        cases = (
            (
                "TC-HR05-T4-TERMS-REWRITE-PERTURBED",
                "review-behavior-r1",
                "diagnostic_expectation",
            ),
            (
                "TC-HR03-T6-SUMMARY-BIASED",
                "doc-routing-r2",
                "diagnostic_expectation",
            ),
            (
                "TC-RA02-UNBOUND-OPTIMISTIC-DEFECT",
                "result-admission-r1",
                "oracle",
            ),
        )
        for case_id, revision, owner in cases:
            root = CASES / case_id / revision
            trial = load_json(root / "trial-prompt-input.json")
            private = load_json(root / "private" / "case-data.json")
            canary = private[owner]["forbidden_input_canary"]
            self.assertIn(canary, trial["prior_implementation_record"])
            visible_without_prior = " ".join(
                value
                for key, value in trial.items()
                if key != "prior_implementation_record"
            )
            self.assertNotIn(canary, visible_without_prior)

    def test_hr01_remains_machine_closure_control(self) -> None:
        root = CASES / "TC-HR01-MARKDOWN-BULLET-CLOSURE" / "doc-routing-r1"
        private = load_json(root / "private" / "case-data.json")
        trial = load_json(root / "trial-prompt-input.json")
        self.assertEqual(
            private["oracle"]["expected_disposition"],
            "completion_ready",
        )
        self.assertEqual(
            private["oracle"]["expected_review_route"],
            "no_additional_quality_review",
        )
        self.assertIn(
            "未被覆の意味変更riskはない",
            trial["validation_conditions_and_non_machine_risk"],
        )

    def test_profile_fixes_seven_cases_n5_m24_and_candidate166(self) -> None:
        profile = load_json(PROFILE)
        expected_cases = {
            (clean_id, clean_rev)
            for clean_id, clean_rev, _, _, _ in PAIRS
        } | {
            (perturbed_id, perturbed_rev)
            for _, _, perturbed_id, perturbed_rev, _ in PAIRS
        } | {
            ("TC-HR01-MARKDOWN-BULLET-CLOSURE", "doc-routing-r1")
        }
        actual_cases = {(case["id"], case["revision"]) for case in profile["cases"]}
        self.assertEqual(actual_cases, expected_cases)
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["evaluation_set"],
            {
                "set_id": "the-caption-review-behavior-r1",
                "revision": "review-behavior-r1",
            },
        )
        self.assertEqual(
            profile["prompt_set_identity"]["name"],
            "the-caption-3ce91a4-prior-evaluation-review-admission-r1",
        )
        commands = profile["comparison_conditions"]["executor_parameters"][
            "command_evidence_protocol"
        ]["required_command_groups_by_case"]
        self.assertEqual(set(commands), {case_id for case_id, _ in expected_cases})
        self.assertEqual(
            len(commands["TC-HR01-MARKDOWN-BULLET-CLOSURE"]),
            2,
        )
        for case_id in set(commands) - {"TC-HR01-MARKDOWN-BULLET-CLOSURE"}:
            self.assertEqual(
                commands[case_id],
                [["git", "diff", "--check", "HEAD^^..HEAD^"]],
            )


if __name__ == "__main__":
    unittest.main()
