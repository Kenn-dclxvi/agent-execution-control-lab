from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C143 = ROOT / "prompts/candidates/the-caption-3ce91a4-required-outcome-implementation-bind-r1"
C144 = ROOT / "prompts/candidates/the-caption-3ce91a4-required-outcome-validation-method-boundary-r1"
PROFILE = ROOT / "evaluations/profiles/candidate144-required-outcome-validation-method-boundary-v14-reasoning-medium-a01-a02-f01-f02-f04-f07-global-m24-n5-cli0146-r1.json"


class Candidate144Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C143)
        candidate = verify_bundle(C144)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        source_text = (C143 / "files/AGENTS.md.txt").read_text()
        candidate_text = (C144 / "files/AGENTS.md.txt").read_text()
        self.assertIn("implementation_bound :=", source_text)
        self.assertIn("implementation_bound :=", candidate_text)
        self.assertIn("validation_set_ready :=", source_text)
        self.assertNotIn("validation_set_ready :=", candidate_text)
        for term in (
            "validation_predicate_ready :=",
            "exact commandを明示したvalidationだけそのcommandがbind済み",
            "missing validation identityまたはrepository evidenceの開放条件にせず",
            "exact commandの選択だけを理由にrepository evidenceを追加しない",
        ):
            self.assertIn(term, candidate_text)
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
            self.assertNotIn(term, candidate_text)
        profile = json.loads(PROFILE.read_text())
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(len(profile["cases"]), 6)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(profile["prompt_set_identity"]["name"], candidate["prompt_identity"])


if __name__ == "__main__":
    unittest.main()
