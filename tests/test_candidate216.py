from __future__ import annotations

import unittest
import json
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-packet-construction-projection-r1"
DESIGN = ROOT / "docs/candidate216-packet-construction-projection-design.md"
DIRECTION = ROOT / "docs/candidate216-packet-construction-projection-direction-audit.md"
AUDIT = ROOT / "docs/candidate216-packet-construction-projection-implementation-audit.md"
RESULT = ROOT / "evaluations/results/cb903e23e6a14ebea156351c16963cad.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5-mechanism-audit-r1.json"
RESULT_REPORT = ROOT / "evaluations/results/candidate216-packet-construction-projection-adr9-r2-n5_2026-08-14.md"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate216Test(unittest.TestCase):
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
        self.assertEqual(
            candidate["bundle_sha256"],
            "77a0f660d7066bee128785814517a7899d18086e0c0617b9bc90feebe3995eb6",
        )
        base_files = {item["target"]: item for item in base["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(base_files.keys(), candidate_files.keys())
        self.assertEqual(
            [target for target in base_files if base_files[target] != candidate_files[target]],
            ["AGENTS.md"],
        )

    def test_existing_c147_closures_are_preserved(self) -> None:
        base = clauses((BASE / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        candidate = clauses((CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8"))
        self.assertEqual(set(candidate) - set(base), {"PRECHANGE_REVIEW"})
        self.assertEqual([label for label in base if base[label] != candidate[label]], ["EVIDENCE_GATE"])
        for label in set(base) - {"EVIDENCE_GATE"}:
            self.assertEqual(candidate[label], base[label], label)
        self.assertEqual(
            len((CANDIDATE / "files/AGENTS.md.txt").read_bytes())
            - len((BASE / "files/AGENTS.md.txt").read_bytes()),
            5992,
        )

    def test_construction_projection_boundary_is_fixed(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "packet_construction_receipt(item) :=",
            "packet_projection_region_materialized(receipt) :=",
            "packet item構築と同じoperation",
            "source read時のselector有無と独立",
            "一意なstructural path / range / subtree",
            "value equality、field / scopeの名称、意味",
            "一意にmaterializeできない場合だけregionを推測せずcontainer fallback",
            "review_read_conflicts(target) :=",
            "同一 / 子孫 / 祖先 / 重複",
            "review_read_conflicts(observation.target)=false",
        ):
            self.assertIn(fragment, text)
        for prohibited in (
            "source_region_structurally_fixed",
            "paired-scope-evidence",
            "TC-ADR",
            "OBS-",
            "SCOPE-",
            "Candidate215",
            "consumer_inventory",
            "先にこのpredicate",
        ):
            self.assertNotIn(prohibited, text)

    def test_creation_gate_and_direction_are_fixed(self) -> None:
        self.assertIn("creation_gate_fixed", DESIGN.read_text(encoding="utf-8"))
        self.assertIn("direction_passed", DIRECTION.read_text(encoding="utf-8"))
        audit = AUDIT.read_text(encoding="utf-8")
        self.assertIn("static_verification_passed", audit)
        self.assertIn("quality_failed", audit)

    def test_evaluation_result_and_audits_are_fixed(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "cb903e23e6a14ebea156351c16963cad")
        self.assertEqual(quality["valid_run_count"], 45)
        self.assertEqual(quality["quality_score_counts"], {"1": 1, "4": 44})
        self.assertEqual(quality["terminal_match_count"], 44)
        self.assertEqual(quality["artifact_boundary_match_count"], 45)
        self.assertEqual(mechanism["packet_overlap_or_whole_read_count"], 0)
        self.assertEqual(mechanism["allowed_nonoverlap_region_read_count"], 13)
        self.assertEqual(mechanism["unexpected_nonoverlap_region_read_count"], 14)
        self.assertEqual(mechanism["packet_case_wrong_paired_read_count"], 0)
        self.assertEqual(mechanism["root_reviewer_owned_preread_count"], 0)
        self.assertEqual(mechanism["packet_case_expected_terminal_match_count"], 19)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        report = RESULT_REPORT.read_text(encoding="utf-8")
        self.assertIn("quality_failed / mechanism_failed / stopped", report)
        self.assertIn("Standard14", report)


if __name__ == "__main__":
    unittest.main()
