from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-independent-check-same-model-step-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-same-artifact-second-continuation-exclusion-r1"
PROFILE = ROOT / "evaluations/profiles/candidate259-same-artifact-second-continuation-exclusion-v14-reasoning-medium-f04-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/7453ee7e3e0147d5871918a633d1a134.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate259-same-artifact-second-continuation-exclusion-f04-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate259-same-artifact-second-continuation-exclusion-f04-n5-mechanism-audit-r1.json"


class Candidate259Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["bundle_sha256"], "93d1874f285dc1381122248fd4786a13c05ce04ef976d39050cb8892f9616eac")

    def test_only_second_same_artifact_read_permission_sentence_added(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        anchor = "受け取る結果によって次の作業の対象、許可、方法、停止条件が変わらないと既に分かっている複数の確認は、分割せず同一model stepから発行し、すべての結果を受け取った後に一度だけ次を判断する。\n"
        added = "\n同じ変更方針を決めるために同じartifactを読み足せるのは一度だけであり、そのresultがmissingまたはunreadableでない限り、さらに同じartifactを読み足すpermissionはない。\n"
        self.assertEqual(candidate, source.replace(anchor, anchor + added))
        self.assertNotIn("残りの情報を取得する読み取り", candidate)
        self.assertNotIn("調査を発行できる単位", candidate)

    def test_f04_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["cases"], [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["name"], "the-caption-3ce91a4-same-artifact-second-continuation-exclusion-r1")
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "93d1874f285dc1381122248fd4786a13c05ce04ef976d39050cb8892f9616eac")

    def test_f04_n5_result_and_quality(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "7453ee7e3e0147d5871918a633d1a134")
        self.assertEqual(result["compatibility_key"], "1a3b75ac2311cda9630a15db6ee0ab8c3d8e51bb46d4c63c44954fc5a958c24a")
        self.assertEqual(result["median"]["total_tokens"], 145917)
        self.assertEqual([item["quality_score"] for item in result["case_results"]], [4] * 5)
        self.assertEqual(quality["score_counts"], {"4": 5})

    def test_f04_n5_mechanism_passed(self) -> None:
        audit = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(audit["status"], "mechanism_passed")
        self.assertEqual(audit["gates"]["start_check_same_model_step_joint_issuance"]["pass_count"], 5)
        self.assertEqual(audit["gates"]["independent_checks_same_model_step"]["pass_count"], 5)
        self.assertEqual(audit["gates"]["same_artifact_second_continuation_exclusion"]["pass_count"], 5)
        self.assertEqual(audit["gates"]["required_validation_single_issuance_decision"]["pass_count"], 5)


if __name__ == "__main__":
    unittest.main()
