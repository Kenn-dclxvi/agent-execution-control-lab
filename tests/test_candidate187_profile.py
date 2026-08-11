from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "evaluations/profiles/candidate187-review-admission-proof-obligation-targeted-r1-medium-m24-n5-cli0146.json"
RATING_PATH = ROOT / "evaluations/rating-contracts/outcome-terminal-state-evidence-owner-diagnostic-v14.json"
CANDIDATE_PATH = ROOT / "prompts/candidates/the-caption-3ce91a4-review-admission-proof-obligation-r1"
DESIGN_PATH = ROOT / "docs/candidate187-review-admission-proof-obligation-targeted-evaluation-design.md"
CASE_IDS = [f"TC-TPO{index:02d}" for index in range(1, 7)]
REVISION = "review-terminal-proof-obligation-r1"


class Candidate187ProfileTest(unittest.TestCase):
    def setUp(self) -> None:
        self.profile = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))

    def test_profile_binds_candidate_and_six_case_target_gate(self) -> None:
        candidate = verify_bundle(CANDIDATE_PATH)
        self.assertEqual(
            self.profile["profile_id"],
            "candidate187-review-admission-proof-obligation-targeted-r1-medium-m24-n5-cli0146",
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
        prompt = self.profile["prompt_set_identity"]
        self.assertEqual(prompt["name"], candidate["prompt_identity"])
        self.assertEqual(prompt["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(
            self.profile["comparison_conditions"]["task_spec"]["source"],
            "review-terminal-proof-obligation-problem-qualification-execution-design-r1",
        )

    def test_runtime_rating_and_permissions_remain_fixed(self) -> None:
        conditions = self.profile["comparison_conditions"]
        rating = conditions["quality_rating"]
        self.assertEqual(
            rating["contract_sha256"],
            hashlib.sha256(RATING_PATH.read_bytes()).hexdigest(),
        )
        self.assertEqual(rating["owner_producer_evidence_policy"], "diagnostic_only")
        self.assertEqual(conditions["model"], "gpt-5.6-sol")
        self.assertEqual(conditions["agent_environment"]["codex_cli"], "0.146.0")
        self.assertEqual(
            conditions["permission"],
            {"approval_policy": "never", "sandbox": "workspace-write"},
        )
        executor = conditions["executor_parameters"]
        self.assertEqual(executor["reasoning_effort"], "medium")
        self.assertEqual(executor["max_workers"], 24)
        self.assertEqual(executor["max_attempts"], 3)
        self.assertEqual(executor["environment_adjustment"], "none")

    def test_design_keeps_candidate_only_quality_and_mechanism_gate(self) -> None:
        design = DESIGN_PATH.read_text(encoding="utf-8")
        for required in (
            "比較相手の新規runは発行せず",
            "Score `4 = 30 / 30`",
            "`TC-TPO01`〜`TC-TPO04`は各runで独立reviewerを一件",
            "`TC-TPO05`と`TC-TPO06`はreview operation一式を0件",
            "同一誤経路が一件でも",
            "runを一件も発行しない",
        ):
            self.assertIn(required, design)


if __name__ == "__main__":
    unittest.main()
