from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C118 = ROOT / "prompts/candidates/the-caption-3ce91a4-implementation-bind-terminal-closure-r1"
C119 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-predicate-method-boundary-r1"
DESIGN = ROOT / "docs/candidate119-validation-predicate-method-boundary-design.md"
C118_PROFILE = ROOT / "evaluations/profiles/candidate118-implementation-bind-terminal-closure-v14-reasoning-medium-a01-a02-f01-global-m24-n5-cli0146-r1.json"
C119_PROFILE = ROOT / "evaluations/profiles/candidate119-validation-predicate-method-boundary-v14-reasoning-medium-a01-a02-f01-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate119Test(unittest.TestCase):
    def test_is_direct_c118_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C118)
        candidate = verify_bundle(C119)
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

    def test_changes_only_validation_predicate_method_axis(self) -> None:
        source = rules(C118 / "files/AGENTS.md.txt")
        candidate = rules(C119 / "files/AGENTS.md.txt")
        changed = {
            key
            for key in source
            if source[key] != candidate[key]
        }
        self.assertEqual(
            changed,
            {"VALIDATION_CLOSURE", "VALIDATION_PLAN", "METHOD"},
        )
        self.assertEqual(candidate["SPEC"], source["SPEC"])
        self.assertEqual(candidate["EVIDENCE_GATE"], source["EVIDENCE_GATE"])
        self.assertIn("validation_predicate_ready", candidate["VALIDATION_CLOSURE"])
        self.assertIn(
            "TaskSpecまたはcommand evidence protocolがexact commandを明示したvalidationだけ",
            candidate["VALIDATION_CLOSURE"],
        )
        self.assertIn(
            "missing validation identityまたはrepository evidenceの開放条件にせず",
            candidate["VALIDATION_PLAN"],
        )
        self.assertIn(
            "exact commandの選択だけを理由にrepository evidenceを追加しない",
            candidate["METHOD"],
        )
        for case_term in ("A01", "A02", "F01", "run.sh", "pytest"):
            self.assertNotIn(case_term, candidate["VALIDATION_CLOSURE"])
            self.assertNotIn(case_term, candidate["VALIDATION_PLAN"])
            self.assertNotIn(case_term, candidate["METHOD"])

    def test_manifest_and_design_bind_one_axis(self) -> None:
        manifest = verify_bundle(C119)
        self.assertEqual(
            manifest["bundle_sha256"],
            "26894d8cddaea8079ce15bcc7644691c2d14f0a042cd81bafb4e46d99478411c",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate118を直接親", design)
        self.assertIn("validation_predicate_ready", design)
        self.assertIn("Candidate107の`125,559`以下", design)
        self.assertIn("M=24", design)

    def test_targeted_profile_preserves_c118_conditions(self) -> None:
        source = json.loads(C118_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C119_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["iterations"], 5)
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "26894d8cddaea8079ce15bcc7644691c2d14f0a042cd81bafb4e46d99478411c",
                "name": "the-caption-3ce91a4-validation-predicate-method-boundary-r1",
                "revision": "r1",
            },
        )


if __name__ == "__main__":
    unittest.main()
