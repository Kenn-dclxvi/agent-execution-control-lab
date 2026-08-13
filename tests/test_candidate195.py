from __future__ import annotations

import unittest
import json
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-operation-ticketed-review-control-r1"
M2_REDESIGN = ROOT / "docs/post-candidate194-review-control-m2-redesign.md"
M3_REVIEW = ROOT / "docs/post-candidate194-review-control-m3-direction-review.md"
IMPLEMENTATION_AUDIT = ROOT / "docs/candidate195-operation-ticketed-review-control-implementation-audit.md"
EVALUATION_DESIGN = ROOT / "docs/candidate195-operation-ticketed-review-control-adr9-r2-n5-evaluation-design.md"
PLANNED_PROFILE = ROOT / "evaluations/profiles/candidate195-operation-ticketed-review-control-adr9-r2-medium-m24-n5-cli0146.json"
PREPARATION_AUDIT = ROOT / "docs/candidate195-operation-ticketed-review-control-adr9-r2-n5-execution-preparation-audit.md"
REGISTERED_RESULT = ROOT / "evaluations/results/457400a8506d404f8b564074d0b28802.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate195-operation-ticketed-review-control-adr9-r2-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate195-operation-ticketed-review-control-adr9-r2-n5-mechanism-audit-r3.json"
RESULT_REPORT = ROOT / "evaluations/results/candidate195-operation-ticketed-review-control-adr9-r2-n5_2026-08-12.md"
CAUSAL_ANALYSIS = ROOT / "docs/candidate195-m5-causal-analysis.md"


