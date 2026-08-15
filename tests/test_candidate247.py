from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-result-ai-return-exclusion-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-start-result-read-return-exclusion-r1"
PROFILE = ROOT / "evaluations/profiles/candidate247-start-result-read-return-exclusion-v14-reasoning-medium-f04-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/c916f9138a3c4163af9d7fff527d9cfd.json"
MECHANISM = ROOT / "evaluations/results/candidate247-start-result-read-return-exclusion-f04-n5-mechanism-audit-r1.json"


class Candidate247Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["bundle_sha256"], "cd5a394c376026a9b4c47fb5eb1b3f053e682ed8deaf4f8198e0620e9d36f261")

    def test_only_decision_boundary_changed_from_retained_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        before_s, rest_s = source.split("### DECISION_BOUNDARY\n", 1)
        _, after_s = rest_s.split("### VALIDATION_CLOSURE\n", 1)
        before_c, rest_c = candidate.split("### DECISION_BOUNDARY\n", 1)
        boundary, after_c = rest_c.split("### VALIDATION_CLOSURE\n", 1)
        self.assertEqual(before_c, before_s)
        self.assertEqual(after_c, after_s)
        self.assertIn("対象、許可、必要性が変わらない", boundary)
        self.assertIn("その結果をAIへ返してから着手してはならない", boundary)
        self.assertIn("途中結果をAIへ返してから", after_c)

    def test_f04_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["cases"], [{"id": "TC-F04-WEB-AUDIT-COLUMN-VISIBILITY", "revision": "r2"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "cd5a394c376026a9b4c47fb5eb1b3f053e682ed8deaf4f8198e0620e9d36f261")

    def test_registered_result_and_mechanism_failure(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "c916f9138a3c4163af9d7fff527d9cfd")
        self.assertEqual(result["median"]["total_tokens"], 256392)
        self.assertEqual([row["quality_score"] for row in result["case_results"]], [4] * 5)
        start_gate = mechanism["gates"]["start_result_read_return_exclusion"]
        validation_gate = mechanism["gates"]["required_validation_single_issuance_decision"]
        self.assertEqual((start_gate["pass_count"], start_gate["failure_count"]), (0, 5))
        self.assertEqual((validation_gate["pass_count"], validation_gate["failure_count"]), (2, 3))
        self.assertEqual(mechanism["status"], "mechanism_failed")
        self.assertGreater(result["median"]["total_tokens"], 151170)


if __name__ == "__main__":
    unittest.main()
