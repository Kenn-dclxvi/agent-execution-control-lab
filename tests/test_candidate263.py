from __future__ import annotations

import unittest
import json
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-independent-check-same-model-step-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-dependency-closure-r1"
PROFILE = ROOT / "evaluations/profiles/candidate263-result-effect-dependency-closure-v14-reasoning-medium-f03-f10-entrypoint-global-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/478d39fb4327490e8d9c2202bff66e43.json"
QUALITY = ROOT / "evaluations/results/candidate263-result-effect-dependency-closure-f03-f10-entrypoint-n5-quality-audit-r1.json"
MECHANISM = ROOT / "evaluations/results/candidate263-result-effect-dependency-closure-f03-f10-entrypoint-n5-mechanism-audit-r1.json"


class Candidate263Test(unittest.TestCase):
    def test_candidate254_is_direct_parent(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], parent["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "4fd4bb75be18f7882df98368898d38759a9a37336269e61f4f0eef6d77f4841e",
        )

    def test_only_general_decision_boundary_is_replaced(self) -> None:
        parent = (PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        old = (
            "受け取る結果によって次の作業の対象、許可、方法、停止条件が変わらないと既に分かっている複数の確認は、"
            "分割せず同一model stepから発行し、すべての結果を受け取った後に一度だけ次を判断する。"
        )
        new = (
            "`result_effect_scope`は、受領resultが後続operationの対象、許可、方法または停止条件を変え得る"
            "未発行operationの種類だけを含む。後続operationを先行resultの待機対象にできるのは、その種類が"
            "`result_effect_scope`に含まれる場合だけとする。含まれない既知の相互非依存operationは分割せず"
            "同一model stepから発行し、全result受領後に一度だけ次を判断する。"
        )
        self.assertIn(old, parent)
        self.assertEqual(candidate, parent.replace(old, new))
        self.assertIn("開始確認と必要な読み取りを同一model stepから発行する", candidate)
        self.assertIn("途中結果をAIへ返してから", candidate)
        self.assertNotIn("Candidate147", candidate)
        self.assertNotIn("Candidate261", candidate)
        self.assertNotIn("Candidate262", candidate)

    def test_targeted_profile_and_result(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["cases"],
            [
                {"id": "TC-F03-ATOMIC-CONTEXT-CLEANUP", "revision": "r2"},
                {"id": "TC-F10-ENTRYPOINT-INVENTORY-REVIEW", "revision": "r1"},
            ],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "4fd4bb75be18f7882df98368898d38759a9a37336269e61f4f0eef6d77f4841e")
        self.assertEqual(result["result_id"], "478d39fb4327490e8d9c2202bff66e43")
        self.assertEqual([row["quality_score"] for row in result["case_results"]], [4] * 10)
        self.assertEqual(result["median"]["total_tokens"], 270323)

    def test_quality_passed_but_mechanism_did_not_improve(self) -> None:
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(quality["run_count"], 10)
        self.assertEqual(quality["rateable_runs"], 10)
        self.assertEqual(quality["score_counts"], {"4": 10})
        f03 = mechanism["gates"]["f03_unaffected_start_result_did_not_delay_required_read"]
        f10 = mechanism["gates"]["f10_instruction_result_preceded_entrypoint_content_when_permission_could_change"]
        self.assertEqual((f03["candidate263"]["pass_count"], f03["candidate263"]["failure_count"]), (3, 2))
        self.assertEqual((f03["candidate254_reference"]["pass_count"], f03["candidate254_reference"]["failure_count"]), (3, 2))
        self.assertEqual((f10["candidate263"]["pass_count"], f10["candidate263"]["failure_count"]), (3, 2))
        self.assertEqual((f10["candidate254_reference"]["pass_count"], f10["candidate254_reference"]["failure_count"]), (3, 2))
        self.assertEqual(mechanism["status"], "mechanism_failed_no_rate_improvement")


if __name__ == "__main__":
    unittest.main()
