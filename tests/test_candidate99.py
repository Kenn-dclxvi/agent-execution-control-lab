from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C98 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-completion-sheet-r1"
C99 = ROOT / "prompts/candidates/the-caption-3ce91a4-decision-evidence-boundary-r1"
DESIGN = ROOT / "docs/candidate99-decision-evidence-boundary-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate99-decision-evidence-boundary-v14-reasoning-medium-f07-canonical-global-m24-n5-cli0146-r1.json"
C81_PROFILE = ROOT / "evaluations/profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r2.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate99Test(unittest.TestCase):
    def test_is_direct_c98_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C98)
        candidate = verify_bundle(C99)
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

    def test_adds_only_evidence_scope_boundary(self) -> None:
        source = rules(C98 / "files/AGENTS.md.txt")
        candidate = rules(C99 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate) - set(source), {"EVIDENCE_SCOPE"})
        self.assertEqual({key: candidate[key] for key in source}, source)

        rule = candidate["EVIDENCE_SCOPE"]
        self.assertIn("各predicateの判断入力", rule)
        self.assertIn("履歴、対象外探索、未bindのtool output", rule)
        self.assertIn("未取得evidence identityとconsumer predicate", rule)
        self.assertLess(len(rule), 230)
        for case_specific_term in (
            "F07",
            "run.sh",
            "git log",
            "scripts/dev/main_verify.sh",
        ):
            self.assertNotIn(case_specific_term, rule)

    def test_manifest_and_design_keep_the_boundary_separate_from_method(self) -> None:
        manifest = verify_bundle(C99)
        self.assertEqual(
            manifest["bundle_sha256"],
            "482bdd3e17523f3640dacb5d1adfc68023a790b3890f47ce1748782b3b156bd1",
        )
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")

        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("command名や読取回数ではなく、predicateが消費できる入力の所属", design)
        self.assertIn("TaskSpec、repository authority、required validationの変更", design)
        self.assertIn("完全一致のpreflight receiptがない場合は一件も発行しない", design)
        self.assertIn("設定上の`M=24`", design)
        self.assertIn("targeted F07", design)

    def test_f07_profile_reuses_c81_conditions_with_fixed_m24(self) -> None:
        baseline = json.loads(C81_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["comparison_conditions"], baseline["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], baseline["evaluation_set"])
        self.assertEqual(
            candidate["cases"],
            [{"id": "TC-F07-CANONICAL-V4-RUNNER", "revision": "r2"}],
        )
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["comparison_conditions"]["repetition_condition"]["iterations"],
            5,
        )
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "482bdd3e17523f3640dacb5d1adfc68023a790b3890f47ce1748782b3b156bd1",
                "name": "the-caption-3ce91a4-decision-evidence-boundary-r1",
                "revision": "r1",
            },
        )


if __name__ == "__main__":
    unittest.main()
