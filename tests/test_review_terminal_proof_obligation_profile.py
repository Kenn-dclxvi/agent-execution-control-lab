from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = (
    ROOT
    / "evaluations/profiles/candidate173-review-terminal-proof-obligation-problem-qualification-r1-medium-m24-n5-cli0146.json"
)
RATING_PATH = ROOT / "evaluations/rating-contracts/outcome-terminal-state-evidence-owner-diagnostic-v14.json"
DESIGN_PATH = ROOT / "docs/review-terminal-proof-obligation-problem-qualification-execution-design.md"
CASE_IDS = [f"TC-TPO{index:02d}" for index in range(1, 7)]
REVISION = "review-terminal-proof-obligation-r1"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class ReviewTerminalProofObligationProfileTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = load_json(PROFILE_PATH)

    def test_profile_binds_the_six_case_problem_qualification(self) -> None:
        self.assertEqual(
            self.profile["profile_id"],
            "candidate173-review-terminal-proof-obligation-problem-qualification-r1-medium-m24-n5-cli0146",
        )
        self.assertEqual(
            self.profile["evaluation_set"],
            {
                "set_id": "the-caption-review-terminal-proof-obligation-direction-r1",
                "revision": REVISION,
            },
        )
        self.assertEqual(
            self.profile["cases"],
            [{"id": case_id, "revision": REVISION} for case_id in CASE_IDS],
        )
        self.assertEqual(self.profile["iterations"], 5)
        self.assertEqual(
            self.profile["comparison_conditions"]["task_spec"]["source"],
            "review-terminal-proof-obligation-problem-qualification-execution-design-r1",
        )

    def test_profile_reuses_candidate173_only_as_the_diagnostic_prompt(self) -> None:
        prompt = self.profile["prompt_set_identity"]
        self.assertEqual(prompt["name"], "the-caption-3ce91a4-concrete-counterexample-adjudication-r1")
        self.assertEqual(
            prompt["bundle_sha256"],
            "7c8b2cbff1c178e824ca2cac8b8a20b9afc0cab70d0964dd2eef8bc86790c85c",
        )
        scope = self.profile["scope"]
        self.assertEqual(scope["adoption"], "not_applicable")
        self.assertEqual(scope["release"], "not_applicable")
        self.assertEqual(scope["runtime_projection"], "not_authorized")

    def test_rating_runtime_permission_and_executor_match_fixed_values(self) -> None:
        conditions = self.profile["comparison_conditions"]
        rating = conditions["quality_rating"]
        self.assertEqual(rating["contract_id"], "outcome-terminal-state-evidence-owner-diagnostic-v14")
        actual_rating_sha = hashlib.sha256(RATING_PATH.read_bytes()).hexdigest()
        self.assertEqual(rating["contract_sha256"], actual_rating_sha)
        self.assertEqual(conditions["model"], "gpt-5.6-sol")
        self.assertEqual(conditions["agent_environment"]["codex_cli"], "0.146.0")
        self.assertEqual(
            conditions["agent_environment"]["runtime_identity_sha256"],
            "61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73",
        )
        self.assertEqual(conditions["permission"], {"approval_policy": "never", "sandbox": "workspace-write"})
        executor = conditions["executor_parameters"]
        self.assertEqual(executor["reasoning_effort"], "medium")
        self.assertEqual(executor["max_workers"], 24)
        self.assertEqual(executor["max_attempts"], 3)
        self.assertEqual(executor["environment_adjustment"], "none")
        self.assertEqual(executor["token_accounting"]["scope"], "all_agents")

    def test_no_unstated_exact_command_is_promoted_to_quality_requirement(self) -> None:
        groups = self.profile["comparison_conditions"]["executor_parameters"]["command_evidence_protocol"]
        self.assertEqual(groups["required_command_groups_by_case"], {case_id: [] for case_id in CASE_IDS})

    def test_design_fixes_direction_threshold_and_direct_c147_base(self) -> None:
        design = DESIGN_PATH.read_text(encoding="utf-8")
        self.assertIn("同一ケースで2 / 5以上", design)
        self.assertIn("30 valid run", design)
        self.assertIn("既存ADR9 resultからatomic poolをseedせず", design)
        self.assertIn("C147を直接基盤", design)
        self.assertIn("Candidate173は既存ADR9 r2で45 / 45", design)
        self.assertIn("`measurement_incomplete`", design)
        self.assertIn("runを一件も発行しない", design)


if __name__ == "__main__":
    unittest.main()
