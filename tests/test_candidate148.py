from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle

ROOT = Path(__file__).resolve().parents[1]
FREE = ROOT / "prompts/candidates/the-caption-3ce91a4-control-free-repository-r1"
C148 = ROOT / "prompts/candidates/the-caption-3ce91a4-five-point-execution-control-r1"
FREE_PROFILE = ROOT / "evaluations/profiles/control-free-repository-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
C148_PROFILE = ROOT / "evaluations/profiles/candidate148-five-point-execution-control-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


class Candidate148Test(unittest.TestCase):
    def test_free_child_changes_only_root_to_five_items(self) -> None:
        free = verify_bundle(FREE)
        candidate = verify_bundle(C148)
        self.assertEqual(candidate["artifact"]["baseline_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], free["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])

        free_files = {entry["target"]: entry for entry in free["files"]}
        candidate_files = {entry["target"]: entry for entry in candidate["files"]}
        self.assertEqual(set(candidate_files), set(free_files))
        changed = [target for target in sorted(free_files) if free_files[target] != candidate_files[target]]
        self.assertEqual(changed, ["AGENTS.md"])

        text = (C148 / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        bullets = [line for line in text.splitlines() if line.startswith("- ")]
        self.assertEqual(len(bullets), 5)
        self.assertEqual(
            [line.split(":", 1)[0] for line in bullets],
            ["- GOAL", "- START", "- SEARCH", "- SPLIT", "- FINISH"],
        )

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        free = json.loads(FREE_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C148_PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C148)

        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["comparison_conditions"], free["comparison_conditions"])
        self.assertEqual(candidate["cases"], free["cases"])
        self.assertEqual(candidate["evaluation_set"], free["evaluation_set"])
        self.assertEqual(candidate["prompt_set_identity"]["name"], manifest["prompt_identity"])
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
