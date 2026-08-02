from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C125 = ROOT / "prompts/candidates/the-caption-3ce91a4-criterion-complete-single-target-continuation-r1"
C126 = ROOT / "prompts/candidates/the-caption-3ce91a4-criterion-bound-change-input-r1"
DESIGN = ROOT / "docs/candidate126-criterion-bound-change-input-design.md"
C125_PROFILE = ROOT / "evaluations/profiles/candidate125-criterion-complete-single-target-continuation-v14-reasoning-medium-f04-global-m24-n20-cli0146-r1.json"
C126_PROFILE = ROOT / "evaluations/profiles/candidate126-criterion-bound-change-input-v14-reasoning-medium-f04-global-m24-n20-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate126Test(unittest.TestCase):
    def test_is_direct_c125_child(self) -> None:
        source = verify_bundle(C125)
        candidate = verify_bundle(C126)
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

    def test_changes_only_criterion_bound_change_input_axis(self) -> None:
        source = rules(C125 / "files/AGENTS.md.txt")
        candidate = rules(C126 / "files/AGENTS.md.txt")
        self.assertEqual(
            {key for key in source if source[key] != candidate[key]},
            {"EVIDENCE_GATE"},
        )
        gate = candidate["EVIDENCE_GATE"]
        for term in (
            "change_input_ready",
            "未充足の変更criterion",
            "admission済みcontent evidenceのexact value",
            "受領済みevidenceだけから不要または未bindの変更単位を除いて再構成",
            "false自体を追加evidenceの開放条件にしない",
        ):
            self.assertIn(term, gate)
        for forbidden in ("F04", "App.tsx", "colSpan", "npm", "hunkを一つ"):
            self.assertNotIn(forbidden, gate)
        for key in ("VALIDATION_CLOSURE", "VALIDATION_PLAN", "METHOD"):
            self.assertEqual(candidate[key], source[key])

    def test_manifest_design_and_profile(self) -> None:
        manifest = verify_bundle(C126)
        self.assertEqual(
            manifest["bundle_sha256"],
            "aab0d8ce078e3c164668ca3121afd82d3f8d3996ec37af3c2006fe0a031d1a7c",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate125を直接親", design)
        self.assertIn("patchのhunk数は制限しない", design)
        self.assertIn("score `3`以下", design)

        source = json.loads(C125_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C126_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["iterations"], 20)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"]["bundle_sha256"],
            manifest["bundle_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
