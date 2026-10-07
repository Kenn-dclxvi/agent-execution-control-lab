#!/usr/bin/env python3
"""Layer 2 adapter that overlays a prompt bundle and runs Claude Code CLI.

The adapter keeps the workspace preparation, task rendering boundary, teardown
and changed-path rules of the Codex adapter, and replaces only the executor,
the measurement collectors and the executor-specific command protocol text.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from comparison_identity import behavior_plugins
    from export_prompt_bundle import BundleError, verify_bundle
    from all_agent_command_evidence import (
        adapter_owned_cleanup_attempts,
        command_requirement_statuses,
    )
    from claude_all_agent_evidence import (
        COMMAND_EVIDENCE_SCHEMA_VERSION,
        TOKEN_ACCOUNTING,
        ClaudeEvidenceError,
        collect_commands,
        collect_usage,
        parse_stream,
    )
    from run_codex_evaluation import (
        AdapterError,
        adapter_teardown_paths_from_protocol,
        changed_paths,
        command_evidence_external_failure,
        command_protocol_for_case,
        load_object,
        overlay_bundle,
        prepare_runtime_links,
        prompt_fixture_collisions,
        prompt_overlay_commit,
        prompt_set_identity_from_binding,
        remove_adapter_owned_outputs,
        require_object,
        require_string,
        require_string_array,
        write_json,
    )
except ModuleNotFoundError:  # Imported as scripts.run_claude_evaluation in tests.
    from scripts.comparison_identity import behavior_plugins
    from scripts.export_prompt_bundle import BundleError, verify_bundle
    from scripts.all_agent_command_evidence import (
        adapter_owned_cleanup_attempts,
        command_requirement_statuses,
    )
    from scripts.claude_all_agent_evidence import (
        COMMAND_EVIDENCE_SCHEMA_VERSION,
        TOKEN_ACCOUNTING,
        ClaudeEvidenceError,
        collect_commands,
        collect_usage,
        parse_stream,
    )
    from scripts.run_codex_evaluation import (
        AdapterError,
        adapter_teardown_paths_from_protocol,
        changed_paths,
        command_evidence_external_failure,
        command_protocol_for_case,
        load_object,
        overlay_bundle,
        prepare_runtime_links,
        prompt_fixture_collisions,
        prompt_overlay_commit,
        prompt_set_identity_from_binding,
        remove_adapter_owned_outputs,
        require_object,
        require_string,
        require_string_array,
        write_json,
    )


ADAPTER_SCHEMA_VERSION = "the-caption-prompt.claude-adapter/v1"
CLAUDE_ENVIRONMENT_SCHEMA_VERSION = "the-caption-prompt.claude-code-environment/v1"
CLAUDE_COMMAND_PROTOCOL_TEXT_REVISION = "claude-bash-separate-command-r1"
EXTERNAL_FAILURE_EXIT_CODE = 75
FORBIDDEN_CONFIG_ENTRIES = (
    "CLAUDE.md",
    "settings.json",
    "settings.local.json",
    "agents",
    "commands",
    "skills",
    "plugins",
    "output-styles",
    "hooks",
    "rules",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def claude_environment_from_conditions(conditions: dict[str, Any]) -> dict[str, Any]:
    agent_environment = require_object(
        conditions.get("agent_environment"), "comparison_conditions.agent_environment"
    )
    claude = require_object(agent_environment.get("claude_code"), "agent_environment.claude_code")
    if claude.get("schema_version") != CLAUDE_ENVIRONMENT_SCHEMA_VERSION:
        raise AdapterError("unsupported Claude Code environment schema")
    for key in ("executable", "executable_sha256", "version_output", "config_dir", "setting_sources"):
        require_string(claude.get(key), f"agent_environment.claude_code.{key}")
    require_string_array(claude.get("tools"), "agent_environment.claude_code.tools")
    require_string_array(claude.get("agents"), "agent_environment.claude_code.agents")
    if not isinstance(claude.get("plugins"), list):
        raise AdapterError("agent_environment.claude_code.plugins must be an array")
    settings = require_object(claude.get("flag_settings"), "agent_environment.claude_code.flag_settings")
    if set(settings) != {"enabledPlugins"}:
        raise AdapterError("flag_settings may only fix enabledPlugins")
    environment = require_object(
        claude.get("process_environment"), "agent_environment.claude_code.process_environment"
    )
    for key, value in environment.items():
        require_string(value, f"agent_environment.claude_code.process_environment.{key}")
    if "CLAUDE_CONFIG_DIR" in environment or "HOME" in environment:
        raise AdapterError("process_environment must not override config dir or HOME")
    return claude


def verify_executable(claude: dict[str, Any]) -> dict[str, Any]:
    executable = Path(claude["executable"])
    if not executable.is_absolute() or not executable.is_file() or executable.is_symlink():
        raise AdapterError("Claude Code executable must be an absolute regular file")
    actual_sha256 = sha256_file(executable)
    if actual_sha256 != claude["executable_sha256"]:
        raise AdapterError("Claude Code executable hash differs from the comparison condition")
    completed = subprocess.run(
        [str(executable), "--version"], capture_output=True, check=False, env=minimal_environment(claude)
    )
    version_output = completed.stdout.decode("utf-8", errors="replace").strip()
    if completed.returncode != 0 or version_output != claude["version_output"]:
        raise AdapterError("Claude Code version output differs from the comparison condition")
    return {
        "executable": str(executable),
        "executable_sha256": actual_sha256,
        "version_output": version_output,
    }


def minimal_environment(claude: dict[str, Any]) -> dict[str, str]:
    environment = {
        "HOME": str(Path.home()),
        "USER": os.environ.get("USER", ""),
        "LOGNAME": os.environ.get("LOGNAME", os.environ.get("USER", "")),
        "TMPDIR": os.environ.get("TMPDIR", "/tmp"),
        "CLAUDE_CONFIG_DIR": claude["config_dir"],
    }
    environment.update(claude["process_environment"])
    return environment


def config_isolation_receipt(claude: dict[str, Any]) -> dict[str, Any]:
    config_dir = Path(claude["config_dir"])
    if not config_dir.is_absolute() or not config_dir.is_dir():
        raise AdapterError("Claude config dir must be an existing absolute directory")
    present = sorted(name for name in FORBIDDEN_CONFIG_ENTRIES if (config_dir / name).exists())
    if present:
        raise AdapterError("Claude config dir contains personal configuration: " + ", ".join(present))
    entries = sorted(path.name for path in config_dir.iterdir())
    return {
        "schema_version": "the-caption-prompt.claude-config-isolation/v1",
        "config_dir": str(config_dir),
        "forbidden_entries_checked": list(FORBIDDEN_CONFIG_ENTRIES),
        "forbidden_entries_present": present,
        "top_level_entry_names": entries,
        "credential_values_recorded": False,
    }


def render_task(case: dict[str, Any], command_evidence_protocol: dict[str, Any] | None) -> str:
    payload = require_object(case.get("payload"), "case.payload")
    trial_input = require_object(payload.get("trial_prompt_input"), "case.payload.trial_prompt_input")
    serialized = json.dumps(trial_input, ensure_ascii=False, indent=2, sort_keys=True)
    task = "以下のTaskSpecに従って作業してください。\n\n<task-spec-json>\n" + serialized + "\n</task-spec-json>\n"
    if command_evidence_protocol is not None:
        task += (
            "\n以下は全candidate共通の評価用command証跡protocolです。\n"
            "TaskSpecのrequired validation commandは1 commandずつ個別のBash tool呼び出しで実行し、"
            "compound commandへまとめないでください。\n"
            "subagentへ委譲する場合も依頼内容に同じprotocolを含め、成功の終了状態を確認できない"
            "commandをPASSと報告しないでください。\n"
            "<command-evidence-protocol-json>\n"
            + json.dumps(command_evidence_protocol, ensure_ascii=False, sort_keys=True)
            + "\n</command-evidence-protocol-json>\n"
        )
    return task


def surface_mismatches(init: dict[str, Any], claude: dict[str, Any], model: str) -> list[str]:
    observed = dict(init, plugins=behavior_plugins(init.get("plugins")))
    expected = {
        "model": model,
        "permissionMode": "bypassPermissions",
        "apiKeySource": "none",
        "mcp_servers": [],
        "slash_commands": [],
        "skills": [],
        "plugins": behavior_plugins(claude["plugins"]),
        "tools": claude["tools"],
        "agents": claude["agents"],
        "claude_code_version": claude["version_output"].split(" ", 1)[0],
        "output_style": "default",
    }
    return sorted(key for key, value in expected.items() if observed.get(key) != value)


def external_failure(reason_code: str, detector: str, **detail: Any) -> dict[str, Any]:
    value = {
        "schema_version": "the-caption-prompt.run-status/v1",
        "status": "excluded",
        "category": "external_failure",
        "reason_code": reason_code,
        "detector": detector,
    }
    value.update(detail)
    return value


def terminal_failure(result: dict[str, Any]) -> dict[str, Any] | None:
    if result.get("is_error") is not True:
        return None
    status = result.get("api_error_status")
    reason = result.get("terminal_reason")
    if status is not None or reason == "api_error":
        return external_failure(
            "claude_api_error",
            "claude-terminal-result/v1",
            api_error_status=status,
            terminal_reason=reason,
        )
    return None


def write_private(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(value)


def instruction_loads(usage: dict[str, Any]) -> list[dict[str, Any]]:
    """Record instruction files the harness reports as loaded, without content."""
    loads: list[dict[str, Any]] = []
    for session in usage["sessions"]:
        with Path(session["transcript"]).open(encoding="utf-8") as handle:
            for line in handle:
                item = json.loads(line)
                attachment = item.get("attachment")
                if item.get("type") != "attachment" or not isinstance(attachment, dict):
                    continue
                kind = attachment.get("type")
                if kind == "instructions":
                    files = attachment.get("files")
                elif kind == "nested_memory":
                    files = [attachment.get("content")]
                else:
                    continue
                for entry in files if isinstance(files, list) else []:
                    if not isinstance(entry, dict):
                        continue
                    content = entry.get("content")
                    loads.append(
                        {
                            "actor": session["actor"],
                            "agent_id": session["agent_id"],
                            "attachment_type": kind,
                            "instruction_type": entry.get("type"),
                            "path": entry.get("path"),
                            "content_sha256": (
                                hashlib.sha256(content.encode("utf-8")).hexdigest()
                                if isinstance(content, str)
                                else None
                            ),
                        }
                    )
    return loads


def execute() -> int:
    workspace = Path.cwd().resolve()
    case = load_object(Path(require_string(os.environ.get("EVAL_CASE_FILE"), "EVAL_CASE_FILE")), "case capsule")
    capsule = load_object(
        Path(require_string(os.environ.get("EVAL_RUN_CAPSULE_FILE"), "EVAL_RUN_CAPSULE_FILE")), "run capsule"
    )
    usage_path = Path(require_string(os.environ.get("EVAL_USAGE_FILE"), "EVAL_USAGE_FILE"))
    status_path = Path(require_string(os.environ.get("EVAL_RUN_STATUS_FILE"), "EVAL_RUN_STATUS_FILE"))
    extension_root = Path(require_string(os.environ.get("EVAL_EXTENSION_DIR"), "EVAL_EXTENSION_DIR"))
    binding = require_object(capsule.get("binding"), "run.binding")
    parameters = require_object(capsule.get("parameters"), "run.parameters")
    conditions = require_object(capsule.get("comparison_conditions"), "run.comparison_conditions")
    executor_parameters = require_object(
        conditions.get("executor_parameters"), "comparison_conditions.executor_parameters"
    )
    if executor_parameters.get("token_accounting") != TOKEN_ACCOUNTING:
        raise AdapterError("Claude adapter requires Claude token accounting")
    if executor_parameters.get("command_protocol_text_revision") != CLAUDE_COMMAND_PROTOCOL_TEXT_REVISION:
        raise AdapterError("unsupported Claude command protocol text revision")
    claude = claude_environment_from_conditions(conditions)
    bundle = Path(require_string(parameters.get("prompt_bundle"), "parameters.prompt_bundle")).resolve()
    expected_hash = require_string(parameters.get("bundle_sha256"), "parameters.bundle_sha256")
    expected_dirty = set(require_string_array(parameters.get("expected_initial_dirty_paths"), "expected_initial_dirty_paths"))
    allowed_result_paths = set(require_string_array(parameters.get("allowed_result_paths"), "allowed_result_paths"))
    model = require_string(parameters.get("model"), "parameters.model")
    reasoning_effort = require_string(parameters.get("reasoning_effort"), "parameters.reasoning_effort")
    if model != conditions.get("model") or reasoning_effort != executor_parameters.get("reasoning_effort"):
        raise AdapterError("run parameters differ from the comparison conditions")
    manifest = verify_bundle(bundle)
    prompt_set_identity = prompt_set_identity_from_binding(binding, manifest, expected_hash)
    collisions = prompt_fixture_collisions(case, manifest)
    if collisions:
        raise AdapterError("prompt bundle targets collide with fixture condition paths: " + ", ".join(collisions))
    runtime = verify_executable(claude)
    isolation = config_isolation_receipt(claude)
    runtime_links = prepare_runtime_links(workspace, parameters.get("runtime_links"))
    if changed_paths(workspace) != expected_dirty:
        raise AdapterError("fixture dirty paths do not match the run capsule")
    targets = overlay_bundle(workspace, bundle, manifest)
    commit, tree = prompt_overlay_commit(workspace, targets)
    if changed_paths(workspace) != expected_dirty:
        raise AdapterError("prompt overlay commit did not preserve the seeded dirty state")

    case_id = require_string(binding.get("case_id"), "binding.case_id")
    declared_command_protocol, required_command_groups = command_protocol_for_case(
        executor_parameters.get("command_evidence_protocol"), case_id
    )
    adapter_teardown_paths = adapter_teardown_paths_from_protocol(binding, parameters, executor_parameters)
    task = render_task(case, declared_command_protocol)
    task_sha256 = hashlib.sha256(task.encode("utf-8")).hexdigest()
    adapter_extension = extension_root / "claude-adapter"
    adapter_extension.mkdir(parents=True, exist_ok=True)
    write_json(adapter_extension / "config-isolation.json", isolation)
    command = [
        runtime["executable"],
        "-p",
        "--output-format",
        "stream-json",
        "--verbose",
        "--model",
        model,
        "--effort",
        reasoning_effort,
        "--permission-mode",
        "bypassPermissions",
        "--setting-sources",
        claude["setting_sources"],
        "--strict-mcp-config",
        "--disable-slash-commands",
        "--tools",
        ",".join(claude["tools"]),
        "--settings",
        json.dumps(claude["flag_settings"], sort_keys=True, separators=(",", ":")),
    ]
    environment = minimal_environment(claude)
    cli_clock_started = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=workspace,
            input=task.encode("utf-8"),
            capture_output=True,
            check=False,
            env=environment,
        )
    finally:
        cli_clock_ended = time.perf_counter()
        timing_dir = extension_root / "execution-time"
        timing_dir.mkdir(parents=True, exist_ok=True)
        with (timing_dir / "adapter-clock.json").open("x") as timing_stream:
            json.dump(
                {
                    "schema_version": "the-caption-prompt.adapter-clock/v1",
                    "run_id": extension_root.name,
                    "clock": "adapter_process_perf_counter",
                    "cli_started": cli_clock_started,
                    "cli_returned": cli_clock_ended,
                    "cli_elapsed_seconds": cli_clock_ended - cli_clock_started,
                    "boundary_semantics": "subprocess invocation to return or exception; not model work time",
                },
                timing_stream,
            )
    sys.stdout.buffer.write(completed.stdout)
    sys.stderr.buffer.write(completed.stderr)
    write_private(adapter_extension / "claude-stream.jsonl", completed.stdout)
    write_private(adapter_extension / "claude-stderr.bin", completed.stderr)

    failure: dict[str, Any] | None = None
    stream: dict[str, Any] | None = None
    usage: dict[str, Any] | None = None
    command_evidence: dict[str, Any] | None = None
    command_protocol_audit: dict[str, Any] | None = None
    cleanup_attempts: list[dict[str, Any]] = []
    final_text = ""
    try:
        stream = parse_stream(completed.stdout)
    except ClaudeEvidenceError as exc:
        failure = external_failure("claude_stream_incomplete", "claude-stream-json/v1")
        write_json(adapter_extension / "stream-error.json", {"reason": str(exc)})
    if stream is not None:
        result = stream["result"]
        final_text = result.get("result") if isinstance(result.get("result"), str) else ""
        (adapter_extension / "final-response.txt").write_text(final_text, encoding="utf-8")
        mismatches = surface_mismatches(stream["init"], claude, model)
        write_json(
            adapter_extension / "runtime-surface.json",
            {
                "schema_version": "the-caption-prompt.claude-runtime-surface/v1",
                "observed": {
                    key: stream["init"].get(key)
                    for key in (
                        "model",
                        "permissionMode",
                        "apiKeySource",
                        "mcp_servers",
                        "slash_commands",
                        "skills",
                        "plugins",
                        "tools",
                        "agents",
                        "claude_code_version",
                        "output_style",
                        "memory_paths",
                    )
                },
                "mismatched_fields": mismatches,
            },
        )
        failure = terminal_failure(result)
        if failure is None and mismatches:
            failure = external_failure(
                "claude_runtime_surface_mismatch", "claude-init-surface/v1", fields=mismatches
            )
        if failure is None:
            try:
                usage = collect_usage(Path(claude["config_dir"]), stream)
            except ClaudeEvidenceError as exc:
                failure = external_failure("claude_all_agent_usage_incomplete", "claude-transcript-usage/v1")
                write_json(adapter_extension / "all-agent-usage-error.json", {"reason": str(exc)})
        if usage is not None:
            usage["run_id"] = extension_root.name
            usage["generated_at"] = datetime.now(timezone.utc).isoformat()
            write_json(extension_root / "all-agent-usage" / "usage.json", usage)
            write_json(
                adapter_extension / "instruction-loads.json",
                {
                    "schema_version": "the-caption-prompt.claude-instruction-loads/v1",
                    "run_id": extension_root.name,
                    "loads": instruction_loads(usage),
                },
            )
            command_evidence = collect_commands(usage, extension_root.name, stream["task_notifications"])
            write_json(extension_root / "all-agent-command-evidence" / "evidence.json", command_evidence)
            cleanup_attempts = adapter_owned_cleanup_attempts(command_evidence, adapter_teardown_paths)
            if declared_command_protocol is not None:
                requirement_statuses = command_requirement_statuses(command_evidence, required_command_groups)
                command_protocol_audit = {
                    "schema_version": "the-caption-prompt.command-protocol-audit/v1",
                    "run_id": extension_root.name,
                    "requirements": requirement_statuses,
                    "summary": {
                        status: sum(item["status"] == status for item in requirement_statuses)
                        for status in ("successful", "failed", "not_attempted", "evidence_incomplete")
                    },
                }
                write_json(extension_root / "command-protocol-audit" / "audit.json", command_protocol_audit)
                failure = command_evidence_external_failure(requirement_statuses)
            write_json(
                extension_root / "evaluation-diagnostics" / "diagnostics.json",
                {
                    "schema_version": "the-caption-prompt.evaluation-diagnostics/v1",
                    "run_id": extension_root.name,
                    "command_protocol_violation_count": command_evidence["protocol_violation_count"],
                    "command_protocol_violations": command_evidence["protocol_violations"],
                    "model_attempted_adapter_owned_cleanup_count": len(cleanup_attempts),
                    "model_attempted_adapter_owned_cleanup": cleanup_attempts,
                    "model_reported_adapter_owned_cleanup_attempt_count": None,
                    "model_reported_adapter_owned_cleanup_attempt": "unavailable_on_claude_surface",
                },
            )
            if failure is None:
                write_json(
                    usage_path,
                    {
                        "schema_version": "the-caption-prompt.token-usage/v2",
                        "token_accounting": TOKEN_ACCOUNTING,
                        "total_tokens": usage["all_agent_total_tokens"],
                    },
                )
    if failure is None and stream is None:
        failure = external_failure("claude_stream_incomplete", "claude-stream-json/v1")
    adapter_teardown_paths_removed: list[str] = []
    try:
        adapter_teardown_paths_removed = remove_adapter_owned_outputs(workspace, adapter_teardown_paths)
    except OSError as exc:
        if failure is None:
            failure = external_failure("adapter_owned_teardown_failed", "claude-adapter-teardown/v1")
        write_json(adapter_extension / "adapter-teardown-error.json", {"reason": str(exc)})
    if failure is not None:
        write_json(status_path, failure)
    final_paths = changed_paths(workspace)
    unexpected_paths = sorted(final_paths - allowed_result_paths)
    result = stream["result"] if stream is not None else {}
    write_json(
        adapter_extension / "execution.json",
        {
            "adapter_schema_version": ADAPTER_SCHEMA_VERSION,
            "bundle_sha256": expected_hash,
            "claude_exit_code": completed.returncode,
            "claude_runtime": runtime,
            "claude_session_id": None if stream is None else stream["session_id"],
            "claude_result_event_count": None if stream is None else stream["result_count"],
            "terminal": {
                key: result.get(key)
                for key in ("type", "subtype", "is_error", "terminal_reason", "api_error_status", "num_turns", "stop_reason")
            },
            "prompt_overlay_commit": commit,
            "prompt_overlay_tree": tree,
            "final_changed_paths": sorted(final_paths),
            "model": model,
            "resolved_models": None if usage is None else [item["model"] for item in usage["by_model"]],
            "prompt_set_identity": prompt_set_identity,
            "all_agent_total_tokens": None if usage is None else usage["all_agent_total_tokens"],
            "command_evidence_schema_version": None if command_evidence is None else COMMAND_EVIDENCE_SCHEMA_VERSION,
            "command_protocol_audit_schema_version": (
                None if command_protocol_audit is None else command_protocol_audit["schema_version"]
            ),
            "command_protocol_text_revision": CLAUDE_COMMAND_PROTOCOL_TEXT_REVISION,
            "token_accounting": TOKEN_ACCOUNTING,
            "reasoning_effort": reasoning_effort,
            "runtime_links": runtime_links,
            "adapter_teardown_paths_removed": adapter_teardown_paths_removed,
            "model_attempted_adapter_owned_cleanup_count": len(cleanup_attempts),
            "session_mode": "persisted",
            "task_sha256": task_sha256,
            "unexpected_changed_paths": unexpected_paths,
            "external_failure": failure,
        },
    )
    if failure is not None:
        return EXTERNAL_FAILURE_EXIT_CODE
    if completed.returncode != 0:
        return completed.returncode
    if unexpected_paths:
        print(f"unexpected changed paths: {unexpected_paths}", file=sys.stderr)
        return 3
    return 0


def main() -> int:
    try:
        return execute()
    except (AdapterError, BundleError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
