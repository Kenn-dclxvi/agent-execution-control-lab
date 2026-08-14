from __future__ import annotations

import unittest
import json
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-scope-exact-carrier-r1"
DESIGN = ROOT / "docs/candidate223-review-scope-exact-carrier-design.md"
DIRECTION = ROOT / "docs/candidate223-review-scope-exact-carrier-direction-audit.md"
RESULT = ROOT / "evaluations/results/abac73500213486e80469c7066dbdc43.json"
QUALITY = ROOT / "evaluations/results/candidate223-review-scope-exact-carrier-adr9-r4-n5-quality-audit-r1.json"
MECHANISM = ROOT / "evaluations/results/candidate223-review-scope-exact-carrier-adr9-r4-n5-delivery-boundary-audit-r1.json"


def clauses(text: str) -> dict[str, str]:
    return {
        line[2:].split(":", 1)[0]: line
        for line in text.splitlines()
        if line.startswith("- ") and ":" in line
    }


class Candidate223Test(unittest.TestCase):
    def test_direct_c147_child_changes_only_root_agents(self) -> None:
        base = verify_bundle(BASE)
        candidate = verify_bundle(CANDIDATE)
        self.assertEqual(candidate["artifact"]["baseline_identity"], base["prompt_identity"])
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": base["prompt_identity"],
            },
        )
        self.assertEqual(candidate["bundle_sha256"], "85473ee6fc8d50c1e9946b2fb4d328fae68a260ade5380e9c32501ed2fbd9320")
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual([target for target in base_files if base_files[target] != candidate_files[target]], ["AGENTS.md"])

    def test_only_review_clauses_are_added(self) -> None:
        base = clauses((BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = clauses((CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(set(candidate) - set(base), {"PRECHANGE_REVIEW", "REVIEW_SCOPE_CARRIER"})
        for label in base:
            self.assertEqual(candidate[label], base[label], label)

    def test_scope_exact_permission_closure_is_fixed(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "source外のreview scope carrier contract",
            "required review scopeごとのrequired proposition",
            "現在のscope-to-observation対応へ列挙されないmanifest targetはdefault deny",
            "全scopeの和集合",
            "whole-source read",
            "rootはreviewer direct resultを受領せず",
            "特定tool、selector、read回数または判断順は固定しない",
        ):
            self.assertIn(fragment, text)
        for prohibited in ("TC-ADR", "consumer_inventory", "OBS-", "SCOPE-"):
            self.assertNotIn(prohibited, text)

    def test_creation_gate_is_fixed(self) -> None:
        self.assertIn("creation_gate_fixed", DESIGN.read_text(encoding="utf-8"))
        direction = DIRECTION.read_text(encoding="utf-8")
        self.assertIn("direction_passed", direction)
        self.assertIn("evaluation_input_change_required", direction)

    def test_evaluation_result_and_stop_gate_are_fixed(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "abac73500213486e80469c7066dbdc43")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(quality["quality_score_counts"], {"4": 43, "1": 2})
        self.assertEqual(quality["reviewer_cardinality_match_count"], 43)
        self.assertEqual(mechanism["root_projection_match_count"], 45)
        self.assertEqual(mechanism["root_whole_container_read_count"], 0)
        self.assertEqual(mechanism["packet_case_paired_read_count"], 0)
        self.assertEqual(mechanism["paired_case_design_read_count"], 0)
        self.assertFalse(mechanism["mechanism_gate_passed"])


if __name__ == "__main__":
    unittest.main()
