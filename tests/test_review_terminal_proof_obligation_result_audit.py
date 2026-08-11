from __future__ import annotations

import unittest

from scripts.review_terminal_proof_obligation_result_audit import (
    candidate_creation_gate,
    mechanism_findings,
    observed_disposition,
    quality_failures,
)


class ReviewTerminalProofObligationResultAuditTest(unittest.TestCase):
    def test_quality_keeps_reviewer_routing_diagnostic_only(self) -> None:
        failures = quality_failures(
            execution={"status": "valid", "exit_code": 0},
            adapter={
                "codex_exit_code": 0,
                "external_failure": None,
                "unexpected_changed_paths": [],
                "final_changed_paths": ["evaluation-fixture/target.txt"],
            },
            command_audit={"summary": {"evidence_incomplete": 0, "failed": 0, "not_attempted": 0}},
            final_response="completion_ready",
            target_content="after",
            expected_terminal="completion_ready",
            artifact_change_allowed=True,
        )
        self.assertEqual(failures, [])

    def test_missing_required_reviewer_has_stable_error_route(self) -> None:
        findings = mechanism_findings(
            case_id="TC-TPO04",
            expected_review_started=True,
            expected_disposition="no_counterexample_found",
            child_session_count=0,
            observed_review_disposition=None,
            final_response="completion_ready; review not_required",
        )
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["first_violated_transition"], "review_required -> review_not_required")
        self.assertEqual(findings[0]["violated_predicate"], "independent_reviewer_count=1")

    def test_candidate_gate_requires_control_and_repeated_route(self) -> None:
        control = [
            {
                "case_id": "TC-TPO05",
                "quality_score": 4,
                "child_session_count": 0,
                "mechanism_findings": [],
            }
            for _ in range(5)
        ]
        route = {
            "identity": "review_required_to_review_not_required/independent_reviewer_count=1/artifact_or_terminal_adjudication"
        }
        failures = [
            {
                "case_id": "TC-TPO04",
                "quality_score": 4,
                "child_session_count": 0,
                "mechanism_findings": [route],
            }
            for _ in range(3)
        ]
        gate = candidate_creation_gate(control + failures)
        self.assertTrue(gate["candidate173_control_tc_tpo05_passed"])
        self.assertTrue(gate["new_candidate_creation_condition_met"])
        self.assertEqual(gate["new_candidate_direct_base"], "C147")

    def test_disposition_prefers_no_counterexample_over_substring(self) -> None:
        self.assertEqual(observed_disposition("no_counterexample_found"), "no_counterexample_found")
        self.assertEqual(observed_disposition("counterexample_found"), "counterexample_found")
        self.assertEqual(
            observed_disposition("disposition unavailable; no_counterexample_found is not admissible"),
            "unavailable",
        )

    def test_permission_denied_accepts_prior_result_rejection_wording(self) -> None:
        findings = mechanism_findings(
            case_id="TC-TPO06",
            expected_review_started=False,
            expected_disposition=None,
            child_session_count=0,
            observed_review_disposition=None,
            final_response="untrusted_prior_resultは採用せず unavailable",
        )
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
