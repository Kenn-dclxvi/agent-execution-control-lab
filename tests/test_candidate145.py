from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C144 = ROOT / "prompts/candidates/the-caption-3ce91a4-required-outcome-validation-method-boundary-r1"
C145 = ROOT / "prompts/candidates/the-caption-3ce91a4-lifecycle-consumer-evidence-admission-r1"
PROFILE = ROOT / "evaluations/profiles/candidate145-lifecycle-consumer-evidence-admission-v14-reasoning-medium-a01-a02-f01-f02-f04-f07-global-m24-n5-cli0146-r1.json"
STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate145-lifecycle-consumer-evidence-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


class Candidate145Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C144)
        candidate = verify_bundle(C145)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        source_text = (C144 / "files/AGENTS.md.txt").read_text()
        candidate_text = (C145 / "files/AGENTS.md.txt").read_text()
        for term in (
            "implementation_bound :=",
            "validation_predicate_ready :=",
            "exact commandを明示したvalidationだけそのcommandがbind済み",
        ):
            self.assertIn(term, source_text)
            self.assertIn(term, candidate_text)
        for term in (
            "required_predicate_state := satisfied | unsatisfied | unobserved",
            "evidence_consumer_ready :=",
            "repository evidence invocationは全lifecycleでdefault deny",
            "exact command / test locator / 既存test symbol / 一般的repository慣行が未固定なだけでは",
            "consumerがterminalになれば未発行evidenceを失効",
        ):
            self.assertIn(term, candidate_text)
            self.assertNotIn(term, source_text)
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
        standard14 = json.loads(STANDARD14_PROFILE.read_text())
        self.assertEqual(standard14["iterations"], 5)
        self.assertEqual(standard14["execution"]["max_workers"], 24)
        self.assertEqual(len(standard14["cases"]), 14)
        self.assertEqual(standard14["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(standard14["prompt_set_identity"]["name"], candidate["prompt_identity"])


if __name__ == "__main__":
    unittest.main()
