import hashlib
import json
from pathlib import Path

import pytest

from scripts.semantic_protocol_codex_adapter import (
    SemanticCodexAdapterError,
    adapter_contract,
    build_command,
    collect_accounted_usage,
    parse_codex_jsonl,
    prepare_instruction_workspace,
    validate_final_response,
    validate_prompt_draft,
    validate_registered_profile,
)


ROOT = Path(__file__).resolve().parents[1]
PROMPT_MANIFEST = ROOT / "docs/portable-instruction-control-free-prompt-draft-r1/manifest.json"
RESPONSE_SCHEMA = ROOT / "docs/portable-instruction-semantic-conformance-heldout-r1/response.schema.json"
ORACLE = ROOT / "docs/portable-instruction-semantic-conformance-heldout-r1/oracle.json"
TARGET_ROOT = ROOT / "evaluations/targets/portable-instruction-semantic-conformance"
FORMAL_PROFILE = TARGET_ROOT / "profiles/portable-semantic-control-free-codex-cli0146-sol-medium-heldout-r1-n1-r1.json"
FORMAL_TARGET = TARGET_ROOT / "target.json"
FORMAL_BUNDLE = TARGET_ROOT / "prompts/baselines/portable-semantic-a544769-control-free-r1"


def test_control_free_draft_is_zero_byte_agents_md_delivery() -> None:
    manifest, content = validate_prompt_draft(PROMPT_MANIFEST)
    assert content == b""
    assert manifest["delivery"]["target"] == "AGENTS.md"
    assert manifest["delivery"]["sha256"] == hashlib.sha256(b"").hexdigest()
    assert manifest["formal_prompt_identity_ready"] is False
    assert manifest["source_authority"]["repository_commit"] is None


def test_workspace_contains_only_one_self_contained_agents_file(tmp_path: Path) -> None:
    _, content = validate_prompt_draft(PROMPT_MANIFEST)
    workspace = tmp_path / "workspace"
    receipt = prepare_instruction_workspace(workspace, content)
    assert [path.name for path in workspace.iterdir()] == ["AGENTS.md"]
    assert (workspace / "AGENTS.md").read_bytes() == b""
    assert (workspace / "AGENTS.md").stat().st_mode & 0o777 == 0o600
    assert receipt["instruction_sha256"] == hashlib.sha256(b"").hexdigest()


def test_registered_profile_is_fully_bound_but_not_dispatchable() -> None:
    receipt = validate_registered_profile(
        profile_path=FORMAL_PROFILE,
        target_path=FORMAL_TARGET,
        bundle_path=FORMAL_BUNDLE,
        repository_root=ROOT,
    )
    assert receipt["profile_id"] == FORMAL_PROFILE.stem
    assert set(receipt["bound_files"]) == {
        "task_spec",
        "evaluation_set",
        "rating",
        "transcript",
        "capability_catalog",
    }
    assert receipt["dispatch_allowed"] is False
    assert receipt["stop_reason"] == "adapter_execution_entrypoint_disabled"


