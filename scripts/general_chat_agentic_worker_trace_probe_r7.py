#!/usr/bin/env python3
"""Final worker-trace diagnostic using the dedicated sub_agent_activity event."""

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
    from scripts import general_chat_agentic_worker_trace_probe_r5 as base
except ModuleNotFoundError:
    import general_chat_agentic_worker_trace_probe_r5 as base


ROOT = Path(__file__).resolve().parents[1]
PROBE_ID = "general-chat-agentic-worker-activity-preflight-r7"
DEFAULT_AUTHORIZATION = ROOT / "docs/general-chat-agentic-worker-trace-probe-r7-authorization.json"
DEFAULT_SCHEMA = ROOT / "docs/general-chat-agentic-worker-trace-probe-r7-authorization.schema.json"
RECORD_NAMES = base.RECORD_NAMES
REQUIRED_PACKET_STRINGS = ("parking_fact_check", "parking-saturday-r1", "駐車場利用案内", "土曜日の駐車場利用時間は9時00分から18時30分までです。", "18時まで駐車できる", "18時30分まで")
FORBIDDEN_PACKET_STRINGS = ("branch-counter-hours-r1", "parking-weekday-r1")


def activity_bindings(events: list[dict[str, Any]]) -> list[dict[str, str]]:
    values = []
    for event in events:
        payload = event.get("payload")
        if event.get("type") != "event_msg" or not isinstance(payload, dict) or payload.get("type") != "sub_agent_activity":
            continue
        thread_id = payload.get("agent_thread_id")
        agent_path = payload.get("agent_path")
        if isinstance(thread_id, str) and isinstance(agent_path, str):
            values.append({"child_thread_id": thread_id, "agent_path": agent_path})
    unique = {(item["child_thread_id"], item["agent_path"]) for item in values}
    return values[:1] if len(unique) == 1 else []


def packet_material_state(message: Any) -> str:
    if not isinstance(message, str):
        return "unobserved"
    if any(value in message for value in FORBIDDEN_PACKET_STRINGS):
        return "unsatisfied"
    return "satisfied" if all(value in message for value in REQUIRED_PACKET_STRINGS) else "unsatisfied"


