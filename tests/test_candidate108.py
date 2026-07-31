from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C107 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-reentry-closure-r1"
C108 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-ticket-terminal-closure-r1"
DESIGN = ROOT / "docs/candidate108-validation-ticket-terminal-closure-design.md"
C107_PROFILE = ROOT / "evaluations/profiles/candidate107-validation-wrapper-reentry-closure-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"
C108_PROFILE = ROOT / "evaluations/profiles/candidate108-validation-ticket-terminal-closure-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"
C107_STANDARD_PROFILE = ROOT / "evaluations/profiles/candidate107-validation-wrapper-reentry-closure-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
C108_STANDARD_PROFILE = ROOT / "evaluations/profiles/candidate108-validation-ticket-terminal-closure-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate108Test(unittest.TestCase):
    def test_is_direct_c107_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C107)
        candidate = verify_bundle(C108)
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

    def test_replaces_only_validation_plan_with_ticket_terminal_transition(self) -> None:
        source = rules(C107 / "files/AGENTS.md.txt")
        candidate = rules(C108 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key != "VALIDATION_PLAN"},
            {key: source[key] for key in source if key != "VALIDATION_PLAN"},
        )
        self.assertNotIn("outer yield deadline", candidate["VALIDATION_PLAN"])
        self.assertNotIn("wait deadline以上", candidate["VALIDATION_PLAN"])
        self.assertIn("その返却を実行票の完了判定へ使わず", candidate["VALIDATION_PLAN"])
        self.assertIn("実行票全体がterminalになるまで同じcell IDへのwaitだけ", candidate["VALIDATION_PLAN"])
        self.assertIn("commentary / 進捗報告 / 判断 / 別toolを先に発行しない", candidate["VALIDATION_PLAN"])

    def test_manifest_and_design_bind_one_axis(self) -> None:
        manifest = verify_bundle(C108)
        self.assertEqual(
            manifest["bundle_sha256"],
            "f0d2f7ad6c69fd471509ca429d7d0f22b7120d43a2394298228ef7b453b72495",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate107を直接親", design)
        self.assertIn("変更軸はdeadline計算からterminal状態遷移への一本化", design)
        self.assertIn("M=24", design)

    def test_f03_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C107_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C108_PROFILE.read_text(encoding="utf-8"))
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
                "bundle_sha256": "f0d2f7ad6c69fd471509ca429d7d0f22b7120d43a2394298228ef7b453b72495",
                "name": "the-caption-3ce91a4-validation-ticket-terminal-closure-r1",
                "revision": "r1",
            },
        )
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C107_STANDARD_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C108_STANDARD_PROFILE.read_text(encoding="utf-8"))
        for key in source:
            if key not in {"profile_id", "prompt_set_identity"}:
                self.assertEqual(candidate[key], source[key])
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "f0d2f7ad6c69fd471509ca429d7d0f22b7120d43a2394298228ef7b453b72495",
                "name": "the-caption-3ce91a4-validation-ticket-terminal-closure-r1",
                "revision": "r1",
            },
        )
        self.assertEqual(len(candidate["cases"]), 14)
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)


if __name__ == "__main__":
    unittest.main()
