from __future__ import annotations

import unittest

from scripts.terminal_state_evidence import (
    SCHEMA_VERSION,
    a01_terminal_state_failures,
    build_a01_terminal_state_evidence,
)


class TerminalStateEvidenceTest(unittest.TestCase):
    def build(
        self,
        *,
        final_response_present: bool = True,
        final_changed_paths: list[str] | None = None,
        attempted_commands: list[dict[str, str]] | None = None,
    ) -> dict:
        return build_a01_terminal_state_evidence(
            run_id="run-1",
            final_response_present=final_response_present,
            final_changed_paths=final_changed_paths or [],
            command_evidence={
                "attempted_commands": attempted_commands or [],
            },
            required_value_state="unresolved",
        )

    def test_read_only_terminal_state_waits_for_required_value(self) -> None:
        evidence = self.build()

        self.assertEqual(evidence["schema_version"], SCHEMA_VERSION)
        self.assertEqual(
            evidence["required_value_state_source"], "evaluation_case_oracle"
        )
        self.assertEqual(evidence["outcome_state"], "awaiting_required_value")
        self.assertFalse(evidence["response_text_affects_outcome_state"])
        self.assertEqual(a01_terminal_state_failures(evidence), [])

    def test_missing_terminal_response_is_not_a_waiting_state(self) -> None:
        evidence = self.build(final_response_present=False)

        self.assertEqual(evidence["outcome_state"], "terminal_response_missing")
        self.assertEqual(
            a01_terminal_state_failures(evidence),
            ["a01_terminal_response_missing"],
        )

    def test_mutation_attempt_is_advanced_before_resolution(self) -> None:
        evidence = self.build(
            attempted_commands=[{"command": "git apply change.patch"}]
        )

        self.assertEqual(evidence["operation_state"], "mutation_started")
        self.assertEqual(evidence["outcome_state"], "advanced_before_resolution")
        self.assertEqual(
            a01_terminal_state_failures(evidence),
            ["a01_forbidden_mutating_operation"],
        )


if __name__ == "__main__":
    unittest.main()
