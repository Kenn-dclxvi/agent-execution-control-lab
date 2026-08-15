from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-observed-value-reread-exclusion-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-taskspec-output-boundary-r1"
PROFILE = ROOT / "evaluations/profiles/candidate236-taskspec-output-boundary-v14-reasoning-medium-f02-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/cfc9678fda814da3a6f8eea818cb4335.json"
MECHANISM = ROOT / "evaluations/results/candidate236-taskspec-output-boundary-f02-n5-mechanism-audit-r1.json"


class Candidate236Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "f345646bf3ad44296ff52466e9c71922df5a69b92e2b9241a84653d891ad043d",
        )

    def test_only_spec_output_boundary_changes_from_candidate235_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        before_s, rest_s = source.split("### SPEC\n", 1)
        _, after_s = rest_s.split("### PRODUCER\n", 1)
        before_c, rest_c = candidate.split("### SPEC\n", 1)
        spec, after_c = rest_c.split("### PRODUCER\n", 1)
        self.assertEqual(before_c, before_s)
        self.assertEqual(after_c, after_s)
        self.assertIn("内部状態", spec)
        self.assertIn("進捗resultにして項目別に書き出してはいけない", spec)
        self.assertIn("固定が完了した事実は伝えられる", spec)

    def test_f02_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["cases"], [{"id": "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND", "revision": "r1"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)

    def test_result_records_retained_mechanism_failure(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "cfc9678fda814da3a6f8eea818cb4335")
        self.assertEqual(result["median"]["total_tokens"], 180024)
        self.assertEqual(
            mechanism["gates"]["taskspec_internal_fields_were_not_itemized_as_progress"]["status"],
            "passed",
        )
        self.assertEqual(
            mechanism["gates"]["observed_value_was_not_reread_or_researched"]["status"],
            "failed",
        )


if __name__ == "__main__":
    unittest.main()
