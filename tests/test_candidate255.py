from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-independent-check-same-model-step-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-partial-evidence-result-exclusion-r1"
PROFILE = ROOT / "evaluations/profiles/candidate255-partial-evidence-result-exclusion-v14-reasoning-medium-f04-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/51f9afed64664f009c99a3a35ecac89a.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate255-partial-evidence-result-exclusion-f04-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate255-partial-evidence-result-exclusion-f04-n5-mechanism-audit-r1.json"


class Candidate255Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["bundle_sha256"], "7578b10d76cb3aab15f36e0ae7b50a270f5798d6e6837595e041fa8ccec85fa3")

    def test_only_partial_read_exclusion_sentence_added(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        anchor = (
            "repository内の調査や証拠取得は、作業のどの段階でも原則として行わない。必要な判定がまだ終わっておらず、状態が`unobserved`で、"
            "現在欠けている具体的な観測値が決まっており、取得する結果だけでその状態を確定できる場合に限って行う。"
            "状態は`satisfied`、`unsatisfied`、`unobserved`の三つとする。この制限は、対象探索、変更前後の調査、validation準備、recoveryのすべてに適用する。\n"
        )
        added = "\n一回の調査resultだけで現在欠けている観測値を確定できない部分readは発行しない。\n"
        self.assertEqual(candidate, source.replace(anchor, anchor + added))
        self.assertIn("分割せず同一model stepから発行し", candidate)
        self.assertIn("開始確認と必要な読み取りを同一model stepから発行する", candidate)
        self.assertIn("途中結果をAIへ返してから", candidate)

    def test_f04_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["cases"], [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "7578b10d76cb3aab15f36e0ae7b50a270f5798d6e6837595e041fa8ccec85fa3")

    def test_f04_n5_result_and_quality(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(len(result["case_results"]), 5)
        self.assertEqual([item["quality_score"] for item in result["case_results"]], [4] * 5)
        self.assertEqual(quality["score_counts"], {"4": 5})
        self.assertEqual(sorted(item["total_tokens"] for item in result["case_results"])[2], 152970)

    def test_f04_n5_mechanism_failed(self) -> None:
        audit = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(audit["status"], "mechanism_failed")
        self.assertEqual(audit["gates"]["start_check_same_model_step_joint_issuance"]["pass_count"], 3)
        self.assertEqual(audit["gates"]["independent_checks_same_model_step"]["pass_count"], 3)
        self.assertEqual(audit["gates"]["partial_evidence_result_exclusion"]["pass_count"], 3)
        self.assertEqual(audit["gates"]["required_validation_single_issuance_decision"]["pass_count"], 4)


if __name__ == "__main__":
    unittest.main()
