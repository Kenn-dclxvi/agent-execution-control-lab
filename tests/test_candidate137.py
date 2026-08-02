from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C136 = ROOT / "prompts/candidates/the-caption-3ce91a4-effect-local-change-admission-r1"
C137 = ROOT / "prompts/candidates/the-caption-3ce91a4-pending-effect-validation-admission-r1"
PROFILE = ROOT / "evaluations/profiles/candidate137-pending-effect-validation-admission-v14-reasoning-medium-f04-global-m24-n5-cli0146-r1.json"
EXTENSION_PROFILE = ROOT / "evaluations/profiles/candidate137-pending-effect-validation-admission-v14-reasoning-medium-f04-global-m24-n29-cli0146-r1.json"
SECOND_EXTENSION_PROFILE = ROOT / "evaluations/profiles/candidate137-pending-effect-validation-admission-v14-reasoning-medium-f04-global-m24-n53-cli0146-r1.json"


class Candidate137Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C136)
        candidate = verify_bundle(C137)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        gate = (C137 / "files/AGENTS.md.txt").read_text()
        for term in (
            "effect_prechange_state(effect)",
            "pending_effect_validation_admitted(effect)",
            "required_effects_validation_ready",
            "required_effects_closed",
            "TaskSpec-required validation",
            "direct result",
            "単なるtest / lint / build成功、diffまたはstatus",
        ):
            self.assertIn(term, gate)
        for term in ("F04", "App.tsx", "hasAuditKey", "colSpan"):
            self.assertNotIn(term, gate)
        profile = json.loads(PROFILE.read_text())
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])
        extension = json.loads(EXTENSION_PROFILE.read_text())
        self.assertEqual(extension["iterations"], 29)
        self.assertEqual(extension["comparison_conditions"]["repetition_condition"]["iterations"], 29)
        self.assertEqual(extension["execution"]["max_workers"], 24)
        self.assertEqual(extension["prompt_set_identity"], profile["prompt_set_identity"])
        second_extension = json.loads(SECOND_EXTENSION_PROFILE.read_text())
        self.assertEqual(second_extension["iterations"], 53)
        self.assertEqual(second_extension["comparison_conditions"]["repetition_condition"]["iterations"], 53)
        self.assertEqual(second_extension["execution"]["max_workers"], 24)
        self.assertEqual(second_extension["prompt_set_identity"], profile["prompt_set_identity"])


if __name__ == "__main__":
    unittest.main()
