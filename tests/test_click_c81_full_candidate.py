from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
CLICK = ROOT / "evaluations/targets/click"
CANDIDATE = CLICK / "prompts/candidates/click-00e592c-validation-wrapper-precedence-r1"
DONOR = ROOT / "prompts/candidates/the-caption-3ce91a4-validation-wrapper-precedence-r1"
BASELINE_PROFILE = CLICK / "profiles/click-control-free-standard14-global-m24-n5-r1.json"
CANDIDATE_PROFILE = CLICK / "profiles/click-c81-full-standard14-global-m24-n5-r1.json"
BASELINE_MEDIUM_PROFILE = (
    CLICK
    / "profiles/click-control-free-reasoning-medium-standard14-global-m24-n5-r1.json"
)
CANDIDATE_MEDIUM_PROFILE = (
    CLICK / "profiles/click-c81-full-reasoning-medium-standard14-global-m24-n5-r1.json"
)
MEDIUM_RESULT = (
    CLICK
    / "results/click-control-free-c81-full-reasoning-medium-standard14-n5_2026-07-27.md"
)
MEDIUM_RESIDUAL_ANALYSIS = ROOT / "docs/click-c81-medium-residual-analysis.md"


class ClickC81FullCandidateTest(unittest.TestCase):
    def test_bundle_is_single_target_and_byte_identical_to_c81_root(self) -> None:
        candidate = verify_bundle(CANDIDATE)
        donor = verify_bundle(DONOR)
        self.assertEqual(candidate["prompt_identity"], "click-00e592c-validation-wrapper-precedence-r1")
        self.assertEqual([entry["target"] for entry in candidate["files"]], ["AGENTS.md"])
        self.assertEqual(candidate["files"][0], next(entry for entry in donor["files"] if entry["target"] == "AGENTS.md"))
        self.assertEqual(
            (CANDIDATE / "files/AGENTS.md.txt").read_bytes(),
            (DONOR / "files/AGENTS.md.txt").read_bytes(),
        )

    def test_standard14_profile_changes_only_prompt_identity(self) -> None:
        candidate = verify_bundle(CANDIDATE)
        baseline = json.loads(BASELINE_PROFILE.read_text(encoding="utf-8"))
        profile = json.loads(CANDIDATE_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "bundle_sha256": candidate["bundle_sha256"],
                "name": candidate["prompt_identity"],
                "revision": "r1",
            },
        )
        comparable_baseline = copy.deepcopy(baseline)
        comparable_profile = copy.deepcopy(profile)
        for value in (comparable_baseline, comparable_profile):
            value.pop("profile_id")
            value.pop("prompt_set_identity")
        self.assertEqual(comparable_profile, comparable_baseline)

    def test_manifest_records_full_configuration_portability_boundary(self) -> None:
        manifest = verify_bundle(CANDIDATE)
        self.assertEqual(manifest["artifact"]["baseline_identity"], "click-00e592c-control-free-r1")
        self.assertEqual(
            manifest["provenance"]["donor_prompt_identity"],
            "the-caption-3ce91a4-validation-wrapper-precedence-r1",
        )
        self.assertEqual(manifest["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(manifest["artifact"]["state"], "draft")

    def test_medium_profiles_change_only_reasoning_and_profile_identity(self) -> None:
        for high_path, medium_path in (
            (BASELINE_PROFILE, BASELINE_MEDIUM_PROFILE),
            (CANDIDATE_PROFILE, CANDIDATE_MEDIUM_PROFILE),
        ):
            high = json.loads(high_path.read_text(encoding="utf-8"))
            medium = json.loads(medium_path.read_text(encoding="utf-8"))
            expected = copy.deepcopy(high)
            expected["profile_id"] = medium_path.stem
            expected["comparison_conditions"]["executor_parameters"][
                "reasoning_effort"
            ] = "medium"
            self.assertEqual(medium, expected)

    def test_medium_profiles_are_prompt_only_peers(self) -> None:
        baseline = json.loads(BASELINE_MEDIUM_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(CANDIDATE_MEDIUM_PROFILE.read_text(encoding="utf-8"))
        for value in (baseline, candidate):
            self.assertEqual(
                value["comparison_conditions"]["executor_parameters"][
                    "reasoning_effort"
                ],
                "medium",
            )
            value.pop("profile_id")
            value.pop("prompt_set_identity")
        self.assertEqual(candidate, baseline)

    def test_medium_result_records_compatible_completed_comparison(self) -> None:
        result = MEDIUM_RESULT.read_text(encoding="utf-8")
        self.assertIn("ade5719ca1484443bfc3c1d9af4daac6", result)
        self.assertIn("ab324fc854989f27b51bb1e312bc6bb4881a17fe6cb07e06128c2d3b112c4039", result)
        self.assertIn("-28.79%", result)
        self.assertIn("-12.62%", result)
        self.assertIn("70 / 70", result)
        self.assertIn("5 iterationすべて", result)

    def test_medium_residual_analysis_records_pre_candidate_stop(self) -> None:
        analysis = MEDIUM_RESIDUAL_ANALYSIS.read_text(encoding="utf-8")
        self.assertIn("paired差の中央値は`-970 token`", analysis)
        self.assertIn("Control-freeはHigh / Medium合計`0 / 10`件", analysis)
        self.assertIn("`PRECHANGE_EVIDENCE_SCOPE`", analysis)
        self.assertIn("method bind後の代替探索", analysis)
        self.assertIn("`0 / 4`件", analysis)
        self.assertIn("87f3dfcd98e94f33a8004a863e3d4486", analysis)
        self.assertIn("`stopped_before_candidate`", analysis)


if __name__ == "__main__":
    unittest.main()