def validate_authorization(path: Path, schema_path: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    value = base.load_object(path); schema = base.load_object(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema); jsonschema.Draft202012Validator(schema).validate(value)
    paths = {name: base.verified_relative(identity) for name, identity in value["artifacts"].items()}
    runtime = Path(value["runtime"]["path"]); data = runtime.read_bytes()
    if len(data) != value["runtime"]["bytes"] or base.sha256(data) != value["runtime"]["sha256"]: raise base.ProbeError("runtime identity mismatch")
    paths["runtime"] = runtime; return value, paths


def record_root(value: dict[str, Any]) -> Path:
    path = (ROOT / value["issuance_records"]["root"] / PROBE_ID).resolve(); path.relative_to(ROOT); return path


def prepare() -> dict[str, Any]:
    value, _ = validate_authorization(DEFAULT_AUTHORIZATION, DEFAULT_SCHEMA); root = record_root(value)
    present = [name for name in RECORD_NAMES if (root / name).exists()]
    return {"schema_version": "general-chat-agentic-worker-activity-preparation/v1", "probe_id": PROBE_ID, "authorization_state": value["issuance_authority"], "identity_available": not present, "existing_records": present, "dispatch_state": "allowed" if not present else "denied", "model_invocations": 0, "probe_issues": 0}


def build_receipt(value: dict[str, Any], private: Path, started: int, ended: int, exit_code: int) -> dict[str, Any]:
    stdout, stderr, final_path = private / "stdout.jsonl", private / "stderr.txt", private / "final.txt"
    stdout_events = base.json_lines(stdout)
    root_ids = [event.get("thread_id") for event in stdout_events if event.get("type") == "thread.started" and isinstance(event.get("thread_id"), str)]
    root_id = root_ids[0] if len(root_ids) == 1 else None
    records = []
    session_root = private / "codex-home" / "sessions"
    for path in session_root.rglob("*.jsonl") if session_root.is_dir() else []:
        projected = base.session(path)
        if projected is not None: records.append((projected, base.json_lines(path)))
    roots = [item for item in records if item[0]["thread_id"] == root_id and item[0]["parent_thread_id"] is None]
    root, root_events = roots[0] if len(roots) == 1 else (None, [])
    calls, _ = base.find_spawn(root) if root else ([], [])
    call = calls[0] if len(calls) == 1 else None; args = call.get("arguments") if call else None
    activities = activity_bindings(root_events)
    activity = activities[0] if len(activities) == 1 else None
    child_id = activity.get("child_thread_id") if activity else None
    children = [item for item in records if item[0]["thread_id"] == child_id and item[0]["parent_thread_id"] == root_id]
    child = children[0][0] if len(children) == 1 else None
    terminal = child.get("terminal") if child else None
    final = final_path.read_text(encoding="utf-8").strip() if final_path.is_file() else None
    usages = [item[0]["usage"] for item in records]
    activity_path = activity.get("agent_path") if activity else None
    criteria = {
        "root_thread_identity": "satisfied" if root else "unobserved",
        "spawn_request": "satisfied" if isinstance(args, dict) and args.get("task_name") == base.TASK_NAME and args.get("fork_turns") == "none" else ("unobserved" if args is None else "unsatisfied"),
        "worker_packet_material": packet_material_state(args.get("message") if isinstance(args, dict) else None),
        "sub_agent_activity_binding": "satisfied" if activity and activity_path == f"/root/{base.TASK_NAME}" else ("unobserved" if activity is None else "unsatisfied"),
        "child_session_binding": "satisfied" if child and child.get("agent_path") == activity_path == f"/root/{base.TASK_NAME}" else ("unobserved" if child is None or child.get("agent_path") is None else "unsatisfied"),
        "child_terminal_result": "satisfied" if isinstance(terminal, str) and all(text in terminal for text in ("18時まで駐車できる", "18時30分まで")) else ("unobserved" if terminal is None else "unsatisfied"),
        "root_final_response": "satisfied" if final == base.EXPECTED_FINAL else ("unobserved" if final is None else "unsatisfied"),
        "all_agent_final_usage": "satisfied" if len(usages) == 2 and all(isinstance(usage, dict) and all(isinstance(usage.get(field), int) for field in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")) for usage in usages) else "unobserved",
        "monotonic_elapsed": "satisfied" if ended >= started else "unsatisfied", "safe_projection": "satisfied",
    }
    available = exit_code == 0 and all(state == "satisfied" for state in criteria.values())
    return {"schema_version": "general-chat-agentic-worker-activity-receipt/v1", "probe_id": PROBE_ID, "authorization_id": value["authorization_id"], "terminal_state": "worker_trace_available" if available else "worker_trace_unavailable", "process": {"exit_code": exit_code, "started_monotonic_ms": started, "ended_monotonic_ms": ended, "elapsed_ms": ended - started}, "criteria": criteria, "bindings": {"root_thread_id": root_id, "spawn_call_count": len(calls), "activity_binding_count": len(activities), "child_thread_id": child_id, "packet_message_sha256": base.sha256(args["message"].encode("utf-8")) if isinstance(args, dict) and isinstance(args.get("message"), str) else None, "child_terminal_sha256": base.sha256(terminal.encode("utf-8")) if isinstance(terminal, str) else None, "final_response_sha256": base.sha256(final.encode("utf-8")) if isinstance(final, str) else None}, "usage": {"sessions": [{"thread_id": item[0]["thread_id"], "parent_thread_id": item[0]["parent_thread_id"], **(item[0]["usage"] or {})} for item in records], "complete": criteria["all_agent_final_usage"] == "satisfied"}, "artifact_hashes": {"stdout_jsonl": base.sha256(stdout.read_bytes()) if stdout.is_file() else None, "stderr": base.sha256(stderr.read_bytes()) if stderr.is_file() else None, "final_message": base.sha256(final_path.read_bytes()) if final_path.is_file() else None}, "model_invocations": 1, "probe_issues": 1, "retry_performed": False, "raw_transcript_saved": False, "sensitive_material_saved": False}


def issue() -> dict[str, Any]:
    value, paths = validate_authorization(DEFAULT_AUTHORIZATION, DEFAULT_SCHEMA); target = record_root(value); target.mkdir(parents=True, exist_ok=True, mode=0o700)
    if any((target / name).exists() for name in RECORD_NAMES): raise base.ProbeError("probe identity already used")
    auth_hash = base.sha256(DEFAULT_AUTHORIZATION.read_bytes()); base.write_once(target / "reservation.json", {"schema_version": "general-chat-agentic-worker-activity-reservation/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "reserved_at_unix_ms": int(time.time() * 1000)})
    private = Path(tempfile.mkdtemp(prefix="general-chat-worker-r7.", dir="/Users/kenn/repos/_verification")); private.chmod(0o700)
    home, workspace = private / "codex-home", private / "workspace"; home.mkdir(mode=0o700); workspace.mkdir(mode=0o700)
    stdout, stderr, final = private / "stdout.jsonl", private / "stderr.txt", private / "final.txt"; started = time.monotonic_ns() // 1_000_000; exit_code = 125
    try:
        base.copy_auth(home)
        command = [str(paths["runtime"]), "exec", "--ignore-user-config", "--ignore-rules", "--strict-config", "--enable", "multi_agent", "--disable", "memories", "-c", "agents.max_threads=2", "-c", 'approval_policy="never"', "-m", "gpt-5.6-sol", "-c", 'model_reasoning_effort="medium"', "-s", "workspace-write", "--skip-git-repo-check", "--json", "--output-last-message", str(final), "-C", str(workspace), "-"]
        base.write_once(target / "issued.json", {"schema_version": "general-chat-agentic-worker-activity-issued/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "command_sha256": base.sha256(base.canonical_bytes(command)), "started_monotonic_ms": started})
        environment = os.environ.copy(); environment["CODEX_HOME"] = str(home)
        with paths["model_input"].open("rb") as stdin_file, stdout.open("wb") as stdout_file, stderr.open("wb") as stderr_file: exit_code = subprocess.run(command, stdin=stdin_file, stdout=stdout_file, stderr=stderr_file, env=environment, timeout=900, check=False).returncode
    except subprocess.TimeoutExpired: exit_code = 124
    ended = time.monotonic_ns() // 1_000_000
    try:
        receipt = build_receipt(value, private, started, ended, exit_code); jsonschema.Draft202012Validator(base.load_object(paths["receipt_schema"])).validate(receipt); base.write_once(target / "receipt.json", receipt); return receipt
    finally: shutil.rmtree(private, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("action", choices=("prepare", "issue")); args = parser.parse_args()
    try: result = prepare() if args.action == "prepare" else issue()
    except Exception as error: print(json.dumps({"schema_version": "general-chat-agentic-worker-activity-error/v1", "status": "error", "reason": str(error)}, ensure_ascii=False, sort_keys=True)); return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__": raise SystemExit(main())
