#!/usr/bin/env python3
"""Serve the single fixed branch-hours MCP tool for the capability probe."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


TOOL_NAME = "fetch_branch_counter_hours"
ALLOWED_INPUT = {"record_id": "branch-counter-hours-r1"}
TERMINAL_RESULT = {
    "record_id": "branch-counter-hours-r1",
    "day": "土曜日",
    "opens_at": "10:00",
    "closes_at": "17:00",
}


def emit(value: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def append_audit(value: dict[str, Any]) -> None:
    raw = os.environ.get("GENERAL_CHAT_BRANCH_TOOL_AUDIT")
    if not raw:
        raise RuntimeError("audit path unavailable")
    path = Path(raw)
    line = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(descriptor, line.encode("utf-8"))
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def handle(request: dict[str, Any]) -> dict[str, Any] | None:
    method = request.get("method")
    request_id = request.get("id")
    if method == "initialize":
        params = request.get("params")
        requested_version = params.get("protocolVersion") if isinstance(params, dict) else None
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": requested_version if isinstance(requested_version, str) else "2025-06-18",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "general-chat-branch-hours", "version": "1.0.0"},
            },
        }
    if method == "notifications/initialized":
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": TOOL_NAME,
                        "description": "固定済みの支店窓口営業時間レコードを取得する。",
                        "inputSchema": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": ["record_id"],
                            "properties": {"record_id": {"const": "branch-counter-hours-r1"}},
                        },
                    }
                ]
            },
        }
    if method == "tools/call":
        params = request.get("params")
        if not isinstance(params, dict):
            return error(request_id, -32602, "invalid params")
        name = params.get("name")
        arguments = params.get("arguments")
        if name != TOOL_NAME or arguments != ALLOWED_INPUT:
            return error(request_id, -32602, "tool name or input outside fixed contract")
        append_audit({"tool_id": TOOL_NAME, "input": arguments, "result": TERMINAL_RESULT})
        result_text = json.dumps(TERMINAL_RESULT, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [{"type": "text", "text": result_text}],
                "structuredContent": TERMINAL_RESULT,
                "isError": False,
            },
        }
    return error(request_id, -32601, "method not found") if request_id is not None else None


def main() -> int:
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if not isinstance(request, dict):
                raise ValueError("request is not an object")
            response = handle(request)
        except Exception as exc:  # keep protocol errors on stdout and details off the audit record
            response = error(None, -32603, type(exc).__name__)
        if response is not None:
            emit(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
