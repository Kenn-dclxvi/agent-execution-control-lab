#!/usr/bin/env python3
"""Collect final Codex token usage for one root agent and all descendants."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


class AllAgentUsageError(Exception):
    pass


TOKEN_ACCOUNTING = {
    "scope": "all_agents",
    "revision": "v1",
    "source": "codex_rollout_final_usage_by_workspace",
}
TOKEN_ACCOUNTING_V2 = {
    "scope": "all_agents",
    "revision": "v2",
    "source": "codex_rollout_final_usage_by_thread_bound_workspace",
}
USAGE_SCHEMA_VERSION = "the-caption-prompt.all-agent-usage/v1"


def parse_root_thread_id(jsonl: bytes) -> str:
    for raw_line in jsonl.splitlines():
        try:
            item = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        if item.get("type") == "thread.started":
            thread_id = item.get("thread_id")
            if isinstance(thread_id, str) and thread_id:
                return thread_id
    raise AllAgentUsageError("Codex JSONL did not contain thread.started")


def session_record(path: Path) -> dict[str, Any] | None:
    meta: dict[str, Any] | None = None
    final_usage: dict[str, int] | None = None
    try:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                item = json.loads(line)
                payload = item.get("payload")
                if not isinstance(payload, dict):
                    continue
                # A forked rollout can contain the parent's inherited
                # session_meta after its own metadata.  The first metadata
                # record identifies the rollout file itself.
                if item.get("type") == "session_meta" and meta is None:
                    meta = payload
                elif (
                    item.get("type") == "event_msg"
                    and payload.get("type") == "token_count"
                ):
                    raw_usage = ((payload.get("info") or {}).get("total_token_usage") or {})
                    if isinstance(raw_usage.get("total_tokens"), int):
                        final_usage = {
                            key: value
                            for key, value in raw_usage.items()
                            if isinstance(key, str)
                            and isinstance(value, int)
                            and not isinstance(value, bool)
                            and value >= 0
                        }
    except (OSError, json.JSONDecodeError):
        return None
    if meta is None:
        return None
    thread_id = meta.get("id") or meta.get("session_id")
    cwd = meta.get("cwd")
    if not isinstance(thread_id, str) or not thread_id or not isinstance(cwd, str) or not cwd:
        return None
    return {
        "rollout_file": str(path),
        "thread_id": thread_id,
        "parent_thread_id": meta.get("parent_thread_id"),
        "source": meta.get("source"),
        "cwd": cwd,
        "usage": final_usage,
    }


def session_files(root: Path, modified_since: float | None = None) -> Iterable[Path]:
    if not root.is_dir():
        raise AllAgentUsageError(f"Codex session root is not a directory: {root}")
    for path in root.rglob("*.jsonl"):
        if modified_since is not None:
            try:
                if path.stat().st_mtime < modified_since:
                    continue
            except OSError:
                continue
        yield path


def index_sessions(
    root: Path,
    modified_since: float | None = None,
) -> dict[str, list[dict[str, Any]]]:
    indexed: dict[str, list[dict[str, Any]]] = {}
    for path in session_files(root, modified_since):
        record = session_record(path)
        if record is not None:
            indexed.setdefault(record["cwd"], []).append(record)
    return indexed


def root_and_descendants(
    records: list[dict[str, Any]],
    root_thread_id: str,
) -> list[dict[str, Any]]:
    by_thread: dict[str, dict[str, Any]] = {}
    for record in records:
        thread_id = record["thread_id"]
        if thread_id in by_thread:
            raise AllAgentUsageError(f"duplicate Codex session for thread: {thread_id}")
        by_thread[thread_id] = record
    if root_thread_id not in by_thread:
        raise AllAgentUsageError(f"root Codex session was not found: {root_thread_id}")
    selected = {root_thread_id}
    changed = True
    while changed:
        changed = False
        for thread_id, record in by_thread.items():
            if thread_id not in selected and record.get("parent_thread_id") in selected:
                selected.add(thread_id)
                changed = True
    return [by_thread[thread_id] for thread_id in sorted(selected)]


def infer_root_thread_id(records: list[dict[str, Any]], root_total_tokens: int) -> str:
    thread_ids = {record["thread_id"] for record in records}
    candidates = [
        record["thread_id"]
        for record in records
        if record.get("parent_thread_id") not in thread_ids
        and isinstance(record.get("usage"), dict)
        and record["usage"].get("total_tokens") == root_total_tokens
    ]
    if len(candidates) != 1:
        raise AllAgentUsageError(
            "could not infer one root Codex session from workspace and root total_tokens"
        )
    return candidates[0]


def summarize_workspace_usage(
    records: list[dict[str, Any]],
    root_total_tokens: int,
    root_thread_id: str | None = None,
) -> dict[str, Any]:
    if not records:
        raise AllAgentUsageError("no Codex sessions found for evaluation workspace")
    selected_root = root_thread_id or infer_root_thread_id(records, root_total_tokens)
    selected = root_and_descendants(records, selected_root)
    incomplete = [record["thread_id"] for record in selected if not isinstance(record.get("usage"), dict)]
    if incomplete:
        raise AllAgentUsageError(
            "Codex session lacks final token usage: " + ", ".join(incomplete)
        )
    root = next(record for record in selected if record["thread_id"] == selected_root)
    if root["usage"]["total_tokens"] != root_total_tokens:
        raise AllAgentUsageError("root Codex session usage differs from exec JSONL usage")
    all_agent_total = sum(record["usage"]["total_tokens"] for record in selected)
    return {
        "schema_version": USAGE_SCHEMA_VERSION,
        "token_accounting": TOKEN_ACCOUNTING,
        "root_thread_id": selected_root,
        "root_total_tokens": root_total_tokens,
        "all_agent_total_tokens": all_agent_total,
        "child_and_additional_tokens": all_agent_total - root_total_tokens,
        "session_count": len(selected),
        "sessions": [
            {
                key: record[key]
                for key in (
                    "rollout_file",
                    "thread_id",
                    "parent_thread_id",
                    "source",
                    "usage",
                )
            }
            for record in selected
        ],
    }


def summarize_workspace_usage_by_root(
    records: list[dict[str, Any]],
    root_thread_id: str,
) -> dict[str, Any]:
    if not records:
        raise AllAgentUsageError("no Codex sessions found for evaluation workspace")
    selected = root_and_descendants(records, root_thread_id)
    incomplete = [record["thread_id"] for record in selected if not isinstance(record.get("usage"), dict)]
    if incomplete:
        raise AllAgentUsageError("Codex session lacks final token usage: " + ", ".join(incomplete))
    root = next(record for record in selected if record["thread_id"] == root_thread_id)
    root_total = root["usage"].get("total_tokens")
    if not isinstance(root_total, int):
        raise AllAgentUsageError("persisted root session lacks primary total_tokens")
    all_agent_total = sum(record["usage"]["total_tokens"] for record in selected)
    return {
        "schema_version": USAGE_SCHEMA_VERSION,
        "token_accounting": TOKEN_ACCOUNTING_V2,
        "root_thread_id": root_thread_id,
        "root_total_tokens": root_total,
        "all_agent_total_tokens": all_agent_total,
        "child_and_additional_tokens": all_agent_total - root_total,
        "session_count": len(selected),
        "sessions": [
            {
                key: record[key]
                for key in ("rollout_file", "thread_id", "parent_thread_id", "source", "usage")
            }
            for record in selected
        ],
    }


def collect_workspace_usage(
    session_root: Path,
    workspace: Path,
    root_thread_id: str,
    root_total_tokens: int,
    modified_since: float | None = None,
) -> dict[str, Any]:
    indexed = index_sessions(session_root, modified_since)
    records = indexed.get(str(workspace.resolve()), [])
    return summarize_workspace_usage(records, root_total_tokens, root_thread_id)


def collect_workspace_usage_by_root(
    session_root: Path,
    workspace: Path,
    root_thread_id: str,
    modified_since: float | None = None,
) -> dict[str, Any]:
    indexed = index_sessions(session_root, modified_since)
    records = indexed.get(str(workspace.resolve()), [])
    return summarize_workspace_usage_by_root(records, root_thread_id)
