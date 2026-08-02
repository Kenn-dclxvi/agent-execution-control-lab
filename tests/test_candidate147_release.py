from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
RELEASE = ROOT / "prompts/releases/the-caption-3ce91a4-result-effect-scope-release-r1"


class Candidate147ReleaseTest(unittest.TestCase):
    def test_release_is_content_identical_and_approved(self) -> None:
        candidate = verify_bundle(CANDIDATE)
        release = verify_bundle(RELEASE)

        self.assertEqual(release["bundle_sha256"], candidate["bundle_sha256"])
        self.assertEqual(release["files"], candidate["files"])
        self.assertEqual(release["artifact"]["release_status"], "projected")
        self.assertEqual(release["artifact"]["approval_status"], "approved")
        self.assertEqual(
            release["provenance"]["candidate_source_commit"],
            "b62063b7be57853318d17a154363e4b39a55144d",
        )
        self.assertEqual(release["provenance"]["runtime_projection_status"], "projected")
        self.assertEqual(release["content_relation"]["changed_targets"], [])

        projection = json.loads((RELEASE / "projection.json").read_text())
        self.assertEqual(
            projection["projection"]["merge_commit"],
            "3119a91d3fad63180884f80ac6b742fbae328afe",
        )
        self.assertEqual(projection["validation"]["post_merge_manifest_match"], "15/19")
        self.assertEqual(projection["validation"]["post_merge_effective_path_match"], "1/1")
        self.assertEqual(projection["projection"]["production_checkout_status"], "not_updated")


if __name__ == "__main__":
    unittest.main()
