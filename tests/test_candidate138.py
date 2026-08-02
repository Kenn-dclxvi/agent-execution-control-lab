from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C137 = ROOT / "prompts/candidates/the-caption-3ce91a4-pending-effect-validation-admission-r1"
C138 = ROOT / "prompts/candidates/the-caption-3ce91a4-continuation-effect-change-handoff-r1"
PROFILE = ROOT / "evaluations/profiles/candidate138-continuation-effect-change-handoff-v14-reasoning-medium-f04-global-m24-n5-cli0146-r1.json"
EXTENSION_PROFILE = ROOT / "evaluations/profiles/candidate138-continuation-effect-change-handoff-v14-reasoning-medium-f04-global-m24-n29-cli0146-r1.json"
GENERALITY_PROFILE = ROOT / "evaluations/profiles/candidate138-continuation-effect-change-handoff-v14-reasoning-medium-f02-f04-f07-global-m24-n5-cli0146-r1.json"


class Candidate138Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C137)
        candidate = verify_bundle(C138)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        source_gate = (C137 / "files/AGENTS.md.txt").read_text()
        candidate_gate = (C138 / "files/AGENTS.md.txt").read_text()
        self.assertNotIn("continuation_effect_change_ready", source_gate)
        for term in (
            "continuation_effect_change_ready",
            "initial_change_effect_setが非空",
            "観測済みcurrent contentだけへbind済み",
            "unobserved effectを充足済みとはbindせず",
            "pending_effect_validation_admitted(effect)",
            "required_effects_validation_ready",
        ):
            self.assertIn(term, candidate_gate)
        for term in ("F04", "App.tsx", "hasAuditKey", "colSpan"):
            self.assertNotIn(term, candidate_gate)
        profile = json.loads(PROFILE.read_text())
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])
        extension = json.loads(EXTENSION_PROFILE.read_text())
        self.assertEqual(extension["iterations"], 29)
        self.assertEqual(extension["comparison_conditions"]["repetition_condition"]["iterations"], 29)
        self.assertEqual(extension["execution"]["max_workers"], 24)
        self.assertEqual(extension["prompt_set_identity"], profile["prompt_set_identity"])
        generality = json.loads(GENERALITY_PROFILE.read_text())
        self.assertEqual(generality["iterations"], 5)
        self.assertEqual(
            [case["id"] for case in generality["cases"]],
            [
                "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND",
                "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY",
                "TC-F07-DEPENDENCY-PROVENANCE-PAIR",
            ],
        )
        self.assertEqual(generality["execution"]["max_workers"], 24)
        self.assertEqual(generality["prompt_set_identity"], profile["prompt_set_identity"])


if __name__ == "__main__":
    unittest.main()