class Candidate195Test(unittest.TestCase):
    def test_c147_direct_child_has_27_ticketed_responsibilities(self) -> None:
        parent = verify_bundle(PARENT)
        candidate = verify_bundle(CANDIDATE)

        self.assertEqual(candidate["artifact"]["baseline_identity"], parent["prompt_identity"])
        self.assertEqual(
            candidate["content_relation"],
            {
                "changed_targets": ["AGENTS.md"],
                "kind": "direct_child_full_bundle",
                "source_prompt_identity": parent["prompt_identity"],
            },
        )
        self.assertEqual(candidate["artifact"]["evaluation_status"], "not_evaluated")
        self.assertEqual(
            candidate["bundle_sha256"],
            "097a7d2c0f35f60aca40c23ecb912714f96a9bf0255db7dadd58dad835bdda64",
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
                "TASK_SPEC",
                "OPERATION_TICKET",
                "PREDECESSOR_EDGE",
                "PRODUCER_BINDING",
                "PRODUCER_RESULT",
                "OWNER_ROLE",
                "ROOT",
                "WORKER_CONTEXT",
                "METHOD_SELECTION",
                "METHOD_RESULT",
                "RECOVERY",
                "EVIDENCE_ADMISSION",
                "ISSUANCE",
                "IMPLEMENTATION_BINDING",
                "FINITE_CLOSURE_CERTIFICATE",
                "REVIEW_REQUIREMENT",
                "PRIOR_REVIEW_RESULT_ADMISSION",
                "REVIEW_EXECUTION_PERMISSION",
                "REVIEW_PACKET",
                "OBSERVATION_LEDGER",
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
            "control stateを`suppressed_by_predecessor`",
            "同じmodel response、custom wrapperまたはshell compound command内",
            "conflict_keys",
            "method_eligible := permission内",
            "does_not_bind_requested_result",
            "実tool-call identityをready ticketへ一対一bind",
            "finite_closure_certificate_ready=true",
            "observation_batch_identity",
            "machine-generatedな`ledger_receipt_identity`",
            "同じcell IDへのwait以外を発行しない",
        ):
            self.assertIn(required, text)

        for rejected in (
            "DISPATCH_ADMISSION",
            "DISPATCH_TRANSITION",
            "dispatch_candidate",
            "dispatch_predecessor",
            "dispatch_frontier",
            "Candidate191",
            "Candidate192",
            "Candidate193",
            "Candidate194",
            "Standard14",
            "ADR9",
        ):
            self.assertNotIn(rejected, text)

    def test_implementation_audit_preserves_m2_and_m3_boundaries(self) -> None:
        m2 = M2_REDESIGN.read_text(encoding="utf-8")
        m3 = M3_REVIEW.read_text(encoding="utf-8")
        audit = IMPLEMENTATION_AUDIT.read_text(encoding="utf-8")

        self.assertIn("responsibilities_27", m2)
        self.assertIn("unresolved_blocking_counterexamples_0", m3)
        for status in (
            "candidate_created / static_verification_passed / not_evaluated",
            "C147を直接親",
            "評価profile、評価run、採用、releaseおよびprojectionは作成・実施していない",
        ):
            self.assertIn(status, audit)

    def test_evaluation_design_checks_actual_cases_before_profile_creation(self) -> None:
        design = EVALUATION_DESIGN.read_text(encoding="utf-8")

        for status in (
            "design_complete / profile_created / comparison_preflight_ready / authorized_45 / slots_issued_0 / not_evaluated",
            "actual_trial_inputs_9_checked",
            "private_oracles_9_checked",
            "quality_oracle_unchanged",
            "mechanism_predicates_frozen",
            "suppressed_by_predecessor_not_observed",
            "conflict_keys_not_observed",
        ):
            self.assertIn(status, design)

        expected = {
            "ADR01": "not_required / artifact_change / completion_ready",
            "ADR02": "not_required / artifact_change / completion_ready",
            "ADR03": "counterexample_found / no_change / blocked",
            "ADR04": "counterexample_found / no_change / blocked",
            "ADR05": "counterexample_found / no_change / blocked",
            "ADR06": "counterexample_found / no_change / blocked",
            "ADR07": "no_counterexample_found / artifact_change / completion_ready",
            "ADR08": "inadmissible_prior_result / no_change / unavailable",
            "ADR09": "unavailable / no_change / unavailable",
        }
        for case, route in expected.items():
            with self.subTest(case=case):
                self.assertIn(f"| {case} |", design)
                self.assertIn(route, design)

        self.assertIn("04c8b680e4884eafa39929e06a935035", design)
        profile = json.loads(PLANNED_PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(
            profile["profile_id"],
            "candidate195-operation-ticketed-review-control-adr9-r2-medium-m24-n5-cli0146",
        )
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-operation-ticketed-review-control-r1",
                "revision": "r1",
                "bundle_sha256": "097a7d2c0f35f60aca40c23ecb912714f96a9bf0255db7dadd58dad835bdda64",
            },
        )
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)

        audit = PREPARATION_AUDIT.read_text(encoding="utf-8")
        for status in (
            "comparison_preflight_ready",
            "candidate195_existing_0",
            "candidate195_missing_45",
            "authorized_45",
            "issued_0",
            "parallel-run`: 不存在",
        ):
            self.assertIn(status, audit)

    def test_registered_result_stops_after_quality_and_mechanism_failures(self) -> None:
        result = json.loads(REGISTERED_RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        report = RESULT_REPORT.read_text(encoding="utf-8")

        self.assertEqual(result["result_id"], "457400a8506d404f8b564074d0b28802")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(quality["quality_score_counts"], {"4": 43, "1": 2})
        self.assertEqual(quality["status"], "quality_failed_stopped")
        self.assertEqual(mechanism["status"], "mechanism_failed_stopped")
        self.assertEqual(mechanism["initial_coissuance_count"], 3)
        self.assertEqual(mechanism["ineligible_status_identity_command_count"], 5)
        self.assertEqual(mechanism["reviewer_cardinality_match_count"], 43)
        self.assertEqual(len(mechanism["failure_run_ids"]), 9)
        self.assertTrue(mechanism["command_evidence_gate_passed"])
        self.assertFalse(mechanism["mechanism_gate_passed"])
        for status in (
            "quality_failed / mechanism_failed / stopped",
            "M6_not_started",
            "Standard14_not_started",
            "Candidate147のままである",
        ):
            self.assertIn(status, report)

    def test_m1_causal_analysis_classifies_all_failures_and_returns_to_c147(self) -> None:
        analysis = CAUSAL_ANALYSIS.read_text(encoding="utf-8")
        for status in (
            "mechanism_failures_9_classified",
            "predispatch_adjudication_not_terminal_operation_8",
            "judgement_dependency_not_ticketed_1",
            "unknown_cause_0",
            "c147_direct_base_retained",
            "candidate195_not_parent",
            "M2_reopen_ready",
        ):
            self.assertIn(status, analysis)
        self.assertEqual(analysis.count("| ADR"), 9)


if __name__ == "__main__":
    unittest.main()
