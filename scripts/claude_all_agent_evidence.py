#!/usr/bin/env python3
"""Collect all-agent usage and command evidence from Claude Code transcripts.

The collector reads only harness-written records: the stream-json stdout of one
``claude -p`` invocation, the root session transcript and every subagent
transcript stored under the same session.  It never estimates missing usage.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

try:
    from usage_components import claude_components
except ModuleNotFoundError:  # Imported as scripts.claude_all_agent_evidence in tests.
    from scripts.usage_components import claude_components


class ClaudeEvidenceError(Exception):
    pass


TOKEN_ACCOUNTING = {
    "scope": "all_agents",
    "revision": "claude-v1",
    "source": "claude_code_transcript_request_usage_dedup_by_message",
}
USAGE_SCHEMA_VERSION = "the-caption-prompt.claude-all-agent-usage/v1"
COMMAND_EVIDENCE_SCHEMA_VERSION = "the-caption-prompt.claude-all-agent-command-evidence/v1"
USAGE_FIELDS = (
    "input_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
    "output_tokens",
)
MODEL_USAGE_FIELDS = {
    "input_tokens": "inputTokens",
    "cache_creation_input_tokens": "cacheCreationInputTokens",
    "cache_read_input_tokens": "cacheReadInputTokens",
    "output_tokens": "outputTokens",
}
SYNTHETIC_MODEL = "<synthetic>"
EXIT_CODE_PATTERN = re.compile(r"\AExit code (-?\d+)(?:\n|\Z)")
NOTIFICATION_PATTERN = re.compile(r"<task-notification>(.*?)</task-notification>", re.S)


def jsonl_items(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ClaudeEvidenceError(f"invalid JSONL at {path}:{number}") from exc
            if isinstance(item, dict):
                yield item


def parse_stream(stdout: bytes) -> dict[str, Any]:
    """Return the init and terminal result events of one stream-json invocation."""
    init: dict[str, Any] | None = None
    results: list[dict[str, Any]] = []
    notifications: list[dict[str, Any]] = []
    for raw_line in stdout.splitlines():
        if not raw_line.strip():
            continue
        try:
            item = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise ClaudeEvidenceError("stdout is not stream-json") from exc
        if not isinstance(item, dict):
            continue
        if item.get("type") == "system" and item.get("subtype") == "init" and init is None:
            init = item
        elif item.get("type") == "result":
            results.append(item)
        elif item.get("type") == "system" and item.get("subtype") == "task_notification":
            notifications.append(item)
    if init is None:
        raise ClaudeEvidenceError("stream-json has no init event")
    if not results:
        raise ClaudeEvidenceError("stream-json has no result event")
    # A background task that finishes after the model ends its turn resumes the
    # session and emits another result.  modelUsage in the last result is
    # cumulative for the whole session, so the last result is terminal.
    result = results[-1]
    session_id = init.get("session_id")
    if not isinstance(session_id, str) or not session_id:
        raise ClaudeEvidenceError("init event has no session_id")
    if result.get("session_id") != session_id:
        raise ClaudeEvidenceError("result session_id differs from init")
    if any(item.get("session_id") != session_id for item in results):
        raise ClaudeEvidenceError("result session_id differs from init")
    return {
        "init": init,
        "result": result,
        "session_id": session_id,
        "result_count": len(results),
        "task_notifications": notifications,
    }


def locate_session(config_dir: Path, session_id: str) -> tuple[Path, list[Path]]:
    matches = sorted((config_dir / "projects").glob(f"*/{session_id}.jsonl"))
    if len(matches) != 1:
        raise ClaudeEvidenceError(
            f"expected one root transcript for session {session_id}, found {len(matches)}"
        )
    root = matches[0]
    subagent_dir = root.parent / session_id / "subagents"
    subagents = sorted(subagent_dir.glob("agent-*.jsonl")) if subagent_dir.is_dir() else []
    return root, subagents


def text_of(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str):
                parts.append(block["text"])
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts)
    return ""


def transcript_messages(path: Path) -> dict[str, dict[str, Any]]:
    """Return the final usage of each assistant API response in one transcript."""
    messages: dict[str, dict[str, Any]] = {}
    for item in jsonl_items(path):
        if item.get("type") != "assistant":
            continue
        message = item.get("message")
        if not isinstance(message, dict):
            continue
        model = message.get("model")
        if model == SYNTHETIC_MODEL:
            continue
        message_id = message.get("id")
        usage = message.get("usage")
        if not isinstance(message_id, str) or not message_id or not isinstance(usage, dict):
            raise ClaudeEvidenceError(f"assistant record without message id or usage: {path}")
        if not isinstance(model, str) or not model:
            raise ClaudeEvidenceError(f"assistant record without model: {path}")
        values: dict[str, int] = {}
        for field in USAGE_FIELDS:
            value = usage.get(field, 0)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ClaudeEvidenceError(f"invalid usage field {field}: {path}")
            values[field] = value
        previous = messages.get(message_id)
        if previous is not None and previous["model"] != model:
            raise ClaudeEvidenceError(f"message id reused across models: {message_id}")
        split = None
        cache_creation = usage.get("cache_creation")
        if isinstance(cache_creation, dict):
            split = {
                key: cache_creation.get(key, 0)
                for key in ("ephemeral_1h_input_tokens", "ephemeral_5m_input_tokens")
            }
            if not all(isinstance(value, int) and not isinstance(value, bool) and value >= 0 for value in split.values()):
                raise ClaudeEvidenceError(f"invalid cache write split: {path}")
        # Streaming writes one record per content block; the last record of a
        # response carries the final usage of that response.
        messages[message_id] = {
            "model": model,
            "request_id": item.get("requestId"),
            "usage": values,
            "cache_creation_split": split,
        }
    return messages


def subagent_identity(path: Path, session_id: str) -> dict[str, Any]:
    agent_id = path.stem.removeprefix("agent-")
    meta_path = path.with_suffix(".meta.json")
    meta: dict[str, Any] = {}
    if meta_path.is_file():
        loaded = json.loads(meta_path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            meta = loaded
    for item in jsonl_items(path):
        observed_session = item.get("sessionId")
        if observed_session is not None and observed_session != session_id:
            raise ClaudeEvidenceError(f"subagent transcript belongs to another session: {path}")
        observed_agent = item.get("agentId")
        if observed_agent is not None and observed_agent != agent_id:
            raise ClaudeEvidenceError(f"subagent transcript agent id mismatch: {path}")
    return {
        "agent_id": agent_id,
        "agent_type": meta.get("agentType"),
        "spawn_depth": meta.get("spawnDepth"),
        "tool_use_id": meta.get("toolUseId"),
        "transcript": str(path),
        "transcript_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def referenced_agent_ids(paths: list[Path]) -> set[str]:
    referenced: set[str] = set()
    for path in paths:
        for item in jsonl_items(path):
            result = item.get("toolUseResult")
            if isinstance(result, dict) and isinstance(result.get("agentId"), str):
                referenced.add(result["agentId"])
    return referenced


def collect_usage(config_dir: Path, stream: dict[str, Any]) -> dict[str, Any]:
    session_id = stream["session_id"]
    result = stream["result"]
    root, subagents = locate_session(config_dir, session_id)
    sessions = [
        {
            "actor": "root",
            "agent_id": None,
            "transcript": str(root),
            "transcript_sha256": hashlib.sha256(root.read_bytes()).hexdigest(),
        }
    ]
    sessions.extend({"actor": "subagent", **subagent_identity(path, session_id)} for path in subagents)
    observed_agents = {item["agent_id"] for item in sessions if item["agent_id"] is not None}
    missing_agents = sorted(referenced_agent_ids([root, *subagents]) - observed_agents)
    if missing_agents:
        raise ClaudeEvidenceError(f"subagent transcript missing: {missing_agents}")

    merged: dict[str, dict[str, Any]] = {}
    per_session: list[dict[str, Any]] = []
    for session, path in zip(sessions, [root, *subagents]):
        messages = transcript_messages(path)
        session_totals = {field: 0 for field in USAGE_FIELDS}
        for message_id, record in messages.items():
            if message_id in merged:
                if merged[message_id]["usage"] != record["usage"]:
                    raise ClaudeEvidenceError(f"message usage differs across transcripts: {message_id}")
                continue
            merged[message_id] = record
            for field in USAGE_FIELDS:
                session_totals[field] += record["usage"][field]
        per_session.append(
            {
                "actor": session["actor"],
                "agent_id": session["agent_id"],
                "response_count": len(messages),
                "total_tokens": sum(session_totals.values()),
                **session_totals,
            }
        )

    by_model: dict[str, dict[str, int]] = {}
    for record in merged.values():
        totals = by_model.setdefault(record["model"], {field: 0 for field in USAGE_FIELDS})
        for field in USAGE_FIELDS:
            totals[field] += record["usage"][field]

    model_usage = result.get("modelUsage")
    if not isinstance(model_usage, dict):
        raise ClaudeEvidenceError("terminal result has no modelUsage")
    reconciliation: list[dict[str, Any]] = []
    for model, totals in sorted(by_model.items()):
        reported = model_usage.get(model)
        if not isinstance(reported, dict):
            raise ClaudeEvidenceError(f"transcript model absent from modelUsage: {model}")
        reported_values = {field: reported.get(key) for field, key in MODEL_USAGE_FIELDS.items()}
        if reported_values != totals:
            raise ClaudeEvidenceError(
                f"transcript usage differs from modelUsage for {model}: "
                f"{json.dumps(totals, sort_keys=True)} != {json.dumps(reported_values, sort_keys=True)}"
            )
        reconciliation.append({"model": model, "status": "equal", **totals})
    auxiliary: list[dict[str, Any]] = []
    for model, reported in sorted(model_usage.items()):
        if model in by_model:
            continue
        if not isinstance(reported, dict):
            raise ClaudeEvidenceError(f"invalid modelUsage entry: {model}")
        values = {field: reported.get(key) for field, key in MODEL_USAGE_FIELDS.items()}
        if not all(isinstance(value, int) and value >= 0 for value in values.values()):
            raise ClaudeEvidenceError(f"invalid auxiliary modelUsage entry: {model}")
        auxiliary.append({"model": model, "total_tokens": sum(values.values()), **values})

    all_agent_total = sum(sum(totals.values()) for totals in by_model.values())
    root_usage = result.get("usage") if isinstance(result.get("usage"), dict) else {}
    return {
        "schema_version": USAGE_SCHEMA_VERSION,
        "token_accounting": TOKEN_ACCOUNTING,
        "session_id": session_id,
        "root_transcript": str(root),
        "sessions": sessions,
        "per_session": per_session,
        "response_count": len(merged),
        "by_model": [{"model": model, "total_tokens": sum(t.values()), **t} for model, t in sorted(by_model.items())],
        "model_usage_reconciliation": reconciliation,
        "auxiliary_model_usage_excluded_from_kpi": auxiliary,
        "root_terminal_usage_not_all_agent": {
            field: root_usage.get(field) for field in USAGE_FIELDS
        },
        "all_agent_total_tokens": all_agent_total,
        "usage_components": claude_components(merged.values()),
    }


def notification_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for key, value in re.findall(r"<([a-z_-]+)>(.*?)</\1>", text, re.S):
        fields[key] = value.strip()
    return fields


def exit_code_from_summary(summary: Any) -> int | None:
    if not isinstance(summary, str):
        return None
    match = re.search(r"(?:\(exit code|failed with exit code) (-?\d+)\)?\s*\Z", summary)
    return int(match.group(1)) if match else None


def notification_completion(fields: dict[str, Any], source: str) -> tuple[str, dict[str, Any]] | None:
    tool_use_id = fields.get("tool-use-id") or fields.get("tool_use_id")
    if not isinstance(tool_use_id, str) or not tool_use_id:
        return None
    return tool_use_id, {
        "task_id": fields.get("task-id") or fields.get("task_id"),
        "status": fields.get("status"),
        "exit_code": exit_code_from_summary(fields.get("summary")),
        "source": source,
    }


def background_completions(path: Path, stream_notifications: list[dict[str, Any]] | None = None) -> dict[str, dict[str, Any]]:
    """Map background Bash tool_use IDs to harness-written completion records.

    Accepted sources are only harness records: stream-json ``system /
    task_notification`` events, transcript ``queue-operation`` enqueue records
    and ``queued_command`` attachments whose origin is ``task-notification``.
    Text written by the model is never read.
    """
    completions: dict[str, dict[str, Any]] = {}

    def add(found: tuple[str, dict[str, Any]] | None) -> None:
        if found is not None:
            completions.setdefault(found[0], found[1])

    for event in stream_notifications or []:
        add(notification_completion(event, "stream_task_notification"))
    for item in jsonl_items(path):
        bodies: list[tuple[str, str]] = []
        attachment = item.get("attachment")
        if item.get("type") == "attachment" and isinstance(attachment, dict):
            origin = attachment.get("origin")
            if (
                attachment.get("type") == "queued_command"
                and attachment.get("commandMode") == "task-notification"
                and isinstance(origin, dict)
                and origin.get("kind") == "task-notification"
                and isinstance(attachment.get("prompt"), str)
            ):
                bodies.append((attachment["prompt"], "task_notification_attachment"))
        if item.get("type") == "queue-operation" and item.get("operation") == "enqueue" and isinstance(item.get("content"), str):
            bodies.append((item["content"], "queue_operation_enqueue"))
        for text, source in bodies:
            for body in NOTIFICATION_PATTERN.findall(text):
                add(notification_completion(notification_fields(body), source))
    return completions


def transcript_commands(
    path: Path,
    actor: str,
    agent_id: str | None,
    stream_notifications: list[dict[str, Any]] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    calls: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    results: dict[str, dict[str, Any]] = {}
    for item in jsonl_items(path):
        message = item.get("message")
        if not isinstance(message, dict) or not isinstance(message.get("content"), list):
            continue
        for block in message["content"]:
            if not isinstance(block, dict):
                continue
            if item.get("type") == "assistant" and block.get("type") == "tool_use" and block.get("name") == "Bash":
                tool_input = block.get("input") if isinstance(block.get("input"), dict) else {}
                tool_use_id = block.get("id")
                if isinstance(tool_use_id, str) and tool_use_id not in calls:
                    calls[tool_use_id] = {
                        "command": tool_input.get("command"),
                        "run_in_background": bool(tool_input.get("run_in_background")),
                    }
                    order.append(tool_use_id)
            elif item.get("type") == "user" and block.get("type") == "tool_result":
                tool_use_id = block.get("tool_use_id")
                if isinstance(tool_use_id, str):
                    results[tool_use_id] = {
                        "is_error": block.get("is_error") is True,
                        "text": text_of(block.get("content")),
                        "tool_use_result": item.get("toolUseResult"),
                    }
    completions = background_completions(path, stream_notifications)
    attempted: list[dict[str, Any]] = []
    successful: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    for tool_use_id in order:
        call = calls[tool_use_id]
        command = call["command"]
        base = {
            "actor": actor,
            "agent_id": agent_id,
            "tool_use_id": tool_use_id,
            "source": "claude_transcript_bash",
            "command": command,
        }
        if not isinstance(command, str) or not command:
            violations.append({**base, "reason_code": "bash_call_without_command"})
            continue
        attempted.append(base)
        result = results.get(tool_use_id)
        if result is None:
            violations.append({**base, "reason_code": "missing_tool_result"})
            continue
        exit_code: int | None = None
        binding = "foreground_tool_result"
        if call["run_in_background"] and not result["is_error"]:
            binding = "background_completion"
            completion = completions.get(tool_use_id)
            if completion is not None and completion["exit_code"] is not None:
                exit_code = completion["exit_code"]
        elif result["is_error"]:
            match = EXIT_CODE_PATTERN.match(result["text"])
            if match:
                exit_code = int(match.group(1))
        else:
            interrupted = isinstance(result["tool_use_result"], dict) and result["tool_use_result"].get("interrupted") is True
            exit_code = None if interrupted else 0
        if exit_code is None:
            violations.append({**base, "binding": binding, "reason_code": "missing_machine_bound_exit_code"})
            continue
        completed = {**base, "binding": binding, "exit_code": exit_code}
        (successful if exit_code == 0 else failed).append(completed)
    return {
        "attempted_commands": attempted,
        "successful_commands": successful,
        "failed_commands": failed,
        "protocol_violations": violations,
    }


def collect_commands(
    usage: dict[str, Any], run_id: str, stream_notifications: list[dict[str, Any]] | None = None
) -> dict[str, Any]:
    evidence: dict[str, list[dict[str, Any]]] = {
        "attempted_commands": [],
        "successful_commands": [],
        "failed_commands": [],
        "protocol_violations": [],
    }
    for session in usage["sessions"]:
        part = transcript_commands(
            Path(session["transcript"]), session["actor"], session["agent_id"], stream_notifications
        )
        for key in evidence:
            evidence[key].extend(part[key])
    return {
        "schema_version": COMMAND_EVIDENCE_SCHEMA_VERSION,
        "run_id": run_id,
        "session_id": usage["session_id"],
        "session_count": len(usage["sessions"]),
        "attempted_command_count": len(evidence["attempted_commands"]),
        "attempted_commands": evidence["attempted_commands"],
        "successful_command_count": len(evidence["successful_commands"]),
        "successful_commands": evidence["successful_commands"],
        "failed_command_count": len(evidence["failed_commands"]),
        "failed_commands": evidence["failed_commands"],
        "protocol_violation_count": len(evidence["protocol_violations"]),
        "protocol_violations": evidence["protocol_violations"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stdout", type=Path, required=True)
    parser.add_argument("--config-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args()
    stream = parse_stream(args.stdout.read_bytes())
    usage = collect_usage(args.config_dir, stream)
    usage["run_id"] = args.run_id
    commands = collect_commands(usage, args.run_id, stream["task_notifications"])
    print(json.dumps({"usage": usage, "commands": commands}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
