from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
FREE = ROOT / "prompts/candidates/the-caption-3ce91a4-control-free-repository-r1"
C157 = ROOT / "prompts/candidates/the-caption-3ce91a4-focused-prechange-research-readable-r1"
REFERENCE_PROFILE = ROOT / "evaluations/profiles/candidate152-four-decision-rules-readable-v14-reasoning-medium-f08-global-m24-n5-cli0146-r1.json"
C157_PROFILE = ROOT / "evaluations/profiles/candidate157-focused-prechange-research-readable-v14-reasoning-medium-f08-global-m24-n5-cli0146-r1.json"


class Candidate157Test(unittest.TestCase):
    def test_free_child_changes_only_root_to_one_research_sentence(self) -> None:
        free = verify_bundle(FREE)
        candidate = verify_bundle(C157)
        self.assertEqual(candidate["artifact"]["baseline_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])

        free_files = {entry["target"]: entry for entry in free["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}
        self.assertEqual(set(candidate_files), set(free_files))
        changed = [target for target in sorted(free_files) if free_files[target] != candidate_files[target]]
        self.assertEqual(changed, ["AGENTS.md"])

        text = (C157 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertEqual(len(text.splitlines()), 1)
        self.assertIn("不足している情報だけに絞り", text)
        self.assertIn("念のための探索、再確認、履歴調査をせず", text)

    def test_f08_profile_changes_only_prompt_identity(self) -> None:
        reference = json.loads(REFERENCE_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C157_PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C157)

        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["comparison_conditions"], reference["comparison_conditions"])
        self.assertEqual(candidate["cases"], reference["cases"])
        self.assertEqual(candidate["evaluation_set"], reference["evaluation_set"])
        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
