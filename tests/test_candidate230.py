from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-reader-ai-plain-japanese-translation-r1"
DESIGN = ROOT / "docs/candidate230-reader-ai-plain-japanese-translation-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate230-reader-ai-plain-japanese-translation-v14-reasoning-medium-a02-f02-f03-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/d90d4257c5c1451ab2119e9fa5367cf8.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate230-reader-ai-plain-japanese-translation-targeted-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate230-reader-ai-plain-japanese-translation-targeted-n5-mechanism-audit-r1.json"


class Candidate230Test(unittest.TestCase):
    def test_c147_is_direct_baseline_and_only_root_agents_changes(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["artifact"]["state"], "evaluation_ready")
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "b7f9374e6d7d239472b69f4666de20ab5d6ed31bfc3e6bfa6aad12e572768f78",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_submitted_translation_keeps_thirteen_control_groups(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for heading in (
            "### SPEC", "### PRODUCER", "### TERMINAL", "### CONTEXT",
            "### EVIDENCE_GATE", "### OWNER_ROLE", "### ROOT", "### INDEPENDENCE",
            "### DECISION_BOUNDARY", "### VALIDATION_CLOSURE", "### VALIDATION_PLAN",
            "### METHOD", "### RECOVERY",
        ):
            self.assertIn(heading, text)
        self.assertIn("互いに独立しており", text)
        self.assertIn("同じmodel stepで発行", text)
        self.assertIn("owner」と書かれている名前だけを見てproducerを選んではいけない", text)
        self.assertNotIn("以下は、root の", text)

    def test_targeted_comparison_gate_is_fixed(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            [case["id"] for case in profile["cases"]],
            [
                "TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING",
                "TC-F02-CROSS-LAYER-HISTORY-DATE-BOUND",
                "TC-F03-ATOMIC-CONTEXT-CLEANUP",
            ],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate228と同じA02・F02・F03", design)
        self.assertIn("失敗機能数", design)

    def test_targeted_result_is_registered_and_stopped(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "d90d4257c5c1451ab2119e9fa5367cf8")
        self.assertEqual(len(result["case_results"]), 15)
        self.assertEqual(result["median"]["quality_score"], 100.0)
        self.assertEqual(quality["score_counts"], {"4": 15})
        self.assertEqual(
            mechanism["gates"]["a02_result_effect_scope"]["pass_count"],
            3,
        )
        self.assertEqual(
            mechanism["gates"]["a02_result_effect_scope"]["failure_count"],
            2,
        )
        self.assertEqual(
            mechanism["gates"]["criterion_owner_did_not_create_producer"]["pass_count"],
            10,
        )
        self.assertEqual(mechanism["status"], "mechanism_failed")


if __name__ == "__main__":
    unittest.main()
