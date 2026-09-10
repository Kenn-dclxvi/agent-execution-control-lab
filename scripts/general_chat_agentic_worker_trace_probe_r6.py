#!/usr/bin/env python3
"""Issue r6 with recursive runtime-output and bounded packet projection selectors."""

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
PROBE_ID = "general-chat-agentic-worker-trace-selector-preflight-r6"
DEFAULT_AUTHORIZATION = ROOT / "docs/general-chat-agentic-worker-trace-probe-r6-authorization.json"
DEFAULT_SCHEMA = ROOT / "docs/general-chat-agentic-worker-trace-probe-r6-authorization.schema.json"
RECORD_NAMES = base.RECORD_NAMES


def nested_objects(value: Any) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(value, dict):
        found.append(value)
        for item in value.values():
            found.extend(nested_objects(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(nested_objects(item))
    elif isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return found
        found.extend(nested_objects(parsed))
    return found


def exact_packet_from_message(message: Any) -> dict[str, Any] | None:
    if not isinstance(message, str):
        return None
    if any(forbidden in message for forbidden in ("branch-counter-hours-r1", "parking-weekday-r1")):
        return None
    decoder = json.JSONDecoder()
    matches = []
    for index, character in enumerate(message):
        if character != "{":
            continue
        try:
            value, _ = decoder.raw_decode(message[index:])
        except json.JSONDecodeError:
            continue
        if value == base.EXPECTED_PACKET:
            matches.append(value)
    return matches[0] if len(matches) == 1 else None


def spawn_result(call_id: str | None, outputs: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates = []
    for output in outputs:
        if output.get("call_id") != call_id:
            continue
        for value in nested_objects(output.get("raw")):
            child = value.get("child_thread_id") or value.get("new_thread_id") or value.get("agent_id") or value.get("agent_thread_id")
            task = value.get("task_name") or value.get("agent_path") or value.get("child_agent_path")
            if isinstance(child, str):
                candidates.append({"child_thread_id": child, "task_name": task})
    unique = {(item["child_thread_id"], item.get("task_name")) for item in candidates}
    return candidates[0] if len(unique) == 1 else None


def root_calls(root: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    calls, outputs = [], []
    for item in root["items"]:
        if item.get("type") in {"function_call", "custom_tool_call"} and item.get("name") == "spawn_agent":
            calls.append({"call_id": item.get("call_id"), "arguments": base.decode_object(item.get("arguments") or item.get("input"))})
        if item.get("type") in {"function_call_output", "custom_tool_call_output"}:
            outputs.append({"call_id": item.get("call_id"), "raw": item.get("output") if "output" in item else item.get("content")})
    return calls, outputs


def build_receipt(value: dict[str, Any], private: Path, started: int, ended: int, exit_code: int) -> dict[str, Any]:
    stdout, stderr, final_path = private / "stdout.jsonl", private / "stderr.txt", private / "final.txt"
    stdout_events = base.json_lines(stdout)
    root_ids = [event.get("thread_id") for event in stdout_events if event.get("type") == "thread.started" and isinstance(event.get("thread_id"), str)]
    root_id = root_ids[0] if len(root_ids) == 1 else None
    session_root = private / "codex-home" / "sessions"
    sessions = [candidate for path in session_root.rglob("*.jsonl") if (candidate := base.session(path)) is not None] if session_root.is_dir() else []
    roots = [candidate for candidate in sessions if candidate["thread_id"] == root_id and candidate["parent_thread_id"] is None]
    root = roots[0] if len(roots) == 1 else None
    calls, outputs = root_calls(root) if root else ([], [])
    call = calls[0] if len(calls) == 1 else None
    args = call.get("arguments") if call else None
    packet = exact_packet_from_message(args.get("message")) if isinstance(args, dict) else None
    result = spawn_result(call.get("call_id"), outputs) if call else None
    child_id = result.get("child_thread_id") if result else None
    children = [candidate for candidate in sessions if candidate["thread_id"] == child_id and candidate["parent_thread_id"] == root_id]
    child = children[0] if len(children) == 1 else None
    terminal = child.get("terminal") if child else None
    final = final_path.read_text(encoding="utf-8").strip() if final_path.is_file() else None
    usages = [candidate["usage"] for candidate in sessions]
    task_value = result.get("task_name") if result else None
    criteria = {
        "root_thread_identity": "satisfied" if root else "unobserved",
        "spawn_request": "satisfied" if isinstance(args, dict) and args.get("task_name") == base.TASK_NAME and args.get("fork_turns") == "none" else ("unobserved" if args is None else "unsatisfied"),
        "worker_packet_projection": "satisfied" if packet == base.EXPECTED_PACKET else "unobserved",
        "runtime_spawn_result": "satisfied" if result and task_value in {base.TASK_NAME, f"/root/{base.TASK_NAME}"} else ("unobserved" if result is None or task_value is None else "unsatisfied"),
        "child_session_binding": "satisfied" if child and child.get("agent_path") == f"/root/{base.TASK_NAME}" else ("unobserved" if child is None or child.get("agent_path") is None else "unsatisfied"),
        "child_terminal_result": "satisfied" if isinstance(terminal, str) and all(text in terminal for text in ("18時まで駐車できる", "18時30分まで")) else ("unobserved" if terminal is None else "unsatisfied"),
        "root_final_response": "satisfied" if final == base.EXPECTED_FINAL else ("unobserved" if final is None else "unsatisfied"),
        "all_agent_final_usage": "satisfied" if len(usages) == 2 and all(isinstance(usage, dict) and all(isinstance(usage.get(field), int) for field in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")) for usage in usages) else "unobserved",
        "monotonic_elapsed": "satisfied" if ended >= started else "unsatisfied", "safe_projection": "satisfied",
    }
    available = exit_code == 0 and all(state == "satisfied" for state in criteria.values())
    return {
        "schema_version": "general-chat-agentic-worker-trace-selector-receipt/v1", "probe_id": PROBE_ID, "authorization_id": value["authorization_id"], "terminal_state": "worker_trace_available" if available else "worker_trace_unavailable",
        "process": {"exit_code": exit_code, "started_monotonic_ms": started, "ended_monotonic_ms": ended, "elapsed_ms": ended - started}, "criteria": criteria,
        "bindings": {"root_thread_id": root_id, "spawn_call_count": len(calls), "matched_spawn_output_count": 1 if result else 0, "worker_packet_sha256": base.sha256(base.canonical_bytes(packet)) if isinstance(packet, dict) else None, "child_thread_id": child_id, "child_terminal_sha256": base.sha256(terminal.encode("utf-8")) if isinstance(terminal, str) else None, "final_response_sha256": base.sha256(final.encode("utf-8")) if isinstance(final, str) else None},
        "usage": {"sessions": [{"thread_id": candidate["thread_id"], "parent_thread_id": candidate["parent_thread_id"], **(candidate["usage"] or {})} for candidate in sessions], "complete": criteria["all_agent_final_usage"] == "satisfied"},
        "artifact_hashes": {"stdout_jsonl": base.sha256(stdout.read_bytes()) if stdout.is_file() else None, "stderr": base.sha256(stderr.read_bytes()) if stderr.is_file() else None, "final_message": base.sha256(final_path.read_bytes()) if final_path.is_file() else None},
        "model_invocations": 1, "probe_issues": 1, "retry_performed": False, "raw_transcript_saved": False, "sensitive_material_saved": False,
    }


def validate_authorization(path: Path, schema_path: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    value = base.load_object(path)
    schema = base.load_object(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(schema).validate(value)
    paths = {name: base.verified_relative(identity) for name, identity in value["artifacts"].items()}
    runtime = Path(value["runtime"]["path"])
    data = runtime.read_bytes()
    if len(data) != value["runtime"]["bytes"] or base.sha256(data) != value["runtime"]["sha256"]:
        raise base.ProbeError("runtime identity mismatch")
    paths["runtime"] = runtime
    return value, paths


def record_root(value: dict[str, Any]) -> Path:
    path = (ROOT / value["issuance_records"]["root"] / PROBE_ID).resolve()
    path.relative_to(ROOT)
    return path


def prepare() -> dict[str, Any]:
    value, _ = validate_authorization(DEFAULT_AUTHORIZATION, DEFAULT_SCHEMA)
    root = record_root(value)
    present = [name for name in RECORD_NAMES if (root / name).exists()]
    return {"schema_version": "general-chat-agentic-worker-trace-selector-preparation/v1", "probe_id": PROBE_ID, "authorization_state": value["issuance_authority"], "identity_available": not present, "existing_records": present, "dispatch_state": "allowed" if not present else "denied", "model_invocations": 0, "probe_issues": 0}


def issue() -> dict[str, Any]:
    value, paths = validate_authorization(DEFAULT_AUTHORIZATION, DEFAULT_SCHEMA)
    target = record_root(value)
    target.mkdir(parents=True, exist_ok=True, mode=0o700)
    if any((target / name).exists() for name in RECORD_NAMES):
        raise base.ProbeError("probe identity already used")
    auth_hash = base.sha256(DEFAULT_AUTHORIZATION.read_bytes())
    base.write_once(target / "reservation.json", {"schema_version": "general-chat-agentic-worker-trace-selector-reservation/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "reserved_at_unix_ms": int(time.time() * 1000)})
    private = Path(tempfile.mkdtemp(prefix="general-chat-worker-r6.", dir="/Users/kenn/repos/_verification"))
    private.chmod(0o700)
    home, workspace = private / "codex-home", private / "workspace"
    home.mkdir(mode=0o700); workspace.mkdir(mode=0o700)
    stdout, stderr, final = private / "stdout.jsonl", private / "stderr.txt", private / "final.txt"
    started = time.monotonic_ns() // 1_000_000
    exit_code = 125
    try:
        base.copy_auth(home)
        command = [str(paths["runtime"]), "exec", "--ignore-user-config", "--ignore-rules", "--strict-config", "--enable", "multi_agent", "--disable", "memories", "-c", "agents.max_threads=2", "-c", 'approval_policy="never"', "-m", "gpt-5.6-sol", "-c", 'model_reasoning_effort="medium"', "-s", "workspace-write", "--skip-git-repo-check", "--json", "--output-last-message", str(final), "-C", str(workspace), "-"]
        base.write_once(target / "issued.json", {"schema_version": "general-chat-agentic-worker-trace-selector-issued/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "command_sha256": base.sha256(base.canonical_bytes(command)), "started_monotonic_ms": started})
        environment = os.environ.copy(); environment["CODEX_HOME"] = str(home)
        with paths["model_input"].open("rb") as stdin_file, stdout.open("wb") as stdout_file, stderr.open("wb") as stderr_file:
            exit_code = subprocess.run(command, stdin=stdin_file, stdout=stdout_file, stderr=stderr_file, env=environment, timeout=900, check=False).returncode
    except subprocess.TimeoutExpired:
        exit_code = 124
    ended = time.monotonic_ns() // 1_000_000
    try:
        receipt = build_receipt(value, private, started, ended, exit_code)
        jsonschema.Draft202012Validator(base.load_object(paths["receipt_schema"])).validate(receipt)
        base.write_once(target / "receipt.json", receipt)
        return receipt
    finally:
        shutil.rmtree(private, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("action", choices=("prepare", "issue")); args = parser.parse_args()
    try:
        result = prepare() if args.action == "prepare" else issue()
    except Exception as error:
        print(json.dumps({"schema_version": "general-chat-agentic-worker-trace-selector-error/v1", "status": "error", "reason": str(error)}, ensure_ascii=False, sort_keys=True)); return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
