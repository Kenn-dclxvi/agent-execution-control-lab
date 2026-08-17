#!/usr/bin/env python3
"""Core contract for a one-response Codex semantic-protocol adapter.

This module intentionally has no execution entrypoint.  Formal target and
profile identities must be fixed before any model invocation can use it.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
from typing import Any

import jsonschema


class SemanticCodexAdapterError(Exception):
    pass


TOKEN_ACCOUNTING = {
    "scope": "all_agents",
    "revision": "v1",
    "source": "codex_rollout_final_usage_by_workspace",
}
ELAPSED_BOUNDARY = "adapter_start_to_terminal_process_result_monotonic"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise SemanticCodexAdapterError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise SemanticCodexAdapterError(f"expected JSON object: {path}")
    return value


def validate_prompt_draft(manifest_path: Path) -> tuple[dict[str, Any], bytes]:
    manifest_path = manifest_path.resolve()
    manifest = load_object(manifest_path)
    if manifest.get("schema_version") != "portable-instruction-prompt-draft/v1":
        raise SemanticCodexAdapterError("unsupported prompt draft schema")
    delivery = manifest.get("delivery")
    if not isinstance(delivery, dict) or delivery.get("target") != "AGENTS.md":
        raise SemanticCodexAdapterError("prompt draft must target AGENTS.md")
    source_path = Path(delivery.get("source_path", ""))
    if not source_path.is_absolute():
        source_path = manifest_path.parents[2] / source_path
    source_path = source_path.resolve()
    try:
        content = source_path.read_bytes()
    except OSError as error:
        raise SemanticCodexAdapterError("prompt draft source is unavailable") from error
    if len(content) != delivery.get("bytes"):
        raise SemanticCodexAdapterError("prompt draft byte count mismatch")
    if sha256_bytes(content) != delivery.get("sha256"):
        raise SemanticCodexAdapterError("prompt draft SHA-256 mismatch")
    return manifest, content


def prepare_instruction_workspace(workspace: Path, prompt_bytes: bytes) -> dict[str, Any]:
    workspace = workspace.resolve()
    if workspace.exists():
        raise SemanticCodexAdapterError(f"refusing to overwrite workspace: {workspace}")
    workspace.mkdir(parents=True, mode=0o700)
    instruction = workspace / "AGENTS.md"
    try:
        instruction.write_bytes(prompt_bytes)
    except Exception:
        shutil.rmtree(workspace, ignore_errors=True)
        raise
    instruction.chmod(0o600)
    return {
        "workspace": str(workspace),
        "instruction_path": str(instruction),
        "instruction_bytes": len(prompt_bytes),
        "instruction_sha256": sha256_bytes(prompt_bytes),
        "instruction_mode": "0600",
    }


def build_command(
    *,
    codex: str,
    workspace: Path,
    model: str,
    reasoning_effort: str,
    response_schema: Path,
    final_response: Path,
) -> list[str]:
    for label, value in (("codex", codex), ("model", model), ("reasoning_effort", reasoning_effort)):
        if not isinstance(value, str) or not value or value == "unbound":
            raise SemanticCodexAdapterError(f"{label} is not bound")
    if reasoning_effort not in {"low", "medium", "high", "xhigh", "max"}:
        raise SemanticCodexAdapterError("unsupported reasoning effort")
    workspace = workspace.resolve()
    response_schema = response_schema.resolve()
    final_response = final_response.resolve()
    if not workspace.is_dir() or not (workspace / "AGENTS.md").is_file():
        raise SemanticCodexAdapterError("instruction workspace is not prepared")
    if not response_schema.is_file():
        raise SemanticCodexAdapterError("response schema is unavailable")
    final_response.parent.mkdir(parents=True, exist_ok=True)
    return [
        codex,
        "exec",
        "--skip-git-repo-check",
        "--cd",
        str(workspace),
        "--ignore-user-config",
        "--ignore-rules",
        "--strict-config",
        "--disable",
        "multi_agent",
        "--disable",
        "memories",
        "--disable",
        "apps",
        "--disable",
        "plugins",
        "--disable",
        "plugin_sharing",
        "-c",
        'approval_policy="never"',
        "--model",
        model,
        "-c",
        f'model_reasoning_effort="{reasoning_effort}"',
        "--sandbox",
        "read-only",
        "--output-schema",
        str(response_schema),
        "--json",
        "--output-last-message",
        str(final_response),
        "-",
    ]


def parse_codex_jsonl(value: bytes) -> dict[str, Any]:
    thread_ids: list[str] = []
    completed_usage: list[dict[str, int]] = []
    failures: list[str] = []
    for raw_line in value.splitlines():
        if not raw_line.strip():
            continue
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as error:
            raise SemanticCodexAdapterError("Codex stdout contains non-JSONL data") from error
        if not isinstance(event, dict):
            raise SemanticCodexAdapterError("Codex JSONL event is not an object")
        if event.get("type") == "thread.started" and isinstance(event.get("thread_id"), str):
            thread_ids.append(event["thread_id"])
        elif event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            usage = {
                key: item
                for key, item in event["usage"].items()
                if isinstance(key, str) and isinstance(item, int) and not isinstance(item, bool) and item >= 0
            }
            completed_usage.append(usage)
        elif event.get("type") in {"error", "turn.failed"}:
            failures.append(event.get("type"))
    if failures:
        raise SemanticCodexAdapterError(f"Codex JSONL contains failure events: {failures}")
    if len(thread_ids) != 1:
        raise SemanticCodexAdapterError("Codex JSONL must contain one thread.started")
    if len(completed_usage) != 1:
        raise SemanticCodexAdapterError("Codex JSONL must contain one turn.completed usage")
    total_tokens = completed_usage[0].get("total_tokens")
    if total_tokens is None:
        raise SemanticCodexAdapterError("Codex usage lacks primary total_tokens")
    return {"root_thread_id": thread_ids[0], "root_total_tokens": total_tokens, "raw_usage": completed_usage[0]}


def validate_final_response(final_response: Path, response_schema: Path) -> dict[str, Any]:
    response = load_object(final_response)
    schema = load_object(response_schema)
    try:
        jsonschema.Draft202012Validator(schema).validate(response)
    except jsonschema.ValidationError as error:
        raise SemanticCodexAdapterError("final response does not satisfy response schema") from error
    return response


def adapter_contract() -> dict[str, Any]:
    return {
        "schema_version": "portable-instruction-semantic-codex-adapter-contract/v1",
        "execution_entrypoint_enabled": False,
        "instruction_delivery": {"target": "AGENTS.md", "workspace_contents": ["AGENTS.md"]},
        "model_input": "packet bytes on stdin",
        "output": "one schema-valid JSON object",
        "session_mode": "persisted_for_usage_collection",
        "token_accounting": TOKEN_ACCOUNTING,
        "elapsed_boundary": ELAPSED_BOUNDARY,
        "raw_evidence": ["Codex JSONL stdout", "stderr", "last response", "root and descendant private session transcripts"],
        "formal_target_required_before_execution": True,
    }
