#!/usr/bin/env python3
"""Project a hash-bound synthetic Codex trace packet into the normalized r2 trace."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

try:
    from scripts.general_chat_agentic_raw_normalizer import normalize_known_fields
except ModuleNotFoundError:  # direct script execution puts scripts/ on sys.path
    from general_chat_agentic_raw_normalizer import normalize_known_fields


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PACKET = ROOT / "docs/general-chat-agentic-real-trace-adapter-synthetic-packet-r1.json"
DEFAULT_PACKET_SCHEMA = ROOT / "docs/general-chat-agentic-real-trace-adapter-input.schema.json"
NORMALIZED_SCHEMA_VERSION = "general-chat-agentic-normalized-trace/v1"
EXPECTED_OUTPUT_SCHEMA_IDENTITY = {
    "path": "docs/general-chat-agentic-binding-extractor-input-r2.schema.json",
    "sha256": "42a85185964df04ea0b085c25b13d155c06658d758c76f95f617e69730c167e8",
    "bytes": 4917,
}


class AdapterError(Exception):
    """A packet boundary or trace identity check failed."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def load_json_object(path: Path, error_code: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AdapterError(error_code) from error
    if not isinstance(value, dict):
        raise AdapterError(error_code)
    return value


def validate_packet(packet: dict[str, Any], schema: dict[str, Any]) -> None:
    try:
        jsonschema.Draft202012Validator(schema).validate(packet)
    except (jsonschema.ValidationError, jsonschema.SchemaError) as error:
        raise AdapterError("PACKET_SCHEMA_INVALID") from error


def resolve_bound_file(repository_root: Path, identity: dict[str, Any]) -> tuple[Path, bytes]:
    root = repository_root.resolve()
    candidate = (root / identity["path"]).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise AdapterError("BOUND_PATH_OUTSIDE_REPOSITORY") from error
    if not candidate.is_file():
        raise AdapterError("BOUND_FILE_UNAVAILABLE")
    try:
        data = candidate.read_bytes()
    except OSError as error:
        raise AdapterError("BOUND_FILE_UNAVAILABLE") from error
    if len(data) != identity["bytes"]:
        raise AdapterError("BOUND_FILE_BYTE_COUNT_MISMATCH")
    if hashlib.sha256(data).hexdigest() != identity["sha256"]:
        raise AdapterError("BOUND_FILE_HASH_MISMATCH")
    return candidate, data


