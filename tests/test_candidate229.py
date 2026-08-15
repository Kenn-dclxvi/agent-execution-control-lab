from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-c147-direct-human-wait-permission-closure-r1"
DESIGN = ROOT / "docs/candidate229-c147-direct-human-wait-permission-closure-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate229-c147-direct-human-wait-permission-closure-v14-reasoning-medium-a02-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/671dd3cd50ae4d41bbc4203a797a7e42.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate229-c147-direct-human-wait-permission-closure-a02-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate229-c147-direct-human-wait-permission-closure-a02-n5-mechanism-audit-r1.json"


class Candidate229Test(unittest.TestCase):
    def test_c147_is_direct_baseline_and_only_root_agents_changes(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["artifact"]["state"], "evaluation_ready")
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "4ca0c25b38db273f82d6f7555c3f9d70bb69a4a75cdb440ab330ceab3b241c14",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_wait_permission_edge_is_closed_in_human_language(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertEqual(len([line for line in text.splitlines() if line.startswith("- ")]), 13)
        self.assertIn("その結果の受領後まで発行しないこと自体が、その結果への待機依存", text)
        self.assertIn("結果を待つ間に保留できるのは", text)
        self.assertNotIn("custom exec wrapper", text)
        self.assertNotIn("model step", text)

    def test_a02_gate_is_fixed_before_dispatch(self) -> None:
        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            [case["id"] for case in profile["cases"]],
            ["TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING"],
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("Candidate228は親にせず", design)
        self.assertIn("未発行にしたrunが0件", design)

    def test_a02_result_stops_before_standard14(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "671dd3cd50ae4d41bbc4203a797a7e42")
        self.assertEqual(quality["score_counts"], {"4": 5})
        self.assertEqual(mechanism["gates"]["a02_result_effect_scope"]["pass_count"], 1)
        self.assertEqual(mechanism["gates"]["a02_result_effect_scope"]["failure_count"], 4)
        self.assertEqual(mechanism["status"], "mechanism_failed")
        self.assertIn("standard14_not_started", DESIGN.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
