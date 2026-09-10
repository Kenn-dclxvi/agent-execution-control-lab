#!/usr/bin/env python3
"""Prepare or issue the one-shot isolated MCP transport probe r4."""

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
PROBE_ID = "general-chat-agentic-tool-transport-preflight-r4"
DEFAULT_AUTHORIZATION = ROOT / "docs/general-chat-agentic-tool-transport-probe-r4-authorization.json"
DEFAULT_SCHEMA = ROOT / "docs/general-chat-agentic-tool-transport-probe-r4-authorization.schema.json"
RECORD_NAMES = ("reservation.json", "issued.json", "receipt.json")
EXPECTED_FINAL = "支店窓口は土曜日17時に終了します。"


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
    return {"schema_version": "general-chat-agentic-tool-transport-preparation/v1", "probe_id": PROBE_ID, "authorization_state": value["issuance_authority"], "identity_available": not present, "existing_records": present, "dispatch_state": "allowed" if not present else "denied", "model_invocations": 0, "probe_issues": 0}


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
    result = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if isinstance(value, dict):
                result.append(value)
    return result


def root_rollout(codex_home: Path, root_thread_id: str | None) -> list[dict[str, Any]]:
    if not isinstance(root_thread_id, str):
        return []
    for path in (codex_home / "sessions").rglob("*.jsonl") if (codex_home / "sessions").is_dir() else []:
        events = json_lines(path)
        if events and events[0].get("type") == "session_meta" and isinstance(events[0].get("payload"), dict) and events[0]["payload"].get("id") == root_thread_id:
            return events
    return []


