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

try:
    from .all_agent_usage import (
        AllAgentUsageError,
        TOKEN_ACCOUNTING as ALL_AGENT_TOKEN_ACCOUNTING,
        collect_workspace_usage,
        collect_workspace_usage_by_root,
    )
    from .export_prompt_bundle import BundleError, verify_bundle
except ImportError:
    from all_agent_usage import (
        AllAgentUsageError,
        TOKEN_ACCOUNTING as ALL_AGENT_TOKEN_ACCOUNTING,
        collect_workspace_usage,
        collect_workspace_usage_by_root,
    )
    from export_prompt_bundle import BundleError, verify_bundle


class SemanticCodexAdapterError(Exception):
    pass


TOKEN_ACCOUNTING = {
    "scope": "all_agents",
    "revision": "v1",
    "source": "codex_rollout_final_usage_by_workspace",
}
TOKEN_ACCOUNTING_V2 = {
    "scope": "all_agents",
    "revision": "v2",
    "source": "codex_rollout_final_usage_by_thread_bound_workspace",
}
ELAPSED_BOUNDARY = "adapter_start_to_terminal_process_result_monotonic"
OUTPUT_SCHEMA_TRANSPORT_R2 = {
    "revision": "codex-structured-output-projection-r2",
    "api_schema_projection": "remove_uniqueItems_only",
    "canonical_post_validation": True,
}
OUTPUT_SCHEMA_TRANSPORT_R3 = {
    "revision": "codex-structured-output-supported-subset-r3",
    "api_schema_projection": "supported_subset_semantic_equivalence",
    "canonical_post_validation": True,
}


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


def validate_registered_profile(
    *,
    profile_path: Path,
    target_path: Path,
    bundle_path: Path,
    repository_root: Path,
) -> dict[str, Any]:
    profile = load_object(profile_path.resolve())
    target = load_object(target_path.resolve())
    repository_root = repository_root.resolve()
    if profile.get("schema_version") != "portable-instruction-semantic-profile/v1":
        raise SemanticCodexAdapterError("unsupported semantic profile schema")
    if profile.get("lifecycle_state") != "registered_not_qualified":
        raise SemanticCodexAdapterError("semantic profile lifecycle state is invalid")
    if target.get("schema_version") != "the-caption-prompt.evaluation-target/v2":
        raise SemanticCodexAdapterError("semantic target is not registered as v2")
    if profile.get("target_id") != target.get("target_id"):
        raise SemanticCodexAdapterError("profile target identity mismatch")
    subject = dict(target.get("target_subject") or {})
    subject.pop("subject_authority", None)
    if profile.get("target_subject_ref") != subject:
        raise SemanticCodexAdapterError("profile target subject mismatch")
    try:
        bundle = verify_bundle(bundle_path.resolve())
    except (BundleError, OSError) as error:
        raise SemanticCodexAdapterError("registered prompt bundle is invalid") from error
    prompt = profile.get("prompt_set_identity")
    if not isinstance(prompt, dict) or prompt.get("name") != bundle.get("prompt_identity"):
        raise SemanticCodexAdapterError("profile prompt identity mismatch")
    if prompt.get("sha256") != bundle.get("bundle_sha256"):
        raise SemanticCodexAdapterError("profile prompt bundle hash mismatch")

    bound_files: dict[str, str] = {}
    references = {
        "task_spec": profile.get("task_spec_ref"),
        "evaluation_set": profile.get("evaluation_set_ref"),
        "rating": profile.get("rating_ref"),
        "transcript": profile.get("transcript_ref"),
        "capability_catalog": (profile.get("runtime_ref") or {}).get("capability_catalog"),
    }
    for label, reference in references.items():
        if not isinstance(reference, dict):
            raise SemanticCodexAdapterError(f"profile {label} reference is invalid")
        raw_path = reference.get("path")
        expected = reference.get("sha256")
        if not isinstance(raw_path, str) or not isinstance(expected, str):
            raise SemanticCodexAdapterError(f"profile {label} reference is unbound")
        path = (repository_root / raw_path).resolve()
        try:
            path.relative_to(repository_root)
        except ValueError as error:
            raise SemanticCodexAdapterError(f"profile {label} path escapes repository") from error
        if not path.is_file() or sha256_bytes(path.read_bytes()) != expected:
            raise SemanticCodexAdapterError(f"profile {label} hash mismatch")
        bound_files[label] = expected

    runtime = profile.get("runtime_ref")
    expected_runtime = {
        "runtime": "codex-cli",
        "version": "0.146.0",
        "model": "gpt-5.6-sol",
        "reasoning_effort": "medium",
        "token_accounting": TOKEN_ACCOUNTING,
        "session_mode": "persisted_for_usage_collection",
        "instruction_isolation": {
            "ignore_user_config": True,
            "ignore_rules": True,
            "memory": False,
            "apps": False,
            "plugins": False,
            "plugin_sharing": False,
            "multi_agent": False,
        },
        "permission": {"sandbox": "read-only", "approval_policy": "never"},
        "capability_catalog": references["capability_catalog"],
        "elapsed_boundary": ELAPSED_BOUNDARY,
    }
    allowed_runtimes = [
        expected_runtime,
        {**expected_runtime, "output_schema_transport": OUTPUT_SCHEMA_TRANSPORT_R2},
        {**expected_runtime, "output_schema_transport": OUTPUT_SCHEMA_TRANSPORT_R3},
        {
            **expected_runtime,
            "token_accounting": TOKEN_ACCOUNTING_V2,
            "output_schema_transport": OUTPUT_SCHEMA_TRANSPORT_R3,
        },
    ]
    if runtime not in allowed_runtimes:
        raise SemanticCodexAdapterError("profile runtime differs from adapter contract")
    if profile.get("execution") != {
        "max_workers": 24,
        "schedule_policy": "global_queue",
        "max_attempts_per_slot": 1,
        "dispatch_gate": "adapter_entrypoint_and_preflight_required",
    }:
        raise SemanticCodexAdapterError("profile execution gate is invalid")
    wrapper_path = repository_root / profile["task_spec_ref"]["path"]
    if wrapper_path.read_text(encoding="utf-8").count("{{MODEL_PACKET_JSON}}") != 1:
        raise SemanticCodexAdapterError("TaskSpec wrapper must contain one packet placeholder")
    return {
        "schema_version": "portable-instruction-semantic-profile-binding/v1",
        "profile_id": profile["profile_id"],
        "target_id": target["target_id"],
        "prompt_identity": bundle["prompt_identity"],
        "bound_files": bound_files,
        "dispatch_allowed": False,
        "stop_reason": "adapter_execution_entrypoint_disabled",
    }


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
    parsed = parse_codex_jsonl_identity(value)
    total_tokens = parsed["raw_usage"].get("total_tokens")
    if total_tokens is None:
        raise SemanticCodexAdapterError("Codex usage lacks primary total_tokens")
    return {**parsed, "root_total_tokens": total_tokens}


