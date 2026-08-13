from __future__ import annotations

import unittest
import json
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-materialized-adjudication-control-r1"
M2_DESIGN = ROOT / "docs/post-candidate195-review-control-m2-materialized-adjudication-design.md"
M3_REVIEW = ROOT / "docs/post-candidate195-review-control-m3-direction-review.md"
IMPLEMENTATION_AUDIT = ROOT / "docs/candidate196-materialized-adjudication-control-implementation-audit.md"
EVALUATION_DESIGN = ROOT / "docs/candidate196-materialized-adjudication-control-adr9-r2-n5-evaluation-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate196-materialized-adjudication-control-adr9-r2-medium-m24-n5-cli0146.json"
PREPARATION_AUDIT = ROOT / "docs/candidate196-materialized-adjudication-control-adr9-r2-n5-execution-preparation-audit.md"
REGISTERED_RESULT = ROOT / "evaluations/results/76fa5af714b149baa2328516e5722f9f.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate196-materialized-adjudication-control-adr9-r2-n5-quality-audit-r3.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate196-materialized-adjudication-control-adr9-r2-n5-mechanism-audit-r3.json"
RESULT_REPORT = ROOT / "evaluations/results/candidate196-materialized-adjudication-control-adr9-r2-n5_2026-08-12.md"


class Candidate196Test(unittest.TestCase):
    def test_c147_direct_child_has_30_materialized_responsibilities(self) -> None:
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
            "352eee02c72101769d374d398db4aae061f4e97a38dc24fa283af8a87e839e2c",
        )

        parent_files = {item["target"]: item for item in parent["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(parent_files.keys(), candidate_files.keys())
        for target in parent_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], parent_files[target], target)

        text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        labels = [line.split(":", 1)[0][2:] for line in text.splitlines() if line.startswith("- ")]
        self.assertEqual(
            labels,
            [
                "TASK_SPEC", "OPERATION_TICKET", "PREDECESSOR_EDGE", "PRODUCER_BINDING",
                "PRODUCER_RESULT", "OWNER_ROLE", "ROOT", "WORKER_CONTEXT", "METHOD_SELECTION",
                "METHOD_RESULT", "RECOVERY", "EVIDENCE_ADMISSION", "ADJUDICATION_MATERIALIZATION",
                "ISSUANCE", "IMPLEMENTATION_BINDING", "FINITE_CLOSURE_CERTIFICATE",
                "REVIEW_REQUIREMENT", "PRIOR_REVIEW_RESULT_ADMISSION", "REVIEW_EXECUTION_PERMISSION",
                "REVIEW_PACKET", "OBSERVATION_LEDGER", "COUNTEREXAMPLE_ADJUDICATION",
                "NO_COUNTEREXAMPLE_ADJUDICATION", "UNAVAILABLE_ADJUDICATION",
                "CURRENT_REVIEW_RESULT_ADMISSION", "CHANGE_ADMISSION", "VALIDATION_PLAN",
                "VALIDATION_CLOSURE", "OPERATION_TERMINAL", "OUTER_TERMINAL",
            ],
        )

        for required in (
            "そのmodel responseで唯一のtool invocation",
            "事前receipt不要の唯一のinvocation class",
            "input_result_identities",
            "selected_invocation_identities",
            "terminal successのadjudication receiptがmodelへ返った次のmodel step",
            "三値tupleなら現在HEADしか返さない",
            "全witnessのOR closure",
            "certificate外missing",
            "同じcell IDへのwait以外を発行せず",
        ):
            self.assertIn(required, text)

        for rejected in (
            "DISPATCH_ADMISSION", "DISPATCH_TRANSITION", "dispatch_candidate",
            "dispatch_predecessor", "dispatch_frontier", "Candidate191", "Candidate192",
            "Candidate193", "Candidate194", "Candidate195", "Standard14", "ADR9",
        ):
            self.assertNotIn(rejected, text)

    def test_m2_m3_and_implementation_boundaries_are_preserved(self) -> None:
        m2 = M2_DESIGN.read_text(encoding="utf-8")
        m3 = M3_REVIEW.read_text(encoding="utf-8")
        audit = IMPLEMENTATION_AUDIT.read_text(encoding="utf-8")

        self.assertIn("responsibilities_30", m2)
        self.assertIn("unresolved_blocking_counterexamples_0", m3)
        for status in (
            "candidate_created / static_verification_passed / not_evaluated",
            "Candidate147 `the-caption-3ce91a4-result-effect-scope-r1`の直接child",
            "評価profileと評価runは別アーティファクト単位",
        ):
            self.assertIn(status, audit)

    def test_evaluation_design_and_preflight_keep_the_fixed_adr9_contract(self) -> None:
        design = EVALUATION_DESIGN.read_text(encoding="utf-8")
        for status in (
            "actual_trial_inputs_9_checked",
            "private_oracles_9_checked",
            "quality_oracle_unchanged",
            "materialized_adjudication_predicates_frozen",
            "result_kind_adjudication_predicates_frozen",
            "comparison_preflight_ready",
            "authorized_45",
            "slots_issued_0",
        ):
            self.assertIn(status, design)

        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-materialized-adjudication-control-r1",
                "revision": "r1",
                "bundle_sha256": "352eee02c72101769d374d398db4aae061f4e97a38dc24fa283af8a87e839e2c",
            },
        )

        preparation = PREPARATION_AUDIT.read_text(encoding="utf-8")
        for status in (
            "candidate196_existing_0",
            "candidate196_missing_45",
            "authorized_45",
            "issued_0",
            "comparison_preflight_ready",
        ):
            self.assertIn(status, preparation)

    def test_registered_result_preserves_quality_and_mechanism_failures(self) -> None:
        result = json.loads(REGISTERED_RESULT.read_text(encoding="utf-8"))
        quality = json.loads(QUALITY_AUDIT.read_text(encoding="utf-8"))
        mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
        report = RESULT_REPORT.read_text(encoding="utf-8")

        self.assertEqual(result["result_id"], "76fa5af714b149baa2328516e5722f9f")
        self.assertEqual(result["result_content_sha256"], "3f0e05b9e1c9dc31f93963990ed13c454a4c16fc781c2e7f942a83bab2a70fd3")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(quality["quality_score_counts"], {"4": 36, "1": 9})
        self.assertEqual(quality["status"], "quality_failed_stopped")
        self.assertEqual(mechanism["status"], "mechanism_failed_stopped")
        self.assertEqual(mechanism["initial_identity_only_count"], 33)
        self.assertEqual(mechanism["receipt_covered_target_count"], 140)
        self.assertEqual(mechanism["receipt_method_family_match_count"], 136)
        self.assertEqual(mechanism["result_kind_adjudication_route_match_count"], 26)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        for status in (
            "quality_failed / mechanism_failed / stopped",
            "M6_not_started",
            "Standard14_not_started",
            "c147_direct_base_retained",
            "candidate196_not_parent",
        ):
            self.assertIn(status, report)


if __name__ == "__main__":
    unittest.main()
