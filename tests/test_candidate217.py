from __future__ import annotations

import unittest
import json
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-review-proposition-operand-closure-r1"
DESIGN = ROOT / "docs/candidate217-review-proposition-operand-closure-design.md"
DIRECTION = ROOT / "docs/candidate217-review-proposition-operand-closure-direction-audit.md"
AUDIT = ROOT / "docs/candidate217-review-proposition-operand-closure-implementation-audit.md"
RESULT = ROOT / "evaluations/results/906c23433e3c4ac7ba679b916f0bb311.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5-mechanism-audit-r1.json"
RESULT_REPORT = ROOT / "evaluations/results/candidate217-review-proposition-operand-closure-adr9-r2-n5_2026-08-14.md"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate217Test(unittest.TestCase):
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
            "627c8e27541e0b6ab96129e19121def1a43a289d903222d8260d52cf66507056",
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
        self.assertEqual(set(candidate) - set(base), {"PRECHANGE_REVIEW", "REVIEW_INPUT_CLOSURE"})
        self.assertEqual([label for label in base if base[label] != candidate[label]], ["EVIDENCE_GATE"])
        for label in set(base) - {"EVIDENCE_GATE"}:
            self.assertEqual(candidate[label], base[label], label)

    def test_operand_supply_closure_is_fixed(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "REVIEW_INPUT_CLOSURE",
            "direct_review_operand(proposition, value_identity) :=",
            "predicate dependency",
            "review_operand_binding :=",
            "packet_construction_receiptへ一件bind",
            "observation targetへ一件bind",
            "exactly one review_operand_binding",
            "全required propositionでtrueの場合だけreviewerを起動",
            "admission済みcurrent valueをmissing / unobserved / reviewer-ownedへ再分類しない",
            "未admit operandだけ",
        ):
            self.assertIn(fragment, text)
        for prohibited in (
            "TC-ADR",
            "OBS-",
            "SCOPE-",
            "consumer_inventory",
            "inventory field",
            "先にinventory",
            "Candidate216",
        ):
            self.assertNotIn(prohibited, text)

    def test_creation_gate_and_static_audit_are_fixed(self) -> None:
        self.assertIn("creation_gate_fixed", DESIGN.read_text(encoding="utf-8"))
        direction = DIRECTION.read_text(encoding="utf-8")
        self.assertIn("direction_passed_at_creation", direction)
        self.assertIn("direction_assumption_refuted_by_evaluation", direction)
        audit = AUDIT.read_text(encoding="utf-8")
        self.assertIn("static_verification_passed", audit)
        self.assertIn("quality_failed", audit)

    def test_evaluation_result_and_legal_carrier_audits_are_fixed(self) -> None:
        result = json.loads(RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(result["result_id"], "906c23433e3c4ac7ba679b916f0bb311")
        self.assertEqual(result["median"]["quality_score"], 91.66666666666666)
        self.assertEqual(quality["valid_run_count"], 45)
        self.assertEqual(quality["quality_score_counts"], {"1": 5, "4": 40})
        self.assertEqual(quality["terminal_match_count"], 40)
        self.assertEqual(quality["artifact_boundary_match_count"], 45)
        self.assertEqual(mechanism["fixed_input_packet_carrier_conflict_run_count"], 20)
        self.assertEqual(mechanism["closure_blocked_reviewer_start_count"], 5)
        self.assertEqual(mechanism["reviewer_started_despite_carrier_conflict_count"], 15)
        self.assertEqual(mechanism["admitted_operand_reread_count"], 12)
        self.assertEqual(mechanism["packet_overlap_or_whole_read_count"], 0)
        self.assertEqual(mechanism["adr07_exact_paired_only_count"], 5)
        self.assertEqual(mechanism["adr09_exact_paired_only_count"], 4)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        report = RESULT_REPORT.read_text(encoding="utf-8")
        self.assertIn("model-visible", report)
        self.assertIn("合法carrier", report)
        self.assertIn("quality_failed / mechanism_failed / stopped", report)


if __name__ == "__main__":
    unittest.main()
