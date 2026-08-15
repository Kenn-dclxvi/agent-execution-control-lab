from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-result-ai-return-exclusion-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-start-check-joint-issuance-boundary-r1"
PROFILE = ROOT / "evaluations/profiles/candidate251-start-check-joint-issuance-boundary-v14-reasoning-medium-f04-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/a56cefa0e70e46c0a352eb8f7a9e068a.json"
MECHANISM = ROOT / "evaluations/results/candidate251-start-check-joint-issuance-boundary-f04-n5-mechanism-audit-r1.json"


class Candidate251Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["bundle_sha256"], "a6d25f4930f5a4f6af59fdfbc901565ab3feb3c115530d936be1912f479d5707")

    def test_only_decision_boundary_changed_from_retained_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        before_s, rest_s = source.split("### DECISION_BOUNDARY\n", 1)
        _, after_s = rest_s.split("### VALIDATION_CLOSURE\n", 1)
        before_c, rest_c = candidate.split("### DECISION_BOUNDARY\n", 1)
        boundary, after_c = rest_c.split("### VALIDATION_CLOSURE\n", 1)
        self.assertEqual(before_c, before_s)
        self.assertEqual(after_c, after_s)
        self.assertIn("その確認と同じ判断から発行する", boundary)
        self.assertIn("確認後へ分けられるのは", boundary)
        self.assertIn("読み取りが禁止されるか、対象または許可が変わり得る場合だけ", boundary)
        self.assertNotIn("model step", boundary)
        self.assertNotIn("command", boundary)
        self.assertIn("途中結果をAIへ返してから", after_c)

    def test_f04_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["cases"], [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "a6d25f4930f5a4f6af59fdfbc901565ab3feb3c115530d936be1912f479d5707")

    def test_registered_result_and_partial_mechanism_effect(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "a56cefa0e70e46c0a352eb8f7a9e068a")
        self.assertEqual(result["median"]["total_tokens"], 173626)
        self.assertEqual([row["quality_score"] for row in result["case_results"]], [4] * 5)
        joint_gate = mechanism["gates"]["start_check_joint_issuance_boundary"]
        validation_gate = mechanism["gates"]["required_validation_single_issuance_decision"]
        self.assertEqual((joint_gate["pass_count"], joint_gate["failure_count"]), (2, 3))
        self.assertEqual((validation_gate["pass_count"], validation_gate["failure_count"]), (3, 2))
        self.assertEqual(mechanism["status"], "mechanism_failed")
        self.assertGreater(result["median"]["total_tokens"], 151170)


if __name__ == "__main__":
    unittest.main()
