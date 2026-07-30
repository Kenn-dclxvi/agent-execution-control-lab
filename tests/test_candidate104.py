from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C98 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-completion-sheet-r1"
C104 = ROOT / "prompts/candidates/the-caption-3ce91a4-staged-evidence-admission-r1"
DESIGN = ROOT / "docs/candidate104-staged-evidence-admission-design.md"
C103_PROFILE = ROOT / "evaluations/profiles/candidate103-prechange-evidence-receipt-v14-reasoning-medium-f07-canonical-global-m24-n5-cli0146-r1.json"
C104_PROFILE = ROOT / "evaluations/profiles/candidate104-staged-evidence-admission-v14-reasoning-medium-a02-f07-global-m24-n5-cli0146-r1.json"
C81_STANDARD_PROFILE = ROOT / "evaluations/profiles/candidate81-validation-wrapper-precedence-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r2.json"
C104_STANDARD_PROFILE = ROOT / "evaluations/profiles/candidate104-staged-evidence-admission-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate104Test(unittest.TestCase):
    def test_is_direct_c98_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C98)
        candidate = verify_bundle(C104)
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

    def test_adds_only_one_staged_evidence_rule(self) -> None:
        source = rules(C98 / "files/AGENTS.md.txt")
        candidate = rules(C104 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate) - set(source), {"EVIDENCE_GATE"})
        self.assertEqual({key: candidate[key] for key in source}, source)
        rule = candidate["EVIDENCE_GATE"]
        self.assertIn("default deny", rule)
        self.assertIn("TaskSpec明示の開始状態の直接観測", rule)
        self.assertIn("requested outcome valueが未固定", rule)
        self.assertIn("authority invocationを一件", rule)
        self.assertIn("変更前evidence operationをterminal", rule)
        self.assertIn("一般的安全確認は開放条件にしない", rule)
        for case_specific_term in ("F07", "A02", "run.sh", "git log", "main_verify.sh"):
            self.assertNotIn(case_specific_term, rule)

    def test_manifest_and_design_bind_one_axis(self) -> None:
        manifest = verify_bundle(C104)
        self.assertEqual(
            manifest["bundle_sha256"],
            "b25d13fb2f9d598adfae2359bd5cfbcef2591731d07e9165b1f9b3fc83e036b0",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate98を直接親", design)
        self.assertIn("prompt lineageには含めない", design)
        self.assertIn("設定上の`M=24`", design)
        self.assertIn("既存C81 resultは再実行しない", design)

    def test_profile_preserves_conditions_and_adds_a02_coverage(self) -> None:
        source = json.loads(C103_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C104_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(candidate["comparison_conditions"]["repetition_condition"]["iterations"], 5)
        self.assertEqual(
            candidate["cases"],
            [
                {"id": "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING", "revision": "r2"},
                {"id": "TC-F07-CANONICAL-V4-RUNNER", "revision": "r2"},
            ],
        )
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "b25d13fb2f9d598adfae2359bd5cfbcef2591731d07e9165b1f9b3fc83e036b0",
                "name": "the-caption-3ce91a4-staged-evidence-admission-r1",
                "revision": "r1",
            },
        )

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C81_STANDARD_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C104_STANDARD_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["execution"], source["execution"])
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "b25d13fb2f9d598adfae2359bd5cfbcef2591731d07e9165b1f9b3fc83e036b0",
                "name": "the-caption-3ce91a4-staged-evidence-admission-r1",
                "revision": "r1",
            },
        )


if __name__ == "__main__":
    unittest.main()
