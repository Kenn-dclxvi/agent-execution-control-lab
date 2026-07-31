from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-criterion-complete-single-target-continuation-r1"
RELEASE = ROOT / "prompts/releases/the-caption-3ce91a4-criterion-complete-single-target-continuation-release-r1"
C81_RELEASE = ROOT / "prompts/releases/the-caption-3ce91a4-validation-wrapper-precedence-release-r1"


class Candidate125ReleaseTest(unittest.TestCase):
    def test_release_is_content_identical_and_approved(self) -> None:
        candidate = verify_bundle(CANDIDATE)
        release = verify_bundle(RELEASE)

        self.assertEqual(release["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(release["files"], candidate["files"])
        self.assertEqual(release["artifact"]["release_status"], "projected")
        self.assertEqual(release["artifact"]["approval_status"], "approved")
        self.assertEqual(
            release["provenance"]["candidate_source_commit"],
            "912ee3d2f80f5bedab3df8da52456823db91e829",
        )
        self.assertEqual(
            release["provenance"]["runtime_projection_status"],
            "projected",
        )
        self.assertEqual(release["content_relation"]["changed_targets"], [])

        projection = json.loads((RELEASE / "projection.json").read_text())
        self.assertEqual(
            projection["projection"]["merge_commit"],
            "2791c21d414d849b376be0d9496fc455f7e10e45",
        )
        self.assertEqual(projection["validation"]["post_merge_manifest_match"], "18/19")
        self.assertEqual(projection["validation"]["post_merge_effective_path_match"], "1/1")
        self.assertEqual(
            projection["future_evaluation"]["candidate125_n100"],
            "planned_not_started",
        )
        self.assertFalse(projection["future_evaluation"]["blocks_current_projection"])
        self.assertEqual(
            projection["scope"]["preserved_target_drift"][0]["path"],
            "docs/how-to/index.md",
        )

    def test_only_root_agents_differs_from_projected_candidate81(self) -> None:
        current = verify_bundle(C81_RELEASE)
        release = verify_bundle(RELEASE)
        current_files = {entry["target"]: entry for entry in current["files"]}
        release_files = {entry["target"]: entry for entry in release["files"]}

        changed = [
            target
            for target in sorted(current_files)
            if current_files[target] != release_files[target]
        ]
        self.assertEqual(changed, ["AGENTS.md"])


if __name__ == "__main__":
    unittest.main()
