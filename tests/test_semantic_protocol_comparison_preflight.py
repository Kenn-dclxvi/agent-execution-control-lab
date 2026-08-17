import copy

import pytest

from scripts.semantic_protocol_comparison_preflight import PreflightError, preflight


def condition(prompt_name: str) -> dict:
    return {
        "schema_version": "portable-instruction-semantic-comparison-condition/v1",
        "prompt_set_identity": {"name": prompt_name, "revision": "r1", "sha256": "1" * 64},
        "target_subject_ref": {
            "kind": "semantic_protocol",
            "protocol_id": "portable-instruction-semantic-conformance",
            "protocol_revision": "response-r2",
            "interaction_mode": "single_response_operation_ledger",
            "response_schema_sha256": "2" * 64,
        },
        "runtime_ref": {
            "runtime": "codex-cli",
            "version": "0.146.0",
            "model": "gpt-5.6-sol",
            "reasoning_effort": "medium",
            "token_accounting": {
                "scope": "all_agents",
                "revision": "v1",
                "source": "codex_rollout_final_usage_by_workspace",
            },
            "session_mode": "persisted_for_usage_collection",
            "instruction_isolation": {
                "ignore_user_config": True,
                "ignore_rules": True,
                "memory": False,
                "apps": False,
                "plugins": False,
            },
            "permission": {"sandbox": "read-only", "approval_policy": "never"},
            "capability_catalog": {"schema_version": "model-visible-capability-catalog/v1", "sha256": "3" * 64},
            "elapsed_boundary": "adapter_start_to_terminal_process_result_monotonic",
        },
        "task_spec_ref": {"revision": "semantic-single-json-r1", "sha256": "4" * 64},
        "case_ref": {"set_id": "heldout-r1", "case_id": "PIC-H01", "revision": "r1", "input_sha256": "5" * 64},
        "rating_ref": {"contract_id": "portable-instruction-semantic-exact-v1", "sha256": "6" * 64},
        "repetition_condition": {"iterations": 1, "order": "fixed"},
    }


def test_only_prompt_identity_may_differ() -> None:
    receipt = preflight(condition("control-free"), condition("kernel"))
    assert receipt["compatible"] is True
    assert receipt["dispatch_allowed"] is True
    assert receipt["mismatch_paths"] == []
    assert len(receipt["non_prompt_conditions_sha256"]) == 64


def test_runtime_or_case_drift_blocks_dispatch() -> None:
    left = condition("control-free")
    right = condition("kernel")
    right["runtime_ref"]["model"] = "different-model"
    right["case_ref"]["case_id"] = "PIC-H02"
    receipt = preflight(left, right)
    assert receipt["compatible"] is False
    assert receipt["dispatch_allowed"] is False
    assert receipt["non_prompt_conditions_sha256"] is None
    assert receipt["mismatch_paths"] == ["case_ref.case_id", "runtime_ref.model"]


def test_rejects_repository_ref_and_unbound_values() -> None:
    repository = condition("control-free")
    repository["runtime_ref"]["target_repository_ref"] = {"commit": "fake"}
    with pytest.raises(PreflightError, match="target_repository_ref|runtime fields"):
        preflight(repository, condition("kernel"))

    unbound = condition("control-free")
    unbound["runtime_ref"]["model"] = "unbound"
    with pytest.raises(PreflightError, match="unbound"):
        preflight(unbound, condition("kernel"))


def test_rejects_ephemeral_session_with_transcript_accounting() -> None:
    left = condition("control-free")
    left["runtime_ref"]["session_mode"] = "ephemeral"
    with pytest.raises(PreflightError, match="ephemeral session"):
        preflight(left, condition("kernel"))


def test_rejects_same_prompt_identity() -> None:
    value = condition("same")
    with pytest.raises(PreflightError, match="must differ"):
        preflight(value, copy.deepcopy(value))
