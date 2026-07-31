from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C119 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-predicate-method-boundary-r1"
C120 = ROOT / "prompts/candidates/the-caption-3ce91a4-implementation-edit-ticket-closure-r1"
DESIGN = ROOT / "docs/candidate120-implementation-edit-ticket-closure-design.md"
C119_PROFILE = ROOT / "evaluations/profiles/candidate119-validation-predicate-method-boundary-v14-reasoning-medium-a01-a02-f01-global-m24-n5-cli0146-r1.json"
C120_PROFILE = ROOT / "evaluations/profiles/candidate120-implementation-edit-ticket-closure-v14-reasoning-medium-a01-a02-f01-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate120Test(unittest.TestCase):
    def test_is_direct_c119_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C119)
        candidate = verify_bundle(C120)
        self.assertEqual(candidate["content_relation"], {
            "changed_targets": ["AGENTS.md"],
            "kind": "direct_child_full_bundle",
            "source_prompt_identity": source["prompt_identity"],
        })
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_changes_only_evidence_gate(self) -> None:
        source = rules(C119 / "files/AGENTS.md.txt")
        candidate = rules(C120 / "files/AGENTS.md.txt")
        self.assertEqual({key for key in source if source[key] != candidate[key]}, {"EVIDENCE_GATE"})
        self.assertIn("implementation_edit_ticket_ready", candidate["EVIDENCE_GATE"])
        self.assertIn("次のtool invocationはartifact変更だけ", candidate["EVIDENCE_GATE"])
        for key in ("VALIDATION_CLOSURE", "VALIDATION_PLAN", "METHOD"):
            self.assertEqual(candidate[key], source[key])
        for case_term in ("A01", "A02", "F01", "run.sh", "pytest"):
            self.assertNotIn(case_term, candidate["EVIDENCE_GATE"])

    def test_manifest_design_and_profile(self) -> None:
        manifest = verify_bundle(C120)
        self.assertEqual(manifest["bundle_sha256"], "c171d3c12fcd81158b72fa234975c252fa06bae6917909efef2ad6ff41f0a8c1")
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate119を直接親", design)
        self.assertIn("Candidate107 `125,559`以下", design)
        source = json.loads(C119_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C120_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])


if __name__ == "__main__":
    unittest.main()
