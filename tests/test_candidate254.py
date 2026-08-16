from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-start-check-same-model-step-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-independent-check-same-model-step-r1"
PROFILE = ROOT / "evaluations/profiles/candidate254-independent-check-same-model-step-v14-reasoning-medium-f04-m24-n5-cli0146-r1.json"
STANDARD14_N20_PROFILE = ROOT / "evaluations/profiles/candidate254-independent-check-same-model-step-v14-reasoning-medium-standard14-global-m24-n20-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/c22f1c7eda584010976ee4ce6647fc2f.json"
MECHANISM = ROOT / "evaluations/results/candidate254-independent-check-same-model-step-f04-n5-mechanism-audit-r1.json"
STANDARD14_N20_AUDIT = ROOT / "evaluations/results/candidate254-independent-check-same-model-step-standard14-n20-quality-audit-r1.json"


class Candidate254Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["bundle_sha256"], "7cd564be0904efb5cee59ce8d72935971d080282686e5ff7be9e85e62aa0fd52")

    def test_only_general_decision_boundary_sentence_added(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        added = (
            "受け取る結果によって次の作業の対象、許可、方法、停止条件が変わらないと既に分かっている複数の確認は、"
            "分割せず同一model stepから発行し、すべての結果を受け取った後に一度だけ次を判断する。\n\n"
        )
        self.assertEqual(candidate, source.replace("### DECISION_BOUNDARY\n\n", "### DECISION_BOUNDARY\n\n" + added))
        self.assertIn("開始確認と必要な読み取りを同一model stepから発行する", candidate)
        self.assertIn("途中結果をAIへ返してから", candidate)

    def test_f04_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["cases"], [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "7cd564be0904efb5cee59ce8d72935971d080282686e5ff7be9e85e62aa0fd52")

    def test_standard14_n20_profile(self) -> None:
        profile = json.loads(STANDARD14_N20_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["profile_id"],
            "candidate254-independent-check-same-model-step-v14-reasoning-medium-standard14-global-m24-n20-cli0146-r1",
        )
        self.assertEqual(len(profile["cases"]), 14)
        self.assertEqual(profile["iterations"], 20)
        self.assertEqual(profile["comparison_conditions"]["repetition_condition"]["iterations"], 20)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "7cd564be0904efb5cee59ce8d72935971d080282686e5ff7be9e85e62aa0fd52")

    def test_registered_result_and_mechanism_failure(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "c22f1c7eda584010976ee4ce6647fc2f")
        self.assertEqual(result["median"]["total_tokens"], 147796)
        self.assertEqual([row["quality_score"] for row in result["case_results"]], [4] * 5)
        gate = mechanism["gates"]["independent_checks_same_model_step"]
        self.assertEqual((gate["pass_count"], gate["failure_count"]), (4, 1))
        self.assertEqual(mechanism["status"], "mechanism_failed")
        self.assertLess(result["median"]["total_tokens"], 151170)

    def test_standard14_n20_quality_and_cost_diagnostics(self) -> None:
        audit = json.loads(STANDARD14_N20_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(audit["registered_result_id"], "2e40123a1b0642e3bbddb1812ba4414e")
        self.assertEqual(audit["selected_run_count"], 280)
        self.assertEqual(audit["selected_score_counts"], {"4": 280})
        self.assertEqual(audit["candidate147_reference"]["n100_result_id"], "e6fc6e10dedd47f5a1d59d114e6e0f57")
        self.assertAlmostEqual(
            audit["candidate254_n20_difference_from_candidate147_n20"]["total_tokens_percent"],
            9.325152221575069,
        )
        self.assertEqual(audit["diagnostic_counts"]["f02_runs_with_completion_wait"], 7)
        self.assertEqual(audit["diagnostic_counts"]["f03_runs_with_completion_wait"], 9)
        self.assertEqual(audit["diagnostic_counts"]["f03_start_check_and_read_split"], 6)


if __name__ == "__main__":
    unittest.main()
