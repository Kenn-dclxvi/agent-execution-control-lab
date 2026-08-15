from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-observed-value-reread-exclusion-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-taskspec-progress-suppression-r1"
PROFILE = ROOT / "evaluations/profiles/candidate237-taskspec-progress-suppression-v14-reasoning-medium-f02-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/6cca8a10140c4e35be2594c6cd0e9013.json"
MECHANISM = ROOT / "evaluations/results/candidate237-taskspec-progress-suppression-f02-n5-mechanism-audit-r1.json"


class Candidate237Test(unittest.TestCase):
    def test_direct_baseline_and_single_target(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "2c6f93c228d5b77fc0de4766d54119733aa2e839eaa8b94b786f59703acd0eb7",
        )

    def test_only_spec_progress_boundary_changes_from_candidate235_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        before_s, rest_s = source.split("### SPEC\n", 1)
        _, after_s = rest_s.split("### PRODUCER\n", 1)
        before_c, rest_c = candidate.split("### SPEC\n", 1)
        spec, after_c = rest_c.split("### PRODUCER\n", 1)
        self.assertEqual(before_c, before_s)
        self.assertEqual(after_c, after_s)
        self.assertIn("固定した事実も、その内容も、利用者向けの進捗として出力してはいけない", spec)
        self.assertNotIn("固定が完了した事実は伝えられる", spec)

    def test_f02_n5_profile(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["cases"], [{"id": "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND", "revision": "r1"}])
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(profile["prompt_set_identity"]["bundle_sha256"], "2c6f93c228d5b77fc0de4766d54119733aa2e839eaa8b94b786f59703acd0eb7")

    def test_result_records_targeted_pass(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "6cca8a10140c4e35be2594c6cd0e9013")
        self.assertEqual(result["median"]["total_tokens"], 128940)
        self.assertEqual(
            mechanism["gates"]["taskspec_fixation_was_not_reported_as_progress"]["status"],
            "passed",
        )
        self.assertEqual(
            mechanism["gates"]["observed_value_was_not_reread_or_researched"]["status"],
            "passed",
        )
        self.assertEqual(mechanism["status"], "mechanism_passed_cost_reduced_vs_candidate235")


if __name__ == "__main__":
    unittest.main()
