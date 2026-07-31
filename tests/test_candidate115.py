from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C114 = ROOT / "prompts/candidates/the-caption-3ce91a4-spec-ready-evidence-phase-boundary-r1"
C115 = ROOT / "prompts/candidates/the-caption-3ce91a4-authority-location-discovery-r1"
PROFILE = ROOT / "evaluations/profiles/candidate115-authority-location-discovery-v14-reasoning-medium-a01-a02-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate115Test(unittest.TestCase):
    def test_is_direct_c114_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C114)
        candidate = verify_bundle(C115)
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], source["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_changes_only_authority_location_condition(self) -> None:
        source = rules(C114 / "files/AGENTS.md.txt")
        candidate = rules(C115 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key != "EVIDENCE_GATE"},
            {key: source[key] for key in source if key != "EVIDENCE_GATE"},
        )
        rule = candidate["EVIDENCE_GATE"]
        self.assertIn("authorityのpath未記載だけをclarification理由にせず", rule)
        self.assertIn("allowed read内でauthority locationを解決", rule)
        self.assertIn("`spec_ready=false`", rule)

    def test_profile_is_a01_a02_n5_m24(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual([case["id"] for case in profile["cases"]], [
            "TC-A01-LATENT-MODE-POLICY",
            "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING",
        ])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], verify_bundle(C115)["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
