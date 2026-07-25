from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import SCHEMA_VERSION, bundle_sha256, verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "evaluations/targets/click/prompts/baselines/click-00e592c-control-free-r1"
PROMPT_IDENTITY = "click-00e592c-control-free-r1"
EMPTY_SHA256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
EMPTY_BLOB_SHA1 = "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"


class ClickControlFreeBaselineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads((BUNDLE / "manifest.json").read_text(encoding="utf-8"))

    def test_bundle_verifies(self) -> None:
        verified = verify_bundle(BUNDLE)
        self.assertEqual(verified["prompt_identity"], PROMPT_IDENTITY)
        self.assertEqual(verified["schema_version"], SCHEMA_VERSION)

    def test_single_agents_md_target(self) -> None:
        entries = self.manifest["files"]
        self.assertEqual([entry["target"] for entry in entries], ["AGENTS.md"])
        self.assertEqual(entries[0]["type"], "file")
        self.assertEqual(entries[0]["mode"], "100644")

    def test_control_free_condition_is_an_empty_file(self) -> None:
        entry = self.manifest["files"][0]
        self.assertEqual(entry["sha256"], EMPTY_SHA256)
        self.assertEqual(entry["git_blob_sha1"], EMPTY_BLOB_SHA1)
        stored = BUNDLE / "files/AGENTS.md.txt"
        self.assertTrue(stored.is_file())
        self.assertEqual(stored.read_bytes(), b"")

    def test_bundle_sha256_matches_files(self) -> None:
        self.assertEqual(self.manifest["bundle_sha256"], bundle_sha256(self.manifest["files"]))

    def test_source_matches_registered_target_pin(self) -> None:
        descriptor = json.loads(
            (ROOT / "evaluations/targets/click/target.json").read_text(encoding="utf-8")
        )
        repository = descriptor["target_repository"]
        source = self.manifest["source"]
        self.assertEqual(source["repository"], repository["repository"])
        self.assertEqual(source["commit"], repository["primary_ref"]["commit"])
        self.assertEqual(source["tree"], repository["primary_ref"]["tree"])

    def test_artifact_role_is_baseline_and_not_evaluated(self) -> None:
        artifact = self.manifest["artifact"]
        self.assertEqual(artifact["artifact_role"], "baseline")
        self.assertEqual(artifact["evaluation_status"], "not_evaluated")

    def test_bundle_sha256_is_indexed(self) -> None:
        index = (ROOT / "evaluations/targets/click/prompts/README.md").read_text(encoding="utf-8")
        self.assertIn(self.manifest["bundle_sha256"], index)
        self.assertIn(PROMPT_IDENTITY, index)


if __name__ == "__main__":
    unittest.main()
