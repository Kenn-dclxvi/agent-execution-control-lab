from __future__ import annotations

import json
import unittest
from collections import Counter
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
STANDARD14_PROFILE = ROOT / "evaluations/profiles/candidate259-same-artifact-second-continuation-exclusion-v14-reasoning-medium-standard14-global-m24-n5-cli0146-r1.json"
STANDARD14_RESULT = ROOT / "evaluations/results/1d27ee8fc6b74946aa76132aee5478aa.json"
STANDARD14_QUALITY_AUDIT = ROOT / "evaluations/results/candidate259-same-artifact-second-continuation-exclusion-standard14-n5-quality-audit-r1.json"


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

    def test_standard14_profile(self) -> None:
        profile = json.loads(STANDARD14_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(len(profile["cases"]), 14)
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "bundle_sha256": "93d1874f285dc1381122248fd4786a13c05ce04ef976d39050cb8892f9616eac",
                "name": "the-caption-3ce91a4-same-artifact-second-continuation-exclusion-r1",
                "revision": "r1",
            },
        )

    def test_standard14_n5_result_and_quality(self) -> None:
        result = json.loads(STANDARD14_RESULT.read_text(encoding="utf-8"))
        quality = json.loads(STANDARD14_QUALITY_AUDIT.read_text(encoding="utf-8"))

        self.assertEqual(result["result_id"], "1d27ee8fc6b74946aa76132aee5478aa")
        self.assertEqual(
            result["result_content_sha256"],
            "ef7981f7481bab264b3bc6c68cab1c3f5bb8705df97d41ec04589ce224206a3a",
        )
        self.assertEqual(
            result["compatibility_key"],
            "cc0c022ac026b55c51597e82c4a7216d4b7fdf498250c6a299d24203f1027561",
        )
        self.assertEqual(len(result["case_results"]), 70)
        self.assertEqual(
            Counter(item["case_id"] for item in result["case_results"]),
            Counter({case: 5 for case in result["compatibility"]["coverage"]["case_ids"]}),
        )
        self.assertTrue(all(item["quality_score"] == 4 for item in result["case_results"]))
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(result["median"]["total_tokens"], 1510151)
        self.assertAlmostEqual(result["median"]["elapsed_seconds"], 795.3871456260094)

        self.assertEqual(quality["run_count"], 70)
        self.assertEqual(quality["rateable_runs"], 70)
        self.assertEqual(quality["score_counts"], {"4": 70})
        self.assertEqual(quality["failure_counts"], {})
        self.assertEqual(quality["diagnostic_counts"]["command_protocol_violations"], 0)
        self.assertEqual(
            {(item["run_id"], item["case_id"]) for item in result["case_results"]},
            {(item["run_id"], item["case_id"]) for item in quality["runs"]},
        )


if __name__ == "__main__":
    unittest.main()
