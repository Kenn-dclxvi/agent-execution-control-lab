from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
FREE = ROOT / "prompts/candidates/the-caption-3ce91a4-control-free-repository-r1"
C162 = ROOT / "prompts/candidates/the-caption-3ce91a4-completion-ticket-readable-r1"
REFERENCE_PROFILE = ROOT / "evaluations/profiles/candidate152-four-decision-rules-readable-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"
C162_PROFILE = ROOT / "evaluations/profiles/candidate162-completion-ticket-readable-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"


class Candidate162Test(unittest.TestCase):
    def test_free_child_changes_only_root_to_one_completion_ticket_line(self) -> None:
        free = verify_bundle(FREE)
        candidate = verify_bundle(C162)
        self.assertEqual(candidate["artifact"]["baseline_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        free_files = {entry["target"]: entry for entry in free["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}
        self.assertEqual([target for target in sorted(free_files) if free_files[target] != candidate_files[target]], ["AGENTS.md"])
        text = (C162 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertEqual(len(text.splitlines()), 1)
        for phrase in ("実行票", "先に固定", "失敗なら後続を止め", "追加確認せず", "一度だけ完了"):
            self.assertIn(phrase, text)

    def test_f03_profile_changes_only_prompt_identity(self) -> None:
        reference = json.loads(REFERENCE_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C162_PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C162)
        self.assertEqual(candidate["comparison_conditions"], reference["comparison_conditions"])
        self.assertEqual(candidate["cases"], reference["cases"])
        self.assertEqual(candidate["evaluation_set"], reference["evaluation_set"])
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