def usage_from(events: list[dict[str, Any]]) -> dict[str, int] | None:
    usage = None
    for event in events:
        payload = event.get("payload")
        if event.get("type") == "event_msg" and isinstance(payload, dict) and payload.get("type") == "token_count":
            info = payload.get("info")
            candidate = info.get("total_token_usage") if isinstance(info, dict) else None
            if isinstance(candidate, dict):
                usage = {field: candidate.get(field) for field in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")}
    return usage


def count_tool_calls(events: list[dict[str, Any]]) -> int:
    count = 0
    for event in events:
        payload = event.get("payload")
        if event.get("type") != "response_item" or not isinstance(payload, dict):
            continue
        name = payload.get("name") or payload.get("tool_name")
        if payload.get("type") in {"function_call", "custom_tool_call", "mcp_tool_call"} and isinstance(name, str) and (name == "fetch_branch_counter_hours" or name.endswith("__fetch_branch_counter_hours")):
            count += 1
    return count


def safe_error_categories(stdout: Path, stderr: Path) -> list[str]:
    joined = b""
    for path in (stdout, stderr):
        if path.is_file():
            joined += path.read_bytes().lower()
    patterns = {
        b"mcp startup failed": "mcp_startup_failed",
        b"failed to start mcp": "mcp_startup_failed",
        b"tools/list": "tools_list_error",
        b"method not found": "method_not_found",
        b"timed out": "timeout",
    }
    return sorted({label for pattern, label in patterns.items() if pattern in joined})


def build_receipt(value: dict[str, Any], private_root: Path, started: int, ended: int, exit_code: int) -> dict[str, Any]:
    stdout = private_root / "stdout.jsonl"
    stderr = private_root / "stderr.txt"
    final_path = private_root / "final.txt"
    audit_path = private_root / "tool-audit.jsonl"
    stdout_events = json_lines(stdout)
    root_ids = [event.get("thread_id") for event in stdout_events if event.get("type") == "thread.started" and isinstance(event.get("thread_id"), str)]
    root_id = root_ids[0] if len(root_ids) == 1 else None
    rollout = root_rollout(private_root / "codex-home", root_id)
    usage = usage_from(rollout)
    audit = json_lines(audit_path)
    audit_names = [event.get("event") for event in audit]
    call_events = [event for event in audit if event.get("event") == "tools_call"]
    final = final_path.read_text(encoding="utf-8").strip() if final_path.is_file() else None
    criteria = {
        "root_thread_identity": "satisfied" if root_id and rollout else "unobserved",
        "mcp_initialize": "satisfied" if "initialize" in audit_names and "initialized" in audit_names else "unobserved",
        "mcp_tools_list": "satisfied" if "tools_list" in audit_names else "unobserved",
        "fixed_tool_call_and_result": "satisfied" if len(call_events) == 1 and call_events[0].get("input") == {"record_id": "branch-counter-hours-r1"} and call_events[0].get("result", {}).get("closes_at") == "17:00" else ("unobserved" if not call_events else "unsatisfied"),
        "root_rollout_tool_call": "satisfied" if count_tool_calls(rollout) == 1 else ("unobserved" if count_tool_calls(rollout) == 0 else "unsatisfied"),
        "final_response": "satisfied" if final == EXPECTED_FINAL else ("unobserved" if final is None else "unsatisfied"),
        "root_final_usage": "satisfied" if isinstance(usage, dict) and all(isinstance(usage.get(field), int) for field in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")) else "unobserved",
        "monotonic_elapsed": "satisfied" if ended >= started else "unsatisfied",
        "safe_projection": "satisfied",
    }
    available = exit_code == 0 and all(state == "satisfied" for state in criteria.values())
    return {
        "schema_version": "general-chat-agentic-tool-transport-receipt/v1",
        "probe_id": PROBE_ID,
        "authorization_id": value["authorization_id"],
        "terminal_state": "tool_transport_available" if available else "tool_transport_unavailable",
        "process": {"exit_code": exit_code, "started_monotonic_ms": started, "ended_monotonic_ms": ended, "elapsed_ms": ended - started},
        "criteria": criteria,
        "bindings": {"root_thread_id": root_id, "server_event_counts": {name: audit_names.count(name) for name in sorted(set(audit_names)) if isinstance(name, str)}, "root_rollout_tool_call_count": count_tool_calls(rollout), "final_response_sha256": sha256(final.encode("utf-8")) if isinstance(final, str) else None},
        "usage": usage,
        "safe_error_categories": safe_error_categories(stdout, stderr),
        "artifact_hashes": {"stdout_jsonl": sha256(stdout.read_bytes()) if stdout.is_file() else None, "stderr": sha256(stderr.read_bytes()) if stderr.is_file() else None, "final_message": sha256(final_path.read_bytes()) if final_path.is_file() else None, "tool_audit": sha256(audit_path.read_bytes()) if audit_path.is_file() else None},
        "model_invocations": 1, "probe_issues": 1, "retry_performed": False, "raw_transcript_saved": False, "sensitive_material_saved": False,
    }


def issue(path: Path = DEFAULT_AUTHORIZATION, schema_path: Path = DEFAULT_SCHEMA) -> dict[str, Any]:
    value, paths = validate_authorization(path, schema_path)
    target = record_root(value)
    target.mkdir(parents=True, exist_ok=True, mode=0o700)
    if any((target / name).exists() for name in RECORD_NAMES):
        raise ProbeError("probe identity already used")
    auth_hash = sha256(path.read_bytes())
    write_once(target / "reservation.json", {"schema_version": "general-chat-agentic-tool-transport-reservation/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "reserved_at_unix_ms": int(time.time() * 1000)})
    private = Path(tempfile.mkdtemp(prefix="general-chat-tool-r4.", dir="/Users/kenn/repos/_verification"))
    private.chmod(0o700)
    home = private / "codex-home"
    workspace = private / "workspace"
    home.mkdir(mode=0o700)
    workspace.mkdir(mode=0o700)
    stdout = private / "stdout.jsonl"
    stderr = private / "stderr.txt"
    final = private / "final.txt"
    audit = private / "tool-audit.jsonl"
    started = time.monotonic_ns() // 1_000_000
    exit_code = 125
    try:
        copy_auth(home)
        command = [str(paths["runtime"]), "exec", "--ignore-user-config", "--ignore-rules", "--strict-config", "--disable", "memories", "-c", 'approval_policy="never"', "-m", "gpt-5.6-sol", "-c", 'model_reasoning_effort="medium"', "-s", "workspace-write", "--skip-git-repo-check", "--json", "--output-last-message", str(final), "-c", 'mcp_servers.branch_hours.command="/usr/bin/python3"', "-c", 'mcp_servers.branch_hours.args=["' + str(paths["tool_server"]) + '"]', "-c", 'mcp_servers.branch_hours.env.GENERAL_CHAT_BRANCH_TOOL_AUDIT="' + str(audit) + '"', "-C", str(workspace), "-"]
        write_once(target / "issued.json", {"schema_version": "general-chat-agentic-tool-transport-issued/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "command_sha256": sha256(canonical_bytes(command)), "started_monotonic_ms": started})
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
        print(json.dumps({"schema_version": "general-chat-agentic-tool-transport-error/v1", "status": "error", "reason": str(error)}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
