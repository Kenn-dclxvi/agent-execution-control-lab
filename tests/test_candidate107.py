from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C104 = ROOT / "prompts/candidates/the-caption-3ce91a4-staged-evidence-admission-r1"
C106 = ROOT / "prompts/candidates/the-caption-3ce91a4-compact-validation-terminal-wait-r1"
C107 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-reentry-closure-r1"
DESIGN = ROOT / "docs/candidate107-validation-wrapper-reentry-closure-design.md"
C106_PROFILE = ROOT / "evaluations/profiles/candidate106-compact-validation-terminal-wait-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"
C107_PROFILE = ROOT / "evaluations/profiles/candidate107-validation-wrapper-reentry-closure-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate107Test(unittest.TestCase):
    def test_is_direct_c106_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C106)
        candidate = verify_bundle(C107)
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

    def test_replaces_only_validation_plan_with_observable_transition(self) -> None:
        base = rules(C104 / "files/AGENTS.md.txt")
        source = rules(C106 / "files/AGENTS.md.txt")
        candidate = rules(C107 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key != "VALIDATION_PLAN"},
            {key: source[key] for key in source if key != "VALIDATION_PLAN"},
        )
        self.assertTrue(candidate["VALIDATION_PLAN"].startswith(base["VALIDATION_PLAN"]))
        suffix = candidate["VALIDATION_PLAN"][len(base["VALIDATION_PLAN"]):]
        self.assertEqual(
            suffix,
            "validation wrapperのouter yield deadlineは未指定にするか、内部required commandのwait deadline以上にする。cell ID付きnonterminal result後は、terminalまで同じcell IDへのwaitだけを発行する。commentary / 進捗報告 / 判断 / 別toolを先に発行しない。",
        )
        self.assertNotIn("意図的な短時間yield", candidate["VALIDATION_PLAN"])
        self.assertNotIn("同じsession", candidate["VALIDATION_PLAN"])

    def test_manifest_and_design_bind_one_axis(self) -> None:
        manifest = verify_bundle(C107)
        self.assertEqual(
            manifest["bundle_sha256"],
            "72c6f4b8818065300ca24fd0a42bdf49ce834ae44d4f2406da497f98c064c50d",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate106を直接親", design)
        self.assertIn("変更軸はvalidation wrapperのnonterminal再入closure一つ", design)
        self.assertIn("M=24", design)

    def test_f03_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C106_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C107_PROFILE.read_text(encoding="utf-8"))
        for key in source:
            if key not in {"profile_id", "prompt_set_identity"}:
                self.assertEqual(candidate[key], source[key])
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "72c6f4b8818065300ca24fd0a42bdf49ce834ae44d4f2406da497f98c064c50d",
                "name": "the-caption-3ce91a4-validation-wrapper-reentry-closure-r1",
                "revision": "r1",
            },
        )
        self.assertEqual(candidate["execution"]["max_workers"], 24)


if __name__ == "__main__":
    unittest.main()
