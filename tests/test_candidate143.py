from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C118 = ROOT / "prompts/candidates/the-caption-3ce91a4-implementation-bind-terminal-closure-r1"
C143 = ROOT / "prompts/candidates/the-caption-3ce91a4-required-outcome-implementation-bind-r1"
PROFILE = ROOT / "evaluations/profiles/candidate143-required-outcome-implementation-bind-v14-reasoning-medium-f02-f04-f07-global-m24-n5-cli0146-r1.json"
STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate143-required-outcome-implementation-bind-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


class Candidate143Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C118)
        candidate = verify_bundle(C143)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        source_gate = (C118 / "files/AGENTS.md.txt").read_text()
        candidate_gate = (C143 / "files/AGENTS.md.txt").read_text()
        old = "許可済みresultから`target artifact / targetへ適用中のrepository instruction / 実行可能な変更predicate / 保持するconstraint`がbindされartifact変更を発行できる時点"
        self.assertIn(old, source_gate)
        self.assertNotIn(old, candidate_gate)
        for term in (
            "implementation_bound :=",
            "TaskSpecがrequired outcomeに明示した全change effectとartifact間relation",
            "一つのimplementation choiceへbind済み",
            "implementation_bound=true",
        ):
            self.assertIn(term, candidate_gate)
        for term in (
            "prechange_evidence_wave_ready",
            "single_change_target_ready",
            "effect_prechange_state",
            "joint_owner_domain",
            "F02",
            "F04",
            "App.tsx",
            "colSpan",
        ):
            self.assertNotIn(term, candidate_gate)
        profile = json.loads(PROFILE.read_text())
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(profile["prompt_set_identity"]["name"], candidate["prompt_identity"])
        standard14 = json.loads(STANDARD14_PROFILE.read_text())
        self.assertEqual(standard14["iterations"], 5)
        self.assertEqual(len(standard14["cases"]), 14)
        self.assertEqual(standard14["execution"]["max_workers"], 24)
        self.assertEqual(standard14["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(standard14["prompt_set_identity"]["name"], candidate["prompt_identity"])


if __name__ == "__main__":
    unittest.main()
