from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C141 = ROOT / "prompts/candidates/the-caption-3ce91a4-prechange-relation-coverage-r1"
C142 = ROOT / "prompts/candidates/the-caption-3ce91a4-initial-joint-effect-admission-r1"
PROFILE = ROOT / "evaluations/profiles/candidate142-initial-joint-effect-admission-v14-reasoning-medium-f02-f04-f07-global-m24-n5-cli0146-r1.json"


class Candidate142Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C141)
        candidate = verify_bundle(C142)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        source_gate = (C141 / "files/AGENTS.md.txt").read_text()
        candidate_gate = (C142 / "files/AGENTS.md.txt").read_text()
        self.assertNotIn("joint_owner_domain", source_gate)
        for term in (
            "joint_owner_domain",
            "single_change_target_ready=false",
            "全required effectのeffect_prechange_stateがsatisfiedまたはunsatisfiedへbind済み",
            "joint_owner_domain=true",
            "required_relation_evidence_scope",
            "effect_satisfaction_witness(effect)",
            "continuation_effect_change_ready",
        ):
            self.assertIn(term, candidate_gate)
        for term in ("F02", "F04", "App.tsx", "hasAuditKey", "colSpan"):
            self.assertNotIn(term, candidate_gate)
        profile = json.loads(PROFILE.read_text())
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(profile["prompt_set_identity"]["name"], candidate["prompt_identity"])


if __name__ == "__main__":
    unittest.main()
