from __future__ import annotations

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
        self.assertEqual(release["artifact"]["release_status"], "approved")
        self.assertEqual(release["artifact"]["approval_status"], "approved")
        self.assertEqual(
            release["provenance"]["candidate_source_commit"],
            "b62063b7be57853318d17a154363e4b39a55144d",
        )
        self.assertEqual(release["provenance"]["runtime_projection_status"], "not_projected")
        self.assertEqual(release["content_relation"]["changed_targets"], [])


if __name__ == "__main__":
    unittest.main()
