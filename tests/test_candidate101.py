from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C98 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-completion-sheet-r1"
C101 = ROOT / "prompts/candidates/the-caption-3ce91a4-additional-investigation-trigger-r1"
DESIGN = ROOT / "docs/candidate101-additional-investigation-trigger-design.md"
C100_PROFILE = ROOT / "evaluations/profiles/candidate100-outcome-source-closure-v14-reasoning-medium-f07-canonical-global-m24-n5-cli0146-r1.json"
C101_PROFILE = ROOT / "evaluations/profiles/candidate101-additional-investigation-trigger-v14-reasoning-medium-f07-canonical-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate101Test(unittest.TestCase):
    def test_is_direct_c98_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C98)
        candidate = verify_bundle(C101)
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

    def test_replaces_only_method_with_observed_investigation_triggers(self) -> None:
        source = rules(C98 / "files/AGENTS.md.txt")
        candidate = rules(C101 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key != "METHOD"},
            {key: source[key] for key in source if key != "METHOD"},
        )

        rule = candidate["METHOD"]
        self.assertTrue(rule.startswith(source["METHOD"]))
        for trigger in (
            "曖昧さ",
            "複数artifactへの波及",
            "bind済みconstraintとの矛盾",
            "変更起因のvalidation failure",
        ):
            self.assertIn(trigger, rule)
        self.assertIn("一般的安全確認 / 念のため / 既存経路全体の再監査", rule)
        for case_specific_term in (
            "F07",
            "run.sh",
            "git log",
            "scripts/dev/main_verify.sh",
        ):
            self.assertNotIn(case_specific_term, rule)

    def test_manifest_and_design_bind_one_replacement_axis(self) -> None:
        manifest = verify_bundle(C101)
        self.assertEqual(
            manifest["bundle_sha256"],
            "b31f2156e599319bd243ad5487453b83297d149654f15e58c6a0b5c84d3056e9",
        )
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate98を直接親", design)
        self.assertIn("prompt lineageには含めない", design)
        self.assertIn("正式評価でもない", design)
        self.assertIn("設定上の`M=24`", design)
        self.assertIn("targeted gate通過前にStandard14またはB20へ進めない", design)

    def test_f07_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C100_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C101_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["execution"], source["execution"])
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "b31f2156e599319bd243ad5487453b83297d149654f15e58c6a0b5c84d3056e9",
                "name": "the-caption-3ce91a4-additional-investigation-trigger-r1",
                "revision": "r1",
            },
        )


if __name__ == "__main__":
    unittest.main()
