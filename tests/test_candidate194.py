from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-c147-direct-review-control-reconstruction-r1"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate194-c147-direct-review-control-reconstruction-adr9-r2-n5-mechanism-audit-r2.json"
CAUSAL_ANALYSIS = ROOT / "docs/candidate194-m5-causal-analysis.md"
M2_REDESIGN = ROOT / "docs/post-candidate194-review-control-m2-redesign.md"
M3_REVIEW = ROOT / "docs/post-candidate194-review-control-m3-direction-review.md"


class Candidate194Test(unittest.TestCase):
    def test_post_m5_m3_review_resolves_four_blocking_counterexamples(self) -> None:
        review = M3_REVIEW.read_text(encoding="utf-8")

        for status in (
            "M3_passed_after_revision",
            "initial_blocking_counterexamples_4",
            "unresolved_blocking_counterexamples_0",
            "reviewed_states_22",
            "c147_direct_parent_retained",
            "next_candidate_not_created",
            "profile_not_created",
            "evaluation_not_started",
        ):
            self.assertIn(status, review)

        for correction in (
            "suppressed_by_predecessor",
            "conflict_keys",
            "method_eligible=false",
            "ledger_receipt_identity",
        ):
            self.assertIn(correction, review)

    def test_post_m5_m2_redesign_binds_four_causes_without_creating_a_candidate(self) -> None:
        redesign = M2_REDESIGN.read_text(encoding="utf-8")

        for status in (
            "M2_complete_after_candidate194",
            "c147_direct_parent_retained",
            "operation_ticket_fixed",
            "predecessor_edge_fixed",
            "method_receipt_fixed",
            "finite_closure_certificate_fixed",
            "observation_ledger_fixed",
            "responsibilities_27",
            "M3_passed_after_revision",
            "candidate_not_created",
            "evaluation_not_started",
        ):
            self.assertIn(status, redesign)

        self.assertIn("does_not_bind_requested_result", redesign)
        self.assertIn("ledger_receipt_identity + observation_identity", redesign)
        self.assertIn("抽象frontierは作らない", redesign)

    def test_m5_causal_analysis_covers_every_mechanism_failure(self) -> None:
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        analysis = CAUSAL_ANALYSIS.read_text(encoding="utf-8")

        self.assertEqual(len(mechanism["failure_run_ids"]), 15)
        for run_id in mechanism["failure_run_ids"]:
            with self.subTest(run_id=run_id):
                self.assertIn(run_id, analysis)

        for status in (
            "dispatch_precedence_7",
            "method_early_terminal_6",
            "finite_closure_misclassification_1",
            "observation_identity_mismatch_1",
            "unknown_cause_0",
            "c147_direct_parent_retained",
            "M2_not_started",
        ):
            self.assertIn(status, analysis)

    def test_c147_direct_reconstruction_has_24_bound_responsibilities(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)

        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(
            candidate["content_relation"]["source_prompt_identity"],
            parent["prompt_identity"],
        )
        self.assertEqual(candidate["content_relation"]["changed_targets"], ["AGENTS.md"])
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(
            candidate["bundle_sha256"],
            "226fd8599620ed5e71b9963a39faab51ed3dbb42b0f45078838680fa13818243",
        )

        parent_files = {item["target"]: item for item in parent["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(parent_files.keys(), candidate_files.keys())
        for target in parent_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], parent_files[target], target)

        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        labels = [
            line.split(":", 1)[0][2:]
            for line in text.splitlines()
            if line.startswith("- ")
        ]
        self.assertEqual(
            labels,
            [
                "OPERATION_SPEC",
                "PRODUCER_BINDING",
                "PRODUCER_RESULT",
                "OWNER_ROLE",
                "ROOT",
                "WORKER_CONTEXT",
                "RESULT_DEPENDENCY",
                "METHOD",
                "RECOVERY",
                "EVIDENCE_ADMISSION",
                "DECISION_BOUNDARY",
                "IMPLEMENTATION_BINDING",
                "REVIEW_REQUIREMENT",
                "PRIOR_REVIEW_RESULT_ADMISSION",
                "REVIEW_EXECUTION_PERMISSION",
                "REVIEW_PACKET",
                "OBSERVATION_RESULT",
                "REVIEW_JUDGEMENT",
                "CURRENT_REVIEW_RESULT_ADMISSION",
                "CHANGE_ADMISSION",
                "VALIDATION_PLAN",
                "VALIDATION_CLOSURE",
                "OPERATION_TERMINAL",
                "OUTER_TERMINAL",
            ],
        )

        for required in (
            "別のclarification operation identity",
            "そのresultを消費する未発行operationがある場合だけ観測",
            "result_dependency(result, next_operation) :=",
            "certificate外missing / 無関係field / task全体を含めない",
            "同じmodel responseから個別tool callとして全件発行",
            "一部だけを発行して残りを次responseへ送らず",
            "同じcell IDへのwait以外を追加発行しない",
            "依頼自体がroot producerのreviewである場合はprimary operation",
            "prior resultへ新規review execution permissionを要求せず",
            "固定targetの存在 / read成功 / 現在valueはreadinessへ含めず",
            "invocation result contract identity",
            "current resultへ別の`result_use_permission`を追加要求せず",
            "変更後required validationは所有しない",
            "未固定の実装operationをcompletedにしない",
        ):
            self.assertIn(required, text)

        for rejected in (
            "DISPATCH_ADMISSION",
            "DISPATCH_TRANSITION",
            "dispatch_candidate",
            "dispatch_predecessor",
            "dispatch_frontier",
        ):
            self.assertNotIn(rejected, text)

        for historical_identity in (
            "C147",
            "Candidate147",
            "Candidate191",
            "Candidate192",
            "Candidate193",
            "Standard14",
            "ADR9",
        ):
            self.assertNotIn(historical_identity, text)


if __name__ == "__main__":
    unittest.main()
