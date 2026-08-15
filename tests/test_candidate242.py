from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-taskspec-progress-suppression-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-start-check-only-completion-exclusion-r1"
PROFILE = ROOT / "evaluations/profiles/candidate242-start-check-only-completion-exclusion-v14-reasoning-medium-a02-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/f5f78ea591414f949e33d0c84edf4665.json"
MECHANISM = ROOT / "evaluations/results/candidate242-start-check-only-completion-exclusion-a02-n5-mechanism-audit-r1.json"


class Candidate242Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "685c08b155bff522d20b9110264cdcaf11f894acc790c2df12dbefaddd82b283",
        )

    def test_only_decision_boundary_changed_from_retained_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        before_s, rest_s = source.split("### DECISION_BOUNDARY\n", 1)
        _, after_s = rest_s.split("### VALIDATION_CLOSURE\n", 1)
        before_c, rest_c = candidate.split("### DECISION_BOUNDARY\n", 1)
        boundary, after_c = rest_c.split("### VALIDATION_CLOSURE\n", 1)
        self.assertEqual(before_c, before_s)
        self.assertEqual(after_c, after_s)
        self.assertIn("開始状態の確認だけを先に完了してはならない", boundary)
        for forbidden in (
            "同じmodel step",
            "未着手のまま残してはならない",
            "該当する作業すべてに着手",
            "custom exec wrapper",
        ):
            self.assertNotIn(forbidden, boundary)

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
            "685c08b155bff522d20b9110264cdcaf11f894acc790c2df12dbefaddd82b283",
        )

    def test_registered_result_and_mechanism_stop(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "f5f78ea591414f949e33d0c84edf4665")
        self.assertEqual(result["median"]["total_tokens"], 190525)
        self.assertEqual([row["quality_score"] for row in result["case_results"]], [4] * 5)
        gate = mechanism["gates"]["a02_start_check_only_did_not_complete_before_unaffected_read_selection"]
        self.assertEqual(gate["pass_count"], 3)
        self.assertEqual(gate["failure_count"], 2)
        self.assertEqual(mechanism["status"], "mechanism_failed")


if __name__ == "__main__":
    unittest.main()
