#!/usr/bin/env python3
"""Prepare or issue the r8 combined agentic capability probe."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

import jsonschema

try:
    from scripts import general_chat_agentic_worker_trace_probe_r5 as worker_base
    from scripts import general_chat_agentic_worker_trace_probe_r7 as worker_activity
    from scripts import general_chat_agentic_tool_transport_probe_r4 as tool_base
except ModuleNotFoundError:
    import general_chat_agentic_worker_trace_probe_r5 as worker_base
    import general_chat_agentic_worker_trace_probe_r7 as worker_activity
    import general_chat_agentic_tool_transport_probe_r4 as tool_base


ROOT = Path(__file__).resolve().parents[1]
PROBE_ID = "general-chat-agentic-capability-preflight-r8"
DEFAULT_AUTHORIZATION = ROOT / "docs/general-chat-agentic-capability-probe-r8-authorization.json"
DEFAULT_SCHEMA = ROOT / "docs/general-chat-agentic-capability-probe-r8-authorization.schema.json"
RECORD_NAMES = worker_base.RECORD_NAMES
FIXTURE_RELATIVE = "worker-material/parking-saturday-r8.txt"
EXPECTED_FINAL = "土曜日は18時まで駐車でき、利用時間は18時30分までです。支店窓口は土曜日17時に終了します。"
FULL_TOOL_ID = "mcp__branch_hours__fetch_branch_counter_hours"


def validate_authorization(path: Path, schema_path: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    value = worker_base.load_object(path); schema = worker_base.load_object(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema); jsonschema.Draft202012Validator(schema).validate(value)
    paths = {name: worker_base.verified_relative(identity) for name, identity in value["artifacts"].items()}
    runtime = Path(value["runtime"]["path"]); data = runtime.read_bytes()
    if len(data) != value["runtime"]["bytes"] or worker_base.sha256(data) != value["runtime"]["sha256"]: raise worker_base.ProbeError("runtime identity mismatch")
    paths["runtime"] = runtime; return value, paths


def record_root(value: dict[str, Any]) -> Path:
    path = (ROOT / value["issuance_records"]["root"] / PROBE_ID).resolve(); path.relative_to(ROOT); return path


def prepare() -> dict[str, Any]:
    value, _ = validate_authorization(DEFAULT_AUTHORIZATION, DEFAULT_SCHEMA); root = record_root(value)
    present = [name for name in RECORD_NAMES if (root / name).exists()]
    return {"schema_version": "general-chat-agentic-capability-r8-preparation/v1", "probe_id": PROBE_ID, "authorization_state": value["issuance_authority"], "identity_available": not present, "existing_records": present, "dispatch_state": "allowed" if not present else "denied", "model_invocations": 0, "probe_issues": 0}


def command_uses_path(session: dict[str, Any], path: str) -> int:
    count = 0
    for item in session["items"]:
        if item.get("type") not in {"custom_tool_call", "function_call"}: continue
        name = item.get("name") or item.get("tool_name")
        if name not in {"exec", "exec_command"}: continue
        rendered = json.dumps(item.get("input") if "input" in item else item.get("arguments"), ensure_ascii=False, sort_keys=True)
        if path in rendered: count += 1
    return count


def packet_state(message: Any) -> str:
    if not isinstance(message, str): return "unobserved"
    required = (FIXTURE_RELATIVE, "18時まで駐車できる", "終了時刻", "一文")
    forbidden = ("18時30分", "branch-counter-hours-r1", "17時", "parking-weekday")
    if any(value in message for value in forbidden): return "unsatisfied"
    return "satisfied" if all(value in message for value in required) else "unsatisfied"


def tool_call_count(session: dict[str, Any]) -> int:
    count = 0
    for item in session["items"]:
        name = item.get("name") or item.get("tool_name")
        if item.get("type") in {"function_call", "custom_tool_call", "mcp_tool_call"} and name in {FULL_TOOL_ID, "fetch_branch_counter_hours"}: count += 1
    return count


def build_receipt(value: dict[str, Any], private: Path, started: int, ended: int, exit_code: int) -> dict[str, Any]:
    stdout, stderr, final_path, audit_path = private / "stdout.jsonl", private / "stderr.txt", private / "final.txt", private / "tool-audit.jsonl"
    root_ids = [event.get("thread_id") for event in worker_base.json_lines(stdout) if event.get("type") == "thread.started" and isinstance(event.get("thread_id"), str)]
    root_id = root_ids[0] if len(root_ids) == 1 else None
    records = []
    session_root = private / "codex-home" / "sessions"
    for path in session_root.rglob("*.jsonl") if session_root.is_dir() else []:
        projected = worker_base.session(path)
        if projected is not None: records.append((projected, worker_base.json_lines(path)))
    roots = [item for item in records if item[0]["thread_id"] == root_id and item[0]["parent_thread_id"] is None]
    root, root_events = roots[0] if len(roots) == 1 else (None, [])
    calls, _ = worker_base.find_spawn(root) if root else ([], [])
    call = calls[0] if len(calls) == 1 else None; args = call.get("arguments") if call else None
    activities = worker_activity.activity_bindings(root_events); activity = activities[0] if len(activities) == 1 else None
    child_id = activity.get("child_thread_id") if activity else None
    children = [item for item in records if item[0]["thread_id"] == child_id and item[0]["parent_thread_id"] == root_id]
    child = children[0][0] if len(children) == 1 else None
    terminal = child.get("terminal") if child else None
    audits = tool_base.json_lines(audit_path); audit_names = [event.get("event") for event in audits]
    tool_events = [event for event in audits if event.get("event") == "tools_call"]
    final = final_path.read_text(encoding="utf-8").strip() if final_path.is_file() else None
    usages = [item[0]["usage"] for item in records]
    root_reads = command_uses_path(root, FIXTURE_RELATIVE) if root else 0
    child_reads = command_uses_path(child, FIXTURE_RELATIVE) if child else 0
    criteria = {
        "root_thread_identity": "satisfied" if root else "unobserved",
        "spawn_request": "satisfied" if isinstance(args, dict) and args.get("task_name") == worker_base.TASK_NAME and args.get("fork_turns") == "none" else ("unobserved" if args is None else "unsatisfied"),
        "worker_packet_carrier": packet_state(args.get("message") if isinstance(args, dict) else None),
        "root_fixture_read_closed": "satisfied" if root and root_reads == 0 else ("unobserved" if root is None else "unsatisfied"),
        "worker_fixture_read": "satisfied" if child and child_reads >= 1 else ("unobserved" if child is None else "unsatisfied"),
        "worker_identity_binding": "satisfied" if activity and child and activity.get("agent_path") == child.get("agent_path") == f"/root/{worker_base.TASK_NAME}" else ("unobserved" if activity is None or child is None else "unsatisfied"),
        "worker_terminal_result": "satisfied" if isinstance(terminal, str) and all(text in terminal for text in ("18時まで駐車できる", "18時30分まで")) else ("unobserved" if terminal is None else "unsatisfied"),
        "mcp_initialize_and_list": "satisfied" if all(name in audit_names for name in ("initialize", "initialized", "tools_list")) else "unobserved",
        "fixed_tool_call_and_result": "satisfied" if root and tool_call_count(root) == 1 and len(tool_events) == 1 and tool_events[0].get("input") == {"record_id": "branch-counter-hours-r1"} and tool_events[0].get("result", {}).get("closes_at") == "17:00" else ("unobserved" if not tool_events else "unsatisfied"),
        "root_final_response": "satisfied" if final == EXPECTED_FINAL else ("unobserved" if final is None else "unsatisfied"),
        "all_agent_final_usage": "satisfied" if len(usages) == 2 and all(isinstance(usage, dict) and all(isinstance(usage.get(field), int) for field in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")) for usage in usages) else "unobserved",
        "monotonic_elapsed": "satisfied" if ended >= started else "unsatisfied", "safe_projection": "satisfied",
    }
    available = exit_code == 0 and all(state == "satisfied" for state in criteria.values())
    return {"schema_version": "general-chat-agentic-capability-r8-receipt/v1", "probe_id": PROBE_ID, "authorization_id": value["authorization_id"], "terminal_state": "agentic_runtime_capability_available" if available else "agentic_runtime_capability_unavailable", "process": {"exit_code": exit_code, "started_monotonic_ms": started, "ended_monotonic_ms": ended, "elapsed_ms": ended - started}, "criteria": criteria, "bindings": {"root_thread_id": root_id, "child_thread_id": child_id, "root_fixture_read_count": root_reads, "worker_fixture_read_count": child_reads, "tool_call_count": tool_call_count(root) if root else 0, "tool_audit_call_count": len(tool_events), "worker_terminal_sha256": worker_base.sha256(terminal.encode("utf-8")) if isinstance(terminal, str) else None, "final_response_sha256": worker_base.sha256(final.encode("utf-8")) if isinstance(final, str) else None}, "usage": {"sessions": [{"thread_id": item[0]["thread_id"], "parent_thread_id": item[0]["parent_thread_id"], **(item[0]["usage"] or {})} for item in records], "complete": criteria["all_agent_final_usage"] == "satisfied"}, "artifact_hashes": {"stdout_jsonl": worker_base.sha256(stdout.read_bytes()) if stdout.is_file() else None, "stderr": worker_base.sha256(stderr.read_bytes()) if stderr.is_file() else None, "final_message": worker_base.sha256(final_path.read_bytes()) if final_path.is_file() else None, "tool_audit": worker_base.sha256(audit_path.read_bytes()) if audit_path.is_file() else None}, "model_invocations": 1, "probe_issues": 1, "retry_performed": False, "raw_transcript_saved": False, "sensitive_material_saved": False}


def issue() -> dict[str, Any]:
    value, paths = validate_authorization(DEFAULT_AUTHORIZATION, DEFAULT_SCHEMA); target = record_root(value); target.mkdir(parents=True, exist_ok=True, mode=0o700)
    if any((target / name).exists() for name in RECORD_NAMES): raise worker_base.ProbeError("probe identity already used")
    auth_hash = worker_base.sha256(DEFAULT_AUTHORIZATION.read_bytes()); worker_base.write_once(target / "reservation.json", {"schema_version": "general-chat-agentic-capability-r8-reservation/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "reserved_at_unix_ms": int(time.time() * 1000)})
    private = Path(tempfile.mkdtemp(prefix="general-chat-agentic-r8.", dir="/Users/kenn/repos/_verification")); private.chmod(0o700)
    home, workspace = private / "codex-home", private / "workspace"; home.mkdir(mode=0o700); (workspace / "worker-material").mkdir(parents=True, mode=0o700)
    shutil.copyfile(paths["worker_material"], workspace / FIXTURE_RELATIVE)
    stdout, stderr, final, audit = private / "stdout.jsonl", private / "stderr.txt", private / "final.txt", private / "tool-audit.jsonl"
    started = time.monotonic_ns() // 1_000_000; exit_code = 125
    try:
        worker_base.copy_auth(home)
        command = [str(paths["runtime"]), "exec", "--ignore-user-config", "--ignore-rules", "--strict-config", "--enable", "multi_agent", "--disable", "memories", "-c", "agents.max_threads=2", "-c", 'approval_policy="never"', "-m", "gpt-5.6-sol", "-c", 'model_reasoning_effort="medium"', "-s", "workspace-write", "--skip-git-repo-check", "--json", "--output-last-message", str(final), "-c", 'mcp_servers.branch_hours.command="/usr/bin/python3"', "-c", 'mcp_servers.branch_hours.args=["' + str(paths["tool_server"]) + '"]', "-c", 'mcp_servers.branch_hours.env.GENERAL_CHAT_BRANCH_TOOL_AUDIT="' + str(audit) + '"', "-C", str(workspace), "-"]
        worker_base.write_once(target / "issued.json", {"schema_version": "general-chat-agentic-capability-r8-issued/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "command_sha256": worker_base.sha256(worker_base.canonical_bytes(command)), "started_monotonic_ms": started})
        environment = os.environ.copy(); environment["CODEX_HOME"] = str(home)
        with paths["model_input"].open("rb") as stdin_file, stdout.open("wb") as stdout_file, stderr.open("wb") as stderr_file: exit_code = subprocess.run(command, stdin=stdin_file, stdout=stdout_file, stderr=stderr_file, env=environment, timeout=900, check=False).returncode
    except subprocess.TimeoutExpired: exit_code = 124
    ended = time.monotonic_ns() // 1_000_000
    try:
        receipt = build_receipt(value, private, started, ended, exit_code); jsonschema.Draft202012Validator(worker_base.load_object(paths["receipt_schema"])).validate(receipt); worker_base.write_once(target / "receipt.json", receipt); return receipt
    finally: shutil.rmtree(private, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("action", choices=("prepare", "issue")); args = parser.parse_args()
    try: result = prepare() if args.action == "prepare" else issue()
    except Exception as error: print(json.dumps({"schema_version": "general-chat-agentic-capability-r8-error/v1", "status": "error", "reason": str(error)}, ensure_ascii=False, sort_keys=True)); return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
