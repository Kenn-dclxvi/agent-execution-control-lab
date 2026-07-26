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


if __name__ == "__main__":
    unittest.main()
