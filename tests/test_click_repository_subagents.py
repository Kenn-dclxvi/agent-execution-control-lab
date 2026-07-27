from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import bundle_sha256, verify_bundle


ROOT = Path(__file__).resolve().parents[1]
CLICK = ROOT / "evaluations/targets/click"
NO_AGENTS = CLICK / "prompts/baselines/click-00e592c-no-agents-r1"
SUBAGENTS = CLICK / "prompts/candidates/click-00e592c-repository-subagents-r1"
NO_AGENTS_PROFILE = (
    CLICK / "profiles/click-no-agents-reasoning-medium-standard14-global-m24-n5-r1.json"
)
SUBAGENTS_PROFILE = (
    CLICK
    / "profiles/click-repository-subagents-reasoning-medium-standard14-global-m24-n5-r1.json"
)
RESULT = (
    CLICK
    / "results/click-no-agents-repository-subagents-reasoning-medium-standard14-n5_2026-07-27.md"
)


class ClickRepositorySubagentsTest(unittest.TestCase):
    def test_no_agents_bundle_is_a_true_empty_identity(self) -> None:
        manifest = verify_bundle(NO_AGENTS)
        self.assertEqual(manifest["prompt_identity"], "click-00e592c-no-agents-r1")
        self.assertEqual(manifest["files"], [])
        self.assertEqual(manifest["bundle_sha256"], bundle_sha256([]))

    def test_subagents_bundle_has_only_existing_click_scopes(self) -> None:
        manifest = verify_bundle(SUBAGENTS)
        self.assertEqual(
            [entry["target"] for entry in manifest["files"]],
            ["docs/AGENTS.md", "src/AGENTS.md", "tests/AGENTS.md"],
        )
        self.assertNotIn("AGENTS.md", [entry["target"] for entry in manifest["files"]])
        self.assertNotIn("scripts/AGENTS.md", [entry["target"] for entry in manifest["files"]])
        self.assertEqual(
            manifest["artifact"]["baseline_identity"], "click-00e592c-no-agents-r1"
        )

    def test_subagents_content_is_click_specific(self) -> None:
        src = (SUBAGENTS / "files/src/AGENTS.md.txt").read_text(encoding="utf-8")
        tests = (SUBAGENTS / "files/tests/AGENTS.md.txt").read_text(encoding="utf-8")
        docs = (SUBAGENTS / "files/docs/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertIn("`src/click/`", src)
        self.assertIn("`tests/typing/`", tests)
        self.assertIn("`CliRunner.invoke`", tests)
        self.assertIn("MyST", docs)
        self.assertIn("80 characters", docs)

    def test_medium_profiles_differ_only_by_prompt_identity(self) -> None:
        no_agents = json.loads(NO_AGENTS_PROFILE.read_text(encoding="utf-8"))
        subagents = json.loads(SUBAGENTS_PROFILE.read_text(encoding="utf-8"))
        for profile, bundle in ((no_agents, NO_AGENTS), (subagents, SUBAGENTS)):
            manifest = verify_bundle(bundle)
            self.assertEqual(
                profile["prompt_set_identity"],
                {
                    "bundle_sha256": manifest["bundle_sha256"],
                    "name": manifest["prompt_identity"],
                    "revision": "r1",
                },
            )
            self.assertEqual(
                profile["comparison_conditions"]["executor_parameters"]["reasoning_effort"],
                "medium",
            )
        comparable_no_agents = copy.deepcopy(no_agents)
        comparable_subagents = copy.deepcopy(subagents)
        for value in (comparable_no_agents, comparable_subagents):
            value.pop("profile_id")
            value.pop("prompt_set_identity")
        self.assertEqual(comparable_no_agents, comparable_subagents)

    def test_result_records_completed_comparison_and_exposure_boundary(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        self.assertIn("c8c1092f445f4c8ca67bd1fbe409e999", result)
        self.assertIn("00194b3331524a0c8b0e4895e6885aa9", result)
        self.assertIn("+3.74%", result)
        self.assertIn("+7.90%", result)
        self.assertIn("初期contextへ入ったrunは`0 / 70`", result)
        self.assertIn("A01の5 / 5件", result)
        self.assertIn("本文のStd14全体効果", result)


if __name__ == "__main__":
    unittest.main()
