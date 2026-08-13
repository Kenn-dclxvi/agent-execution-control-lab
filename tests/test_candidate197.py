from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.export_prompt_bundle import verify_bundle


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "prompts/candidates/the-caption-3ce91a4-result-effect-scope-r1"
CANDIDATE = ROOT / "prompts/candidates/the-caption-3ce91a4-local-review-application-r1"
DESIGN = ROOT / "docs/post-candidate196-c147-local-review-application-design.md"
DIRECTION_REVIEW = ROOT / "docs/post-candidate196-c147-local-review-direction-review.md"
IMPLEMENTATION_AUDIT = ROOT / "docs/candidate197-local-review-application-implementation-audit.md"
EVALUATION_DESIGN = ROOT / "docs/candidate197-local-review-application-adr9-r2-n5-evaluation-design.md"
PROFILE = ROOT / "evaluations/profiles/candidate197-local-review-application-adr9-r2-medium-m24-n5-cli0146.json"
PREPARATION_AUDIT = ROOT / "docs/candidate197-local-review-application-adr9-r2-n5-execution-preparation-audit.md"
REGISTERED_RESULT = ROOT / "evaluations/results/01ec5be067fb4c25924130860f622794.json"
QUALITY_AUDIT = ROOT / "evaluations/results/candidate197-local-review-application-adr9-r2-n5-quality-audit-r1.json"
MECHANISM_AUDIT = ROOT / "evaluations/results/candidate197-local-review-application-adr9-r2-n5-mechanism-audit-r1.json"
RESULT_REPORT = ROOT / "evaluations/results/candidate197-local-review-application-adr9-r2-n5_2026-08-12.md"


class Candidate197Test(unittest.TestCase):
    def test_c147_direct_child_appends_only_three_local_review_connections(self) -> None:
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
            "7891dcb31349a2e57581d53f518c9cd4778662ce0f3bfd430d2b803457b50901",
        )

        parent_files = {item["target"]: item for item in parent["files"]}
        candidate_files = {item["target"]: item for item in candidate["files"]}
        self.assertEqual(parent_files.keys(), candidate_files.keys())
        for target in parent_files:
            if target != "AGENTS.md":
                self.assertEqual(candidate_files[target], parent_files[target], target)

        parent_text = (PARENT / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        candidate_text = (CANDIDATE / "files/AGENTS.md.txt").read_text(encoding="utf-8")
        self.assertTrue(candidate_text.startswith(parent_text))

        labels = [
            line.split(":", 1)[0][2:]
            for line in candidate_text.splitlines()
            if line.startswith("- ")
        ]
        self.assertEqual(
            labels,
            [
                "SPEC", "PRODUCER", "TERMINAL", "CONTEXT", "EVIDENCE_GATE",
                "OWNER_ROLE", "ROOT", "INDEPENDENCE", "DECISION_BOUNDARY",
                "VALIDATION_CLOSURE", "VALIDATION_PLAN", "METHOD", "RECOVERY",
                "REVIEW_OBLIGATION", "REVIEW_RESULT_ADMISSION", "REVIEW_RESULT_EFFECT",
            ],
        )

        for required in (
            "review_obligation := not_required | required | denied",
            "closure successまたは`implementation_bound=true`だけでrequired reviewを免除しない",
            "counterexample_found | no_counterexample_found | unavailable",
            "saved prior resultはcurrent resultと分け",
            "certificateが消費しないmissing",
            "変更も外側terminalも形成しない",
            "開始identity、repository evidence、method、validationおよび一般dispatchを所有または変更しない",
        ):
            self.assertIn(required, candidate_text)

        for rejected in (
            "OPERATION_TICKET", "PREDECESSOR_EDGE", "method receipt",
            "observation ledger", "ADJUDICATION_MATERIALIZATION", "DISPATCH_ADMISSION",
            "DISPATCH_TRANSITION", "dispatch_frontier", "Candidate194", "Candidate195",
            "Candidate196", "Standard14", "ADR9",
        ):
            self.assertNotIn(rejected, candidate_text)

    def test_design_direction_review_and_audit_preserve_static_boundary(self) -> None:
        design = DESIGN.read_text(encoding="utf-8")
        review = DIRECTION_REVIEW.read_text(encoding="utf-8")
        audit = IMPLEMENTATION_AUDIT.read_text(encoding="utf-8")

        for status in (
            "known_cases_23_classified",
            "unclassified_0",
            "candidate_not_created",
        ):
            self.assertIn(status, design)
        for status in (
            "reviewed_states_16",
            "blocking_counterexamples_0",
            "candidate_implementation_not_started",
        ):
            self.assertIn(status, review)
        for status in (
            "candidate_created / static_verification_passed / not_evaluated",
            "C147の13条項を逐語保持",
            "profile、comparison preflightおよび評価slot",
        ):
            self.assertIn(status, audit)

        evaluation_design = EVALUATION_DESIGN.read_text(encoding="utf-8")
        for status in (
            "actual_trial_inputs_9_checked",
            "private_oracles_9_checked",
            "quality_oracle_unchanged",
            "mechanism_predicates_frozen",
            "profile_created",
            "comparison_preflight_ready",
            "authorized_45",
            "slots_issued_0",
        ):
            self.assertIn(status, evaluation_design)

        profile = json.loads(PROFILE.read_text(encoding="utf-8"))
        self.assertEqual(profile["iterations"], 5)
        self.assertEqual(profile["execution"]["max_workers"], 24)
        self.assertEqual(
            profile["prompt_set_identity"],
            {
                "name": "the-caption-3ce91a4-local-review-application-r1",
                "revision": "r1",
                "bundle_sha256": "7891dcb31349a2e57581d53f518c9cd4778662ce0f3bfd430d2b803457b50901",
            },
        )

        preparation = PREPARATION_AUDIT.read_text(encoding="utf-8")
        for status in (
            "candidate197_existing_0",
            "candidate197_missing_45",
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

        self.assertEqual(result["result_id"], "01ec5be067fb4c25924130860f622794")
        self.assertEqual(result["result_content_sha256"], "20325b3fb629796f0a62eceffb9e17030f2d3c69852adffd846533274eea7cad")
        self.assertEqual(len(result["case_results"]), 45)
        self.assertEqual(quality["quality_score_counts"], {"4": 32, "1": 13})
        self.assertEqual(quality["status"], "quality_failed_stopped")
        self.assertEqual(mechanism["status"], "mechanism_failed_stopped")
        self.assertEqual(mechanism["reviewer_cardinality_match_count"], 29)
        self.assertEqual(mechanism["review_result_admission_match_count"], 21)
        self.assertEqual(mechanism["review_result_effect_match_count"], 33)
        self.assertEqual(mechanism["initial_identity_only_count"], 4)
        self.assertFalse(mechanism["mechanism_gate_passed"])
        for status in (
            "quality_failed / mechanism_failed / stopped",
            "Standard14_not_started",
            "c147_direct_base_retained",
            "candidate197_not_parent",
        ):
            self.assertIn(status, report)


if __name__ == "__main__":
    unittest.main()
