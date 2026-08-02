from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C131 = ROOT / "prompts/candidates/the-caption-3ce91a4-criterion-anchor-continuation-r1"
C132 = ROOT / "prompts/candidates/the-caption-3ce91a4-observed-preimage-change-construction-r1"
DESIGN = ROOT / "docs/candidate132-observed-preimage-change-construction-design.md"
C131_PROFILE = ROOT / "evaluations/profiles/candidate131-criterion-anchor-continuation-v14-reasoning-medium-f04-global-m24-n5-cli0146-r1.json"
C132_PROFILE = ROOT / "evaluations/profiles/candidate132-observed-preimage-change-construction-v14-reasoning-medium-f04-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate132Test(unittest.TestCase):
    def test_is_direct_c131_child(self) -> None:
        source = verify_bundle(C131)
        candidate = verify_bundle(C132)
        self.assertEqual(candidate["content_relation"], {
            "changed_targets": ["AGENTS.md"],
            "kind": "direct_child_full_bundle",
            "source_prompt_identity": source["prompt_identity"],
        })
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_adds_only_observed_preimage_predicate(self) -> None:
        source = rules(C131 / "files/AGENTS.md.txt")
        candidate = rules(C132 / "files/AGENTS.md.txt")
        self.assertEqual({key for key in source if source[key] != candidate[key]}, {"EVIDENCE_GATE"})
        gate = candidate["EVIDENCE_GATE"]
        for term in (
            "change_preimage_ready",
            "削除行 / 置換前文字列 / contextの全operand",
            "最新のadmission済みcontent evidenceに現れるexact value",
            "独立してreadyな変更単位を止めず",
            "追加readまたは全criterion再監査の開放条件にしない",
        ):
            self.assertIn(term, gate)
        self.assertNotIn("change_input_ready", gate)
        for forbidden in ("F04", "App.tsx", "hasAuditKey", "colSpan"):
            self.assertNotIn(forbidden, gate)
        for key in ("SPEC", "RECOVERY", "VALIDATION_PLAN", "METHOD"):
            self.assertEqual(candidate[key], source[key])

    def test_design_separates_points_and_n5_gate(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        for term in (
            "Candidate126",
            "Candidate131",
            "全criterionの充足状態を変更前に完全再監査する条件",
            "Point 2 Evidence coverage",
            "Point 3 Effect state",
            "Point 4 Dependency",
            "Point 5 Change construction",
            "Point 6 Closure / recovery",
            "score `3`以下: 0 / 5",
        ):
            self.assertIn(term, design)

    def test_f04_profile_preserves_c131_conditions(self) -> None:
        source = json.loads(C131_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C132_PROFILE.read_text(encoding="utf-8"))
        manifest = verify_bundle(C132)
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
