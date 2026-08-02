from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C128 = ROOT / "prompts/candidates/the-caption-3ce91a4-required-effect-closure-r1"
C135 = ROOT / "prompts/candidates/the-caption-3ce91a4-criterion-span-request-authority-r1"
PROFILE = ROOT / "evaluations/profiles/candidate135-criterion-span-request-authority-v14-reasoning-medium-f04-global-m24-n5-cli0146-r1.json"

class Candidate135Test(unittest.TestCase):
    def test_single_axis_and_profile(self) -> None:
        source = verify_bundle(C128)
        candidate = verify_bundle(C135)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        gate = (C135 / "files/AGENTS.md.txt").read_text()
        for term in ("criterion_span", "task_kind_goal_and_done_condition", "criterion_request_lexeme_set", "他fieldのallowed path", "reference identifierのdefinitionを別memberとして展開せず"):
            self.assertIn(term, gate)
        for term in ("F04", "App.tsx", "hasAuditKey", "colSpan"):
            self.assertNotIn(term, gate)
        profile = json.loads(PROFILE.read_text())
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])

if __name__ == "__main__":
    unittest.main()
