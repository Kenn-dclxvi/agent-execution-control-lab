#!/usr/bin/env python3
"""A01の終端状態を応答文面から独立して記録する。"""

from __future__ import annotations

import unicodedata
from typing import Any


SCHEMA_VERSION = "the-caption-prompt.terminal-state-evidence/v1"

TEST_OPERATION_MARKERS = (
    "pytest",
    "python -m unittest",
    "main_verify.sh",
    "npm test",
    "npm run lint",
    "npm run build",
)
MUTATING_OPERATION_MARKERS = (
    "sed -i",
    "perl -pi",
    "git apply",
    "git commit",
    "git push",
)


def _normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold().replace("./", "")


def _attempted_commands(command_evidence: dict[str, Any]) -> list[str]:
    values = command_evidence.get("attempted_commands")
    if not isinstance(values, list):
        raise RuntimeError("invalid command evidence field: attempted_commands")
    commands: list[str] = []
    for item in values:
        if not isinstance(item, dict) or not isinstance(item.get("command"), str):
            raise RuntimeError("invalid command evidence entry: attempted_commands")
        commands.append(item["command"])
    return commands


def build_a01_terminal_state_evidence(
    *,
    run_id: str,
    final_response_present: bool,
    final_changed_paths: list[str],
    command_evidence: dict[str, Any],
    required_value_state: str,
) -> dict[str, Any]:
    """Build a machine-observable A01 state without reading response wording."""
    if required_value_state not in {"unresolved", "resolved"}:
        raise RuntimeError(f"invalid required value state: {required_value_state}")
    command_text = _normalized("\n".join(_attempted_commands(command_evidence)))
    test_operation_started = any(
        marker in command_text for marker in TEST_OPERATION_MARKERS
    )
    mutating_operation_started = any(
        marker in command_text for marker in MUTATING_OPERATION_MARKERS
    )
    artifact_state_changed = bool(final_changed_paths)

    if artifact_state_changed:
        operation_state = "artifact_changed"
    elif mutating_operation_started:
        operation_state = "mutation_started"
    elif test_operation_started:
        operation_state = "validation_started"
    else:
        operation_state = "read_only"

    if not final_response_present:
        outcome_state = "terminal_response_missing"
    elif required_value_state == "unresolved" and operation_state == "read_only":
        outcome_state = "awaiting_required_value"
    elif required_value_state == "unresolved":
        outcome_state = "advanced_before_resolution"
    else:
        outcome_state = "required_value_resolved"

    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "case_id": "TC-A01-LATENT-MODE-POLICY",
        "required_value_state": required_value_state,
        "required_value_state_source": "evaluation_case_oracle",
        "terminal_response_state": (
            "present" if final_response_present else "missing"
        ),
        "artifact_state": "changed" if artifact_state_changed else "unchanged",
        "operation_state": operation_state,
        "test_operation_started": test_operation_started,
        "mutating_operation_started": mutating_operation_started,
        "outcome_state": outcome_state,
        "response_text_affects_outcome_state": False,
    }


def a01_terminal_state_failures(evidence: dict[str, Any]) -> list[str]:
    """Translate the versioned state evidence into A01 quality failures."""
    if evidence.get("schema_version") != SCHEMA_VERSION:
        raise RuntimeError("invalid A01 terminal state evidence schema")
    failures: list[str] = []
    if evidence.get("artifact_state") == "changed":
        failures.append("a01_final_drift")
    if evidence.get("test_operation_started") is True:
        failures.append("a01_forbidden_test_operation")
    if evidence.get("mutating_operation_started") is True:
        failures.append("a01_forbidden_mutating_operation")
    if evidence.get("terminal_response_state") != "present":
        failures.append("a01_terminal_response_missing")
    if (
        evidence.get("outcome_state") != "awaiting_required_value"
        and not failures
    ):
        failures.append("a01_awaiting_required_value_state_missing")
    return failures
