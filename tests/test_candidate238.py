from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-taskspec-progress-suppression-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-independent-result-prerequisite-exclusion-r1"
PROFILE = ROOT / "evaluations/profiles/candidate238-independent-result-prerequisite-exclusion-v14-reasoning-medium-a02-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/d4cd0d9aec174d2fabf6743deb32d65c.json"
MECHANISM = ROOT / "evaluations/results/candidate238-independent-result-prerequisite-exclusion-a02-n5-mechanism-audit-r1.json"


class Candidate238Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "1dfca2ca29c0a66af6c11f956c231c80622322c0e5a008d9bf6f35d13152f8f9",
        )

    def test_only_decision_boundary_changes_from_candidate237_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        before_s, rest_s = source.split("### DECISION_BOUNDARY\n", 1)
        _, after_s = rest_s.split("### VALIDATION_CLOSURE\n", 1)
        before_c, rest_c = candidate.split("### DECISION_BOUNDARY\n", 1)
        boundary, after_c = rest_c.split("### VALIDATION_CLOSURE\n", 1)
        self.assertEqual(before_c, before_s)
        self.assertEqual(after_c, after_s)
        self.assertIn("そのresultはreadの先行条件ではない", boundary)
        self.assertIn("影響しない作業の間に待機依存を作るため許可しない", boundary)
        self.assertNotIn("同じmodel stepで発行", boundary)
        self.assertNotIn("readを後のstepへ分ける", boundary)

    def test_a02_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["cases"],
            [{"id": "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING", "revision": "r2"}],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"]["bundle_sha256"],
            "1dfca2ca29c0a66af6c11f956c231c80622322c0e5a008d9bf6f35d13152f8f9",
        )

    def test_result_records_quality_pass_and_mechanism_failure(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "d4cd0d9aec174d2fabf6743deb32d65c")
        self.assertEqual(result["median"]["total_tokens"], 183521)
        self.assertEqual(mechanism["gates"]["a02_unaffected_read_did_not_wait_for_start_result"]["pass_count"], 0)
        self.assertEqual(mechanism["gates"]["a02_unaffected_read_did_not_wait_for_start_result"]["failure_count"], 5)
        self.assertEqual(mechanism["status"], "mechanism_failed")


if __name__ == "__main__":
    unittest.main()
