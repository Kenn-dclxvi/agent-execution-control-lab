from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-taskspec-progress-suppression-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-portable-result-wait-closure-r1"
PROFILE = ROOT / "evaluations/profiles/candidate240-portable-result-wait-closure-v14-reasoning-medium-a02-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/e878ab6593f448fab3b8353bc16b9895.json"
MECHANISM = ROOT / "evaluations/results/candidate240-portable-result-wait-closure-a02-n5-mechanism-audit-r1.json"


class Candidate240Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "aed214874743be48960901f58902f007e564bf4e6d3e9db95809aba3884a2103",
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
        self.assertIn("その結果が返るまで保留してはならない", boundary)
        self.assertIn("それらの一部の結果を次の作業の選択や停止に使わない", boundary)
        self.assertIn("その確認を理由に読み取りを保留してはならない", boundary)
        self.assertIn("読み取りを確認後へ分ける", boundary)
        for forbidden in ("同じmodel step", "invocation", "custom exec wrapper"):
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
            "aed214874743be48960901f58902f007e564bf4e6d3e9db95809aba3884a2103",
        )

    def test_registered_result_and_mechanism_stop(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "e878ab6593f448fab3b8353bc16b9895")
        self.assertEqual(result["median"]["total_tokens"], 193418)
        self.assertEqual([row["quality_score"] for row in result["case_results"]], [4] * 5)
        for gate in mechanism["gates"].values():
            self.assertEqual(gate["pass_count"], 0)
            self.assertEqual(gate["failure_count"], 5)
        self.assertEqual(mechanism["status"], "mechanism_failed")


if __name__ == "__main__":
    unittest.main()
