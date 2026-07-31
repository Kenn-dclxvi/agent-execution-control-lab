from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
CLICK = ROOT / "evaluations/targets/click"
CANDIDATE = (
    CLICK
    / "prompts/candidates/click-00e592c-criterion-complete-single-target-continuation-r1"
)
DONOR = (
    ROOT
    / "prompts/candidates/the-caption-3ce91a4-criterion-complete-single-target-continuation-r1"
)
C81_PROFILE = (
    CLICK
    / "profiles/click-c81-reasoning-medium-standard14-r2-global-m24-n5-r1.json"
)
C125_PROFILE = (
    CLICK
    / "profiles/click-c125-reasoning-medium-standard14-r2-global-m24-n5-cli0146-r1.json"
)
DESIGN = ROOT / "docs/click-c125-full-portability-design.md"
RESULT = (
    CLICK
    / "results/click-c125-reasoning-medium-standard14-r2-n5-cli0146_2026-07-31.md"
)


class ClickC125FullCandidateTest(unittest.TestCase):
    def test_bundle_is_single_target_and_byte_identical_to_c125_root(self) -> None:
        candidate = verify_bundle(CANDIDATE)
        donor = verify_bundle(DONOR)
        self.assertEqual(
            candidate["prompt_identity"],
            "click-00e592c-criterion-complete-single-target-continuation-r1",
        )
        self.assertEqual([item["target"] for item in candidate["files"]], ["AGENTS.md"])
        self.assertEqual(
            candidate["files"][0],
            next(item for item in donor["files"] if item["target"] == "AGENTS.md"),
        )
        self.assertEqual(
            (CANDIDATE / "files/AGENTS.md.txt").read_bytes(),
            (DONOR / "files/AGENTS.md.txt").read_bytes(),
        )

    def test_profile_changes_c81_only_by_prompt_and_cli(self) -> None:
        c81 = json.loads(C81_PROFILE.read_text(encoding="utf-8"))
        c125 = json.loads(C125_PROFILE.read_text(encoding="utf-8"))
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(
            c125["prompt_set_identity"],
            {
                "bundle_sha256": candidate["bundle_sha256"],
                "name": candidate["prompt_identity"],
                "revision": "r1",
            },
        )
        self.assertEqual(
            c125["comparison_conditions"]["agent_environment"]["codex_cli"],
            "0.146.0",
        )
        comparable_c81 = copy.deepcopy(c81)
        comparable_c125 = copy.deepcopy(c125)
        for value in (comparable_c81, comparable_c125):
            value.pop("profile_id")
            value.pop("prompt_set_identity")
            value["comparison_conditions"]["agent_environment"].pop("codex_cli")
        self.assertEqual(comparable_c125, comparable_c81)

    def test_design_and_result_record_the_noncompatible_boundary(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        result = RESULT.read_text(encoding="utf-8")
        self.assertIn("Codex CLI `0.144.0`", design)
        self.assertIn("`0.146.0`", design)
        self.assertIn("tokenとelapsedの差は算出しない", result)
        self.assertIn("7560599fef024dfb8011264352707ab8", result)
        self.assertIn("`4 = 65`、`1 = 5`", result)
        self.assertIn("`authority_unavailable = 5`", result)
        self.assertIn("all-agent token `1,348,515`", result)


if __name__ == "__main__":
    unittest.main()
