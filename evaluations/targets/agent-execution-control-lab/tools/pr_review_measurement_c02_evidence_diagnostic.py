#!/usr/bin/env python3
"""Run Candidate170 with content-free evidence and token diagnostics."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

import pr_review_measurement_c02_evidence_scope as base


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-measurement-c02-evidence-diagnostic-n1-r2"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-measure-c02-evidence-diagnostic-r2.yml"
WORKFLOW_REVISION = "pr-review-measure-c02-evidence-diagnostic-r2"
COMPARISON_REVISION = "pr-review-measurement-c02-evidence-diagnostic-r2"
TOKEN_FIELDS = (
    "input_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
    "output_tokens",
)


def _patch_base() -> dict:
    original = {
        "PROFILE_ID": base.PROFILE_ID,
        "PROFILE_PATH": base.PROFILE_PATH,
        "PREFLIGHT_PATH": base.PREFLIGHT_PATH,
        "WORKFLOW_PATH": base.WORKFLOW_PATH,
        "WORKFLOW_REVISION": base.WORKFLOW_REVISION,
        "COMPARISON_REVISION": base.COMPARISON_REVISION,
        "file": base.__file__,
    }
    base.PROFILE_ID = PROFILE_ID
    base.PROFILE_PATH = PROFILE_PATH
    base.PREFLIGHT_PATH = PREFLIGHT_PATH
    base.WORKFLOW_PATH = WORKFLOW_PATH
    base.WORKFLOW_REVISION = WORKFLOW_REVISION
    base.COMPARISON_REVISION = COMPARISON_REVISION
    base.__file__ = __file__
    return original


def _restore_base(original: dict) -> None:
    for key in (
        "PROFILE_ID",
        "PROFILE_PATH",
        "PREFLIGHT_PATH",
        "WORKFLOW_PATH",
        "WORKFLOW_REVISION",
        "COMPARISON_REVISION",
    ):
        setattr(base, key, original[key])
    base.__file__ = original["file"]


def validate_preflight(case_id: str) -> tuple[dict, dict]:
    original = _patch_base()
    try:
        return base.validate_preflight(case_id)
    finally:
        _restore_base(original)


def prepare_input(case_id: str, output_dir: Path) -> dict:
    original = _patch_base()
    try:
        metadata = base.prepare_input(case_id, output_dir)
    finally:
        _restore_base(original)
    shutil.copyfile(__file__, output_dir / "pr_review_measurement_c02_evidence_diagnostic.py")
    shutil.copyfile(
        INSTANCE_ROOT / "tools/pr_review_subagent_hook_r3.py",
        output_dir / "pr_review_subagent_hook_r3.py",
    )
    settings_path = output_dir / "claude-project-settings.json"
    settings = json.loads(settings_path.read_text(encoding="utf-8"))
    for groups in settings.get("hooks", {}).values():
        for group in groups if isinstance(groups, list) else []:
            for hook in group.get("hooks", []) if isinstance(group, dict) else []:
                command = hook.get("command")
                if isinstance(command, str):
                    hook["command"] = command.replace(
                        "pr_review_subagent_hook.py", "pr_review_subagent_hook_r3.py"
                    )
                args = hook.get("args")
                if isinstance(args, list):
                    hook["args"] = [
                        item.replace(
                            "pr_review_subagent_hook.py",
                            "pr_review_subagent_hook_r3.py",
                        )
                        if isinstance(item, str)
                        else item
                        for item in args
                    ]
    settings_path.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    metadata.update(profile_id=PROFILE_ID, diagnostic_revision="content-free-evidence-and-token-r2")
    (output_dir / "prepare-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def _token_diagnostics(execution_file: Path | None) -> dict:
    totals = {
        role: {field: 0 for field in TOKEN_FIELDS}
        for role in ("root", "subagent", "all")
    }
    records = {"root": 0, "subagent": 0, "all": 0}
    if execution_file is None or not execution_file.is_file():
        return {"complete": False, "usage_records": records, "tokens": totals}
    try:
        documents = json.loads(execution_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"complete": False, "usage_records": records, "tokens": totals}
    if not isinstance(documents, list):
        documents = [documents]
    for message in documents:
        if not isinstance(message, dict) or message.get("type") != "assistant":
            continue
        body = message.get("message")
        usage = body.get("usage") if isinstance(body, dict) else None
        if not isinstance(usage, dict):
            continue
        role = "subagent" if message.get("parent_tool_use_id") is not None else "root"
        observed = False
        for field in TOKEN_FIELDS:
            value = usage.get(field)
            if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0:
                totals[role][field] += value
                totals["all"][field] += value
                observed = True
        if observed:
            records[role] += 1
            records["all"] += 1
    return {
        "complete": records["all"] > 0,
        "usage_records": records,
        "tokens": totals,
    }


def _evidence_diagnostics(events: list[dict]) -> dict:
    calls: dict[str, dict] = {}
    batches: list[dict] = []
    for event in events:
        if event.get("event") in {"PostToolUse", "PostToolUseFailure", "PermissionDenied"}:
            tool_id = event.get("tool_use_id")
            operations = event.get("fixture_tool_operations")
            if isinstance(tool_id, str) and isinstance(operations, list) and operations:
                calls[tool_id] = {
                    "operations": [item for item in operations if isinstance(item, str)],
                    "outcome": event.get("outcome", "unknown"),
                }
        elif event.get("event") == "PostToolBatch":
            items = [
                calls[tool_id]
                for tool_id in event.get("tool_use_ids", [])
                if isinstance(tool_id, str) and tool_id in calls
            ]
            if items:
                batches.append({"calls": items})
    batched_ids = {
        tool_id
        for event in events
        if event.get("event") == "PostToolBatch"
        for tool_id in event.get("tool_use_ids", [])
        if isinstance(tool_id, str)
    }
    unbatched = [call for tool_id, call in calls.items() if tool_id not in batched_ids]
    counts: dict[str, dict[str, int]] = {}
    for call in calls.values():
        for operation in call["operations"]:
            outcomes = counts.setdefault(operation, {})
            outcome = call["outcome"]
            outcomes[outcome] = outcomes.get(outcome, 0) + 1
    return {
        "content_saved": False,
        "operation_counts": counts,
        "batches": batches,
        "unbatched_calls": unbatched,
    }


def collect_review(
    raw_output: Path,
    action_conclusion: str,
    execution_file: Path | None,
    hook_file: Path | None,
    started_ms: int,
    finished_ms: int,
    model_requested: str,
    review_input: Path,
    output_dir: Path,
) -> dict:
    original = _patch_base()
    try:
        metadata = base.collect_review(
            raw_output,
            action_conclusion,
            execution_file,
            hook_file,
            started_ms,
            finished_ms,
            model_requested,
            review_input,
            output_dir,
        )
    finally:
        _restore_base(original)
    events = base.relationship.free._read_hook_events(hook_file)
    metadata["workflow_trace"]["evidence_diagnostics"] = _evidence_diagnostics(events)
    metadata["workflow_trace"]["token_diagnostics"] = _token_diagnostics(execution_file)
    (output_dir / "review-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def grade_run(
    case_id: str,
    attempt: int,
    model_requested: str,
    review_output: Path,
    review_metadata: Path,
    prepare_metadata: Path,
    output: Path,
    github_run_id: str,
) -> dict:
    original = _patch_base()
    try:
        with tempfile.TemporaryDirectory() as directory:
            intermediate = Path(directory) / "run-result.json"
            run = base.grade_run(
                case_id,
                attempt,
                model_requested,
                review_output,
                review_metadata,
                prepare_metadata,
                intermediate,
                github_run_id,
            )
    finally:
        _restore_base(original)
    run.update(
        schema_version=20,
        comparison_revision=COMPARISON_REVISION,
        profile_id=PROFILE_ID,
        workflow_revision=WORKFLOW_REVISION,
    )
    base.held_out.free.core.legacy._write_json_once(output, run)
    return run


def record_terminal(
    case_id: str,
    attempt: int,
    model_requested: str,
    status: str,
    output: Path,
    github_run_id: str,
) -> dict:
    original = _patch_base()
    try:
        with tempfile.TemporaryDirectory() as directory:
            intermediate = Path(directory) / "run-result.json"
            run = base.record_terminal(
                case_id, attempt, model_requested, status, intermediate, github_run_id
            )
    finally:
        _restore_base(original)
    run.update(
        schema_version=20,
        comparison_revision=COMPARISON_REVISION,
        profile_id=PROFILE_ID,
        workflow_revision=WORKFLOW_REVISION,
    )
    run.setdefault("workflow_trace", {}).update(
        evidence_diagnostics={
            "content_saved": False,
            "operation_counts": {},
            "batches": [],
            "unbatched_calls": [],
        },
        token_diagnostics={
            "complete": False,
            "usage_records": {"root": 0, "subagent": 0, "all": 0},
            "tokens": {
                role: {field: 0 for field in TOKEN_FIELDS}
                for role in ("root", "subagent", "all")
            },
        },
    )
    base.held_out.free.core.legacy._write_json_once(output, run)
    return run


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate-preflight", "prepare"):
        item = sub.add_parser(name)
        item.add_argument("--case-id", required=True, choices=base.CASES)
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
        item.add_argument("--case-id", required=True, choices=base.CASES)
        item.add_argument("--attempt", required=True, type=int)
        item.add_argument("--model-requested", required=True)
        item.add_argument("--github-run-id", required=True)
        item.add_argument("--output", required=True, type=Path)
        if command == "grade":
            for name in ("review-output", "review-metadata", "prepare-metadata"):
                item.add_argument(f"--{name}", required=True, type=Path)
        else:
            item.add_argument("--status", required=True)
    args = parser.parse_args()
    if args.command == "validate-preflight":
        validate_preflight(args.case_id)
        print("Candidate170 diagnostic preflight is valid")
    elif args.command == "prepare":
        print(json.dumps(prepare_input(args.case_id, args.output_dir), ensure_ascii=False))
    elif args.command == "collect":
        print(
            json.dumps(
                collect_review(
                    args.raw_output,
                    args.action_conclusion,
                    args.execution_file,
                    args.hook_file,
                    args.started_ms,
                    args.finished_ms,
                    args.model_requested,
                    args.review_input,
                    args.output_dir,
                ),
                ensure_ascii=False,
            )
        )
    elif args.command == "grade":
        print(
            json.dumps(
                grade_run(
                    args.case_id,
                    args.attempt,
                    args.model_requested,
                    args.review_output,
                    args.review_metadata,
                    args.prepare_metadata,
                    args.output,
                    args.github_run_id,
                ),
                ensure_ascii=False,
            )
        )
    else:
        print(
            json.dumps(
                record_terminal(
                    args.case_id,
                    args.attempt,
                    args.model_requested,
                    args.status,
                    args.output,
                    args.github_run_id,
                ),
                ensure_ascii=False,
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
