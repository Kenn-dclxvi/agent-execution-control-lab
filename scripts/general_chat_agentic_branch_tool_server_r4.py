#!/usr/bin/env python3
"""Serve and audit the fixed MCP tool for the isolated r4 transport probe."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


TOOL_NAME = "fetch_branch_counter_hours"
ALLOWED_INPUT = {"record_id": "branch-counter-hours-r1"}
TERMINAL_RESULT = {"record_id": "branch-counter-hours-r1", "day": "土曜日", "opens_at": "10:00", "closes_at": "17:00"}


def append_audit(event: str, **fields: Any) -> None:
    raw = os.environ.get("GENERAL_CHAT_BRANCH_TOOL_AUDIT")
    if not raw:
        raise RuntimeError("audit path unavailable")
    value = {"event": event, **fields}
    descriptor = os.open(Path(raw), os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(descriptor, json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n")
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def emit(value: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def handle(request: dict[str, Any]) -> dict[str, Any] | None:
    method = request.get("method")
    request_id = request.get("id")
    if method == "initialize":
        params = request.get("params")
        requested = params.get("protocolVersion") if isinstance(params, dict) else None
        version = requested if isinstance(requested, str) else "2025-06-18"
        append_audit("initialize", protocol_version=version)
        return {"jsonrpc": "2.0", "id": request_id, "result": {"protocolVersion": version, "capabilities": {"tools": {}}, "serverInfo": {"name": "general-chat-branch-hours-r4", "version": "1.0.0"}}}
    if method == "notifications/initialized":
        append_audit("initialized")
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        append_audit("tools_list")
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": [{"name": TOOL_NAME, "description": "固定済みの支店窓口営業時間レコードを取得する。", "inputSchema": {"type": "object", "additionalProperties": False, "required": ["record_id"], "properties": {"record_id": {"const": "branch-counter-hours-r1"}}}}]}}
    if method == "tools/call":
        params = request.get("params")
        if not isinstance(params, dict) or params.get("name") != TOOL_NAME or params.get("arguments") != ALLOWED_INPUT:
            append_audit("rejected_call")
            return error(request_id, -32602, "tool name or input outside fixed contract")
        append_audit("tools_call", tool_id=TOOL_NAME, input=ALLOWED_INPUT, result=TERMINAL_RESULT)
        text = json.dumps(TERMINAL_RESULT, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return {"jsonrpc": "2.0", "id": request_id, "result": {"content": [{"type": "text", "text": text}], "structuredContent": TERMINAL_RESULT, "isError": False}}
    return error(request_id, -32601, "method not found") if request_id is not None else None


def main() -> int:
    for line in sys.stdin:
        try:
            request = json.loads(line)
            if not isinstance(request, dict):
                raise ValueError
            response = handle(request)
        except Exception as exc:
            response = error(None, -32603, type(exc).__name__)
        if response is not None:
            emit(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
