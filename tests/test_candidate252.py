from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-result-ai-return-exclusion-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-start-check-static-stop-scope-r1"
PROFILE = ROOT / "evaluations/profiles/candidate252-start-check-static-stop-scope-v14-reasoning-medium-f04-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/50b096f7f02f4f56a27babe8d63610aa.json"
MECHANISM = ROOT / "evaluations/results/candidate252-start-check-static-stop-scope-f04-n5-mechanism-audit-r1.json"


class Candidate252Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["bundle_sha256"], "3642a4bc9b996339ca7f6b0bcb999ea80cd86dd06117a635d756c10acacaffe1")

    def test_only_decision_boundary_changed_from_retained_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        before_s, rest_s = source.split("### DECISION_BOUNDARY\n", 1)
        _, after_s = rest_s.split("### VALIDATION_CLOSURE\n", 1)
        before_c, rest_c = candidate.split("### DECISION_BOUNDARY\n", 1)
        boundary, after_c = rest_c.split("### VALIDATION_CLOSURE\n", 1)
        self.assertEqual(before_c, before_s)
        self.assertEqual(after_c, after_s)
        self.assertIn("停止条件が変更や必須コマンドだけを禁じ", boundary)
        self.assertIn("開始確認と必要な読み取りを同じ判断から発行する", boundary)
        self.assertIn("停止条件が読み取りも禁じるか", boundary)
        self.assertIn("対象または許可が変わり得る場合だけ", boundary)
        self.assertNotIn("model step", boundary)
        self.assertIn("途中結果をAIへ返してから", after_c)

    def test_f04_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["cases"], [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "3642a4bc9b996339ca7f6b0bcb999ea80cd86dd06117a635d756c10acacaffe1")

    def test_registered_result_and_mechanism_failure(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "50b096f7f02f4f56a27babe8d63610aa")
        self.assertEqual(result["median"]["total_tokens"], 191361)
        self.assertEqual([row["quality_score"] for row in result["case_results"]], [4] * 5)
        joint_gate = mechanism["gates"]["start_check_static_stop_scope_joint_issuance"]
        validation_gate = mechanism["gates"]["required_validation_single_issuance_decision"]
        self.assertEqual((joint_gate["pass_count"], joint_gate["failure_count"]), (1, 4))
        self.assertEqual((validation_gate["pass_count"], validation_gate["failure_count"]), (5, 0))
        self.assertEqual(mechanism["status"], "mechanism_failed")
        self.assertGreater(result["median"]["total_tokens"], 151170)


if __name__ == "__main__":
    unittest.main()
