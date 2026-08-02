from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C135 = ROOT / "prompts/candidates/the-caption-3ce91a4-criterion-span-request-authority-r1"
C136 = ROOT / "prompts/candidates/the-caption-3ce91a4-effect-local-change-admission-r1"
PROFILE = ROOT / "evaluations/profiles/candidate136-effect-local-change-admission-v14-reasoning-medium-f04-global-m24-n5-cli0146-r1.json"


class Candidate136Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C135)
        candidate = verify_bundle(C136)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        gate = (C136 / "files/AGENTS.md.txt").read_text()
        for term in (
            "criterion_span",
            "effect_prechange_state(effect)",
            "satisfied",
            "unsatisfied",
            "unobserved",
            "initial_change_effect_set",
            "別のunsatisfied effectの変更開始拒否にも使わない",
            "required_effects_closed",
        ):
            self.assertIn(term, gate)
        for term in ("F04", "App.tsx", "hasAuditKey", "colSpan"):
            self.assertNotIn(term, gate)
        profile = json.loads(PROFILE.read_text())
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
