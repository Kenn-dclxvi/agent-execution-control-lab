#!/usr/bin/env python3
"""Record content-free lifecycle events and recognize nested fixture-tool calls."""

from __future__ import annotations

import re

import pr_review_subagent_hook as base


def _fixture_tool_command(value: object) -> bool:
    if not isinstance(value, dict) or not isinstance(value.get("command"), str):
        return False
    return re.search(r"(?<![A-Za-z0-9_./-])\./fixture-tool(?:\s|$)", value["command"]) is not None


base._fixture_tool_command = _fixture_tool_command


if __name__ == "__main__":
    raise SystemExit(base.main())
