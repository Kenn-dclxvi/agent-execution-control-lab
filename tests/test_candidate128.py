from __future__ import annotations

import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C125 = ROOT / "prompts/candidates/the-caption-3ce91a4-criterion-complete-single-target-continuation-r1"
C128 = ROOT / "prompts/candidates/the-caption-3ce91a4-required-effect-closure-r1"
DESIGN = ROOT / "docs/candidate128-required-effect-closure-design.md"
C125_PROFILE = ROOT / "evaluations/profiles/candidate125-criterion-complete-single-target-continuation-v14-reasoning-medium-f02-f04-f07-global-m24-n5-cli0146-r1.json"
C128_PROFILE = ROOT / "evaluations/profiles/candidate128-required-effect-closure-v14-reasoning-medium-f02-f04-f07-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate128Test(unittest.TestCase):
    def test_is_direct_c125_child(self) -> None:
        source = verify_bundle(C125)
        candidate = verify_bundle(C128)
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

    def test_replaces_only_recovery_with_required_effect_closure(self) -> None:
        source = rules(C125 / "files/AGENTS.md.txt")
        candidate = rules(C128 / "files/AGENTS.md.txt")
        self.assertEqual(
            {key for key in source if source[key] != candidate[key]},
            {"RECOVERY"},
        )
        recovery = candidate["RECOVERY"]
        for term in (
            "required_effects_closed",
            "TaskSpecの各required effect",
            "充足済みeffectを保持",
            "未充足effectだけ",
            "hunk不一致 / invocation failure / 他effectからの独立性",
            "追加read / repository search / 別target / 別method",
            "VALIDATION_PLAN",
        ):
            self.assertIn(term, recovery)
        self.assertNotIn("failed_change_salvage_ready", recovery)
        for forbidden in (
            "F02",
            "F04",
            "F07",
            "v4_engine.py",
            "collection_history_updater.py",
            "hasAuditKey",
            "colSpan",
            "requirements.in",
        ):
            self.assertNotIn(forbidden, recovery)
        for key in (
            "SPEC",
            "EVIDENCE_GATE",
            "VALIDATION_CLOSURE",
            "VALIDATION_PLAN",
            "METHOD",
        ):
            self.assertEqual(candidate[key], source[key])

    def test_design_uses_broad_trace_matrix_and_n5_gate(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        for term in (
            "Candidate125を直接親",
            "F02の低Score 2件",
            "F02の成功経路",
            "F04の成功経路",
            "F07の成功経路",
            "いきなりN=20へ進めず",
            "Standard14 N=5",
        ):
            self.assertIn(term, design)

    def test_targeted_profile_changes_only_prompt_identity(self) -> None:
        import json

        source = json.loads(C125_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C128_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertNotEqual(candidate["prompt_set_identity"], source["prompt_set_identity"])


if __name__ == "__main__":
    unittest.main()
