from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C125 = ROOT / "prompts/candidates/the-caption-3ce91a4-criterion-complete-single-target-continuation-r1"
C127 = ROOT / "prompts/candidates/the-caption-3ce91a4-failed-change-salvage-r1"
DESIGN = ROOT / "docs/candidate127-failed-change-salvage-design.md"
C125_PROFILE = ROOT / "evaluations/profiles/candidate125-criterion-complete-single-target-continuation-v14-reasoning-medium-f04-global-m24-n5-cli0146-r1.json"
C127_PROFILE = ROOT / "evaluations/profiles/candidate127-failed-change-salvage-v14-reasoning-medium-f04-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate127Test(unittest.TestCase):
    def test_is_direct_c125_child(self) -> None:
        source = verify_bundle(C125)
        candidate = verify_bundle(C127)
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

    def test_changes_only_failed_change_salvage_axis(self) -> None:
        source = rules(C125 / "files/AGENTS.md.txt")
        candidate = rules(C127 / "files/AGENTS.md.txt")
        self.assertEqual(
            {key for key in source if source[key] != candidate[key]},
            {"RECOVERY"},
        )
        recovery = candidate["RECOVERY"]
        for term in (
            "failed_change_salvage_ready",
            "target artifactへの変更未適用",
            "不一致単位へ依存しない変更単位",
            "残った独立変更単位だけ",
            "追加read / repository search / 別target / 別method",
            "VALIDATION_PLAN",
        ):
            self.assertIn(term, recovery)
        for forbidden in ("F04", "App.tsx", "colSpan", "hasAuditKey", "apply_patch"):
            self.assertNotIn(forbidden, recovery)
        for key in ("EVIDENCE_GATE", "VALIDATION_CLOSURE", "VALIDATION_PLAN", "METHOD"):
            self.assertEqual(candidate[key], source[key])

    def test_manifest_design_and_profile(self) -> None:
        manifest = verify_bundle(C127)
        self.assertEqual(
            manifest["bundle_sha256"],
            "75d37043e6efbcb91bf4e097e80f38f88e73ca7e05d42273b71c172832d2eba9",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate125を直接親", design)
        self.assertIn("Candidate126の`change_input_ready`は継承しない", design)
        self.assertIn("### F04 N=5", design)

        source = json.loads(C125_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C127_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"]["bundle_sha256"],
            manifest["bundle_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
