from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
RELEASE = ROOT / "prompts/releases/the-caption-3ce91a4-validation-wrapper-precedence-release-r1"
C71_RELEASE = ROOT / "prompts/releases/the-caption-3ce91a4-validation-closure-release-r1"


class Candidate81ReleaseTest(unittest.TestCase):
    def test_release_is_content_identical_to_candidate(self) -> None:
        candidate = verify_bundle(CANDIDATE)
        release = verify_bundle(RELEASE)

        self.assertEqual(release["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(release["files"], candidate["files"])
        self.assertEqual(release["artifact"]["release_status"], "projected")
        self.assertEqual(release["artifact"]["approval_status"], "approved")
        self.assertEqual(
            release["provenance"]["candidate_source_commit"],
            "e52e029a3da3eeab055856d624535c73132aea40",
        )
        self.assertEqual(release["provenance"]["runtime_projection_status"], "projected")
        self.assertEqual(release["content_relation"]["changed_targets"], [])

        projection = json.loads((RELEASE / "projection.json").read_text())
        self.assertEqual(projection["release_identity"], release["artifact"]["release_identity"])
        self.assertEqual(projection["bundle_sha256"], release["bundle_sha256"])
        self.assertEqual(
            projection["projection"]["merge_commit"],
            "592e73aae4f5cf71964efea0d49836e8c894cbbc",
        )
        self.assertEqual(projection["validation"]["post_merge_manifest_match"], "18/19")
        self.assertEqual(projection["validation"]["post_merge_effective_path_match"], "1/1")
        self.assertEqual(
            projection["scope"]["preserved_target_drift"][0]["path"],
            "docs/how-to/index.md",
        )

    def test_only_root_agents_differs_from_projected_candidate71(self) -> None:
        current = verify_bundle(C71_RELEASE)
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
