from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C104 = ROOT / "prompts/candidates/the-caption-3ce91a4-staged-evidence-admission-r1"
C105 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-terminal-return-r1"
DESIGN = ROOT / "docs/candidate105-validation-terminal-return-design.md"
C104_PROFILE = ROOT / "evaluations/profiles/candidate104-staged-evidence-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r3.json"
C105_PROFILE = ROOT / "evaluations/profiles/candidate105-validation-terminal-return-v14-reasoning-medium-f03-global-m24-n5-cli0146-r1.json"
C105_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate105-validation-terminal-return-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate105Test(unittest.TestCase):
    def test_is_direct_c104_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C104)
        candidate = verify_bundle(C105)
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

    def test_replaces_only_validation_plan(self) -> None:
        source = rules(C104 / "files/AGENTS.md.txt")
        candidate = rules(C105 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key != "VALIDATION_PLAN"},
            {key: source[key] for key in source if key != "VALIDATION_PLAN"},
        )
        rule = candidate["VALIDATION_PLAN"]
        for required in (
            "一回のcustom exec wrapper",
            "意図的な短時間yield",
            "progress resultだけをmodelへ返さない",
            "同じwrapperまたはsessionのterminal result受領だけを継続",
            "全resultを一度だけmodelへ返し",
        ):
            self.assertIn(required, rule)
        for case_specific_term in ("F03", "main_verify.sh", "pytest", "yield_time_ms=1000"):
            self.assertNotIn(case_specific_term, rule)

    def test_manifest_and_design_bind_one_axis(self) -> None:
        manifest = verify_bundle(C105)
        self.assertEqual(
            manifest["bundle_sha256"],
            "6eaf12cd58e26244d514a34f4a9238d217058a3b178f138ea3551e930a496aa5",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate104を直接親", design)
        self.assertIn("`VALIDATION_PLAN`一規則だけを置換", design)
        self.assertIn("tool result配送の別軸", design)
        self.assertIn("profileへ固定する並列上限: `M=24`", design)

    def test_f03_profile_reuses_c104_conditions(self) -> None:
        source = json.loads(C104_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C105_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["cases"], [{"id": "TC-F03-ATOMIC-CONTEXT-CLEANUP", "revision": "r2"}])
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["execution"]["duration_hints_seconds"], {"TC-F03-ATOMIC-CONTEXT-CLEANUP": 477.651})
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "6eaf12cd58e26244d514a34f4a9238d217058a3b178f138ea3551e930a496aa5",
                "name": "the-caption-3ce91a4-validation-terminal-return-r1",
                "revision": "r1",
            },
        )

    def test_standard14_profile_differs_from_c104_only_by_prompt_identity(self) -> None:
        source = json.loads(C104_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C105_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["iterations"], source["iterations"])
        self.assertEqual(candidate["execution"], source["execution"])
        self.assertEqual(candidate["scope"], source["scope"])
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "6eaf12cd58e26244d514a34f4a9238d217058a3b178f138ea3551e930a496aa5",
                "name": "the-caption-3ce91a4-validation-terminal-return-r1",
                "revision": "r1",
            },
        )


if __name__ == "__main__":
    unittest.main()
