from __future__ import annotations

import hashlib
import json
import re
import unittest
from dataclasses import asdict
from pathlib import Path

from scripts.review_terminal_direction_probe import DirectionFacts, adjudicate


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evaluations/cases"
REVISION = "review-terminal-proof-obligation-r1"
CASE_IDS = [f"TC-TPO{index:02d}" for index in range(1, 7)]
DESIGN_ID = "review-terminal-proof-obligation-minimal-direction-r1"
EVAL_ID = "review-terminal-proof-obligation-targeted-evaluation-design-r1"
SET_ID = "the-caption-review-terminal-proof-obligation-direction-r1"


def root(case_id: str) -> Path:
    return CASES / case_id / REVISION


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def added_json(case_id: str, relative: str):
    patch = (root(case_id) / "private/seed.patch").read_text(encoding="utf-8")
    section = next(
        chunk
        for chunk in patch.split("diff --git ")
        if f"b/{relative}" in chunk
    )
    body = section.split("@@", 2)[2]
    payload = "\n".join(line[1:] for line in body.splitlines() if line.startswith("+")) + "\n"
    return json.loads(payload)


class ReviewTerminalProofObligationCasesTest(unittest.TestCase):
    def test_all_six_cases_bind_fixed_identities_and_seed_hashes(self) -> None:
        for case_id in CASE_IDS:
            private = load_json(root(case_id) / "private/case-data.json")
            self.assertEqual(private["case_id"], case_id)
            self.assertEqual(private["case_revision"], REVISION)
            self.assertEqual(private["oracle"]["general_design_identity"], DESIGN_ID)
            self.assertEqual(private["oracle"]["target_evaluation_design_identity"], EVAL_ID)
            self.assertEqual(private["oracle"]["set_identity"], SET_ID)
            patch = root(case_id) / "private/seed.patch"
            self.assertGreater(patch.stat().st_size, 0)
            self.assertEqual(
                hashlib.sha256(patch.read_bytes()).hexdigest(),
                private["seed"]["artifact"]["raw_sha256"],
            )
            fixture = added_json(case_id, "evaluation-fixture/review-terminal-direction.json")
            self.assertEqual(fixture["identity"]["case_identity"], f"{case_id}/{REVISION}")
            self.assertEqual(fixture["identity"]["general_design_identity"], DESIGN_ID)
            self.assertEqual(fixture["identity"]["target_evaluation_design_identity"], EVAL_ID)

    def test_private_oracle_matches_minimal_direction_probe(self) -> None:
        for case_id in CASE_IDS:
            private = load_json(root(case_id) / "private/case-data.json")
            fixture = added_json(case_id, "evaluation-fixture/review-terminal-direction.json")
            actual = asdict(adjudicate(DirectionFacts(**fixture["direction_facts"])))
            oracle = private["oracle"]
            expected = {
                "review_required": oracle["expected_review_required"],
                "review_started": oracle["expected_review_started"],
                "review_disposition": oracle["expected_review_disposition"],
                "artifact_change_allowed": oracle["expected_artifact_change_allowed"],
                "terminal": oracle["expected_terminal"],
                "reason": oracle["reason"],
            }
            self.assertEqual(actual, expected, case_id)

    def test_trial_inputs_do_not_leak_private_oracle_or_history(self) -> None:
        forbidden = (
            "expected_terminal",
            "expected_review_disposition",
            "expected_artifact_change_allowed",
            "private/oracle",
            "Candidate173",
            "Candidate185",
            "Candidate186",
            "qualification-contract-r",
        )
        for case_id in CASE_IDS:
            trial = (root(case_id) / "trial-prompt-input.json").read_text(encoding="utf-8")
            self.assertTrue(all(value not in trial for value in forbidden), case_id)
            self.assertNotRegex(trial, r"\bQ[1-6]\b")
            private = load_json(root(case_id) / "private/case-data.json")
            expected_seed = private["seed"]["fixture_materialization"]["commit"]["expected_commit"]
            self.assertIn(expected_seed, trial)
            self.assertRegex(expected_seed, r"^[0-9a-f]{40}$")

    def test_q3_and_q4_differ_on_closure_direction_and_evidence_existence(self) -> None:
        missing = added_json("TC-TPO03", "evaluation-fixture/review-terminal-direction.json")
        complete = added_json("TC-TPO04", "evaluation-fixture/review-terminal-direction.json")
        left = missing["direction_facts"]
        right = complete["direction_facts"]
        self.assertEqual({key for key in left if left[key] != right[key]}, {"closure_complete"})
        self.assertFalse(left["closure_complete"])
        self.assertTrue(right["closure_complete"])
        missing_patch = (root("TC-TPO03") / "private/seed.patch").read_text(encoding="utf-8")
        complete_patch = (root("TC-TPO04") / "private/seed.patch").read_text(encoding="utf-8")
        self.assertNotIn("b/evaluation-fixture/closure-evidence.json", missing_patch)
        self.assertIn("b/evaluation-fixture/closure-evidence.json", complete_patch)

    def test_q5_finite_authority_and_q6_permission_denial_are_direct(self) -> None:
        finite = added_json("TC-TPO05", "evaluation-fixture/review-terminal-direction.json")
        authority = finite["finite_authority"]
        self.assertTrue(finite["direction_facts"]["finite_direct_match"])
        self.assertEqual([effect["identity"] for effect in authority["effects"]], ["effect-a", "effect-b"])
        self.assertEqual(authority["additional_effects"], [])
        self.assertTrue(authority["relations"])

        denied = added_json("TC-TPO06", "evaluation-fixture/review-terminal-direction.json")
        self.assertEqual(denied["review_contract"]["permission"], "denied")
        self.assertNotEqual(
            denied["untrusted_prior_result"]["operation_identity"],
            denied["task_contract"]["operation_identity"],
        )
        private = load_json(root("TC-TPO06") / "private/case-data.json")
        self.assertEqual(private["mechanism_expectation"]["permission_denied_review_operations"], 0)
        self.assertEqual(private["mechanism_expectation"]["untrusted_prior_result_adoption"], 0)


if __name__ == "__main__":
    unittest.main()