def test_command_fixes_isolation_schema_and_persisted_usage_boundary(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    prepare_instruction_workspace(workspace, b"")
    command = build_command(
        codex="/Users/kenn/.local/bin/codex",
        workspace=workspace,
        model="gpt-5.6-sol",
        reasoning_effort="medium",
        response_schema=RESPONSE_SCHEMA,
        final_response=tmp_path / "private/final.json",
    )
    assert command[:2] == ["/Users/kenn/.local/bin/codex", "exec"]
    for fixed in ("--ignore-user-config", "--ignore-rules", "--strict-config", "--skip-git-repo-check", "--output-schema", "--json"):
        assert fixed in command
    assert command.count("--disable") == 5
    assert "--ephemeral" not in command
    assert command[-1] == "-"


def test_parse_codex_jsonl_requires_primary_total_tokens_and_one_turn() -> None:
    valid = b'\n'.join(
        [
            b'{"type":"thread.started","thread_id":"root-1"}',
            b'{"type":"turn.completed","usage":{"input_tokens":10,"output_tokens":2,"total_tokens":12}}',
        ]
    )
    parsed = parse_codex_jsonl(valid)
    assert parsed["root_thread_id"] == "root-1"
    assert parsed["root_total_tokens"] == 12

    inferred_only = valid.replace(b',"total_tokens":12', b"")
    with pytest.raises(SemanticCodexAdapterError, match="primary total_tokens"):
        parse_codex_jsonl(inferred_only)


def write_session(
    path: Path,
    *,
    thread_id: str,
    workspace: Path,
    total_tokens: int | None,
    parent_thread_id: str | None = None,
) -> None:
    records = [
        {
            "type": "session_meta",
            "payload": {
                "id": thread_id,
                "cwd": str(workspace.resolve()),
                "parent_thread_id": parent_thread_id,
                "source": "exec" if parent_thread_id is None else {"subagent": {}},
            },
        }
    ]
    if total_tokens is not None:
        records.append(
            {
                "type": "event_msg",
                "payload": {
                    "type": "token_count",
                    "info": {"total_token_usage": {"total_tokens": total_tokens}},
                },
            }
        )
    path.write_text("".join(json.dumps(record) + "\n" for record in records), encoding="utf-8")


def test_collect_accounted_usage_requires_matching_persisted_root_and_descendants(tmp_path: Path) -> None:
    sessions = tmp_path / "sessions"
    workspace = tmp_path / "workspace"
    sessions.mkdir()
    workspace.mkdir()
    write_session(sessions / "root.jsonl", thread_id="root-1", workspace=workspace, total_tokens=12)
    write_session(
        sessions / "child.jsonl",
        thread_id="child-1",
        workspace=workspace,
        total_tokens=5,
        parent_thread_id="root-1",
    )
    events = b'\n'.join(
        [
            b'{"type":"thread.started","thread_id":"root-1"}',
            b'{"type":"turn.completed","usage":{"total_tokens":12}}',
        ]
    )
    usage = collect_accounted_usage(
        session_root=sessions,
        workspace=workspace,
        codex_jsonl=events,
        modified_since=None,
    )
    assert usage["root_total_tokens"] == 12
    assert usage["all_agent_total_tokens"] == 17
    assert usage["session_count"] == 2


def test_collect_accounted_usage_refuses_incomplete_persisted_usage(tmp_path: Path) -> None:
    sessions = tmp_path / "sessions"
    workspace = tmp_path / "workspace"
    sessions.mkdir()
    workspace.mkdir()
    write_session(sessions / "root.jsonl", thread_id="root-1", workspace=workspace, total_tokens=None)
    events = b'\n'.join(
        [
            b'{"type":"thread.started","thread_id":"root-1"}',
            b'{"type":"turn.completed","usage":{"total_tokens":12}}',
        ]
    )
    with pytest.raises(SemanticCodexAdapterError, match="persisted usage is incomplete"):
        collect_accounted_usage(
            session_root=sessions,
            workspace=workspace,
            codex_jsonl=events,
            modified_since=None,
        )


def test_final_response_schema_validation_uses_no_oracle(tmp_path: Path) -> None:
    response = json.loads(ORACLE.read_text(encoding="utf-8"))["cases"][0]["expected_response"]
    response_path = tmp_path / "response.json"
    response_path.write_text(json.dumps(response), encoding="utf-8")
    assert validate_final_response(response_path, RESPONSE_SCHEMA) == response
    response.pop("start_operation_ids")
    response_path.write_text(json.dumps(response), encoding="utf-8")
    with pytest.raises(SemanticCodexAdapterError, match="does not satisfy"):
        validate_final_response(response_path, RESPONSE_SCHEMA)


def test_adapter_contract_cannot_execute_before_profile() -> None:
    contract = adapter_contract()
    assert contract["execution_entrypoint_enabled"] is False
    assert contract["formal_target_required_before_execution"] is True
    assert contract["profile_required_before_execution"] is True
    assert contract["session_mode"] == "persisted_for_usage_collection"
