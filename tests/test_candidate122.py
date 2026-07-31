from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C119 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-predicate-method-boundary-r1"
C120 = ROOT / "prompts/candidates/the-caption-3ce91a4-implementation-edit-ticket-closure-r1"
C121 = ROOT / "prompts/candidates/the-caption-3ce91a4-evidence-request-scope-closure-r1"
C122 = ROOT / "prompts/candidates/the-caption-3ce91a4-prechange-evidence-wave-closure-r1"
DESIGN = ROOT / "docs/candidate122-prechange-evidence-wave-closure-design.md"
C119_PROFILE = ROOT / "evaluations/profiles/candidate119-validation-predicate-method-boundary-v14-reasoning-medium-a01-a02-f01-global-m24-n5-cli0146-r1.json"
C122_PROFILE = ROOT / "evaluations/profiles/candidate122-prechange-evidence-wave-closure-v14-reasoning-medium-a01-a02-f01-f02-global-m24-n5-cli0146-r1.json"
C118_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate118-implementation-bind-terminal-closure-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
C122_STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate122-prechange-evidence-wave-closure-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate122Test(unittest.TestCase):
    def test_is_direct_c119_child_and_does_not_inherit_stopped_candidates(self) -> None:
        source = verify_bundle(C119)
        candidate = verify_bundle(C122)
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": source["prompt_identity"],
            },
        )
        self.assertNotEqual(candidate["bundle_sha256"], verify_bundle(C120)["bundle_sha256"])
        self.assertNotEqual(candidate["bundle_sha256"], verify_bundle(C121)["bundle_sha256"])
        self.assertEqual(
            [entry for entry in candidate["files"] if entry["target"] != "AGENTS.md"],
            [entry for entry in source["files"] if entry["target"] != "AGENTS.md"],
        )

    def test_changes_only_evidence_request_scope_axis(self) -> None:
        source = rules(C119 / "files/AGENTS.md.txt")
        candidate = rules(C122 / "files/AGENTS.md.txt")
        changed = {key for key in source if source[key] != candidate[key]}
        self.assertEqual(changed, {"EVIDENCE_GATE"})
        gate = candidate["EVIDENCE_GATE"]
        self.assertIn("prechange_evidence_wave_ready", gate)
        self.assertIn("exact target set", gate)
        self.assertIn("一つのinvocation", gate)
        self.assertIn("edit-ready", gate)
        self.assertIn("terminal stop", gate)
        self.assertNotIn("evidence_request_ready", gate)
        for key in ("VALIDATION_CLOSURE", "VALIDATION_PLAN", "METHOD"):
            self.assertEqual(candidate[key], source[key])
        for case_term in ("A01", "A02", "F01", "F02", "run.sh", "pytest"):
            self.assertNotIn(case_term, gate)

    def test_manifest_design_and_profile(self) -> None:
        manifest = verify_bundle(C122)
        self.assertEqual(
            manifest["bundle_sha256"],
            "5b7525ec265ea10f207a3b23f0bbf749f677554aad1c2fa0c5beae0c41e0d2d3",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate119を直接親", design)
        self.assertIn("Candidate120とCandidate121は継承しない", design)
        self.assertIn("F02 token中央値: Candidate107の`173,000`以下", design)

        source = json.loads(C119_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C122_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["cases"][:3], source["cases"])
        self.assertEqual(
            candidate["cases"][3],
            {"id": "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND", "revision": "r1"},
        )
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["prompt_set_identity"]["bundle_sha256"], manifest["bundle_sha256"])

        standard_source = json.loads(C118_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        standard_candidate = json.loads(C122_STANDARD14_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            standard_candidate["comparison_conditions"],
            standard_source["comparison_conditions"],
        )
        self.assertEqual(standard_candidate["evaluation_set"], standard_source["evaluation_set"])
        self.assertEqual(standard_candidate["cases"], standard_source["cases"])
        self.assertEqual(standard_candidate["iterations"], 5)
        self.assertEqual(standard_candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            standard_candidate["prompt_set_identity"]["bundle_sha256"],
            manifest["bundle_sha256"],
        )


if __name__ == "__main__":
    unittest.main()
