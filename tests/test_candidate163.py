from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
FREE = ROOT / "prompts/candidates/the-caption-3ce91a4-control-free-repository-r1"
C163 = ROOT / "prompts/candidates/the-caption-3ce91a4-five-verified-lines-integrated-r1"
FREE_PROFILE = ROOT / "evaluations/profiles/control-free-repository-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
C163_PROFILE = ROOT / "evaluations/profiles/candidate163-five-verified-lines-integrated-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


class Candidate163Test(unittest.TestCase):
    def test_free_child_changes_only_root_to_five_verified_lines(self) -> None:
        free = verify_bundle(FREE)
        candidate = verify_bundle(C163)
        self.assertEqual(candidate["artifact"]["baseline_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        free_files = {entry["target"]: entry for entry in free["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}
        self.assertEqual([target for target in sorted(free_files) if free_files[target] != candidate_files[target]], ["AGENTS.md"])
        lines = (C163 / "files/AGENTS.md.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 5)
        expected = [
            "利用者が決める変更後の動作や値",
            "必要な成果、変更箇所、直し方、維持する動作",
            "担当、判定対象、必要な結果",
            "念のための探索、再確認、履歴調査",
            "必要なテストと差分確認を一つの実行票",
        ]
        for line, phrase in zip(lines, expected, strict=True):
            self.assertIn(phrase, line)

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        free = json.loads(FREE_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C163_PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C163)
        self.assertEqual(candidate["comparison_conditions"], free["comparison_conditions"])
        self.assertEqual(candidate["cases"], free["cases"])
        self.assertEqual(candidate["evaluation_set"], free["evaluation_set"])
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