def parse_json_lines(data: bytes) -> list[dict[str, Any]]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise AdapterError("JSONL_INVALID") from error
    events: list[dict[str, Any]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise AdapterError("JSONL_INVALID") from error
        if not isinstance(event, dict):
            raise AdapterError("JSONL_INVALID")
        events.append(event)
    return events


def project_root_events(events: list[dict[str, Any]], root_thread_id: str) -> list[dict[str, str]]:
    projected = [
        {"type": "thread.started", "thread_id": event["thread_id"]}
        for event in events
        if event.get("type") == "thread.started" and isinstance(event.get("thread_id"), str)
    ]
    if [event["thread_id"] for event in projected] != [root_thread_id]:
        raise AdapterError("ROOT_THREAD_ID_MISMATCH")
    return projected


def project_known_session_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    projected = []
    for event in events:
        if event.get("type") != "event_msg" or not isinstance(event.get("payload"), dict):
            continue
        payload = event["payload"]
        event_type = payload.get("type")
        if event_type == "task_complete":
            result = payload.get("last_agent_message")
            if result is not None and not isinstance(result, str):
                raise AdapterError("KNOWN_EVENT_INVALID")
            projected.append(event)
        elif event_type == "token_count":
            info = payload.get("info")
            usage = info.get("total_token_usage") if isinstance(info, dict) else None
            fields = ("input_tokens", "cached_input_tokens", "output_tokens", "total_tokens")
            if not isinstance(usage, dict) or any(
                not isinstance(usage.get(field), int) or isinstance(usage.get(field), bool) or usage[field] < 0
                for field in fields
            ):
                raise AdapterError("KNOWN_EVENT_INVALID")
            projected.append(event)
    return projected


def verify_session_graph(packet: dict[str, Any]) -> None:
    sessions = packet["sessions"]
    thread_ids = [session["thread_id"] for session in sessions]
    file_paths = [session["file"]["path"] for session in sessions]
    if len(thread_ids) != len(set(thread_ids)):
        raise AdapterError("DUPLICATE_SESSION_THREAD")
    if len(file_paths) != len(set(file_paths)):
        raise AdapterError("DUPLICATE_SESSION_FILE")
    roots = [session for session in sessions if session["role"] == "root"]
    if len(roots) != 1:
        raise AdapterError("ROOT_SESSION_CARDINALITY_INVALID")
    root = roots[0]
    root_thread_id = packet["root_thread_id"]
    if root["thread_id"] != root_thread_id or root["parent_thread_id"] is not None:
        raise AdapterError("ROOT_SESSION_IDENTITY_MISMATCH")
    by_thread = {session["thread_id"]: session for session in sessions}
    for session in sessions:
        if session["role"] == "root":
            continue
        parent = session["parent_thread_id"]
        visited = {session["thread_id"]}
        while parent != root_thread_id:
            if parent not in by_thread or parent in visited:
                raise AdapterError("SESSION_PARENT_CHAIN_INVALID")
            visited.add(parent)
            parent = by_thread[parent]["parent_thread_id"]


def project_session(
    packet: dict[str, Any], session_identity: dict[str, Any], repository_root: Path
) -> dict[str, Any]:
    _, data = resolve_bound_file(repository_root, session_identity["file"])
    events = parse_json_lines(data)
    if not events or events[0].get("type") != "session_meta" or not isinstance(events[0].get("payload"), dict):
        raise AdapterError("SESSION_META_MISSING")
    meta = events[0]
    payload = meta["payload"]
    if payload.get("id") != session_identity["thread_id"]:
        raise AdapterError("SESSION_THREAD_ID_MISMATCH")
    if payload.get("parent_thread_id") != session_identity["parent_thread_id"]:
        raise AdapterError("SESSION_PARENT_ID_MISMATCH")
    if payload.get("cwd") != packet["workspace"]:
        raise AdapterError("SESSION_WORKSPACE_MISMATCH")
    safe_meta = {
        "type": "session_meta",
        "payload": {
            "id": payload["id"],
            "cwd": payload["cwd"],
            "parent_thread_id": payload["parent_thread_id"],
        },
    }
    return {"session_meta": safe_meta, "events": project_known_session_events(events[1:])}


def adapt_packet(packet: dict[str, Any], repository_root: Path = ROOT) -> dict[str, Any]:
    if packet["normalized_output_schema"] != EXPECTED_OUTPUT_SCHEMA_IDENTITY:
        raise AdapterError("NORMALIZED_SCHEMA_IDENTITY_MISMATCH")
    if packet["monotonic"]["ended_ms"] < packet["monotonic"]["started_ms"]:
        raise AdapterError("MONOTONIC_RANGE_INVALID")
    verify_session_graph(packet)
    _, root_data = resolve_bound_file(repository_root, packet["root_events"])
    root_events = project_root_events(parse_json_lines(root_data), packet["root_thread_id"])
    sessions = [project_session(packet, session, repository_root) for session in packet["sessions"]]
    raw = {
        "probe_id": packet["probe_id"],
        "root_events": root_events,
        "sessions": sessions,
        "monotonic": packet["monotonic"],
    }
    normalized = normalize_known_fields(raw)
    _, schema_data = resolve_bound_file(repository_root, packet["normalized_output_schema"])
    try:
        output_schema = json.loads(schema_data)
        jsonschema.Draft202012Validator(output_schema).validate(normalized)
    except (json.JSONDecodeError, jsonschema.ValidationError, jsonschema.SchemaError) as error:
        raise AdapterError("NORMALIZED_OUTPUT_INVALID") from error
    return normalized


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--packet", type=Path, default=DEFAULT_PACKET)
    value.add_argument("--packet-schema", type=Path, default=DEFAULT_PACKET_SCHEMA)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        packet = load_json_object(args.packet.resolve(), "PACKET_UNAVAILABLE")
        packet_schema = load_json_object(args.packet_schema.resolve(), "PACKET_SCHEMA_UNAVAILABLE")
        validate_packet(packet, packet_schema)
        normalized = adapt_packet(packet)
    except AdapterError as error:
        print(
            json.dumps(
                {
                    "schema_version": NORMALIZED_SCHEMA_VERSION,
                    "status": "adapter_error",
                    "reason": error.code,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(normalized, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
