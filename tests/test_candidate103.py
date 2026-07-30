from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
C98 = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-completion-sheet-r1"
C103 = ROOT / "prompts/candidates/the-caption-3ce91a4-prechange-evidence-receipt-r1"
DESIGN = ROOT / "docs/candidate103-prechange-evidence-receipt-design.md"
C102_PROFILE = ROOT / "evaluations/profiles/candidate102-prechange-evidence-freeze-v14-reasoning-medium-f07-canonical-global-m24-n5-cli0146-r1.json"
C103_PROFILE = ROOT / "evaluations/profiles/candidate103-prechange-evidence-receipt-v14-reasoning-medium-f07-canonical-global-m24-n5-cli0146-r1.json"


def rules(path: Path) -> dict[str, str]:
    return {
        line[2:].split(": ", 1)[0]: line[2:].split(": ", 1)[1]
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ") and ": " in line
    }


class Candidate103Test(unittest.TestCase):
    def test_is_direct_c98_child_with_only_root_changed(self) -> None:
        source = verify_bundle(C98)
        candidate = verify_bundle(C103)
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

    def test_replaces_only_spec_with_model_visible_receipt(self) -> None:
        source = rules(C98 / "files/AGENTS.md.txt")
        candidate = rules(C103 / "files/AGENTS.md.txt")
        self.assertEqual(set(candidate), set(source))
        self.assertEqual(
            {key: candidate[key] for key in source if key != "SPEC"},
            {key: source[key] for key in source if key != "SPEC"},
        )
        rule = candidate["SPEC"]
        self.assertIn("最初のinvocation前", rule)
        self.assertIn("PRECHANGE_RECEIPT", rule)
        self.assertIn("model-visible response", rule)
        self.assertIn("resultにより変わる後続判断", rule)
        self.assertIn("receiptにない変更前invocationは発行しない", rule)
        self.assertIn("permission / allowed read / available tool / repository authority", rule)
        for case_specific_term in ("F07", "run.sh", "git log", "main_verify.sh"):
            self.assertNotIn(case_specific_term, rule)

    def test_manifest_and_design_bind_one_replacement_axis(self) -> None:
        manifest = verify_bundle(C103)
        self.assertEqual(
            manifest["bundle_sha256"],
            "e3acc82d0712db6c2834dc69d154a50f470cc119db2db0bb2ed1ceb6cbfede8f",
        )
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate98を直接親", design)
        self.assertIn("prompt lineageには含めない", design)
        self.assertIn("外部executor artifactにはしない", design)
        self.assertIn("設定上の`M=24`", design)

    def test_f07_profile_changes_only_prompt_identity(self) -> None:
        source = json.loads(C102_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(C103_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(candidate["cases"], source["cases"])
        self.assertEqual(candidate["comparison_conditions"], source["comparison_conditions"])
        self.assertEqual(candidate["evaluation_set"], source["evaluation_set"])
        self.assertEqual(candidate["execution"], source["execution"])
        self.assertEqual(candidate["execution"]["max_workers"], 24)
        self.assertEqual(
            candidate["prompt_set_identity"],
            {
                "bundle_sha256": "e3acc82d0712db6c2834dc69d154a50f470cc119db2db0bb2ed1ceb6cbfede8f",
                "name": "the-caption-3ce91a4-prechange-evidence-receipt-r1",
                "revision": "r1",
            },
        )


if __name__ == "__main__":
    unittest.main()
