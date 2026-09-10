#!/usr/bin/env python3
"""Prepare or issue the authorized one-shot general-chat capability probe."""

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
DEFAULT_AUTHORIZATION = ROOT / "docs/general-chat-agentic-capability-preflight-authorization-r1.json"
DEFAULT_AUTHORIZATION_SCHEMA = ROOT / "docs/general-chat-agentic-capability-preflight-authorization-r1.schema.json"
PROBE_ID = "general-chat-agentic-capability-preflight-r3"
RECORD_NAMES = ("reservation.json", "issued.json", "receipt.json")


class ProbeError(Exception):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ProbeError(f"JSON object required: {path}")
    return value


def verified_path(identity: dict[str, Any]) -> Path:
    path = (ROOT / identity["path"]).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError as error:
        raise ProbeError("bound path outside repository") from error
    data = path.read_bytes()
    if len(data) != identity["bytes"] or sha256_bytes(data) != identity["sha256"]:
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
    authorization = load_object(path)
    schema = load_object(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.Draft202012Validator(schema).validate(authorization)
    paths = {name: verified_path(identity) for name, identity in authorization["artifacts"].items()}
    runtime = Path(authorization["runtime"]["path"])
    runtime_data = runtime.read_bytes()
    if len(runtime_data) != authorization["runtime"]["bytes"] or sha256_bytes(runtime_data) != authorization["runtime"]["sha256"]:
        raise ProbeError("runtime identity mismatch")
    paths["runtime"] = runtime
    if authorization["probe_id"] != PROBE_ID:
        raise ProbeError("probe identity mismatch")
    return authorization, paths


def record_root(authorization: dict[str, Any]) -> Path:
    root = (ROOT / authorization["issuance_records"]["root"] / PROBE_ID).resolve()
    root.relative_to(ROOT)
    return root


def prepare(authorization_path: Path, schema_path: Path) -> dict[str, Any]:
    authorization, _ = validate_authorization(authorization_path, schema_path)
    target = record_root(authorization)
    present = [name for name in RECORD_NAMES if (target / name).exists()]
    return {
        "schema_version": "general-chat-agentic-probe-preparation/v1",
        "probe_id": PROBE_ID,
        "authorization_state": authorization["issuance_authority"],
        "identity_available": not present,
        "existing_records": present,
        "dispatch_state": "allowed" if not present else "denied",
        "model_invocations": 0,
        "probe_issues": 0,
    }


def copy_auth(codex_home: Path) -> None:
    source = Path.home() / ".codex" / "auth.json"
    if not source.is_file():
        raise ProbeError("host auth unavailable")
    destination = codex_home / "auth.json"
    shutil.copyfile(source, destination)
    destination.chmod(0o600)


def parse_jsonl(path: Path) -> list[dict[str, Any]]:
    values = []
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            value = json.loads(line)
            if isinstance(value, dict):
                values.append(value)
    return values


def extract_thread_id(events: list[dict[str, Any]]) -> str | None:
    values = [event.get("thread_id") for event in events if event.get("type") == "thread.started"]
    values = [value for value in values if isinstance(value, str)]
    return values[0] if len(values) == 1 else None


def rollout_files(codex_home: Path) -> list[Path]:
    return sorted((codex_home / "sessions").rglob("*.jsonl")) if (codex_home / "sessions").is_dir() else []


def session_projection(path: Path) -> dict[str, Any] | None:
    events = parse_jsonl(path)
    if not events or events[0].get("type") != "session_meta":
        return None
    payload = events[0].get("payload")
    if not isinstance(payload, dict):
        return None
    usage = None
    terminal = None
    response_items = []
    for event in events[1:]:
        event_payload = event.get("payload")
        if event.get("type") == "event_msg" and isinstance(event_payload, dict):
            if event_payload.get("type") == "token_count":
                info = event_payload.get("info")
                candidate = info.get("total_token_usage") if isinstance(info, dict) else None
                if isinstance(candidate, dict):
                    usage = {key: candidate.get(key) for key in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")}
            if event_payload.get("type") == "task_complete" and isinstance(event_payload.get("last_agent_message"), str):
                terminal = event_payload["last_agent_message"]
        if event.get("type") == "response_item" and isinstance(event_payload, dict):
            response_items.append(event_payload)
    source = payload.get("source")
    task_name = None
    if isinstance(source, dict):
        subagent = source.get("subagent")
        if isinstance(subagent, dict):
            task_name = subagent.get("task_name")
    return {
        "thread_id": payload.get("id"),
        "parent_thread_id": payload.get("parent_thread_id"),
        "task_name": task_name,
        "usage": usage,
        "terminal": terminal,
        "response_items": response_items,
    }


def decode_arguments(value: Any) -> dict[str, Any] | None:
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return None
        return parsed if isinstance(parsed, dict) else None
    return None


def function_calls(session: dict[str, Any], suffix: str) -> list[dict[str, Any]]:
    found = []
    for item in session["response_items"]:
        if item.get("type") not in {"function_call", "custom_tool_call"}:
            continue
        name = item.get("name") or item.get("tool_name")
        if isinstance(name, str) and (name == suffix or name.endswith("__" + suffix)):
            found.append({"call_id": item.get("call_id"), "name": name, "arguments": decode_arguments(item.get("arguments") or item.get("input"))})
    return found


def messages(session: dict[str, Any]) -> list[str]:
    values = []
    for item in session["response_items"]:
        if item.get("type") != "message" or item.get("role") != "assistant":
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") in {"output_text", "text"} and isinstance(content.get("text"), str):
                values.append(content["text"])
    return values


def build_receipt(
    authorization: dict[str, Any], paths: dict[str, Path], private_root: Path, stdout_path: Path,
    audit_path: Path, final_path: Path, started_ms: int, ended_ms: int, exit_code: int | None,
) -> dict[str, Any]:
    stdout_events = parse_jsonl(stdout_path)
    root_id = extract_thread_id(stdout_events)
    sessions = [value for path in rollout_files(private_root / "codex-home") if (value := session_projection(path)) is not None]
    roots = [value for value in sessions if value["thread_id"] == root_id and value["parent_thread_id"] is None]
    root = roots[0] if len(roots) == 1 else None
    descendants = [value for value in sessions if value["parent_thread_id"] == root_id]
    spawn_calls = function_calls(root, "spawn_agent") if root else []
    tool_calls = function_calls(root, "fetch_branch_counter_hours") if root else []
    audits = parse_jsonl(audit_path)
    final_text = final_path.read_text(encoding="utf-8") if final_path.is_file() else None
    expected_packet = {
        "task_identity": "parking_fact_check",
        "record_id": "parking-saturday-r1",
        "record": {"title": "駐車場利用案内", "text": "土曜日の駐車場利用時間は9時00分から18時30分までです。"},
        "required_result_shape": {"type": "one_sentence", "must_include": ["18時まで駐車できる", "18時30分まで"]},
    }
    spawn_args = spawn_calls[0]["arguments"] if len(spawn_calls) == 1 else None
    packet = None
    if isinstance(spawn_args, dict) and isinstance(spawn_args.get("message"), str):
        try:
            packet = json.loads(spawn_args["message"])
        except json.JSONDecodeError:
            packet = None
    child = next((value for value in descendants if value.get("task_name") == "parking_fact_check"), None)
    criteria = {
        "root_thread_identity": "satisfied" if root is not None else "unobserved",
        "spawn_call_and_task_identity": "satisfied" if len(spawn_calls) == 1 and isinstance(spawn_args, dict) and spawn_args.get("task_name") == "parking_fact_check" and spawn_args.get("fork_turns") == "none" else ("unobserved" if not spawn_calls else "unsatisfied"),
        "worker_packet_projection": "satisfied" if packet == expected_packet else ("unobserved" if packet is None else "unsatisfied"),
        "descendant_parent_and_task_binding": "satisfied" if child is not None else "unobserved",
        "descendant_terminal_sender_and_result": "satisfied" if child and isinstance(child.get("terminal"), str) and all(value in child["terminal"] for value in ("18時まで駐車できる", "18時30分まで")) else ("unobserved" if not child or not child.get("terminal") else "unsatisfied"),
        "root_tool_call_and_terminal_result": "satisfied" if len(tool_calls) == 1 and tool_calls[0]["arguments"] == {"record_id": "branch-counter-hours-r1"} and len(audits) == 1 and audits[0].get("result", {}).get("closes_at") == "17:00" else ("unobserved" if not tool_calls or not audits else "unsatisfied"),
        "final_response_direct_binding": "satisfied" if isinstance(final_text, str) and len([part for part in final_text.split("。") if part.strip()]) == 2 and all(value in final_text for value in ("18時まで駐車できる", "18時30分", "17時")) else ("unobserved" if not final_text else "unsatisfied"),
        "all_agent_final_usage": "satisfied" if sessions and all(isinstance(value.get("usage"), dict) and all(isinstance(value["usage"].get(field), int) for field in ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")) for value in sessions) else "unobserved",
        "monotonic_elapsed": "satisfied" if ended_ms >= started_ms else "unsatisfied",
        "safe_projection_without_raw_transcript": "satisfied",
    }
    usage_sessions = [
        {"thread_id": value["thread_id"], "parent_thread_id": value["parent_thread_id"], **(value["usage"] or {})}
        for value in sessions
    ]
    available = exit_code == 0 and all(value == "satisfied" for value in criteria.values())
    return {
        "schema_version": "general-chat-agentic-capability-probe-receipt/v3",
        "probe_id": PROBE_ID,
        "authorization_id": authorization["authorization_id"],
        "terminal_state": "capability_available" if available else "capability_unavailable",
        "process": {"exit_code": exit_code, "started_monotonic_ms": started_ms, "ended_monotonic_ms": ended_ms, "elapsed_ms": ended_ms - started_ms},
        "criteria": criteria,
        "bindings": {
            "root_thread_id": root_id,
            "spawn_call_count": len(spawn_calls),
            "worker_packet_sha256": sha256_bytes(canonical_bytes(packet)) if isinstance(packet, dict) else None,
            "descendant_thread_id": child.get("thread_id") if child else None,
            "worker_terminal_sha256": sha256_bytes(child["terminal"].encode("utf-8")) if child and isinstance(child.get("terminal"), str) else None,
            "root_tool_call_count": len(tool_calls),
            "root_tool_audit_count": len(audits),
            "final_response_sha256": sha256_bytes(final_text.encode("utf-8")) if isinstance(final_text, str) else None,
        },
        "usage": {"sessions": usage_sessions, "complete": criteria["all_agent_final_usage"] == "satisfied"},
        "artifact_hashes": {"stdout_jsonl": sha256_bytes(stdout_path.read_bytes()) if stdout_path.is_file() else None, "final_message": sha256_bytes(final_path.read_bytes()) if final_path.is_file() else None, "tool_audit": sha256_bytes(audit_path.read_bytes()) if audit_path.is_file() else None},
        "model_invocations": 1,
        "probe_issues": 1,
        "retry_performed": False,
        "raw_transcript_saved": False,
        "sensitive_material_saved": False,
    }


def issue(authorization_path: Path, schema_path: Path) -> dict[str, Any]:
    authorization, paths = validate_authorization(authorization_path, schema_path)
    target = record_root(authorization)
    target.mkdir(parents=True, exist_ok=True, mode=0o700)
    if any((target / name).exists() for name in RECORD_NAMES):
        raise ProbeError("probe identity already used")
    auth_hash = sha256_bytes(authorization_path.read_bytes())
    write_once(target / "reservation.json", {"schema_version": "general-chat-agentic-probe-reservation/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "reserved_at_unix_ms": int(time.time() * 1000)})
    private_root = Path(tempfile.mkdtemp(prefix="general-chat-agentic-r3.", dir="/Users/kenn/repos/_verification"))
    private_root.chmod(0o700)
    codex_home = private_root / "codex-home"
    workspace = private_root / "workspace"
    codex_home.mkdir(mode=0o700)
    workspace.mkdir(mode=0o700)
    stdout_path = private_root / "stdout.jsonl"
    stderr_path = private_root / "stderr.txt"
    final_path = private_root / "final.txt"
    audit_path = private_root / "tool-audit.jsonl"
    exit_code: int | None = None
    started_ms = time.monotonic_ns() // 1_000_000
    try:
        copy_auth(codex_home)
        command = [
            str(paths["runtime"]), "exec", "--ignore-user-config", "--ignore-rules", "--strict-config",
            "--enable", "multi_agent", "--disable", "memories", "--disable", "apps", "--disable", "plugins", "--disable", "plugin_sharing",
            "-c", "agents.max_threads=4", "-c", 'approval_policy="never"', "-m", "gpt-5.6-sol",
            "-c", 'model_reasoning_effort="medium"', "-s", "workspace-write", "--skip-git-repo-check", "--json",
            "--output-last-message", str(final_path),
            "-c", 'mcp_servers.branch_hours.command="/usr/bin/python3"',
            "-c", 'mcp_servers.branch_hours.args=["' + str(paths["tool_server"]) + '"]',
            "-c", 'mcp_servers.branch_hours.env.GENERAL_CHAT_BRANCH_TOOL_AUDIT="' + str(audit_path) + '"',
            "-C", str(workspace), "-",
        ]
        write_once(target / "issued.json", {"schema_version": "general-chat-agentic-probe-issued/v1", "probe_id": PROBE_ID, "authorization_sha256": auth_hash, "command_sha256": sha256_bytes(canonical_bytes(command)), "started_monotonic_ms": started_ms})
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(codex_home)
        with stdout_path.open("wb") as stdout_file, stderr_path.open("wb") as stderr_file, paths["model_input"].open("rb") as stdin_file:
            completed = subprocess.run(command, stdin=stdin_file, stdout=stdout_file, stderr=stderr_file, env=environment, timeout=900, check=False)
        exit_code = completed.returncode
    except subprocess.TimeoutExpired:
        exit_code = 124
    except Exception:
        exit_code = 125
    ended_ms = time.monotonic_ns() // 1_000_000
    try:
        receipt = build_receipt(authorization, paths, private_root, stdout_path, audit_path, final_path, started_ms, ended_ms, exit_code)
        receipt_schema = load_object(paths["receipt_schema"])
        jsonschema.Draft202012Validator(receipt_schema).validate(receipt)
        write_once(target / "receipt.json", receipt)
        return receipt
    finally:
        shutil.rmtree(private_root, ignore_errors=True)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("action", choices=("prepare", "issue"))
    value.add_argument("--authorization", type=Path, default=DEFAULT_AUTHORIZATION)
    value.add_argument("--authorization-schema", type=Path, default=DEFAULT_AUTHORIZATION_SCHEMA)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        result = prepare(args.authorization.resolve(), args.authorization_schema.resolve()) if args.action == "prepare" else issue(args.authorization.resolve(), args.authorization_schema.resolve())
    except Exception as error:
        print(json.dumps({"schema_version": "general-chat-agentic-probe-error/v1", "status": "error", "reason": str(error)}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
