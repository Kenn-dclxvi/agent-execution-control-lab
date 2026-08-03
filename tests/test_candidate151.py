from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
C150 = ROOT / "prompts/candidates/the-caption-3ce91a4-required-outcome-bind-readable-r1"
C151 = ROOT / "prompts/candidates/the-caption-3ce91a4-evidence-consumer-boundary-readable-r1"
PROFILE = ROOT / "evaluations/profiles/candidate151-evidence-consumer-boundary-readable-v14-reasoning-medium-a01-a02-f01-f02-f04-f07-global-m24-n5-cli0146-r1.json"


class Candidate151Test(unittest.TestCase):
    def test_direct_child_adds_one_behavior_boundary(self) -> None:
        source = verify_bundle(C150)
        candidate = verify_bundle(C151)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        source_text = (C150 / "files/AGENTS.md.txt").read_text()
        candidate_text = (C151 / "files/AGENTS.md.txt").read_text()
        self.assertEqual(candidate_text.count("\n- "), source_text.count("\n- ") + 1)
        for term in (
            "EVIDENCE / SEARCH",
            "未完了required predicate",
            "consumerへbind",
            "実行方法を探すだけ",
            "入力が変わったpredicateだけ",
            "consumerがterminal",
        ):
            self.assertIn(term, candidate_text)

    def test_targeted_profile_is_six_case_n5_m24(self) -> None:
        profile = json.loads(PROFILE.read_text())
        candidate = verify_bundle(C151)
        self.assertEqual(
            [case["id"] for case in profile["cases"]],
            [
                "TC-A01-LATENT-MODE-POLICY",
                "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING",
                "TC-F01-DOMAIN-DUPLICATE-ASSET-KEY",
                "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND",
                "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY",
                "TC-F07-DEPENDENCY-PROVENANCE-PAIR",
            ],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["name"], candidate["prompt_identity"])
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], candidate["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
