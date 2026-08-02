from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C138 = ROOT / "prompts/candidates/the-caption-3ce91a4-continuation-effect-change-handoff-r1"
C139 = ROOT / "prompts/candidates/the-caption-3ce91a4-single-target-continuation-handoff-r1"
PROFILE = ROOT / "evaluations/profiles/candidate139-single-target-continuation-handoff-v14-reasoning-medium-f02-f04-f07-global-m24-n5-cli0146-r1.json"


class Candidate139Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C138)
        candidate = verify_bundle(C139)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        source_gate = (C138 / "files/AGENTS.md.txt").read_text()
        candidate_gate = (C139 / "files/AGENTS.md.txt").read_text()
        old = "continuation_effect_change_ready := continuation result受領済み"
        new = "continuation_effect_change_ready := single_change_target_ready ∧ continuation result受領済み"
        self.assertIn(old, source_gate)
        self.assertNotIn(new, source_gate)
        self.assertIn(new, candidate_gate)
        for term in ("pending_effect_validation_admitted(effect)", "required_effects_validation_ready"):
            self.assertIn(term, candidate_gate)
        for term in ("F02", "F04", "App.tsx", "hasAuditKey", "colSpan"):
            self.assertNotIn(term, candidate_gate)
        profile = json.loads(PROFILE.read_text())
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
