from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
FREE = ROOT / "prompts/candidates/the-caption-3ce91a4-control-free-repository-r1"
C160 = ROOT / "prompts/candidates/the-caption-3ce91a4-assignment-result-readable-r1"
FREE_PROFILE = ROOT / "evaluations/profiles/control-free-repository-v14-reasoning-medium-d01-global-m24-n5-cli0146-r1.json"
C160_PROFILE = ROOT / "evaluations/profiles/candidate160-assignment-result-readable-v14-reasoning-medium-d01-global-m24-n5-cli0146-r1.json"


class Candidate160Test(unittest.TestCase):
    def test_free_child_changes_only_root_to_one_assignment_result_line(self) -> None:
        free = verify_bundle(FREE)
        candidate = verify_bundle(C160)
        self.assertEqual(candidate["artifact"]["baseline_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])

        free_files = {entry["target"]: entry for entry in free["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}
        changed = [target for target in sorted(free_files) if free_files[target] != candidate_files[target]]
        self.assertEqual(changed, ["AGENTS.md"])

        text = (C160 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertEqual(len(text.splitlines()), 1)
        for phrase in ("担当", "判定対象", "必要な結果", "進捗報告"):
            self.assertIn(phrase, text)

    def test_pair_profiles_change_only_prompt_identity(self) -> None:
        free = json.loads(FREE_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C160_PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C160)

        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["comparison_conditions"], free["comparison_conditions"])
        self.assertEqual(candidate["cases"], free["cases"])
        self.assertEqual(candidate["evaluation_set"], free["evaluation_set"])
        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
