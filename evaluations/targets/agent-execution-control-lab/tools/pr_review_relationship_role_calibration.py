#!/usr/bin/env python3
"""Prepare, collect, and grade the relationship-reviewer model calibration."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

import pr_review_workflow_free_calibration as free


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
MODELS = {"sonnet", "opus"}
ROOT_MODEL = "claude-sonnet-5"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-calibrate-relationship-reviewer.yml"
WORKFLOW_REVISION = "pr-review-calibrate-relationship-reviewer-r1"
COMPARISON_REVISION = "pr-review-relationship-reviewer-model-calibration-r1"
RATING_ID = "pr-review-finding-quality-v5"
PROMPT_ID = "pr-review-relationship-role-r1"


class CalibrationError(ValueError):
    pass


def profile_id(reviewer_model: str) -> str:
    if reviewer_model not in MODELS:
        raise CalibrationError("relationship reviewer model must be sonnet or opus")
    return f"pr-review-relationship-reviewer-{reviewer_model}-c01-r4-calibration-n3-r1"


def variant(reviewer_model: str) -> str:
    return f"relationship-reviewer-{reviewer_model}"


def _profile_path(reviewer_model: str) -> Path:
    return INSTANCE_ROOT / "profiles" / f"{profile_id(reviewer_model)}.json"


def _preflight_path(reviewer_model: str) -> Path:
    return INSTANCE_ROOT / "contracts" / f"{profile_id(reviewer_model)}-preflight.json"


def _artifact_path(relative_path: str) -> Path:
    return REPOSITORY_ROOT / relative_path if relative_path.startswith(".github/") else INSTANCE_ROOT / relative_path


def validate_preflight(repetition: int, reviewer_model: str) -> tuple[dict, dict]:
    if repetition not in {1, 2, 3}:
        raise CalibrationError("repetition must be 1, 2, or 3")
    profile_path = _profile_path(reviewer_model)
    preflight_path = _preflight_path(reviewer_model)
    profile = free.core.legacy._load_json(profile_path)
    preflight = free.core.legacy._load_json(preflight_path)
    expected_profile_id = profile_id(reviewer_model)
    if profile.get("profile_id") != expected_profile_id or profile.get("state") != "frozen_not_executed":
        raise CalibrationError("profile identity mismatch")
    if profile.get("purpose") != "relationship_reviewer_model_calibration":
        raise CalibrationError("profile purpose mismatch")
    if profile.get("cases") != [{"id": "PRR-C01", "revision": "r4"}]:
        raise CalibrationError("profile case mismatch")
    conditions = profile.get("comparison_conditions", {})
    if conditions.get("variant") != variant(reviewer_model):
        raise CalibrationError("profile variant mismatch")
    if conditions.get("relationship_reviewer_model") != reviewer_model:
        raise CalibrationError("reviewer model mismatch")
    if conditions.get("model", {}).get("requested") != ROOT_MODEL:
        raise CalibrationError("root model mismatch")
    if conditions.get("model", {}).get("relationship_reviewer") != reviewer_model:
        raise CalibrationError("profile model role mismatch")
    if conditions.get("executor_parameters", {}).get("max_workers") != 24:
        raise CalibrationError("max_workers mismatch")
    if conditions.get("executor_parameters", {}).get("dispatch_concurrency") != 1:
        raise CalibrationError("dispatch concurrency mismatch")
    prompt = conditions.get("prompt", {})
    if prompt.get("template_identity") != PROMPT_ID:
        raise CalibrationError("prompt identity mismatch")
    template_path = _artifact_path(prompt["template_path"])
    template = template_path.read_text(encoding="utf-8")
    effective = template.replace("{{RELATIONSHIP_REVIEWER_MODEL}}", reviewer_model)
    if free.core.legacy._sha256(template_path) != prompt.get("template_sha256"):
        raise CalibrationError("prompt template mismatch")
    if hashlib.sha256(effective.encode("utf-8")).hexdigest() != prompt.get("effective_content_sha256"):
        raise CalibrationError("effective prompt mismatch")
    if prompt.get("effective_identity") != f"{PROMPT_ID}:{reviewer_model}":
        raise CalibrationError("effective prompt identity mismatch")
    for artifact in preflight.get("verified_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or free.core.legacy._sha256(path) != artifact.get("sha256"):
            raise CalibrationError(f"preflight artifact mismatch: {artifact.get('path')}")
    if preflight.get("state") != "ready_not_executed" or preflight.get("profile") != {
        "profile_id": expected_profile_id,
        "path": f"profiles/{profile_path.name}",
        "sha256": free.core.legacy._sha256(profile_path),
    }:
        raise CalibrationError("preflight profile receipt mismatch")
    planned = {"case_id": "PRR-C01", "fixture_revision": "r4", "variant": variant(reviewer_model), "repetition": repetition}
    if planned not in preflight.get("planned_slots", []):
        raise CalibrationError("slot is not in the fixed plan")
    comparison = free.core.legacy._load_json(INSTANCE_ROOT / "contracts/pr-review-relationship-reviewer-model-comparison-preflight-r1.json")
    if comparison.get("state") != "ready_not_executed" or comparison.get("changed_axis") != "relationship_reviewer_model":
        raise CalibrationError("model comparison preflight mismatch")
    free.core._fixture_and_oracle()
    return profile, preflight


def _hook_settings() -> dict:
    return free._hook_settings()


def prepare_input(repetition: int, reviewer_model: str, output_dir: Path) -> dict:
    profile_path = _profile_path(reviewer_model)
    preflight_path = _preflight_path(reviewer_model)
    original = {
        "profile_id": free.PROFILE_ID,
        "profile_path": free.PROFILE_PATH,
        "preflight_path": free.PREFLIGHT_PATH,
        "workflow_path": free.WORKFLOW_PATH,
        "file": free.__file__,
    }
    free.PROFILE_ID = profile_id(reviewer_model)
    free.PROFILE_PATH = profile_path
    free.PREFLIGHT_PATH = preflight_path
    free.WORKFLOW_PATH = WORKFLOW_PATH
    free.__file__ = __file__
    original_validate = free.validate_preflight
    free.validate_preflight = lambda repetition, prior_admission=None: validate_preflight(repetition, reviewer_model)
    try:
        metadata = free.prepare_input(repetition, output_dir)
    finally:
        free.PROFILE_ID = original["profile_id"]
        free.PROFILE_PATH = original["profile_path"]
        free.PREFLIGHT_PATH = original["preflight_path"]
        free.WORKFLOW_PATH = original["workflow_path"]
        free.__file__ = original["file"]
        free.validate_preflight = original_validate
    (output_dir / "pr_review_workflow_free_calibration.py").replace(output_dir / "pr_review_relationship_role_calibration.py")
    shutil.copyfile(INSTANCE_ROOT / "tools/pr_review_workflow_free_calibration.py", output_dir / "pr_review_workflow_free_calibration.py")
    metadata.update(profile_id=profile_id(reviewer_model), variant=variant(reviewer_model), relationship_reviewer_model=reviewer_model)
    (output_dir / "prepare-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return metadata


def _workflow_trace(execution_file: Path | None, hook_file: Path | None, reviewer_model: str) -> dict:
    execution_trace = free.core._workflow_trace(execution_file)
    events = free._read_hook_events(hook_file)
    reviewer_ids = {
        event["agent_id"] for event in events
        if event.get("event") == "SubagentStart" and isinstance(event.get("agent_id"), str)
    }
    fixture_events = [
        event for event in events
        if event.get("event") == "PostToolUse" and event.get("tool_name") == "Bash" and event.get("fixture_tool_command") is True
    ]
    reviewer_fixture_access = sum(1 for event in fixture_events if event.get("agent_id") in reviewer_ids)
    root_fixture_access = len(fixture_events) - reviewer_fixture_access
    fixture_denials = sum(
        1 for event in events
        if event.get("event") == "PermissionDenied" and event.get("fixture_tool_command") is True
    )
    starts = sum(1 for event in events if event.get("event") == "SubagentStart")
    stops = sum(1 for event in events if event.get("event") == "SubagentStop")
    groups = execution_trace.get("agent_model_groups", [])
    trace = {
        "agent_model_groups": groups,
        "subagent_usage_observed": execution_trace.get("subagent_usage_observed", False),
        "subagent_start_count": starts,
        "subagent_stop_count": stops,
        "relationship_reviewer_ids_observed": len(reviewer_ids),
        "relationship_reviewer_model_matches": groups == [[reviewer_model]],
        "relationship_reviewer_fixture_access_count": reviewer_fixture_access,
        "root_fixture_tool_access_count": root_fixture_access,
        "fixture_tool_access_count": len(fixture_events),
        "fixture_tool_access_observed": reviewer_fixture_access > 0,
        "fixture_tool_permission_denials": fixture_denials,
        "permission_denials_by_tool": {
            tool: sum(1 for event in events if event.get("event") == "PermissionDenied" and event.get("tool_name") == tool)
            for tool in sorted({event["tool_name"] for event in events if event.get("event") == "PermissionDenied" and isinstance(event.get("tool_name"), str)})
        },
        "usage_records": execution_trace.get("usage_records", 0),
        "all_agent_input_tokens": execution_trace.get("all_agent_input_tokens"),
        "all_agent_output_tokens": execution_trace.get("all_agent_output_tokens"),
        "hook_event_count": len(events),
    }
    trace["complete"] = bool(
        trace["usage_records"] > 0
        and trace["all_agent_input_tokens"] is not None
        and trace["all_agent_output_tokens"] is not None
        and starts == 1
        and stops == 1
        and len(reviewer_ids) == 1
        and trace["subagent_usage_observed"] is True
        and trace["relationship_reviewer_model_matches"] is True
        and reviewer_fixture_access > 0
        and root_fixture_access == 0
        and fixture_denials == 0
    )
    return trace


def collect_review(raw_output: Path, action_conclusion: str, execution_file: Path | None, hook_file: Path | None, started_ms: int, finished_ms: int, model_requested: str, reviewer_model: str, review_input: Path, output_dir: Path) -> dict:
    metadata = free.core.legacy.collect_review(raw_output, action_conclusion, execution_file, started_ms, finished_ms, model_requested, review_input, output_dir)
    trace = _workflow_trace(execution_file, hook_file, reviewer_model)
    metadata["workflow_trace"] = trace
    if trace["usage_records"] > 0:
        metadata["runtime"]["input_tokens"] = trace["all_agent_input_tokens"]
        metadata["runtime"]["output_tokens"] = trace["all_agent_output_tokens"]
    (output_dir / "review-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return metadata


def _measurement_qualification(metadata: dict, model_requested: str) -> dict:
    value = free._measurement_qualification(metadata, model_requested)
    trace = metadata.get("workflow_trace", {})
    value.update(
        exactly_one_relationship_reviewer=trace.get("subagent_start_count") == trace.get("subagent_stop_count") == 1,
        relationship_reviewer_model_matches=trace.get("relationship_reviewer_model_matches") is True,
        relationship_reviewer_fixture_access=trace.get("relationship_reviewer_fixture_access_count", 0) > 0,
        root_fixture_tool_access_count=trace.get("root_fixture_tool_access_count", 0),
    )
    value["state"] = "satisfied" if value.get("state") == "satisfied" and all((value["exactly_one_relationship_reviewer"], value["relationship_reviewer_model_matches"], value["relationship_reviewer_fixture_access"], value["root_fixture_tool_access_count"] == 0, trace.get("complete") is True)) else "unsatisfied"
    return value


def grade_run(repetition: int, attempt: int, model_requested: str, reviewer_model: str, review_output: Path, review_metadata: Path, prepare_metadata: Path, output: Path, github_run_id: str) -> dict:
    profile, _ = validate_preflight(repetition, reviewer_model)
    fixture, oracle = free.core._fixture_and_oracle()
    metadata = free.core.legacy._load_json(review_metadata)
    prepared = free.core.legacy._load_json(prepare_metadata)
    quality = {"observed": False, "expected_findings": 1, "true_positive": 0, "false_positive": 0, "false_negative": 0, "path_accuracy": 0, "line_accuracy": 0, "category_accuracy": 0, "clean_control_major_false_positive": 0, "scope_violation_count": 0, "review_contract_violation": 0, "summary_complete": False}
    quality_status = None
    if metadata.get("action_conclusion") != "success":
        result = "execution_failed"
    elif not metadata.get("output_valid") or not review_output.is_file():
        result = "invalid_output"
    else:
        review = free.core.measurement.validate_review_output_v2(free.core.legacy._load_json(review_output), set(fixture["changed_paths"]))
        quality = free.core.legacy._quality_result(oracle, review, fixture)
        quality_status = "pass" if quality["false_negative"] == quality["false_positive"] == quality["review_contract_violation"] == 0 else "quality_failed"
        result = quality_status
    measurement = _measurement_qualification(metadata, model_requested)
    if measurement["state"] != "satisfied" and result in {"pass", "quality_failed"}:
        result = "measurement_incomplete"
    runtime = metadata.get("runtime", {})
    total_tokens = runtime.get("input_tokens") + runtime.get("output_tokens") if runtime.get("input_tokens") is not None and runtime.get("output_tokens") is not None else None
    run = {
        "schema_version": 12,
        "comparison_revision": COMPARISON_REVISION,
        "profile_id": profile_id(reviewer_model),
        "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:PRR-C01:{variant(reviewer_model)}:r{repetition}:a{attempt}",
        "case_id": "PRR-C01", "fixture_revision": "r4", "variant": variant(reviewer_model), "relationship_reviewer_model": reviewer_model,
        "repetition": repetition, "attempt": attempt, "base_sha": fixture["pr"]["base_sha"], "head_sha": fixture["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": runtime.get("model")},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"],
        "workflow_revision": WORKFLOW_REVISION, "workflow_trace": metadata.get("workflow_trace", {}), "measurement_qualification": measurement,
        "github_run_id": github_run_id,
        "timing": {"queue_ms": None, "setup_ms": None, "input_ms": prepared["input_ms"], "action_step_ms": metadata.get("action_step_ms"), "review_ms": runtime.get("duration_ms"), "report_ms": None, "execution_ms": metadata.get("action_step_ms"), "e2e_ms": None},
        "runtime": {"turns": runtime.get("turns"), "input_tokens": runtime.get("input_tokens"), "output_tokens": runtime.get("output_tokens"), "total_tokens": total_tokens, "reported_cost_usd": runtime.get("reported_cost_usd")},
        "quality": quality,
        "quality_score": free.core.measurement._quality_score(quality_status, quality) if quality_status is not None else None,
        "result": result,
    }
    free.core.legacy._write_json_once(output, run)
    return run


def record_terminal(repetition: int, attempt: int, model_requested: str, reviewer_model: str, status: str, output: Path, github_run_id: str) -> dict:
    profile, _ = validate_preflight(repetition, reviewer_model)
    fixture, _ = free.core._fixture_and_oracle()
    empty_quality = {"observed": False, "expected_findings": 1, "true_positive": 0, "false_positive": 0, "false_negative": 0, "path_accuracy": 0, "line_accuracy": 0, "category_accuracy": 0, "clean_control_major_false_positive": 0, "scope_violation_count": 0, "review_contract_violation": 0, "summary_complete": False}
    run = {
        "schema_version": 12, "comparison_revision": COMPARISON_REVISION, "profile_id": profile_id(reviewer_model), "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:PRR-C01:{variant(reviewer_model)}:r{repetition}:a{attempt}", "case_id": "PRR-C01", "fixture_revision": "r4", "variant": variant(reviewer_model), "relationship_reviewer_model": reviewer_model,
        "repetition": repetition, "attempt": attempt, "base_sha": fixture["pr"]["base_sha"], "head_sha": fixture["pr"]["head_sha"], "model": {"requested": model_requested, "reported": None},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"], "workflow_revision": WORKFLOW_REVISION,
        "workflow_trace": {"complete": False}, "measurement_qualification": {"state": "unsatisfied"}, "github_run_id": github_run_id,
        "timing": {key: None for key in ("queue_ms", "setup_ms", "input_ms", "action_step_ms", "review_ms", "report_ms", "execution_ms", "e2e_ms")},
        "runtime": {key: None for key in ("turns", "input_tokens", "output_tokens", "total_tokens", "reported_cost_usd")}, "quality": empty_quality, "quality_score": None, "result": status,
    }
    free.core.legacy._write_json_once(output, run)
    return run


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate-preflight", "prepare"):
        item = sub.add_parser(name); item.add_argument("--repetition", required=True, type=int); item.add_argument("--relationship-reviewer-model", required=True, choices=sorted(MODELS))
        if name == "prepare": item.add_argument("--output-dir", required=True, type=Path)
    collect = sub.add_parser("collect")
    for name in ("raw-output", "execution-file", "hook-file", "review-input", "output-dir"): collect.add_argument(f"--{name}", type=Path, required=name not in {"execution-file", "hook-file"})
    for name in ("action-conclusion", "model-requested", "relationship-reviewer-model"): collect.add_argument(f"--{name}", required=True)
    for name in ("started-ms", "finished-ms"): collect.add_argument(f"--{name}", required=True, type=int)
    for command in ("grade", "record-terminal"):
        item = sub.add_parser(command)
        for name in ("repetition", "attempt"): item.add_argument(f"--{name}", required=True, type=int)
        for name in ("model-requested", "relationship-reviewer-model", "github-run-id"): item.add_argument(f"--{name}", required=True)
        item.add_argument("--output", required=True, type=Path)
        if command == "grade":
            for name in ("review-output", "review-metadata", "prepare-metadata"): item.add_argument(f"--{name}", required=True, type=Path)
        else: item.add_argument("--status", required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate-preflight": validate_preflight(args.repetition, args.relationship_reviewer_model); print("relationship reviewer model calibration preflight is valid")
        elif args.command == "prepare": print(json.dumps(prepare_input(args.repetition, args.relationship_reviewer_model, args.output_dir), ensure_ascii=False))
        elif args.command == "collect": print(json.dumps(collect_review(args.raw_output, args.action_conclusion, args.execution_file, args.hook_file, args.started_ms, args.finished_ms, args.model_requested, args.relationship_reviewer_model, args.review_input, args.output_dir), ensure_ascii=False))
        elif args.command == "grade": print(json.dumps(grade_run(args.repetition, args.attempt, args.model_requested, args.relationship_reviewer_model, args.review_output, args.review_metadata, args.prepare_metadata, args.output, args.github_run_id), ensure_ascii=False))
        else: print(json.dumps(record_terminal(args.repetition, args.attempt, args.model_requested, args.relationship_reviewer_model, args.status, args.output, args.github_run_id), ensure_ascii=False))
    except (CalibrationError, free.CalibrationError, free.core.QualificationError, free.core.legacy.QualificationError, free.core.measurement.ValidationError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr); return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
