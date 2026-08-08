#!/usr/bin/env python3
"""Record a content-free Claude Code lifecycle event for qualification."""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path


def _fixture_tool_command(value: object) -> bool:
    if not isinstance(value, dict):
        return False
    command = value.get("command")
    if not isinstance(command, str):
        return False
    stripped = command.strip()
    return stripped == "./fixture-tool" or stripped.startswith("./fixture-tool ")


def sanitize_event(value: object) -> dict:
    if not isinstance(value, dict):
        raise ValueError("hook input must be an object")
    event = value.get("hook_event_name")
    if event not in {
        "SubagentStart",
        "SubagentStop",
        "PostToolUse",
        "PostToolUseFailure",
        "PostToolBatch",
        "PermissionDenied",
    }:
        raise ValueError("unsupported hook event")
    record: dict[str, object] = {
        "event": event,
        "timestamp_ns": time.time_ns(),
    }
    for key in ("agent_id", "agent_type"):
        if isinstance(value.get(key), str):
            record[key] = value[key]
    if event in {"PostToolUse", "PostToolUseFailure", "PermissionDenied"}:
        if isinstance(value.get("tool_name"), str):
            record["tool_name"] = value["tool_name"]
        if isinstance(value.get("tool_use_id"), str):
            record["tool_use_id"] = value["tool_use_id"]
        record["fixture_tool_command"] = _fixture_tool_command(value.get("tool_input"))
    elif event == "PostToolBatch":
        calls = value.get("tool_calls")
        if not isinstance(calls, list):
            calls = []
        record["tool_names"] = [
            call.get("tool_name", "unknown")
            if isinstance(call, dict) and isinstance(call.get("tool_name"), str)
            else "unknown"
            for call in calls
        ]
        record["tool_use_ids"] = [
            call["tool_use_id"]
            for call in calls
            if isinstance(call, dict) and isinstance(call.get("tool_use_id"), str)
        ]
    return record


def append_event(path: Path, record: dict) -> None:
    payload = (
        json.dumps(record, ensure_ascii=True, separators=(",", ":"), sort_keys=True)
        + "\n"
    ).encode("utf-8")
    if len(payload) > 4096:
        raise ValueError("sanitized hook event exceeds atomic append limit")
    descriptor = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
    try:
        if os.write(descriptor, payload) != len(payload):
            raise OSError("short hook event write")
    finally:
        os.close(descriptor)


def main() -> int:
    if len(sys.argv) != 2:
        return 2
    try:
        append_event(Path(sys.argv[1]), sanitize_event(json.load(sys.stdin)))
    except (json.JSONDecodeError, OSError, ValueError):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
