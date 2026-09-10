#!/usr/bin/env python3
"""Prepare or issue the one-shot worker trace binding probe r5."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
PROBE_ID = "general-chat-agentic-worker-trace-preflight-r5"
TASK_NAME = "parking_fact_check"
DEFAULT_AUTHORIZATION = ROOT / "docs/general-chat-agentic-worker-trace-probe-r5-authorization.json"
DEFAULT_SCHEMA = ROOT / "docs/general-chat-agentic-worker-trace-probe-r5-authorization.schema.json"
RECORD_NAMES = ("reservation.json", "issued.json", "receipt.json")
EXPECTED_FINAL = "土曜日は18時まで駐車でき、利用時間は18時30分までです。"
EXPECTED_PACKET = {
    "task_identity": TASK_NAME,
    "record_id": "parking-saturday-r1",
    "record": {"title": "駐車場利用案内", "text": "土曜日の駐車場利用時間は9時00分から18時30分までです。"},
    "question": "土曜日に18時まで駐車できるか、根拠とともに一文で答える",
    "required_result_shape": {"type": "one_sentence", "must_include": ["18時まで駐車できる", "18時30分まで"]},
}


class ProbeError(Exception):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProbeError("JSON object required")
    return value


def verified_relative(identity: dict[str, Any]) -> Path:
    path = (ROOT / identity["path"]).resolve()
    path.relative_to(ROOT)
    data = path.read_bytes()
    if len(data) != identity["bytes"] or sha256(data) != identity["sha256"]:
        raise ProbeError(f"identity mismatch: {identity['path']}")
    return path


def write_once(path: Path, value: dict[str, Any]) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(descriptor, canonical_bytes(value) + b"\n")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def validate_authorization(path: Path, schema_path: Path) -> tuple[dict[str, Any], dict[str, Path]]:
    value = load_object(path)
    schema = load_object(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(schema).validate(value)
    paths = {name: verified_relative(identity) for name, identity in value["artifacts"].items()}
    runtime = Path(value["runtime"]["path"])
    data = runtime.read_bytes()
    if len(data) != value["runtime"]["bytes"] or sha256(data) != value["runtime"]["sha256"]:
        raise ProbeError("runtime identity mismatch")
    paths["runtime"] = runtime
    return value, paths


def record_root(value: dict[str, Any]) -> Path:
    path = (ROOT / value["issuance_records"]["root"] / PROBE_ID).resolve()
    path.relative_to(ROOT)
    return path


def prepare(path: Path = DEFAULT_AUTHORIZATION, schema_path: Path = DEFAULT_SCHEMA) -> dict[str, Any]:
    value, _ = validate_authorization(path, schema_path)
    root = record_root(value)
    present = [name for name in RECORD_NAMES if (root / name).exists()]
    return {"schema_version": "general-chat-agentic-worker-trace-preparation/v1", "probe_id": PROBE_ID, "authorization_state": value["issuance_authority"], "identity_available": not present, "existing_records": present, "dispatch_state": "allowed" if not present else "denied", "model_invocations": 0, "probe_issues": 0}


def copy_auth(codex_home: Path) -> None:
    source = Path.home() / ".codex" / "auth.json"
    if not source.is_file():
        raise ProbeError("host auth unavailable")
    destination = codex_home / "auth.json"
    shutil.copyfile(source, destination)
    destination.chmod(0o600)


def json_lines(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    values = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if isinstance(value, dict):
                values.append(value)
    return values


def decode_object(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return None
        return parsed if isinstance(parsed, dict) else None
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                for key in ("text", "output", "content"):
                    parsed = decode_object(item.get(key))
                    if parsed is not None:
                        return parsed
    return None


def session(path: Path) -> dict[str, Any] | None:
    events = json_lines(path)
    if not events or events[0].get("type") != "session_meta" or not isinstance(events[0].get("payload"), dict):
        return None
    meta = events[0]["payload"]
    source = meta.get("source")
    agent_path = None
    if isinstance(source, dict) and isinstance(source.get("subagent"), dict) and isinstance(source["subagent"].get("thread_spawn"), dict):
        agent_path = source["subagent"]["thread_spawn"].get("agent_path")
    terminal = None
    usage = None
    items = []
    event_types = []
    for event in events[1:]:
        payload = event.get("payload")
        if isinstance(payload, dict):
            if isinstance(payload.get("type"), str):
                event_types.append(payload["type"])
            if event.get("type") == "response_item":
                items.append(payload)
            if event.get("type") == "event_msg" and payload.get("type") == "task_complete" and isinstance(payload.get("last_agent_message"), str):
                terminal = payload["last_agent_message"]
            if event.get("type") == "event_msg" and payload.get("type") == "token_count":
                info = payload.get("info")
                candidate = info.get("total_token_usage") if isinstance(info, dict) else None
                if isinstance(candidate, dict):
                    usage = {field: candidate.get(field) for field in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")}
    return {"thread_id": meta.get("id"), "parent_thread_id": meta.get("parent_thread_id"), "agent_path": agent_path, "terminal": terminal, "usage": usage, "items": items, "event_types": sorted(set(event_types))}


def find_spawn(root: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    calls = []
    outputs = []
    for item in root["items"]:
        if item.get("type") in {"function_call", "custom_tool_call"} and item.get("name") == "spawn_agent":
            calls.append({"call_id": item.get("call_id"), "arguments": decode_object(item.get("arguments") or item.get("input"))})
        if item.get("type") in {"function_call_output", "custom_tool_call_output"}:
            outputs.append({"call_id": item.get("call_id"), "value": decode_object(item.get("output") or item.get("content"))})
    return calls, outputs


def spawn_result_from_events(root: dict[str, Any], call_id: str | None, outputs: list[dict[str, Any]]) -> dict[str, Any] | None:
    for output in outputs:
        if output.get("call_id") == call_id and isinstance(output.get("value"), dict):
            value = output["value"]
            child = value.get("child_thread_id") or value.get("new_thread_id") or value.get("agent_id")
            task = value.get("task_name")
            if isinstance(child, str):
                return {"child_thread_id": child, "task_name": task}
    return None


def build_receipt(value: dict[str, Any], private: Path, started: int, ended: int, exit_code: int) -> dict[str, Any]:
    stdout = private / "stdout.jsonl"
    stderr = private / "stderr.txt"
    final_path = private / "final.txt"
    stdout_events = json_lines(stdout)
    root_ids = [event.get("thread_id") for event in stdout_events if event.get("type") == "thread.started" and isinstance(event.get("thread_id"), str)]
    root_id = root_ids[0] if len(root_ids) == 1 else None
    sessions = [candidate for path in (private / "codex-home" / "sessions").rglob("*.jsonl") if (candidate := session(path)) is not None] if (private / "codex-home" / "sessions").is_dir() else []
    roots = [candidate for candidate in sessions if candidate["thread_id"] == root_id and candidate["parent_thread_id"] is None]
    root = roots[0] if len(roots) == 1 else None
    calls, outputs = find_spawn(root) if root else ([], [])
    call = calls[0] if len(calls) == 1 else None
    args = call.get("arguments") if call else None
    packet = decode_object(args.get("message")) if isinstance(args, dict) else None
    spawn_result = spawn_result_from_events(root, call.get("call_id"), outputs) if root and call else None
    child_id = spawn_result.get("child_thread_id") if spawn_result else None
    children = [candidate for candidate in sessions if candidate["thread_id"] == child_id and candidate["parent_thread_id"] == root_id]
    child = children[0] if len(children) == 1 else None
    terminal = child.get("terminal") if child else None
    final = final_path.read_text(encoding="utf-8").strip() if final_path.is_file() else None
    usages = [candidate["usage"] for candidate in sessions]
    criteria = {
        "root_thread_identity": "satisfied" if root else "unobserved",
        "spawn_request": "satisfied" if isinstance(args, dict) and args.get("task_name") == TASK_NAME and args.get("fork_turns") == "none" else ("unobserved" if args is None else "unsatisfied"),
        "worker_packet": "satisfied" if packet == EXPECTED_PACKET else ("unobserved" if packet is None else "unsatisfied"),
        "runtime_spawn_result": "satisfied" if spawn_result and spawn_result.get("task_name") in {TASK_NAME, f"/root/{TASK_NAME}"} else ("unobserved" if spawn_result is None or spawn_result.get("task_name") is None else "unsatisfied"),
        "child_session_binding": "satisfied" if child and child.get("agent_path") == f"/root/{TASK_NAME}" else ("unobserved" if child is None or child.get("agent_path") is None else "unsatisfied"),
        "child_terminal_result": "satisfied" if isinstance(terminal, str) and all(text in terminal for text in ("18時まで駐車できる", "18時30分まで")) else ("unobserved" if terminal is None else "unsatisfied"),
        "root_final_response": "satisfied" if final == EXPECTED_FINAL else ("unobserved" if final is None else "unsatisfied"),
        "all_agent_final_usage": "satisfied" if len(usages) == 2 and all(isinstance(usage, dict) and all(isinstance(usage.get(field), int) for field in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")) for usage in usages) else "unobserved",
        "monotonic_elapsed": "satisfied" if ended >= started else "unsatisfied",
        "safe_projection": "satisfied",
    }
    available = exit_code == 0 and all(state == "satisfied" for state in criteria.values())
    event_types = sorted({item for candidate in sessions for item in candidate["event_types"]})
    response_item_types = sorted({item.get("type") for candidate in sessions for item in candidate["items"] if isinstance(item.get("type"), str)})
    return {
        "schema_version": "general-chat-agentic-worker-trace-receipt/v1", "probe_id": PROBE_ID, "authorization_id": value["authorization_id"],
        "terminal_state": "worker_trace_available" if available else "worker_trace_unavailable",
        "process": {"exit_code": exit_code, "started_monotonic_ms": started, "ended_monotonic_ms": ended, "elapsed_ms": ended - started},
        "criteria": criteria,
        "bindings": {"root_thread_id": root_id, "spawn_call_count": len(calls), "spawn_output_count": len(outputs), "worker_packet_sha256": sha256(canonical_bytes(packet)) if isinstance(packet, dict) else None, "child_thread_id": child_id, "child_terminal_sha256": sha256(terminal.encode("utf-8")) if isinstance(terminal, str) else None, "final_response_sha256": sha256(final.encode("utf-8")) if isinstance(final, str) else None},
        "usage": {"sessions": [{"thread_id": candidate["thread_id"], "parent_thread_id": candidate["parent_thread_id"], **(candidate["usage"] or {})} for candidate in sessions], "complete": criteria["all_agent_final_usage"] == "satisfied"},
        "selector_inventory": {"event_types": event_types, "response_item_types": response_item_types},
        "artifact_hashes": {"stdout_jsonl": sha256(stdout.read_bytes()) if stdout.is_file() else None, "stderr": sha256(stderr.read_bytes()) if stderr.is_file() else None, "final_message": sha256(final_path.read_bytes()) if final_path.is_file() else None},
        "model_invocations": 1, "probe_issues": 1, "retry_performed": False, "raw_transcript_saved": False, "sensitive_material_saved": False,
    }


def issue(path: Path = DEFAULT_AUTHORIZATION, schema_path: Path = DEFAULT_SCHEMA) -> dict[str, Any]:
    value, paths = validate_authorization(path, schema_path)
    target = record_root(value)
    target.mkdir(parents=True, exist_ok=True, mode=0o700)
    if any((target / name).exists() for name in RECORD_NAMES):
        raise ProbeError("probe identity already used")
    auth_hash = sha256(path.read_bytes())
    write_once(target / "reservation.json", {"schema_version": "general-chat-agentic-worker-trace-reservation/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "reserved_at_unix_ms": int(time.time() * 1000)})
    private = Path(tempfile.mkdtemp(prefix="general-chat-worker-r5.", dir="/Users/kenn/repos/_verification"))
    private.chmod(0o700)
    home = private / "codex-home"
    workspace = private / "workspace"
    home.mkdir(mode=0o700)
    workspace.mkdir(mode=0o700)
    stdout, stderr, final = private / "stdout.jsonl", private / "stderr.txt", private / "final.txt"
    started = time.monotonic_ns() // 1_000_000
    exit_code = 125
    try:
        copy_auth(home)
        command = [str(paths["runtime"]), "exec", "--ignore-user-config", "--ignore-rules", "--strict-config", "--enable", "multi_agent", "--disable", "memories", "-c", "agents.max_threads=2", "-c", 'approval_policy="never"', "-m", "gpt-5.6-sol", "-c", 'model_reasoning_effort="medium"', "-s", "workspace-write", "--skip-git-repo-check", "--json", "--output-last-message", str(final), "-C", str(workspace), "-"]
        write_once(target / "issued.json", {"schema_version": "general-chat-agentic-worker-trace-issued/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "command_sha256": sha256(canonical_bytes(command)), "started_monotonic_ms": started})
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(home)
        with paths["model_input"].open("rb") as stdin_file, stdout.open("wb") as stdout_file, stderr.open("wb") as stderr_file:
            exit_code = subprocess.run(command, stdin=stdin_file, stdout=stdout_file, stderr=stderr_file, env=environment, timeout=900, check=False).returncode
    except subprocess.TimeoutExpired:
        exit_code = 124
    ended = time.monotonic_ns() // 1_000_000
    try:
        receipt = build_receipt(value, private, started, ended, exit_code)
        jsonschema.Draft202012Validator(load_object(paths["receipt_schema"])).validate(receipt)
        write_once(target / "receipt.json", receipt)
        return receipt
    finally:
        shutil.rmtree(private, ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "issue"))
    args = parser.parse_args()
    try:
        result = prepare() if args.action == "prepare" else issue()
    except Exception as error:
        print(json.dumps({"schema_version": "general-chat-agentic-worker-trace-error/v1", "status": "error", "reason": str(error)}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
