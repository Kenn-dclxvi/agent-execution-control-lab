from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-unstarted-read-completion-exclusion-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-result-dependency-exclusion-r1"
PROFILE = ROOT / "evaluations/profiles/candidate244-validation-result-dependency-exclusion-v14-reasoning-medium-f04-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/5311ccb065ff404b9f08ccacb23e2269.json"
MECHANISM = ROOT / "evaluations/results/candidate244-validation-result-dependency-exclusion-f04-n5-mechanism-audit-r1.json"


class Candidate244Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "e2ac41057d44d72f74ce89f569893723651cdbfd23ec9aa7180d4af0e0e39945",
        )

    def test_only_validation_closure_changed_from_retained_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        before_s, rest_s = source.split("### VALIDATION_CLOSURE\n", 1)
        _, after_s = rest_s.split("### VALIDATION_PLAN\n", 1)
        before_c, rest_c = candidate.split("### VALIDATION_CLOSURE\n", 1)
        boundary, after_c = rest_c.split("### VALIDATION_PLAN\n", 1)
        self.assertEqual(before_c, before_s)
        self.assertEqual(after_c, after_s)
        self.assertIn("途中結果を次の発行判断に使わない", boundary)
        self.assertIn("一つのshell commandへ結合してはならない", boundary)
        self.assertNotIn("custom exec wrapper", boundary)
        self.assertNotIn("model step", boundary)

    def test_f04_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["cases"],
            [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"]["bundle_sha256"],
            "e2ac41057d44d72f74ce89f569893723651cdbfd23ec9aa7180d4af0e0e39945",
        )

    def test_registered_result_and_mechanism_stop(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "5311ccb065ff404b9f08ccacb23e2269")
        self.assertEqual(result["median"]["total_tokens"], 281762)
        self.assertEqual([row["quality_score"] for row in result["case_results"]], [4] * 5)
        gate = mechanism["gates"]["required_validation_single_issuance_decision"]
        self.assertEqual(gate["pass_count"], 2)
        self.assertEqual(gate["failure_count"], 3)
        self.assertEqual(mechanism["status"], "mechanism_failed")
        self.assertGreater(result["median"]["total_tokens"], 151170)


if __name__ == "__main__":
    unittest.main()
