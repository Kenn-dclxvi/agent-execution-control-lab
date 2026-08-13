from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-c147-review-boundary-recomposition-r1"
DRAFT = ROOT / "docs/candidate207-c147-review-boundary-recomposition-draft.md"
DIRECTION = ROOT / "docs/candidate207-c147-review-boundary-recomposition-direction-review.md"
AUDIT = ROOT / "docs/candidate207-c147-review-boundary-recomposition-implementation-audit.md"
RESULT = ROOT / "evaluations/results/candidate207-c147-review-boundary-recomposition-adr9-r2-n5_2026-08-13.md"
C206_COMPARABLE_AUDIT = ROOT / "evaluations/results/candidate206-admitted-evidence-current-adr9-r2-n5-c207-comparable-mechanism-audit-r1.json"
C207_RESULT_AUDIT = ROOT / "evaluations/results/candidate207-c147-review-boundary-recomposition-adr9-r2-n5-quality-mechanism-audit-r1.json"
REFERENCE_PROFILE = ROOT / "evaluations/profiles/candidate147-result-effect-scope-adr9-r2-medium-m24-n5-selection-cli0146-r1.json"
CANDIDATE_PROFILE = ROOT / "evaluations/profiles/candidate207-c147-review-boundary-recomposition-adr9-r2-medium-m24-n5-cli0146-r1.json"


def clauses(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("- ") and ":" in line:
            label = line[2:].split(":", 1)[0]
            result[label] = line
    return result


class Candidate207Test(unittest.TestCase):
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
            "b37800172decfd0b44e161bbb69fe36a3bb24d7271d68e946966f09014516bed",
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
        self.assertEqual(set(candidate) - set(base), {"REVIEW_BOUNDARY"})
        for label in (
            "SPEC",
            "ROOT",
            "INDEPENDENCE",
            "DECISION_BOUNDARY",
            "VALIDATION_CLOSURE",
            "VALIDATION_PLAN",
            "METHOD",
            "RECOVERY",
        ):
            self.assertEqual(candidate[label], base[label], label)

    def test_review_values_connect_to_existing_groups(self) -> None:
        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        for fragment in (
            "producer_execution_required(operation) :=",
            "projected_counterexample_established(packet) :=",
            "review_observation_consumer_ready(observation) :=",
            "projected_counterexample_established(packet)=false",
            "prechange_review_requirement_state=not_required",
            "bind済みreview terminal result=no_counterexample_found",
            "- REVIEW_BOUNDARY:",
            "独立operation、tool invocationまたはmodel-step barrierを作らない",
        ):
            self.assertIn(fragment, text)
        for prohibited in (
            "admitted_evidence_current",
            "projection receipt",
            "acknowledgement",
            "reviewerは許可済み成功観測または先行固定contract / authorityの明示列挙から先に",
            "改訂は新design identityで台帳と要否を再判定",
            "TC-ADR",
            "Candidate207",
        ):
            self.assertNotIn(prohibited, text)

    def test_design_records_hold_creation_and_evaluation_boundary(self) -> None:
        draft = DRAFT.read_text(encoding="utf-8")
        self.assertIn("pretrace_falsification_passed_after_revision", draft)
        direction = DIRECTION.read_text(encoding="utf-8")
        self.assertIn("blocking_counterexample=0 / candidate_creation_allowed", direction)
        self.assertIn("projected_counterexample_established(packet)=true", direction)
        audit = AUDIT.read_text(encoding="utf-8")
        self.assertIn("ADR9_completed / quality_passed / mechanism_failed / stopped", audit)
        self.assertIn("不足45件を発行", audit)

    def test_adr9_profiles_differ_only_by_prompt_identity_and_provenance(self) -> None:
        reference = json.loads(REFERENCE_PROFILE.read_text(encoding="utf-8"))
        candidate = json.loads(CANDIDATE_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(reference["iterations"], 5)
        self.assertEqual(candidate["iterations"], 5)
        for profile in (reference, candidate):
            profile.pop("profile_id")
            profile.pop("prompt_set_identity")
            profile["scope"].pop("preflight_revision_note")
        self.assertEqual(candidate, reference)

    def test_result_records_c206_comparable_mechanism_without_reinterpreting_history(self) -> None:
        result = RESULT.read_text(encoding="utf-8")
        self.assertIn("13 / 20", result)
        self.assertIn("8 / 20", result)
        audit = json.loads(C206_COMPARABLE_AUDIT.read_text(encoding="utf-8"))
        self.assertEqual(audit["source"]["new_evaluation_slots"], 0)
        self.assertTrue(audit["original_candidate206_decision"]["historical_decision_preserved"])
        self.assertEqual(
            audit["c207_comparable_read_gate"]["counterexample_certificate_priority_violation_count"],
            7,
        )
        result_audit = json.loads(C207_RESULT_AUDIT.read_text(encoding="utf-8"))
        delta = result_audit["kpi_comparison"]["candidate207_minus_candidate206"]
        self.assertEqual(delta["quality_score"], 0.0)
        self.assertEqual(delta["total_tokens"], -40344)
        self.assertAlmostEqual(delta["elapsed_seconds"], -22.153571498929523)


if __name__ == "__main__":
    unittest.main()
