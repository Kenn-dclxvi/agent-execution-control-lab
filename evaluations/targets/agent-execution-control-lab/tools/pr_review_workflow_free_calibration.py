#!/usr/bin/env python3
"""Prepare, collect, and grade Workflow Free calibration runs."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import pr_review_code_review_qualification as core


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-workflow-free-c01-r4-calibration-n2-r1"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
SNAPSHOT_PATH = (
    INSTANCE_ROOT / "contracts/baseline-repository-snapshot-prr-c01-r4-r1.json"
)
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-measure-workflow-free.yml"
WORKFLOW_REVISION = "pr-review-measure-workflow-free-r1"
COMPARISON_REVISION = "pr-review-workflow-free-calibration-r1"
RATING_ID = "pr-review-finding-quality-v5"
VARIANT = "workflow-free"


class CalibrationError(ValueError):
    pass


def validate_preflight(
    repetition: int, prior_admission: Path | None = None
) -> tuple[dict, dict]:
    if repetition not in {1, 2}:
        raise CalibrationError("repetition must be 1 or 2")
    profile = core.legacy._load_json(PROFILE_PATH)
    preflight = core.legacy._load_json(PREFLIGHT_PATH)
    if profile.get("profile_id") != PROFILE_ID or profile.get("state") != "frozen_not_executed":
        raise CalibrationError("profile identity mismatch")
    if profile.get("purpose") != "workflow_free_calibration":
        raise CalibrationError("profile purpose mismatch")
    if profile.get("cases") != [{"id": "PRR-C01", "revision": "r4"}]:
        raise CalibrationError("profile case mismatch")
    conditions = profile.get("comparison_conditions", {})
    if conditions.get("variant") != VARIANT:
        raise CalibrationError("profile variant mismatch")
    condition_artifacts = [
        (conditions["fixture_identity"]["input_path"], conditions["fixture_identity"]["input_sha256"]),
        (conditions["fixture_identity"]["oracle_path"], conditions["fixture_identity"]["oracle_sha256"]),
        (
            conditions["fixture_identity"]["case_design_audit_path"],
            conditions["fixture_identity"]["case_design_audit_sha256"],
        ),
        (conditions["workflow_free_boundary"]["path"], conditions["workflow_free_boundary"]["sha256"]),
        (
            conditions["repository_snapshot"]["receipt_path"],
            conditions["repository_snapshot"]["receipt_sha256"],
        ),
        (
            conditions["repository_snapshot"]["materializer_path"],
            conditions["repository_snapshot"]["materializer_sha256"],
        ),
        (conditions["authority_selection"]["path"], conditions["authority_selection"]["sha256"]),
        (conditions["prompt"]["manifest_path"], conditions["prompt"]["manifest_sha256"]),
        (conditions["prompt"]["content_path"], conditions["prompt"]["content_sha256"]),
        (conditions["eligibility"]["path"], conditions["eligibility"]["sha256"]),
        (conditions["review_contract"]["path"], conditions["review_contract"]["sha256"]),
        (
            conditions["review_output_schema"]["path"],
            conditions["review_output_schema"]["sha256"],
        ),
        (conditions["run_result_schema"]["path"], conditions["run_result_schema"]["sha256"]),
        (conditions["calibration_tool"]["path"], conditions["calibration_tool"]["sha256"]),
        (conditions["lifecycle_recorder"]["path"], conditions["lifecycle_recorder"]["sha256"]),
        (conditions["quality_rating"]["path"], conditions["quality_rating"]["contract_sha256"]),
        (conditions["permission"]["fixture_tool_path"], conditions["permission"]["fixture_tool_sha256"]),
    ]
    for relative_path, expected_sha256 in condition_artifacts:
        artifact_path = INSTANCE_ROOT / relative_path
        if not artifact_path.is_file() or core.legacy._sha256(artifact_path) != expected_sha256:
            raise CalibrationError(f"profile artifact mismatch: {relative_path}")
    workflow = conditions["workflow"]
    workflow_path = REPOSITORY_ROOT / workflow["repository_path"]
    if not workflow_path.is_file() or core.legacy._sha256(workflow_path) != workflow["sha256"]:
        raise CalibrationError("profile workflow mismatch")
    manifest = core.legacy._load_json(INSTANCE_ROOT / conditions["prompt"]["manifest_path"])
    if manifest.get("prompt_identity") != conditions["prompt"]["identity"] or manifest.get(
        "core"
    ) != {
        "path": Path(conditions["prompt"]["content_path"]).name,
        "content_sha256": conditions["prompt"]["content_sha256"],
    }:
        raise CalibrationError("prompt manifest mismatch")
    if preflight.get("state") != "ready_not_executed" or preflight.get("profile") != {
        "profile_id": PROFILE_ID,
        "path": f"profiles/{PROFILE_PATH.name}",
        "sha256": core.legacy._sha256(PROFILE_PATH),
    }:
        raise CalibrationError("preflight profile receipt mismatch")
    for artifact in preflight.get("verified_artifacts", []):
        artifact_path = (
            REPOSITORY_ROOT / artifact["path"]
            if artifact["path"].startswith(".github/")
            else INSTANCE_ROOT / artifact["path"]
        )
        if not artifact_path.is_file() or core.legacy._sha256(artifact_path) != artifact.get("sha256"):
            raise CalibrationError(f"preflight artifact mismatch: {artifact.get('path')}")
    boundary = core.legacy._load_json(
        INSTANCE_ROOT / conditions["workflow_free_boundary"]["path"]
    )
    if boundary.get("state") != "satisfied" or boundary.get(
        "free_prompt_identity"
    ) != conditions["prompt"]["identity"]:
        raise CalibrationError("Workflow Free boundary mismatch")
    audit = core.legacy._load_json(
        INSTANCE_ROOT / conditions["fixture_identity"]["case_design_audit_path"]
    )
    rating = core.legacy._load_json(INSTANCE_ROOT / conditions["quality_rating"]["path"])
    if audit.get("decision") != "satisfied" or rating.get("state") != "independent_qualification_satisfied":
        raise CalibrationError("case admission mismatch")
    if conditions.get("model", {}).get("requested") != "claude-sonnet-5":
        raise CalibrationError("root model mismatch")
    executor = conditions.get("executor_parameters", {})
    if executor.get("max_workers") != 24 or executor.get("dispatch_concurrency") != 1:
        raise CalibrationError("executor concurrency mismatch")
    planned = {
        "case_id": "PRR-C01",
        "fixture_revision": "r4",
        "variant": VARIANT,
        "repetition": repetition,
    }
    if planned not in preflight.get("planned_slots", []):
        raise CalibrationError("slot is not in the fixed plan")
    core._fixture_and_oracle()
    return profile, preflight


def _hook_settings() -> dict:
    recorder = {
        "type": "command",
        "command": "python3",
        "args": [
            "${CLAUDE_PROJECT_DIR}/pr_review_subagent_hook.py",
            "${CLAUDE_PROJECT_DIR}/.claude/pr-review-subagent-events.jsonl",
        ],
    }

    def matched(matcher: str) -> list[dict]:
        return [{"matcher": matcher, "hooks": [recorder]}]

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
    import pr_review_repository_snapshot_r3 as snapshot_r3

    sys.modules["pr_review_repository_snapshot_r2"] = snapshot_r3
    core.legacy.PROFILE_ID = PROFILE_ID
    core.legacy.PROFILE_PATH = PROFILE_PATH
    core.legacy.PREFLIGHT_PATH = PREFLIGHT_PATH
    core.legacy.SNAPSHOT_RECEIPT_PATH = SNAPSHOT_PATH
    core.legacy.validate_preflight = validate_preflight
    original_file = core.legacy.__file__
    core.legacy.__file__ = __file__
    try:
        metadata = core.legacy.prepare_input(repetition, output_dir)
    finally:
        core.legacy.__file__ = original_file
    (output_dir / "pr-review-qualification.py").replace(
        output_dir / "pr_review_workflow_free_calibration.py"
    )
    shutil.copyfile(
        INSTANCE_ROOT / "tools/pr_review_code_review_qualification.py",
        output_dir / "pr_review_code_review_qualification.py",
    )
    shutil.copyfile(
        INSTANCE_ROOT / "tools/pr_review_qualification.py",
        output_dir / "pr_review_qualification.py",
    )
    shutil.copyfile(
        INSTANCE_ROOT / "tools/pr_review_subagent_hook.py",
        output_dir / "pr_review_subagent_hook.py",
    )
    shutil.copyfile(
        INSTANCE_ROOT / "contracts/prr-c01-r4-review-eligibility-r1.json",
        output_dir / "review-eligibility.json",
    )
    (output_dir / "claude-project-settings.json").write_text(
        json.dumps(_hook_settings(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    metadata.update(fixture_revision="r4", variant=VARIANT)
    (output_dir / "prepare-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def _read_hook_events(path: Path | None) -> list[dict]:
    if path is None or not path.is_file():
        return []
    events: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict) and isinstance(value.get("timestamp_ns"), int):
            events.append(value)
    return sorted(events, key=lambda item: item["timestamp_ns"])


def _workflow_trace(execution_file: Path | None, hook_file: Path | None) -> dict:
    execution_trace = core._workflow_trace(execution_file)
    events = _read_hook_events(hook_file)
    fixture_access_count = sum(
        1
        for event in events
        if event.get("event") == "PostToolUse"
        and event.get("tool_name") == "Bash"
        and event.get("fixture_tool_command") is True
    )
    fixture_denials = sum(
        1
        for event in events
        if event.get("event") == "PermissionDenied"
        and event.get("fixture_tool_command") is True
    )
    starts = sum(1 for event in events if event.get("event") == "SubagentStart")
    stops = sum(1 for event in events if event.get("event") == "SubagentStop")
    usage_records = execution_trace.get("usage_records", 0)
    input_tokens = execution_trace.get("all_agent_input_tokens")
    output_tokens = execution_trace.get("all_agent_output_tokens")
    trace = {
        "agent_model_groups": execution_trace.get("agent_model_groups", []),
        "subagent_usage_observed": execution_trace.get("subagent_usage_observed", False),
        "subagent_start_count": starts,
        "subagent_stop_count": stops,
        "fixture_tool_access_count": fixture_access_count,
        "fixture_tool_access_observed": fixture_access_count > 0,
        "fixture_tool_permission_denials": fixture_denials,
        "permission_denials_by_tool": {
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
        "usage_records": usage_records,
        "all_agent_input_tokens": input_tokens,
        "all_agent_output_tokens": output_tokens,
        "hook_event_count": len(events),
    }
    trace["complete"] = bool(
        usage_records > 0
        and input_tokens is not None
        and output_tokens is not None
        and fixture_access_count > 0
        and fixture_denials == 0
        and starts == stops
    )
    return trace


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
    metadata = core.legacy.collect_review(
        raw_output,
        action_conclusion,
        execution_file,
        started_ms,
        finished_ms,
        model_requested,
        review_input,
        output_dir,
    )
    trace = _workflow_trace(execution_file, hook_file)
    metadata["workflow_trace"] = trace
    if trace["usage_records"] > 0:
        metadata["runtime"]["input_tokens"] = trace["all_agent_input_tokens"]
        metadata["runtime"]["output_tokens"] = trace["all_agent_output_tokens"]
    (output_dir / "review-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def _measurement_qualification(metadata: dict, model_requested: str) -> dict:
    runtime = metadata.get("runtime", {})
    trace = metadata.get("workflow_trace", {})
    value = {
        "action_completed": metadata.get("action_conclusion") == "success",
        "structured_output_valid": metadata.get("output_valid") is True,
        "reported_model_matches_requested": runtime.get("model") == model_requested,
        "all_agent_tokens_complete": (
            runtime.get("input_tokens") is not None
            and runtime.get("output_tokens") is not None
        ),
        "elapsed_time_complete": isinstance(metadata.get("action_step_ms"), int),
        "fixture_access_observed": trace.get("fixture_tool_access_observed") is True,
        "fixture_permission_denials": trace.get("fixture_tool_permission_denials", 0),
    }
    value["state"] = (
        "satisfied"
        if all(
            (
                value["action_completed"],
                value["structured_output_valid"],
                value["reported_model_matches_requested"],
                value["all_agent_tokens_complete"],
                value["elapsed_time_complete"],
                value["fixture_access_observed"],
                value["fixture_permission_denials"] == 0,
                trace.get("complete") is True,
            )
        )
        else "unsatisfied"
    )
    return value


def grade_run(
    repetition: int,
    attempt: int,
    model_requested: str,
    review_output: Path,
    review_metadata: Path,
    prepare_metadata: Path,
    output: Path,
    github_run_id: str,
) -> dict:
    profile, _ = validate_preflight(repetition)
    fixture, oracle = core._fixture_and_oracle()
    metadata = core.legacy._load_json(review_metadata)
    prepared = core.legacy._load_json(prepare_metadata)
    quality = {
        "observed": False,
        "expected_findings": 1,
        "true_positive": 0,
        "false_positive": 0,
        "false_negative": 0,
        "path_accuracy": 0,
        "line_accuracy": 0,
        "category_accuracy": 0,
        "clean_control_major_false_positive": 0,
        "scope_violation_count": 0,
        "review_contract_violation": 0,
        "summary_complete": False,
    }
    quality_status: str | None = None
    if metadata.get("action_conclusion") != "success":
        result = "execution_failed"
    elif not metadata.get("output_valid") or not review_output.is_file():
        result = "invalid_output"
    else:
        review = core.measurement.validate_review_output_v2(
            core.legacy._load_json(review_output), set(fixture["changed_paths"])
        )
        quality = core.legacy._quality_result(oracle, review, fixture)
        quality_status = (
            "pass"
            if quality["false_negative"]
            == quality["false_positive"]
            == quality["review_contract_violation"]
            == 0
            else "quality_failed"
        )
        result = quality_status
    measurement = _measurement_qualification(metadata, model_requested)
    if measurement["state"] != "satisfied" and result in {"pass", "quality_failed"}:
        result = "measurement_incomplete"
    runtime = metadata.get("runtime", {})
    total_tokens = None
    if runtime.get("input_tokens") is not None and runtime.get("output_tokens") is not None:
        total_tokens = runtime["input_tokens"] + runtime["output_tokens"]
    quality_score = (
        core.measurement._quality_score(quality_status, quality)
        if quality_status is not None
        else None
    )
    run = {
        "schema_version": 11,
        "comparison_revision": COMPARISON_REVISION,
        "profile_id": PROFILE_ID,
        "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:PRR-C01:{VARIANT}:r{repetition}:a{attempt}",
        "case_id": "PRR-C01",
        "fixture_revision": "r4",
        "variant": VARIANT,
        "repetition": repetition,
        "attempt": attempt,
        "base_sha": fixture["pr"]["base_sha"],
        "head_sha": fixture["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": runtime.get("model")},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"],
        "workflow_revision": WORKFLOW_REVISION,
        "workflow_trace": metadata.get("workflow_trace", {}),
        "measurement_qualification": measurement,
        "github_run_id": github_run_id,
        "timing": {
            "queue_ms": None,
            "setup_ms": None,
            "input_ms": prepared["input_ms"],
            "action_step_ms": metadata.get("action_step_ms"),
            "review_ms": runtime.get("duration_ms"),
            "report_ms": None,
            "execution_ms": metadata.get("action_step_ms"),
            "e2e_ms": None,
        },
        "runtime": {
            "turns": runtime.get("turns"),
            "input_tokens": runtime.get("input_tokens"),
            "output_tokens": runtime.get("output_tokens"),
            "total_tokens": total_tokens,
            "reported_cost_usd": runtime.get("reported_cost_usd"),
        },
        "quality": quality,
        "quality_score": quality_score,
        "result": result,
    }
    core.legacy._write_json_once(output, run)
    return run


def record_terminal(
    repetition: int,
    attempt: int,
    model_requested: str,
    status: str,
    output: Path,
    github_run_id: str,
) -> dict:
    profile, _ = validate_preflight(repetition)
    fixture, _ = core._fixture_and_oracle()
    run = {
        "schema_version": 11,
        "comparison_revision": COMPARISON_REVISION,
        "profile_id": PROFILE_ID,
        "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:PRR-C01:{VARIANT}:r{repetition}:a{attempt}",
        "case_id": "PRR-C01",
        "fixture_revision": "r4",
        "variant": VARIANT,
        "repetition": repetition,
        "attempt": attempt,
        "base_sha": fixture["pr"]["base_sha"],
        "head_sha": fixture["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": None},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"],
        "workflow_revision": WORKFLOW_REVISION,
        "workflow_trace": {
            "complete": False,
            "agent_model_groups": [],
            "subagent_usage_observed": False,
            "subagent_start_count": 0,
            "subagent_stop_count": 0,
            "fixture_tool_access_count": 0,
            "fixture_tool_access_observed": False,
            "fixture_tool_permission_denials": 0,
            "permission_denials_by_tool": {},
            "usage_records": 0,
            "all_agent_input_tokens": None,
            "all_agent_output_tokens": None,
            "hook_event_count": 0,
        },
        "measurement_qualification": {
            "state": "unsatisfied",
            "action_completed": False,
            "structured_output_valid": False,
            "reported_model_matches_requested": False,
            "all_agent_tokens_complete": False,
            "elapsed_time_complete": False,
            "fixture_access_observed": False,
            "fixture_permission_denials": 0,
        },
        "github_run_id": github_run_id,
        "timing": {
            key: None
            for key in (
                "queue_ms",
                "setup_ms",
                "input_ms",
                "action_step_ms",
                "review_ms",
                "report_ms",
                "execution_ms",
                "e2e_ms",
            )
        },
        "runtime": {
            key: None
            for key in (
                "turns",
                "input_tokens",
                "output_tokens",
                "total_tokens",
                "reported_cost_usd",
            )
        },
        "quality": {
            "observed": False,
            "expected_findings": 1,
            "true_positive": 0,
            "false_positive": 0,
            "false_negative": 0,
            "path_accuracy": 0,
            "line_accuracy": 0,
            "category_accuracy": 0,
            "clean_control_major_false_positive": 0,
            "scope_violation_count": 0,
            "review_contract_violation": 0,
            "summary_complete": False,
        },
        "quality_score": None,
        "result": status,
    }
    core.legacy._write_json_once(output, run)
    return run


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
            print("Workflow Free calibration preflight is valid")
        elif args.command == "prepare":
            print(json.dumps(prepare_input(args.repetition, args.output_dir), ensure_ascii=False))
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
                        args.repetition,
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
                        args.repetition,
                        args.attempt,
                        args.model_requested,
                        args.status,
                        args.output,
                        args.github_run_id,
                    ),
                    ensure_ascii=False,
                )
            )
    except (
        CalibrationError,
        core.QualificationError,
        core.legacy.QualificationError,
        core.measurement.ValidationError,
        OSError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
