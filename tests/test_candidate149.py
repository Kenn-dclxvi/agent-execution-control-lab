from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
FREE = ROOT / "prompts/candidates/the-caption-3ce91a4-control-free-repository-r1"
C149 = ROOT / "prompts/candidates/the-caption-3ce91a4-specification-start-boundary-r1"
PROFILE = ROOT / "evaluations/profiles/candidate149-specification-start-boundary-v14-reasoning-medium-a01-a02-global-m24-n5-cli0146-r1.json"
STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate149-specification-start-boundary-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


class Candidate149Test(unittest.TestCase):
    def test_free_child_changes_only_root_to_one_boundary(self) -> None:
        free = verify_bundle(FREE)
        candidate = verify_bundle(C149)
        self.assertEqual(candidate["artifact"]["baseline_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])

        free_files = {entry["target"]: entry for entry in free["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}
        self.assertEqual(set(candidate_files), set(free_files))
        changed = [target for target in sorted(free_files) if free_files[target] != candidate_files[target]]
        self.assertEqual(changed, ["AGENTS.md"])

        text = (C149 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        bullets = [line for line in text.splitlines() if line.startswith("- ")]
        self.assertEqual(len(bullets), 1)
        self.assertTrue(bullets[0].startswith("- SPECIFICATION / START:"))
        for boundary in (
            "required outcome value",
            "current value",
            "option set",
            "test expectation",
            "source / test調査",
            "implementation method",
        ):
            self.assertIn(boundary, bullets[0])

    def test_targeted_profile_is_a01_a02_n5_m24(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C149)
        self.assertEqual(
            [case["id"] for case in profile["cases"]],
            ["TC-A01-LATENT-MODE-POLICY", "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING"],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])

    def test_standard14_profile_matches_free_conditions(self) -> None:
        targeted = json.loads(PROFILE.read_text(encoding="utf-8"))
        standard14 = json.loads(STANDARD14_PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C149)
        self.assertEqual(len(standard14["cases"]), 14)
        self.assertEqual(standard14["iterations"], 5)
        self.assertEqual(standard14["execution"]["max_workers"], 24)
        self.assertEqual(standard14["comparison_conditions"], targeted["comparison_conditions"])
        self.assertEqual(standard14["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(standard14["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
