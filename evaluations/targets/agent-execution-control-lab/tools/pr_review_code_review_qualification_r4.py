#!/usr/bin/env python3
"""Artifact-transfer recovery for Claude Code Core PRR-C01/r4 repetition 1."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import pr_review_code_review_qualification as base


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
PROFILE_ID = "pr-review-claude-code-core-c01-r4-qualification-n2-r4"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
WORKFLOW_REVISION = "pr-review-qualify-claude-code-core-r4"


def _bind_revision() -> None:
    base.PROFILE_ID = PROFILE_ID
    base.PROFILE_PATH = PROFILE_PATH
    base.PREFLIGHT_PATH = PREFLIGHT_PATH
    base.WORKFLOW_REVISION = WORKFLOW_REVISION
    base.WORKFLOW_PATH = (
        base.REPOSITORY_ROOT
        / ".github/workflows/pr-review-qualify-claude-code-core-r4.yml"
    )


def validate_preflight(repetition: int, prior_admission: Path | None = None):
    _bind_revision()
    return base.validate_preflight(repetition, prior_admission)


def _hook_settings() -> dict:
    recorder = {
        "type": "command",
        "command": "python3",
        "args": [
            "${CLAUDE_PROJECT_DIR}/pr_review_subagent_hook.py",
            "${CLAUDE_PROJECT_DIR}/.claude/pr-review-subagent-events.jsonl",
        ],
    }
    matched = lambda matcher: [{"matcher": matcher, "hooks": [recorder]}]
    return {
        "permissions": {
            "allow": ["Agent", "Bash(./fixture-tool:*)"],
            "deny": [
                "Read",
                "Glob",
                "Grep",
                "Write",
                "Edit",
                "NotebookEdit",
                "WebFetch",
                "WebSearch",
                "mcp__github__*",
            ],
        },
        "hooks": {
            "SubagentStart": matched(".*"),
            "SubagentStop": matched(".*"),
            "PostToolUse": matched("Bash"),
            "PostToolUseFailure": matched("Bash"),
            "PermissionDenied": matched(".*"),
            "PostToolBatch": [{"hooks": [recorder]}],
        },
    }


def prepare_input(repetition: int, output_dir: Path) -> dict:
    _bind_revision()
    metadata = base.prepare_input(repetition, output_dir)
    shutil.copyfile(Path(__file__), output_dir / Path(__file__).name)
    shutil.copyfile(
        INSTANCE_ROOT / "tools/pr_review_qualification.py",
        output_dir / "pr_review_qualification.py",
    )
    shutil.copyfile(
        INSTANCE_ROOT / "tools/pr_review_subagent_hook.py",
        output_dir / "pr_review_subagent_hook.py",
    )
    settings = output_dir / "claude-project-settings.json"
    settings.write_text(
        json.dumps(_hook_settings(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def _read_hook_events(path: Path | None) -> list[dict]:
    if path is None or not path.is_file():
        return []
    events = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and isinstance(value.get("timestamp_ns"), int):
            events.append(value)
    return sorted(events, key=lambda item: item["timestamp_ns"])


def _instrumented_trace(execution_file: Path | None, hook_file: Path | None) -> dict:
    trace = base._workflow_trace(execution_file)
    events = _read_hook_events(hook_file)
    starts = [event for event in events if event.get("event") == "SubagentStart"]
    stops = [event for event in events if event.get("event") == "SubagentStop"]
    stop_time = {
        event.get("agent_id"): event["timestamp_ns"]
        for event in stops
        if isinstance(event.get("agent_id"), str)
    }
    prerequisite_ids = [event.get("agent_id") for event in starts[:3]]
    prerequisite_sequence = (
        len(prerequisite_ids) == 3
        and all(isinstance(agent_id, str) and agent_id in stop_time for agent_id in prerequisite_ids)
        and stop_time[prerequisite_ids[0]] < starts[1]["timestamp_ns"]
        and stop_time[prerequisite_ids[1]] < starts[2]["timestamp_ns"]
    )
    reviewer_events = starts[3:7]
    reviewer_ids = [event.get("agent_id") for event in reviewer_events]
    reviewer_overlap = (
        len(reviewer_ids) == 4
        and all(isinstance(agent_id, str) and agent_id in stop_time for agent_id in reviewer_ids)
        and max(event["timestamp_ns"] for event in reviewer_events)
        < min(stop_time[agent_id] for agent_id in reviewer_ids)
    )
    reviewer_batch_end = (
        max(stop_time[agent_id] for agent_id in reviewer_ids)
        if len(reviewer_ids) == 4
        and all(isinstance(agent_id, str) and agent_id in stop_time for agent_id in reviewer_ids)
        else None
    )
    first_validator_start = starts[7]["timestamp_ns"] if len(starts) > 7 else None
    agent_batches = [
        event
        for event in events
        if event.get("event") == "PostToolBatch"
        and event.get("tool_names") == ["Agent", "Agent", "Agent", "Agent"]
        and reviewer_batch_end is not None
        and event["timestamp_ns"] >= reviewer_batch_end
        and (
            first_validator_start is None
            or event["timestamp_ns"] < first_validator_start
        )
    ]
    reviewer_batch = bool(agent_batches)
    successful_fixture_agents = {
        event.get("agent_id")
        for event in events
        if event.get("event") == "PostToolUse"
        and event.get("tool_name") == "Bash"
        and event.get("fixture_tool_command") is True
        and isinstance(event.get("agent_id"), str)
    }
    reviewer_fixture_access = (
        len(reviewer_ids) == 4
        and all(agent_id in successful_fixture_agents for agent_id in reviewer_ids)
    )
    fixture_denials = sum(
        1
        for event in events
        if event.get("event") == "PermissionDenied"
        and event.get("fixture_tool_command") is True
    )
    trace.update(
        hook_event_count=len(events),
        subagent_start_count=len(starts),
        subagent_stop_count=len(stops),
        prerequisite_sequence_observed=prerequisite_sequence,
        reviewer_agent_batch_observed=reviewer_batch,
        reviewer_lifecycle_overlap_observed=reviewer_overlap,
        reviewer_fixture_access_observed=reviewer_fixture_access,
        fixture_tool_permission_denials=fixture_denials,
        permission_denials_by_tool={
            tool: sum(
                1
                for event in events
                if event.get("event") == "PermissionDenied"
                and event.get("tool_name") == tool
            )
            for tool in sorted(
                {
                    event["tool_name"]
                    for event in events
                    if event.get("event") == "PermissionDenied"
                    and isinstance(event.get("tool_name"), str)
                }
            )
        },
    )
    trace["parallel_reviewers_2_sonnet_2_opus"] = bool(
        trace.get("parallel_reviewers_2_sonnet_2_opus")
        and reviewer_batch
        and reviewer_overlap
    )
    trace["complete"] = bool(
        trace.get("eligibility_haiku")
        and trace.get("authority_haiku")
        and trace.get("summary_sonnet")
        and trace.get("parallel_reviewers_2_sonnet_2_opus")
        and trace.get("separate_validation_agents")
        and trace.get("subagent_usage_observed")
        and prerequisite_sequence
        and reviewer_fixture_access
        and fixture_denials == 0
    )
    return trace


def collect_review(*args, **kwargs):
    _bind_revision()
    hook_file = kwargs.pop("hook_file", None)
    metadata = base.collect_review(*args, **kwargs)
    execution_file = args[2] if len(args) > 2 else kwargs.get("execution_file")
    metadata["workflow_trace"] = _instrumented_trace(execution_file, hook_file)
    trace = metadata["workflow_trace"]
    if trace["subagent_usage_observed"]:
        metadata["runtime"]["input_tokens"] = trace["all_agent_input_tokens"]
        metadata["runtime"]["output_tokens"] = trace["all_agent_output_tokens"]
    output_dir = args[-1] if args else kwargs["output_dir"]
    (Path(output_dir) / "review-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def _upgrade_result(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    value["schema_version"] = 10
    trace = value.setdefault("workflow_trace", {})
    trace.setdefault("reviewer_agent_batch_observed", False)
    trace.setdefault("reviewer_lifecycle_overlap_observed", False)
    trace.setdefault("reviewer_fixture_access_observed", False)
    trace.setdefault("fixture_tool_permission_denials", 0)
    trace.setdefault("permission_denials_by_tool", {})
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return value


def grade_run(*args, **kwargs):
    _bind_revision()
    output = args[6] if len(args) > 6 else kwargs["output"]
    base.grade_run(*args, **kwargs)
    return _upgrade_result(output)


def record_terminal(*args, **kwargs):
    _bind_revision()
    output = args[4] if len(args) > 4 else kwargs["output"]
    base.record_terminal(*args, **kwargs)
    return _upgrade_result(output)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate-preflight", "prepare"):
        item = sub.add_parser(name)
        item.add_argument("--repetition", required=True, type=int)
        if name == "prepare":
            item.add_argument("--output-dir", required=True, type=Path)
    collect = sub.add_parser("collect")
    for name in ("raw-output", "execution-file", "hook-file", "review-input", "output-dir"):
        collect.add_argument(
            f"--{name}", type=Path, required=name not in {"execution-file", "hook-file"}
        )
    for name in ("action-conclusion", "model-requested"):
        collect.add_argument(f"--{name}", required=True)
    for name in ("started-ms", "finished-ms"):
        collect.add_argument(f"--{name}", required=True, type=int)
    for command in ("grade", "record-terminal"):
        item = sub.add_parser(command)
        for name in ("repetition", "attempt"):
            item.add_argument(f"--{name}", required=True, type=int)
        for name in ("model-requested", "github-run-id"):
            item.add_argument(f"--{name}", required=True)
        item.add_argument("--output", required=True, type=Path)
        if command == "grade":
            for name in ("review-output", "review-metadata", "prepare-metadata"):
                item.add_argument(f"--{name}", required=True, type=Path)
        else:
            item.add_argument("--status", required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate-preflight":
            validate_preflight(args.repetition)
            print("qualification preflight is valid")
        elif args.command == "prepare":
            print(json.dumps(prepare_input(args.repetition, args.output_dir), ensure_ascii=False))
        elif args.command == "collect":
            print(json.dumps(collect_review(args.raw_output, args.action_conclusion, args.execution_file, args.started_ms, args.finished_ms, args.model_requested, args.review_input, args.output_dir, hook_file=args.hook_file), ensure_ascii=False))
        elif args.command == "grade":
            print(json.dumps(grade_run(args.repetition, args.attempt, args.model_requested, args.review_output, args.review_metadata, args.prepare_metadata, args.output, args.github_run_id), ensure_ascii=False))
        else:
            print(json.dumps(record_terminal(args.repetition, args.attempt, args.model_requested, args.status, args.output, args.github_run_id), ensure_ascii=False))
    except (base.QualificationError, base.legacy.QualificationError, base.measurement.ValidationError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
