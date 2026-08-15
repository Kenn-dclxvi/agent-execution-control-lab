from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-c147-direct-human-permission-boundaries-r1"
DESIGN = ROOT / "docs/candidate228-c147-direct-human-permission-boundaries-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate228-c147-direct-human-permission-boundaries-v14-reasoning-medium-a02-f02-f03-m24-n5-cli0146-r1.json"
RESULT = ROOT / "evaluations/results/7ae274532e454377bab8e715c6380b5b.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate228-c147-direct-human-permission-boundaries-targeted-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate228-c147-direct-human-permission-boundaries-targeted-n5-mechanism-audit-r1.json"


class Candidate228Test(unittest.TestCase):
    def test_c147_is_direct_baseline_and_only_root_agents_changes(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["artifact"]["state"], "evaluation_ready")
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(
            candidate["bundle_sha256"],
            "5d6b1913c31893b14601e94c001082746ef8486528ebbc78cbd896e5108e84b6",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_human_permission_boundaries_are_present(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertEqual(len([line for line in text.splitlines() if line.startswith("- ")]), 13)
        self.assertIn("互いに影響しない作業の間に、待機や停止への依存関係を作らない", text)
        self.assertIn("判断責任者や役割名の記載は、新しい実行担当を起動する許可ではない", text)
        self.assertNotIn("custom exec wrapper", text)
        self.assertNotIn("model step", text)

    def test_targeted_gate_is_fixed_before_dispatch(self) -> None:
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
        self.assertIn("Candidate227は親にせず", design)
        self.assertIn("不要な待機依存0件", design)
        self.assertIn("責任者名からの独立担当起動0件", design)

    def test_targeted_result_stops_before_standard14(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "7ae274532e454377bab8e715c6380b5b")
        self.assertEqual(quality["score_counts"], {"4": 15})
        self.assertEqual(mechanism["gates"]["a02_result_effect_scope"]["failure_count"], 5)
        self.assertEqual(
            mechanism["gates"]["criterion_owner_did_not_create_producer"]["pass_count"],
            10,
        )
        self.assertEqual(mechanism["status"], "mechanism_failed")
        design = DESIGN.read_text(encoding="utf-8")
        self.assertIn("standard14_not_started", design)


if __name__ == "__main__":
    unittest.main()
