#!/usr/bin/env python3
"""Record content-free lifecycle events with fixture operation identities."""

from __future__ import annotations

import re
import json
import sys
from pathlib import Path

import pr_review_subagent_hook as base


OPERATIONS = (
    "workflow",
    "eligibility",
    "metadata",
    "changed-paths",
    "diff",
    "rules",
    "files",
    "file",
    "list-files",
    "contract",
)
_OPERATION_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_./-])\./fixture-tool\s+("
    + "|".join(re.escape(item) for item in OPERATIONS)
    + r")(?:\s|$)"
)
_base_sanitize_event = base.sanitize_event


def _fixture_operations(value: object) -> list[str]:
    if not isinstance(value, dict) or not isinstance(value.get("command"), str):
        return []
    return _OPERATION_PATTERN.findall(value["command"])


def sanitize_event(value: object) -> dict:
    record = _base_sanitize_event(value)
    event = record["event"]
    if event in {"PostToolUse", "PostToolUseFailure", "PermissionDenied"}:
        operations = _fixture_operations(value.get("tool_input") if isinstance(value, dict) else None)
        if operations:
            record["fixture_tool_operations"] = operations
            record["outcome"] = {
                "PostToolUse": "success",
                "PostToolUseFailure": "failure",
                "PermissionDenied": "denied",
            }[event]
    return record


def main() -> int:
    if len(sys.argv) != 2:
        return 2
    try:
        base.append_event(Path(sys.argv[1]), sanitize_event(json.load(sys.stdin)))
    except (json.JSONDecodeError, OSError, ValueError):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
