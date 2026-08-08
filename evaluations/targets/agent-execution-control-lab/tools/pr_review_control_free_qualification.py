#!/usr/bin/env python3
"""Prepare, collect, and grade the four-case control-free qualification."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import pr_review_measurement as measurement
import pr_review_workflow_free_calibration as free


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-control-free-four-qualification-n1-r1"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-qualify-control-free-four.yml"
WORKFLOW_REVISION = "pr-review-qualify-control-free-four-r1"
COMPARISON_REVISION = "pr-review-control-free-four-qualification-r1"
RATING_ID = "pr-review-finding-quality-v6"
VARIANT = "workflow-free-qualification"
ROOT_MODEL = "claude-sonnet-5"
CASES = ("PRR-C02", "PRR-C03", "PRR-C05", "PRR-C06")


class QualificationError(ValueError):
    pass


def _artifact_path(relative_path: str) -> Path:
    return (
        REPOSITORY_ROOT / relative_path
        if relative_path.startswith(".github/")
        else INSTANCE_ROOT / relative_path
    )


def _load(path: Path) -> dict:
    return measurement._load_json(path)


def validate_preflight(case_id: str) -> tuple[dict, dict]:
    if case_id not in CASES:
        raise QualificationError("case is not in the fixed qualification set")
    profile = _load(PROFILE_PATH)
    preflight = _load(PREFLIGHT_PATH)
    if profile.get("profile_id") != PROFILE_ID or profile.get("state") != "frozen_not_executed":
        raise QualificationError("profile identity mismatch")
    if profile.get("purpose") != "control_free_baseline_qualification":
        raise QualificationError("profile purpose mismatch")
    expected_cases = [{"id": item, "revision": "r1"} for item in CASES]
    if profile.get("cases") != expected_cases:
        raise QualificationError("profile case membership mismatch")
    conditions = profile.get("comparison_conditions", {})
    if conditions.get("variant") != VARIANT:
        raise QualificationError("profile variant mismatch")
    if conditions.get("model", {}).get("requested") != ROOT_MODEL:
        raise QualificationError("profile model mismatch")
    executor = conditions.get("executor_parameters", {})
    if executor.get("max_workers") != 24 or executor.get("dispatch_concurrency") != 4:
        raise QualificationError("profile concurrency mismatch")
    for artifact in conditions.get("bound_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or measurement._sha256(path) != artifact.get("sha256"):
            raise QualificationError(f"profile artifact mismatch: {artifact.get('path')}")
    prompt = conditions.get("prompt", {})
    manifest_path = _artifact_path(prompt.get("manifest_path", ""))
    prompt_path = _artifact_path(prompt.get("path", ""))
    manifest = _load(manifest_path)
    if (
        manifest.get("prompt_identity") != prompt.get("identity")
        or manifest.get("core")
        != {"path": prompt_path.name, "content_sha256": prompt.get("sha256")}
        or measurement._sha256(manifest_path) != prompt.get("manifest_sha256")
        or measurement._sha256(prompt_path) != prompt.get("sha256")
    ):
        raise QualificationError("profile prompt binding mismatch")
    expected_profile = {
        "profile_id": PROFILE_ID,
        "path": f"profiles/{PROFILE_PATH.name}",
        "sha256": measurement._sha256(PROFILE_PATH),
    }
    if preflight.get("state") != "ready_not_executed" or preflight.get("profile") != expected_profile:
        raise QualificationError("preflight profile receipt mismatch")
    if {"case_id": case_id, "fixture_revision": "r1", "variant": VARIANT, "repetition": 1} not in preflight.get("planned_slots", []):
        raise QualificationError("slot is not in the fixed plan")
    for artifact in preflight.get("verified_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or measurement._sha256(path) != artifact.get("sha256"):
            raise QualificationError(f"preflight artifact mismatch: {artifact.get('path')}")
    return profile, preflight


def prepare_input(case_id: str, output_dir: Path) -> dict:
    validate_preflight(case_id)
    original_variants = measurement.VARIANTS
    measurement.VARIANTS = (*measurement.VARIANTS, VARIANT)
    try:
        metadata = measurement.prepare_input(case_id, VARIANT, output_dir)
    finally:
        measurement.VARIANTS = original_variants
    shutil.copyfile(Path(__file__), output_dir / Path(__file__).name)
    shutil.copyfile(
        INSTANCE_ROOT / "tools/pr_review_subagent_hook.py",
        output_dir / "pr_review_subagent_hook.py",
    )
    (output_dir / "claude-project-settings.json").write_text(
        json.dumps(free._hook_settings(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def collect_review(
    raw_output: Path,
    action_conclusion: str,
    execution_file: Path | None,
    hook_file: Path | None,
    started_ms: int,
    finished_ms: int,
    model_requested: str,
    output_dir: Path,
) -> dict:
    metadata = measurement.collect_review(
        raw_output,
        action_conclusion,
        execution_file,
        started_ms,
        finished_ms,
        model_requested,
        output_dir,
    )
    trace = free._workflow_trace(execution_file, hook_file)
    metadata["workflow_trace"] = trace
    if trace.get("usage_records", 0) > 0:
        metadata["runtime"]["input_tokens"] = trace.get("all_agent_input_tokens")
        metadata["runtime"]["output_tokens"] = trace.get("all_agent_output_tokens")
    (output_dir / "review-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def _quality_result(oracle: dict, review: dict, fixture: dict) -> dict:
    expected = oracle["expected_findings"]
    actual = review["findings"]
    matched: set[int] = set()
    true_positive = 0
    for wanted in expected:
        for index, finding in enumerate(actual):
            if index in matched:
                continue
            if (
                wanted["category"] == finding["category"]
                and wanted["rule_id"] == finding["rule_id"]
                and wanted["path"] == finding["path"]
                and wanted["severity"] == finding["severity"]
                and measurement._line_ranges_overlap(wanted, finding)
            ):
                matched.add(index)
                true_positive += 1
                break
    rule_ids = {
        rule["rule_id"]
        for source in fixture["rules"]
        for rule in source["rules"]
    }
    finding_categories = {finding["category"] for finding in actual}
    scope_violations = sum(1 for finding in actual if finding["rule_id"] not in rule_ids)
    summary_violations = sum(
        1
        for category in measurement.CATEGORIES
        if review["summary"][category]
        != ("fail" if category in finding_categories else "pass")
    )
    return {
        "observed": True,
        "expected_findings": len(expected),
        "true_positive": true_positive,
        "false_positive": len(actual) - len(matched),
        "false_negative": len(expected) - true_positive,
        "path_accuracy": sum(1 for item in expected if any(item["path"] == finding["path"] for finding in actual)),
        "line_accuracy": sum(1 for item in expected if any(item["path"] == finding["path"] and measurement._line_ranges_overlap(item, finding) for finding in actual)),
        "category_accuracy": sum(1 for item in expected if any(item["path"] == finding["path"] and measurement._line_ranges_overlap(item, finding) and item["category"] == finding["category"] for finding in actual)),
        "clean_control_major_false_positive": sum(1 for finding in actual if oracle["clean_control"] and finding["severity"] == "major"),
        "scope_violation_count": scope_violations,
        "review_contract_violation": scope_violations + summary_violations,
        "summary_complete": set(review["summary"]) == set(measurement.CATEGORIES),
    }


def _quality(case_id: str, review_output: Path, metadata: dict) -> tuple[dict, str | None, str]:
    fixture = measurement.validate_fixture_input(
        _load(INSTANCE_ROOT / f"cases/{case_id}/r1/input.json"), case_id
    )
    oracle = measurement.validate_fixture_oracle(
        _load(INSTANCE_ROOT / f"cases/{case_id}/r1/oracle.json"), fixture
    )
    empty = {
        "observed": False,
        "expected_findings": len(oracle["expected_findings"]),
        "true_positive": 0,
        "false_positive": 0,
        "false_negative": len(oracle["expected_findings"]),
        "path_accuracy": 0,
        "line_accuracy": 0,
        "category_accuracy": 0,
        "clean_control_major_false_positive": 0,
        "scope_violation_count": 0,
        "review_contract_violation": 0,
        "summary_complete": False,
    }
    if metadata.get("action_conclusion") != "success":
        return empty, None, "execution_failed"
    if not metadata.get("output_valid") or not review_output.is_file():
        return empty, None, "invalid_output"
    review = measurement.validate_review_output(_load(review_output))
    quality = _quality_result(oracle, review, fixture)
    quality_status = (
        "pass"
        if quality["false_negative"] == quality["false_positive"] == quality["review_contract_violation"] == 0
        else "quality_failed"
    )
    return quality, quality_status, quality_status


def _measurement(metadata: dict, model_requested: str) -> dict:
    runtime = metadata.get("runtime", {})
    trace = metadata.get("workflow_trace", {})
    value = {
        "action_completed": metadata.get("action_conclusion") == "success",
        "structured_output_valid": metadata.get("output_valid") is True,
        "reported_model_matches_requested": runtime.get("model") == model_requested,
        "all_agent_tokens_complete": runtime.get("input_tokens") is not None and runtime.get("output_tokens") is not None,
        "elapsed_time_complete": isinstance(metadata.get("action_step_ms"), int),
        "fixture_access_observed": trace.get("fixture_tool_access_observed") is True,
        "fixture_permission_denials": trace.get("fixture_tool_permission_denials", 0),
    }
    value["state"] = "satisfied" if all((
        value["action_completed"],
        value["structured_output_valid"],
        value["reported_model_matches_requested"],
        value["all_agent_tokens_complete"],
        value["elapsed_time_complete"],
        value["fixture_access_observed"],
        value["fixture_permission_denials"] == 0,
        trace.get("complete") is True,
    )) else "unsatisfied"
    return value


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
    profile, _ = validate_preflight(case_id)
    fixture = measurement.validate_fixture_input(
        _load(INSTANCE_ROOT / f"cases/{case_id}/r1/input.json"), case_id
    )
    metadata = _load(review_metadata)
    prepared = measurement.validate_prepare_metadata(_load(prepare_metadata), case_id, VARIANT)
    quality, quality_status, result = _quality(case_id, review_output, metadata)
    qualification = _measurement(metadata, model_requested)
    if qualification["state"] != "satisfied" and result in {"pass", "quality_failed"}:
        result = "measurement_incomplete"
    runtime = metadata.get("runtime", {})
    total_tokens = None
    if runtime.get("input_tokens") is not None and runtime.get("output_tokens") is not None:
        total_tokens = runtime["input_tokens"] + runtime["output_tokens"]
    run = {
        "schema_version": 13,
        "comparison_revision": COMPARISON_REVISION,
        "profile_id": PROFILE_ID,
        "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:{case_id}:{VARIANT}:r1:a{attempt}",
        "case_id": case_id,
        "fixture_revision": "r1",
        "variant": VARIANT,
        "repetition": 1,
        "attempt": attempt,
        "base_sha": fixture["pr"]["base_sha"],
        "head_sha": fixture["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": runtime.get("model")},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"],
        "workflow_revision": WORKFLOW_REVISION,
        "workflow_trace": metadata.get("workflow_trace", {}),
        "measurement_qualification": qualification,
        "github_run_id": github_run_id,
        "timing": {
            "queue_ms": None, "setup_ms": None, "input_ms": prepared["input_ms"],
            "action_step_ms": metadata.get("action_step_ms"), "review_ms": runtime.get("duration_ms"),
            "report_ms": None, "execution_ms": metadata.get("action_step_ms"), "e2e_ms": None,
        },
        "runtime": {
            "turns": runtime.get("turns"), "input_tokens": runtime.get("input_tokens"),
            "output_tokens": runtime.get("output_tokens"), "total_tokens": total_tokens,
            "reported_cost_usd": runtime.get("reported_cost_usd"),
        },
        "quality": quality,
        "quality_score": measurement._quality_score(quality_status, quality) if quality_status else None,
        "result": result,
    }
    measurement._write_json_once(output, run)
    return run


def record_terminal(case_id: str, attempt: int, model_requested: str, status: str, output: Path, github_run_id: str) -> dict:
    profile, _ = validate_preflight(case_id)
    fixture = _load(INSTANCE_ROOT / f"cases/{case_id}/r1/input.json")
    expected = len(_load(INSTANCE_ROOT / f"cases/{case_id}/r1/oracle.json")["expected_findings"])
    run = {
        "schema_version": 13, "comparison_revision": COMPARISON_REVISION,
        "profile_id": PROFILE_ID, "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:{case_id}:{VARIANT}:r1:a{attempt}",
        "case_id": case_id, "fixture_revision": "r1", "variant": VARIANT,
        "repetition": 1, "attempt": attempt, "base_sha": fixture["pr"]["base_sha"],
        "head_sha": fixture["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": None},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"],
        "workflow_revision": WORKFLOW_REVISION, "workflow_trace": {"complete": False},
        "measurement_qualification": {"state": "unsatisfied"}, "github_run_id": github_run_id,
        "timing": {key: None for key in ("queue_ms", "setup_ms", "input_ms", "action_step_ms", "review_ms", "report_ms", "execution_ms", "e2e_ms")},
        "runtime": {key: None for key in ("turns", "input_tokens", "output_tokens", "total_tokens", "reported_cost_usd")},
        "quality": {"observed": False, "expected_findings": expected, "true_positive": 0, "false_positive": 0, "false_negative": expected, "path_accuracy": 0, "line_accuracy": 0, "category_accuracy": 0, "clean_control_major_false_positive": 0, "scope_violation_count": 0, "review_contract_violation": 0, "summary_complete": False},
        "quality_score": None, "result": status,
    }
    measurement._write_json_once(output, run)
    return run


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate-preflight", "prepare"):
        item = sub.add_parser(name)
        item.add_argument("--case-id", required=True, choices=CASES)
        if name == "prepare":
            item.add_argument("--output-dir", required=True, type=Path)
    collect = sub.add_parser("collect")
    collect.add_argument("--raw-output", required=True, type=Path)
    collect.add_argument("--action-conclusion", required=True)
    collect.add_argument("--execution-file", type=Path)
    collect.add_argument("--hook-file", type=Path)
    collect.add_argument("--started-ms", required=True, type=int)
    collect.add_argument("--finished-ms", required=True, type=int)
    collect.add_argument("--model-requested", required=True)
    collect.add_argument("--output-dir", required=True, type=Path)
    for name in ("grade", "record-terminal"):
        item = sub.add_parser(name)
        item.add_argument("--case-id", required=True, choices=CASES)
        item.add_argument("--attempt", required=True, type=int)
        item.add_argument("--model-requested", required=True)
        item.add_argument("--github-run-id", required=True)
        item.add_argument("--output", required=True, type=Path)
        if name == "grade":
            item.add_argument("--review-output", required=True, type=Path)
            item.add_argument("--review-metadata", required=True, type=Path)
            item.add_argument("--prepare-metadata", required=True, type=Path)
        else:
            item.add_argument("--status", required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate-preflight":
            validate_preflight(args.case_id)
            print("control-free qualification preflight is valid")
        elif args.command == "prepare":
            print(json.dumps(prepare_input(args.case_id, args.output_dir), ensure_ascii=False))
        elif args.command == "collect":
            print(json.dumps(collect_review(args.raw_output, args.action_conclusion, args.execution_file, args.hook_file, args.started_ms, args.finished_ms, args.model_requested, args.output_dir), ensure_ascii=False))
        elif args.command == "grade":
            print(json.dumps(grade_run(args.case_id, args.attempt, args.model_requested, args.review_output, args.review_metadata, args.prepare_metadata, args.output, args.github_run_id), ensure_ascii=False))
        else:
            print(json.dumps(record_terminal(args.case_id, args.attempt, args.model_requested, args.status, args.output, args.github_run_id), ensure_ascii=False))
    except (QualificationError, measurement.ValidationError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
