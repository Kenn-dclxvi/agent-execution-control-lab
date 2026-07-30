from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C81 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
C98 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-completion-sheet-r1"
DESIGN = ROOT / "docs/candidate98-validation-completion-sheet-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate98-validation-completion-sheet-v14-reasoning-medium-f02-global-m24-n5-cli0146-r1.json"
C81_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r2.json"
C98_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate98-validation-completion-sheet-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate98Test(unittest.TestCase):
    def test_is_direct_c81_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C81)
        candidate = verify_bundle(C98)
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

    def test_adds_only_short_validation_plan_rule(self) -> None:
        source = rules(C81 / "files/AGENTS.md.txt")
        candidate = rules(C98 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate) - set(source), {"VALIDATION_PLAN"})
        self.assertEqual(
            {key: candidate[key] for key in source},
            source,
        )
        rule = candidate["VALIDATION_PLAN"]
        self.assertIn("一つの実行票", rule)
        self.assertIn("検証success後はmodelへ戻らず", rule)
        self.assertIn("実行票完了後", rule)
        self.assertLess(len(rule), 200)

    def test_manifest_design_and_fixed_m24_profile(self) -> None:
        manifest = verify_bundle(C98)
        self.assertEqual(
            manifest["bundle_sha256"],
            "3f2035cc5ea2de93e196506472f1317130fc16a12c7ad605e162c1cf2b0c6f76",
        )
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("profileへ固定する並列上限: `M=24`", design)
        self.assertIn("実際の同時実行数: 最大5件。profileの`M`は変更しない", design)

        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["comparison_conditions"]["executor_parameters"]["max_workers"], 24
        )
        self.assertEqual(profile["comparison_conditions"]["repetition_condition"]["iterations"], 5)
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "bundle_sha256": "3f2035cc5ea2de93e196506472f1317130fc16a12c7ad605e162c1cf2b0c6f76",
                "name": "the-caption-3ce91a4-validation-completion-sheet-r1",
                "revision": "r1",
            },
        )

    def test_standard14_profile_changes_only_profile_and_prompt_identity(self) -> None:
        source = json.loads(C81_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C98_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        for key in ("cases", "comparison_conditions", "evaluation_set", "execution", "scope"):
            self.assertEqual(source[key], candidate[key])
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["comparison_conditions"]["executor_parameters"]["max_workers"], 24
        )
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "3f2035cc5ea2de93e196506472f1317130fc16a12c7ad605e162c1cf2b0c6f76",
                "name": "the-caption-3ce91a4-validation-completion-sheet-r1",
                "revision": "r1",
            },
        )


if __name__ == "__main__":
    unittest.main()
