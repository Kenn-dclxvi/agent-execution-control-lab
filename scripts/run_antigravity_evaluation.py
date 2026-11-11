#!/usr/bin/env python3
"""固定したプロンプトをAntigravity CLIへ渡し、一次証拠だけを収集する。"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import agent_shell_environment
from scripts.antigravity_evidence import AntigravityEvidenceError, TOKEN_ACCOUNTING, collect_all, parse_stream
from scripts.antigravity_runtime import AntigravityRuntimeError, verify_from_conditions
from scripts.all_agent_command_evidence import adapter_owned_cleanup_attempts, command_requirement_statuses
from scripts.export_prompt_bundle import BundleError, verify_bundle
from scripts.run_claude_evaluation import external_failure, render_task as claude_render_task, write_private
from scripts.run_codex_evaluation import (
    AdapterError, adapter_teardown_paths_from_protocol, changed_paths, command_evidence_external_failure,
    command_protocol_for_case, load_object, overlay_bundle, prepare_runtime_links,
    prompt_fixture_collisions, prompt_overlay_commit, prompt_set_identity_from_binding,
    remove_adapter_owned_outputs, write_json,
)

COMMAND_PROTOCOL_REVISION = "antigravity-run-command-separate-r1"


def render_task(case, protocol):
    return claude_render_task(case, protocol).replace("Bash tool", "run_command tool")


def preserve_sessions(usage, destination):
    for session in usage["sessions"]:
        target = destination / "sessions" / session["session_id"]
        target.mkdir(parents=True)
        source = Path(session["database"])
        with sqlite3.connect(source.as_uri() + "?mode=ro", uri=True) as db:
            with sqlite3.connect(target / "conversation.db") as backup:
                db.backup(backup)
        shutil.copyfile(session["transcript"], target / "transcript.jsonl")
        for path in target.iterdir():
            path.chmod(0o600)


def execute():
    workspace = Path.cwd().resolve()
    case = load_object(Path(os.environ["EVAL_CASE_FILE"]), "case")
    capsule = load_object(Path(os.environ["EVAL_RUN_CAPSULE_FILE"]), "capsule")
    extension = Path(os.environ["EVAL_EXTENSION_DIR"])
    binding, parameters, conditions = (capsule[k] for k in ("binding", "parameters", "comparison_conditions"))
    executor = conditions["executor_parameters"]
    if executor["token_accounting"] != TOKEN_ACCOUNTING or executor["command_protocol_text_revision"] != COMMAND_PROTOCOL_REVISION:
        raise AdapterError("計数方法またはコマンド証跡の版が一致しません")
    runtime = verify_from_conditions(conditions)
    if runtime is None:
        raise AdapterError("固定したAntigravity CLIがありません")
    if parameters["model"] != conditions["model"] or parameters["reasoning_effort"] != executor["reasoning_effort"]:
        raise AdapterError("モデル・推論設定が一致しません")
    model = parameters["model"]
    if model != "gemini-4-argon-low" or parameters["reasoning_effort"] != "low":
        raise AdapterError("この収集器はArgon Lowだけを検証済みです")
    bundle = Path(parameters["prompt_bundle"])
    manifest = verify_bundle(bundle)
    identity = prompt_set_identity_from_binding(binding, manifest, parameters["bundle_sha256"])
    if prompt_fixture_collisions(case, manifest):
        raise AdapterError("プロンプトと固定fixtureが衝突しています")
    runtime_links = prepare_runtime_links(workspace, parameters.get("runtime_links"))
    expected = set(parameters["expected_initial_dirty_paths"])
    if changed_paths(workspace) != expected:
        raise AdapterError("初期変更状態が一致しません")
    targets = overlay_bundle(workspace, bundle, manifest)
    commit, tree = prompt_overlay_commit(workspace, targets)
    if changed_paths(workspace) != expected:
        raise AdapterError("プロンプト配置後に初期変更状態が変わりました")
    protocol, groups = command_protocol_for_case(executor.get("command_evidence_protocol"), binding["case_id"])
    teardown = adapter_teardown_paths_from_protocol(binding, parameters, executor)
    task = render_task(case, protocol)
    adapter = extension / "antigravity-adapter"
    adapter.mkdir(parents=True)
    shell = agent_shell_environment.shell_environment_from_conditions(conditions)
    if shell is None:
        raise AdapterError("固定シェル環境がありません")
    with agent_shell_environment.empty_zdotdir() as zdotdir:
        environment = agent_shell_environment.agent_environment(
            shell, workspace, Path(zdotdir), shell="/bin/zsh",
            passthrough={"AGY_CLI_DISABLE_AUTO_UPDATE": "1"},
        )
        receipt = agent_shell_environment.probe_receipt(environment, workspace, agent="antigravity",
                                                       shell="/bin/zsh", agent_shell_arguments=["-c"])
        agent_shell_environment.write_receipt(extension / "shell-environment/receipt.json", receipt)
        if not receipt["ok"]:
            raise AdapterError("シェル環境が固定条件と一致しません")
        command = [runtime["executable"], "-p", task, "--output-format", "stream-json", "--model", model,
                   "--effort", "low", "--dangerously-skip-permissions", "--disable-slash-commands",
                   "--settings", json.dumps(runtime["flag_settings"], sort_keys=True)]
        started = time.perf_counter()
        completed = subprocess.run(command, cwd=workspace, capture_output=True, env=environment)
        returned = time.perf_counter()
    write_json(extension / "execution-time/adapter-clock.json", {
        "schema_version": "the-caption-prompt.adapter-clock/v1", "run_id": extension.name,
        "clock": "adapter_process_perf_counter", "cli_started": started, "cli_returned": returned,
        "cli_elapsed_seconds": returned - started,
        "boundary_semantics": "subprocess invocation to return; not model work time",
    })
    write_private(adapter / "stream.jsonl", completed.stdout)
    write_private(adapter / "stderr.bin", completed.stderr)
    failure, usage, commands, parsed = None, None, None, None
    final = ""
    try:
        parsed = parse_stream(completed.stdout)
        if parsed["init"].get("permission_mode") != "always-proceed" or parsed["init"].get("tools") != runtime["tools"]:
            raise AntigravityEvidenceError("実行時のツール・権限が固定条件と一致しません")
        if completed.returncode or parsed["result"].get("status") != "SUCCESS":
            raise AntigravityEvidenceError("CLIが正常終了していません")
        final = parsed["result"].get("response", "")
        usage, commands = collect_all(parsed, Path(runtime["config_dir"]), model, extension.name)
        preserve_sessions(usage, adapter)
        write_json(extension / "all-agent-usage/usage.json", {**usage, "run_id": extension.name})
        write_json(extension / "all-agent-command-evidence/evidence.json", commands)
        if protocol is not None:
            requirements = command_requirement_statuses(commands, groups)
            write_json(extension / "command-protocol-audit/audit.json", {
                "schema_version": "the-caption-prompt.command-protocol-audit/v1", "run_id": extension.name,
                "requirements": requirements,
            })
            failure = command_evidence_external_failure(requirements)
        if failure is None:
            write_json(Path(os.environ["EVAL_USAGE_FILE"]), {
                "schema_version": "the-caption-prompt.token-usage/v3", "token_accounting": TOKEN_ACCOUNTING,
                "total_tokens": usage["all_agent_total_tokens"], "usage_components": usage["usage_components"],
            })
    except (AntigravityEvidenceError, OSError, ValueError, sqlite3.Error) as exc:
        failure = external_failure("antigravity_measurement_incomplete", "antigravity-155-collector/v1")
        write_json(adapter / "measurement-error.json", {"reason": str(exc)})
    (adapter / "final-response.txt").write_text(final, encoding="utf-8")
    cleanup = [] if commands is None else adapter_owned_cleanup_attempts(commands, teardown)
    removed = remove_adapter_owned_outputs(workspace, teardown)
    paths = changed_paths(workspace)
    unexpected = sorted(paths - set(parameters["allowed_result_paths"]))
    if failure:
        write_json(Path(os.environ["EVAL_RUN_STATUS_FILE"]), failure)
    write_json(adapter / "execution.json", {
        "adapter_schema_version": "the-caption-prompt.antigravity-adapter/v1", "antigravity_exit_code": completed.returncode,
        "terminal": None if parsed is None else parsed["result"]["status"],
        "model": model, "reasoning_effort": "low", "prompt_set_identity": identity,
        "bundle_sha256": parameters["bundle_sha256"], "prompt_overlay_commit": commit, "prompt_overlay_tree": tree,
        "runtime_links": runtime_links, "final_changed_paths": sorted(paths), "unexpected_changed_paths": unexpected,
        "task_sha256": hashlib.sha256(task.encode()).hexdigest(), "token_accounting": TOKEN_ACCOUNTING,
        "external_failure": failure, "adapter_teardown_paths_removed": removed,
        "model_attempted_adapter_owned_cleanup_count": len(cleanup),
    })
    return 75 if failure else (3 if unexpected else 0)


if __name__ == "__main__":
    try:
        raise SystemExit(execute())
    except (AdapterError, BundleError, AntigravityRuntimeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
