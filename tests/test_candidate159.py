from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
FREE = ROOT / "prompts/candidates/the-caption-3ce91a4-control-free-repository-r1"
C159 = ROOT / "prompts/candidates/the-caption-3ce91a4-change-start-readable-r1"
REFERENCE_PROFILE = ROOT / "evaluations/profiles/candidate150-required-outcome-bind-readable-v14-reasoning-medium-f02-f04-f07-global-m24-n5-cli0146-r1.json"
C159_PROFILE = ROOT / "evaluations/profiles/candidate159-change-start-readable-v14-reasoning-medium-f02-global-m24-n5-cli0146-r1.json"


class Candidate159Test(unittest.TestCase):
    def test_free_child_changes_only_root_to_one_change_start_line(self) -> None:
        free = verify_bundle(FREE)
        candidate = verify_bundle(C159)
        self.assertEqual(candidate["artifact"]["baseline_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])

        free_files = {entry["target"]: entry for entry in free["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}
        self.assertEqual(set(candidate_files), set(free_files))
        changed = [target for target in sorted(free_files) if free_files[target] != candidate_files[target]]
        self.assertEqual(changed, ["AGENTS.md"])

        text = (C159 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertEqual(len(text.splitlines()), 1)
        for phrase in ("必要な成果", "変更箇所", "直し方", "維持する動作", "変更しない"):
            self.assertIn(phrase, text)

    def test_f02_profile_changes_prompt_and_coverage_only(self) -> None:
        reference = json.loads(REFERENCE_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C159_PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C159)

        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["comparison_conditions"], reference["comparison_conditions"])
        self.assertEqual(candidate["cases"], [reference["cases"][0]])
        self.assertEqual(candidate["evaluation_set"], reference["evaluation_set"])
        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
