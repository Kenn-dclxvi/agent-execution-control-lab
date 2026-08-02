from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C128 = ROOT / "prompts/candidates/the-caption-3ce91a4-required-effect-closure-r1"
C129 = ROOT / "prompts/candidates/the-caption-3ce91a4-unsatisfied-effect-change-admission-r1"
DESIGN = ROOT / "docs/candidate129-unsatisfied-effect-change-admission-design.md"
C128_PROFILE = ROOT / "evaluations/profiles/candidate128-required-effect-closure-v14-reasoning-medium-f02-f04-f07-global-m24-n5-cli0146-r1.json"
C129_PROFILE = ROOT / "evaluations/profiles/candidate129-unsatisfied-effect-change-admission-v14-reasoning-medium-f04-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate129Test(unittest.TestCase):
    def test_is_direct_c128_child(self) -> None:
        source = verify_bundle(C128)
        candidate = verify_bundle(C129)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        self.assertNotEqual(candidate["bundle_sha256"], source["bundle_sha256"])
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_changes_only_effect_change_admission_axis(self) -> None:
        source = rules(C128 / "files/AGENTS.md.txt")
        candidate = rules(C129 / "files/AGENTS.md.txt")
        self.assertEqual(
            {key for key in source if source[key] != candidate[key]},
            {"EVIDENCE_GATE"},
        )
        gate = candidate["EVIDENCE_GATE"]
        for term in (
            "change_effect_admitted",
            "観測済みcurrent content",
            "未充足",
            "開始状態から充足済み",
            "保持constraint",
            "変更単位へ含めない",
            "未観測current contentから変更単位を推測しない",
        ):
            self.assertIn(term, gate)
        for forbidden in (
            "F04",
            "App.tsx",
            "hasAuditKey",
            "colSpan",
            "apply_patch",
        ):
            self.assertNotIn(forbidden, gate)
        for key in (
            "SPEC",
            "RECOVERY",
            "VALIDATION_CLOSURE",
            "VALIDATION_PLAN",
            "METHOD",
        ):
            self.assertEqual(candidate[key], source[key])

    def test_design_records_trace_cause_and_n5_gate(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        for term in (
            "Candidate128を直接親",
            "Candidate125 | 22 / 30",
            "Candidate128 | 4 / 5",
            "Candidate126を継承しない理由",
            "いきなりN=20へ進めない",
            "initial apply failure: 0 / 5",
        ):
            self.assertIn(term, design)

    def test_f04_profile_preserves_c128_conditions(self) -> None:
        source = json.loads(C128_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C129_PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C129)
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(
            candidate["cases"],
            [case for case in source["cases"] if case["id"] == "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY"],
        )
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"]["bundle_sha256"],
            manifest["bundle_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
