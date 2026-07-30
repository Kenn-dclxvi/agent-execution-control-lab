from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C104 = ROOT / "prompts/candidates/the-caption-3ce91a4-staged-evidence-admission-r1"
C105 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-terminal-return-r1"
C106 = ROOT / "prompts/candidates/the-caption-3ce91a4-compact-validation-terminal-wait-r1"
DESIGN = ROOT / "docs/candidate106-compact-validation-terminal-wait-design.md"
C105_PROFILE = ROOT / "evaluations/profiles/candidate105-validation-terminal-return-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"
C106_PROFILE = ROOT / "evaluations/profiles/candidate106-compact-validation-terminal-wait-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"
C105_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate105-validation-terminal-return-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
C106_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate106-compact-validation-terminal-wait-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate106Test(unittest.TestCase):
    def test_is_direct_c104_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C104)
        candidate = verify_bundle(C106)
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

    def test_replaces_only_validation_plan_with_compact_suffix(self) -> None:
        source = rules(C104 / "files/AGENTS.md.txt")
        candidate = rules(C106 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key != "VALIDATION_PLAN"},
            {key: source[key] for key in source if key != "VALIDATION_PLAN"},
        )
        self.assertTrue(candidate["VALIDATION_PLAN"].startswith(source["VALIDATION_PLAN"]))
        suffix = candidate["VALIDATION_PLAN"][len(source["VALIDATION_PLAN"]):]
        self.assertEqual(
            suffix,
            "実行票は意図的な短時間yieldを使わずterminalまで待つ。nonterminal resultが返った場合は、判断 / 進捗報告 / 別toolを挟まず同じsessionのterminalだけを待つ。",
        )
        for omitted in ("一回のcustom exec wrapper", "stop condition", "shell compound", "runtime上限"):
            self.assertNotIn(omitted, suffix)
        for case_specific_term in ("F03", "main_verify.sh", "pytest", "yield-time_ms"):
            self.assertNotIn(case_specific_term, candidate["VALIDATION_PLAN"])

    def test_is_materially_shorter_than_candidate105(self) -> None:
        source = rules(C104 / "files/AGENTS.md.txt")["VALIDATION_PLAN"]
        verbose = rules(C105 / "files/AGENTS.md.txt")["VALIDATION_PLAN"]
        compact = rules(C106 / "files/AGENTS.md.txt")["VALIDATION_PLAN"]
        self.assertEqual(len(verbose) - len(source), 314)
        self.assertEqual(len(compact) - len(source), 104)
        self.assertLess(len(compact) - len(source), (len(verbose) - len(source)) / 2)

    def test_manifest_and_design_bind_one_axis(self) -> None:
        manifest = verify_bundle(C106)
        self.assertEqual(
            manifest["bundle_sha256"],
            "127e4246b1c0443c53b44aebcbda31cc3e63cf2a1a640769f47ee77adc8661e1",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate104を直接親", design)
        self.assertIn("二つへ限定", design)
        self.assertIn("M=24", design)

    def test_f03_profile_reuses_candidate105_conditions(self) -> None:
        source = json.loads(C105_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C106_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["execution"], source["execution"])
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "127e4246b1c0443c53b44aebcbda31cc3e63cf2a1a640769f47ee77adc8661e1",
                "name": "the-caption-3ce91a4-compact-validation-terminal-wait-r1",
                "revision": "r1",
            },
        )

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C105_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C106_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["iterations"], source["iterations"])
        self.assertEqual(candidate["execution"], source["execution"])
        self.assertEqual(candidate["scope"], source["scope"])
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "127e4246b1c0443c53b44aebcbda31cc3e63cf2a1a640769f47ee77adc8661e1",
                "name": "the-caption-3ce91a4-compact-validation-terminal-wait-r1",
                "revision": "r1",
            },
        )


if __name__ == "__main__":
    unittest.main()
