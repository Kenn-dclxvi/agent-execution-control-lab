from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-ten-principle-execution-control-r1"
DESIGN = ROOT / "docs/candidate225-ten-principle-execution-control-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate225-ten-principle-execution-control-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/89c3babd670c461f8b075e7c9a329248.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate225-ten-principle-execution-control-standard14-n5-quality-audit-r1.json"
RESULT_NOTE = ROOT / "evaluations/results/candidate225-ten-principle-execution-control-standard14-n5_2026-08-14.md"


class Candidate225Test(unittest.TestCase):
    def test_c147_direct_reconstruction_changes_only_root_agents(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(candidate["artifact"]["state"], "evaluation_ready")
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "50d5c742bbf2c983aaa4bf084dfabd810025a023523376323258c124f479613a",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_user_supplied_ten_sections_are_preserved(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        headings = [line for line in text.splitlines() if line.startswith("### ")]
        self.assertEqual(len(headings), 10)
        for fragment in (
            "利用者判断と実装選択を分離する",
            "未完了の結果を推測で補完しない",
            "結果と停止の影響範囲を局所化する",
            "検証を一方向に完了させる",
            "手段の失敗と権限の拒否を区別する",
            "環境起因の失敗だけを限定的に回復する",
        ):
            self.assertIn(fragment, text)

    def test_design_and_profile_bind_standard14_n5(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertIn("14ケース×N=5", design)
        self.assertIn("Candidate214からCandidate224までのreview制御は継承しない", design)
        self.assertEqual(profile["evaluation_set"]["set_id"], "the-caption-standard14-r1")
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"]["bundle_sha256"],
            verify_bundle(CANDIDATE)["bundle_sha256"],
        )

    def test_standard14_n5_result_is_registered(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        audit = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "89c3babd670c461f8b075e7c9a329248")
        self.assertEqual(result["prompt_set_identity"]["name"], CANDIDATE.name)
        self.assertEqual(result["prompt_set_identity"]["bundle_sha256"], verify_bundle(CANDIDATE)["bundle_sha256"])
        self.assertEqual(len(result["case_results"]), 70)
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(result["median"]["total_tokens"], 3_077_793)
        self.assertAlmostEqual(result["median"]["elapsed_seconds"], 1021.6477944179787)
        self.assertEqual(audit["run_count"], 70)
        self.assertEqual(audit["rateable_runs"], 70)
        self.assertEqual(audit["score_counts"], {"4": 70})
        self.assertEqual(audit["failure_counts"], {})

        note = RESULT_NOTE.read_text(encoding="utf-8")
        self.assertIn(RESULT.name, note)
        self.assertIn(QUALITY_AUDIT.name, note)
        self.assertIn("c498dd3944534631a80e70a814fc8171", note)
        self.assertIn("+142,068（+4.84%）", note)
        self.assertIn("-77.647秒（-7.06%）", note)
        self.assertIn(RESULT_NOTE.name, (ROOT / "evaluations/results/README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
