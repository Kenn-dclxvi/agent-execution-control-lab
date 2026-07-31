from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C122 = ROOT / "prompts/candidates/the-caption-3ce91a4-prechange-evidence-wave-closure-r1"
C123 = ROOT / "prompts/candidates/the-caption-3ce91a4-preterminal-result-round-closure-r1"
C124 = ROOT / "prompts/candidates/the-caption-3ce91a4-incomplete-content-continuation-r1"
DESIGN = ROOT / "docs/candidate124-incomplete-content-continuation-design.md"
C122_PROFILE = ROOT / "evaluations/profiles/candidate122-prechange-evidence-wave-closure-v14-reasoning-medium-a01-a02-f01-f02-global-m24-n5-cli0146-r1.json"
C124_PROFILE = ROOT / "evaluations/profiles/candidate124-incomplete-content-continuation-v14-reasoning-medium-a01-a02-f01-f02-f04-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate124Test(unittest.TestCase):
    def test_is_direct_c122_child_and_does_not_inherit_c123(self) -> None:
        source = verify_bundle(C122)
        candidate = verify_bundle(C124)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        self.assertNotEqual(candidate["bundle_sha256"], verify_bundle(C123)["bundle_sha256"])
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_changes_only_incomplete_content_continuation_axis(self) -> None:
        source = rules(C122 / "files/AGENTS.md.txt")
        candidate = rules(C124 / "files/AGENTS.md.txt")
        changed = {key for key in source if source[key] != candidate[key]}
        self.assertEqual(changed, {"EVIDENCE_GATE"})
        gate = candidate["EVIDENCE_GATE"]
        for term in (
            "prechange_wave_complete",
            "未取得range",
            "symbol locator",
            "同じtarget",
            "二回目のcontinuation",
            "単なる取得範囲不足",
        ):
            self.assertIn(term, gate)
        for forbidden in ("A01", "A02", "F02", "F04", "App.tsx", "npm"):
            self.assertNotIn(forbidden, gate)
        for key in ("VALIDATION_CLOSURE", "VALIDATION_PLAN", "METHOD"):
            self.assertEqual(candidate[key], source[key])

    def test_manifest_design_and_profile(self) -> None:
        manifest = verify_bundle(C124)
        self.assertEqual(
            manifest["bundle_sha256"],
            "5c5595bb0debfc2358f5c3e2b8f61cc4bffa496df30a209268ebe70d575ac341",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate122を直接親", design)
        self.assertIn("Candidate123は継承しない", design)
        self.assertIn("F02: token中央値`173,000`以下", design)

        source = json.loads(C122_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C124_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["cases"][:4], source["cases"])
        self.assertEqual(
            candidate["cases"][4],
            {"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"},
        )
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"]["bundle_sha256"],
            manifest["bundle_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
