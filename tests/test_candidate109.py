from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C108 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-ticket-terminal-closure-r1"
C109 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-ticket-outer-wait-closure-r1"
DESIGN = ROOT / "docs/candidate109-validation-ticket-outer-wait-closure-design.md"
C108_PROFILE = ROOT / "evaluations/profiles/candidate108-validation-ticket-terminal-closure-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"
C109_PROFILE = ROOT / "evaluations/profiles/candidate109-validation-ticket-outer-wait-closure-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate109Test(unittest.TestCase):
    def test_is_direct_c108_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C108)
        candidate = verify_bundle(C109)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_replaces_only_validation_plan_with_outer_wait_closure(self) -> None:
        source = rules(C108 / "files/AGENTS.md.txt")
        candidate = rules(C109 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key != "VALIDATION_PLAN"},
            {key: source[key] for key in source if key != "VALIDATION_PLAN"},
        )
        self.assertIn("outer yieldはruntimeが一回で待てる最大値へ固定", candidate["VALIDATION_PLAN"])
        self.assertIn("実行票完了前の返却を意図した短時間yieldを指定しない", candidate["VALIDATION_PLAN"])
        self.assertIn("runtime上限によってcell ID付きnonterminal resultが返った場合", candidate["VALIDATION_PLAN"])
        self.assertIn("実行票全体がterminalになるまで同じcell IDへのwaitだけ", candidate["VALIDATION_PLAN"])
        self.assertIn("commentary / 進捗報告 / 判断 / 別toolを先に発行しない", candidate["VALIDATION_PLAN"])

    def test_manifest_and_design_bind_one_axis(self) -> None:
        manifest = verify_bundle(C109)
        self.assertEqual(
            manifest["bundle_sha256"],
            "fe39d4f66f981f0be35fe20dcf53562cf06dc00442dfc909895e3dcd10fc8c0d",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate108を直接親", design)
        self.assertIn("変更軸はouter yield選択の固定", design)
        self.assertIn("M=24", design)

    def test_f03_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C108_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C109_PROFILE.read_text(encoding="utf-8"))
        for key in source:
            if key not in {"profile_id", "prompt_set_identity"}:
                self.assertEqual(candidate[key], source[key])
        self.assertEqual(
            candidate["iterations"],
            source["comparison_conditions"]["repetition_condition"]["iterations"],
        )
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "fe39d4f66f981f0be35fe20dcf53562cf06dc00442dfc909895e3dcd10fc8c0d",
                "name": "the-caption-3ce91a4-validation-ticket-outer-wait-closure-r1",
                "revision": "r1",
            },
        )
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)

if __name__ == "__main__":
    unittest.main()
