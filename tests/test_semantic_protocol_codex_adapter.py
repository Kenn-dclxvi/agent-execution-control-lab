import hashlib
import json
from pathlib import Path

import pytest

from scripts.semantic_protocol_codex_adapter import (
    SemanticCodexAdapterError,
    adapter_contract,
    build_command,
    parse_codex_jsonl,
    prepare_instruction_workspace,
    validate_final_response,
    validate_prompt_draft,
)


ROOT = Path(__file__).resolve().parents[1]
PROMPT_MANIFEST = ROOT / "docs/portable-instruction-control-free-prompt-draft-r1/manifest.json"
RESPONSE_SCHEMA = ROOT / "docs/portable-instruction-semantic-conformance-heldout-r1/response.schema.json"
ORACLE = ROOT / "docs/portable-instruction-semantic-conformance-heldout-r1/oracle.json"


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


def test_final_response_schema_validation_uses_no_oracle(tmp_path: Path) -> None:
    response = json.loads(ORACLE.read_text(encoding="utf-8"))["cases"][0]["expected_response"]
    response_path = tmp_path / "response.json"
    response_path.write_text(json.dumps(response), encoding="utf-8")
    assert validate_final_response(response_path, RESPONSE_SCHEMA) == response
    response.pop("start_operation_ids")
    response_path.write_text(json.dumps(response), encoding="utf-8")
    with pytest.raises(SemanticCodexAdapterError, match="does not satisfy"):
        validate_final_response(response_path, RESPONSE_SCHEMA)


def test_adapter_contract_cannot_execute_before_formal_target() -> None:
    contract = adapter_contract()
    assert contract["execution_entrypoint_enabled"] is False
    assert contract["formal_target_required_before_execution"] is True
    assert contract["session_mode"] == "persisted_for_usage_collection"
