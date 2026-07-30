from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C98 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-completion-sheet-r1"
C100 = ROOT / "prompts/candidates/the-caption-3ce91a4-outcome-source-closure-r1"
DESIGN = ROOT / "docs/candidate100-outcome-source-closure-design.md"
C99_PROFILE = ROOT / "evaluations/profiles/candidate99-decision-evidence-boundary-v14-reasoning-medium-f07-canonical-global-m24-n5-cli0146-r1.json"
C100_PROFILE = ROOT / "evaluations/profiles/candidate100-outcome-source-closure-v14-reasoning-medium-f07-canonical-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate100Test(unittest.TestCase):
    def test_is_direct_c98_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C98)
        candidate = verify_bundle(C100)
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

    def test_adds_only_outcome_source(self) -> None:
        source = rules(C98 / "files/AGENTS.md.txt")
        candidate = rules(C100 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate) - set(source), {"OUTCOME_SOURCE"})
        self.assertEqual({key: candidate[key] for key in source}, source)

        rule = candidate["OUTCOME_SOURCE"]
        self.assertIn("requested outcome value", rule)
        self.assertIn("再決定 / 再確認しない", rule)
        self.assertIn("target artifactはcurrent stateだけ", rule)
        self.assertIn("変更前調査を終了", rule)
        self.assertIn("missing factとconsumer predicate", rule)
        for case_specific_term in (
            "F07",
            "run.sh",
            "git log",
            "scripts/dev/main_verify.sh",
        ):
            self.assertNotIn(case_specific_term, rule)

    def test_manifest_and_design_bind_one_addition_axis(self) -> None:
        manifest = verify_bundle(C100)
        self.assertEqual(
            manifest["bundle_sha256"],
            "b4c260e5c18c8b5fdc3d005fe931f531c4328a222111f0522d33f0ba71683df3",
        )
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate98を直接親", design)
        self.assertIn("Candidate99は失敗経路を確認した観測証拠", design)
        self.assertIn("5 / 5 score `4`", design)
        self.assertIn("設定上の`M=24`", design)
        self.assertIn("TaskSpec、fixture、rating", design)
        self.assertIn("targeted gate通過前にStandard14またはB20へ進めない", design)

    def test_f07_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C99_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C100_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["execution"], source["execution"])
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "b4c260e5c18c8b5fdc3d005fe931f531c4328a222111f0522d33f0ba71683df3",
                "name": "the-caption-3ce91a4-outcome-source-closure-r1",
                "revision": "r1",
            },
        )


if __name__ == "__main__":
    unittest.main()
