from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-result-ai-return-exclusion-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-start-check-read-interposed-boundary-exclusion-r1"
PROFILE = ROOT / "evaluations/profiles/candidate249-start-check-read-interposed-boundary-exclusion-v14-reasoning-medium-f04-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/ddc840b8bba54a75b63d681d8e4f34ec.json"
MECHANISM = ROOT / "evaluations/results/candidate249-start-check-read-interposed-boundary-exclusion-f04-n5-mechanism-audit-r1.json"


class Candidate249Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["bundle_sha256"], "bedfb4f5b91c1d65300950bdeef10972e0502be3e8da05f6b2f6739a5453a0e0")

    def test_only_decision_boundary_changed_from_retained_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        before_s, rest_s = source.split("### DECISION_BOUNDARY\n", 1)
        _, after_s = rest_s.split("### VALIDATION_CLOSURE\n", 1)
        before_c, rest_c = candidate.split("### DECISION_BOUNDARY\n", 1)
        boundary, after_c = rest_c.split("### VALIDATION_CLOSURE\n", 1)
        self.assertEqual(before_c, before_s)
        self.assertEqual(after_c, after_s)
        self.assertIn("禁止、対象、許可が変わらない", boundary)
        self.assertIn("完了、待機、結果受領の境界", boundary)
        self.assertNotIn("AI", boundary)
        self.assertIn("途中結果をAIへ返してから", after_c)

    def test_f04_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["cases"], [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "bedfb4f5b91c1d65300950bdeef10972e0502be3e8da05f6b2f6739a5453a0e0")

    def test_registered_result_and_mechanism_failure(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "ddc840b8bba54a75b63d681d8e4f34ec")
        self.assertEqual(result["median"]["total_tokens"], 254089)
        self.assertEqual([row["quality_score"] for row in result["case_results"]], [4] * 5)
        start_gate = mechanism["gates"]["start_check_read_interposed_boundary_exclusion"]
        validation_gate = mechanism["gates"]["required_validation_single_issuance_decision"]
        self.assertEqual((start_gate["pass_count"], start_gate["failure_count"]), (0, 5))
        self.assertEqual((validation_gate["pass_count"], validation_gate["failure_count"]), (2, 3))
        self.assertEqual(mechanism["status"], "mechanism_failed")
        self.assertGreater(result["median"]["total_tokens"], 151170)


if __name__ == "__main__":
    unittest.main()