def parse_codex_jsonl_identity(value: bytes) -> dict[str, Any]:
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
    return {"root_thread_id": thread_ids[0], "raw_usage": completed_usage[0]}


def collect_accounted_usage(
    *,
    session_root: Path,
    workspace: Path,
    codex_jsonl: bytes,
    modified_since: float | None,
) -> dict[str, Any]:
    """Bind exec JSONL root usage to the persisted root and descendant rollouts."""

    if ALL_AGENT_TOKEN_ACCOUNTING != TOKEN_ACCOUNTING:
        raise SemanticCodexAdapterError("all-agent token accounting contract mismatch")
    root = parse_codex_jsonl(codex_jsonl)
    try:
        usage = collect_workspace_usage(
            session_root.resolve(),
            workspace.resolve(),
            root["root_thread_id"],
            root["root_total_tokens"],
            modified_since=modified_since,
        )
    except AllAgentUsageError as error:
        raise SemanticCodexAdapterError("all-agent persisted usage is incomplete") from error
    if usage.get("token_accounting") != TOKEN_ACCOUNTING:
        raise SemanticCodexAdapterError("all-agent usage uses an unsupported accounting identity")
    if usage.get("all_agent_total_tokens") is None:
        raise SemanticCodexAdapterError("all-agent usage lacks primary total_tokens")
    return usage


def collect_accounted_usage_persisted(
    *,
    session_root: Path,
    workspace: Path,
    codex_jsonl: bytes,
    modified_since: float | None,
) -> dict[str, Any]:
    root = parse_codex_jsonl_identity(codex_jsonl)
    try:
        usage = collect_workspace_usage_by_root(
            session_root.resolve(),
            workspace.resolve(),
            root["root_thread_id"],
            modified_since=modified_since,
        )
    except AllAgentUsageError as error:
        raise SemanticCodexAdapterError("thread-bound persisted usage is incomplete") from error
    if usage.get("token_accounting") != TOKEN_ACCOUNTING_V2:
        raise SemanticCodexAdapterError("thread-bound usage uses an unsupported accounting identity")
    if usage.get("all_agent_total_tokens") is None:
        raise SemanticCodexAdapterError("thread-bound all-agent usage lacks primary total_tokens")
    return usage


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
        "profile_required_before_execution": True,
        "token_admission": "persisted root and recursive descendant final usage must match exec JSONL root usage",
    }
