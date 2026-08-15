from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
SOURCE = ROOT / "prompts/candidates/the-caption-3ce91a4-compact-evidence-admission-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-owner-field-exclusion-r1"
DESIGN = ROOT / "docs/candidate233-owner-field-exclusion-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate233-owner-field-exclusion-v14-reasoning-medium-f02-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/670d5536ed5a4baaabbba29d55cc6c0e.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate233-owner-field-exclusion-f02-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate233-owner-field-exclusion-f02-n5-mechanism-audit-r1.json"


class Candidate233Test(unittest.TestCase):
    def test_c147_is_direct_baseline_and_only_root_agents_changes(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["source_prompt_identity"], base["prompt_identity"])
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "e86424f86b12c2d414eb6eeb1752057b322507788784df5a8d750d47392c9cf4",
        )

    def test_only_owner_role_differs_from_candidate231_wording_source(self) -> None:
        source = (SOURCE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        source_before, source_rest = source.split("### OWNER_ROLE\n", 1)
        _, source_after = source_rest.split("### ROOT\n", 1)
        candidate_before, candidate_rest = candidate.split("### OWNER_ROLE\n", 1)
        owner, candidate_after = candidate_rest.split("### ROOT\n", 1)
        self.assertEqual(candidate_before, source_before)
        self.assertEqual(candidate_after, source_after)
        self.assertIn("独立した実行担当の明示には当たらない", owner)
        self.assertIn("TaskSpecがownerとは別に", owner)
        self.assertIn("どの実行担当がどの判定を行うか", owner)

    def test_f02_measurement_and_stop_gate_are_fixed(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["cases"],
            [{"id": "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND", "revision": "r1"}],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("判断責任者名によるworker起動0 / 5件", design)
        self.assertIn("追加N、採用、release、projectionへ自動的に進まない", design)

    def test_f02_result_is_registered_and_targeted_passed(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "670d5536ed5a4baaabbba29d55cc6c0e")
        self.assertEqual(
            result["compatibility_key"],
            "b5d172c7fb388438dadd19cea0fd7b87118685232c74be49af77e4b0e965ac7b",
        )
        self.assertEqual(result["median"]["total_tokens"], 169370)
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(quality["score_counts"], {"4": 5})
        owner = mechanism["gates"]["criterion_owner_did_not_create_producer"]
        self.assertEqual(owner["pass_count"], 5)
        self.assertEqual(owner["failure_count"], 0)
        self.assertEqual(mechanism["status"], "mechanism_passed")


if __name__ == "__main__":
    unittest.main()
