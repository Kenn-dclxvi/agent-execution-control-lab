#!/usr/bin/env python3
"""Prepare, collect, and grade the fixed C02 finding-admission calibration."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

import pr_review_held_out_control_free as held_out
import pr_review_held_out_relationship_reviewer as relationship_run
import pr_review_relationship_role_calibration as relationship


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-c02-relationship-reviewer-opus-finding-admission-n1-r1"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
BASELINE_PROFILE_PATH = INSTANCE_ROOT / "profiles/pr-review-held-out-relationship-reviewer-opus-three-n1-r1.json"
BASELINE_RESULT_PATH = INSTANCE_ROOT / "results/pr-review-held-out-workflow-topology-comparison-r1-prr-c02-held-out-relationship-reviewer-opus-r1-a31292887371.json"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-calibrate-c02-finding-admission.yml"
WORKFLOW_REVISION = "pr-review-calibrate-c02-finding-admission-r1"
COMPARISON_REVISION = "pr-review-c02-finding-admission-calibration-r1"
RATING_ID = "pr-review-finding-quality-v9"
VARIANT = "c02-relationship-reviewer-opus-finding-admission"
ROOT_MODEL = "claude-sonnet-5"
REVIEWER_MODEL = "opus"
CASES = ("PRR-C02",)


class CalibrationError(ValueError):
    pass


def _load(path: Path) -> dict:
    return held_out._load(path)


def _sha(path: Path) -> str:
    return held_out._sha(path)


def _artifact_path(relative_path: str) -> Path:
    return REPOSITORY_ROOT / relative_path if relative_path.startswith(".github/") else INSTANCE_ROOT / relative_path


def validate_preflight(case_id: str) -> tuple[dict, dict]:
    if case_id != "PRR-C02":
        raise CalibrationError("only the fixed PRR-C02 slot is allowed")
    held_out._fixture_and_oracle(case_id)
    profile = _load(PROFILE_PATH)
    baseline_profile = _load(BASELINE_PROFILE_PATH)
    baseline_result = _load(BASELINE_RESULT_PATH)
    preflight = _load(PREFLIGHT_PATH)
    if profile.get("profile_id") != PROFILE_ID or profile.get("state") != "frozen_not_executed":
        raise CalibrationError("profile identity mismatch")
    if profile.get("purpose") != "c02_finding_admission_development_calibration" or profile.get("cases") != [{"id": "PRR-C02", "revision": "r2"}]:
        raise CalibrationError("profile scope mismatch")
    conditions = profile.get("comparison_conditions", {})
    baseline = baseline_profile.get("comparison_conditions", {})
    if conditions.get("variant") != VARIANT or conditions.get("relationship_reviewer_model") != REVIEWER_MODEL:
        raise CalibrationError("profile variant mismatch")
    if conditions.get("model", {}).get("requested") != ROOT_MODEL or conditions.get("model", {}).get("relationship_reviewer") != REVIEWER_MODEL:
        raise CalibrationError("model role mismatch")
    executor = conditions.get("executor_parameters", {})
    if executor.get("max_workers") != 24 or executor.get("dispatch_concurrency") != 1:
        raise CalibrationError("executor concurrency mismatch")
    for artifact in conditions.get("bound_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise CalibrationError(f"profile artifact mismatch: {artifact.get('path')}")
    binding = conditions.get("case_bindings", {}).get(case_id)
    if not isinstance(binding, dict):
        raise CalibrationError("case binding is missing")
    for key in ("input", "oracle", "snapshot", "authority", "eligibility"):
        artifact = binding.get(key, {})
        path = _artifact_path(artifact.get("path", ""))
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise CalibrationError(f"case artifact mismatch: {case_id}.{key}")
    common_pairs = (
        (conditions.get("target_repository_ref"), baseline.get("target_repository_ref"), "target repository ref"),
        (binding, baseline.get("case_bindings", {}).get(case_id), "case binding"),
        (conditions.get("task_spec", {}).get("source"), baseline.get("task_spec", {}).get("source"), "TaskSpec source"),
        (conditions.get("task_spec", {}).get("functional_specification"), baseline.get("task_spec", {}).get("functional_specification"), "functional specification"),
        (conditions.get("task_spec", {}).get("required_outcome"), baseline.get("task_spec", {}).get("required_outcome"), "required outcome"),
        (conditions.get("quality_rating"), baseline.get("quality_rating"), "quality rating"),
        (conditions.get("review_contract"), baseline.get("review_contract"), "review contract"),
        (conditions.get("review_output_schema"), baseline.get("review_output_schema"), "review output schema"),
        (conditions.get("model"), baseline.get("model"), "model and topology"),
        (conditions.get("agent_environment"), baseline.get("agent_environment"), "agent environment"),
        (conditions.get("permission"), baseline.get("permission"), "permission"),
        (executor.get("max_attempts_per_case"), baseline.get("executor_parameters", {}).get("max_attempts_per_case"), "max attempts"),
        (executor.get("max_turns"), baseline.get("executor_parameters", {}).get("max_turns"), "max turns"),
        (executor.get("turn_limit_source"), baseline.get("executor_parameters", {}).get("turn_limit_source"), "turn limit source"),
        (executor.get("max_workers"), baseline.get("executor_parameters", {}).get("max_workers"), "max workers"),
        (executor.get("internal_review_topology"), baseline.get("executor_parameters", {}).get("internal_review_topology"), "review topology"),
        (executor.get("action_timeout_seconds"), baseline.get("executor_parameters", {}).get("action_timeout_seconds"), "Action timeout"),
        (executor.get("reviewer_job_timeout_seconds"), baseline.get("executor_parameters", {}).get("reviewer_job_timeout_seconds"), "reviewer timeout"),
        (executor.get("token_accounting"), baseline.get("executor_parameters", {}).get("token_accounting"), "token accounting"),
        (conditions.get("measurement_gate"), baseline.get("measurement_gate"), "measurement gate"),
        (conditions.get("kpis"), baseline.get("kpis"), "KPIs"),
    )
    for observed, expected, label in common_pairs:
        if observed != expected:
            raise CalibrationError(f"comparison compatibility mismatch: {label}")
    if baseline_result.get("result_id") != conditions.get("baseline_result", {}).get("result_id") or _sha(BASELINE_RESULT_PATH) != conditions.get("baseline_result", {}).get("sha256"):
        raise CalibrationError("saved baseline result mismatch")
    if baseline_result.get("measurement_qualification", {}).get("state") != "satisfied":
        raise CalibrationError("saved baseline measurement is not satisfied")
    expected_profile = {"profile_id": PROFILE_ID, "path": f"profiles/{PROFILE_PATH.name}", "sha256": _sha(PROFILE_PATH)}
    if preflight.get("state") != "ready_not_executed" or preflight.get("profile") != expected_profile:
        raise CalibrationError("preflight profile receipt mismatch")
    slot = {"case_id": case_id, "fixture_revision": "r2", "variant": VARIANT, "repetition": 1}
    if preflight.get("planned_slots") != [slot] or preflight.get("compatibility", {}).get("mechanical_diff_state") != "satisfied":
        raise CalibrationError("fixed calibration slot mismatch")
    for artifact in preflight.get("verified_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise CalibrationError(f"preflight artifact mismatch: {artifact.get('path')}")
    return profile, preflight


def prepare_input(case_id: str, output_dir: Path) -> dict:
    original = {
        "profile_id": held_out.PROFILE_ID,
        "profile_path": held_out.PROFILE_PATH,
        "preflight_path": held_out.PREFLIGHT_PATH,
        "workflow_path": held_out.WORKFLOW_PATH,
        "file": held_out.__file__,
        "validate": held_out.validate_preflight,
    }
    held_out.PROFILE_ID = PROFILE_ID
    held_out.PROFILE_PATH = PROFILE_PATH
    held_out.PREFLIGHT_PATH = PREFLIGHT_PATH
    held_out.WORKFLOW_PATH = WORKFLOW_PATH
    held_out.__file__ = __file__
    held_out.validate_preflight = validate_preflight
    try:
        metadata = held_out.prepare_input(case_id, output_dir)
    finally:
        held_out.PROFILE_ID = original["profile_id"]
        held_out.PROFILE_PATH = original["profile_path"]
        held_out.PREFLIGHT_PATH = original["preflight_path"]
        held_out.WORKFLOW_PATH = original["workflow_path"]
        held_out.__file__ = original["file"]
        held_out.validate_preflight = original["validate"]
    shutil.copyfile(INSTANCE_ROOT / "tools/pr_review_held_out_control_free.py", output_dir / "pr_review_held_out_control_free.py")
    shutil.copyfile(INSTANCE_ROOT / "tools/pr_review_held_out_relationship_reviewer.py", output_dir / "pr_review_held_out_relationship_reviewer.py")
    shutil.copyfile(INSTANCE_ROOT / "tools/pr_review_relationship_role_calibration.py", output_dir / "pr_review_relationship_role_calibration.py")
    metadata.update(profile_id=PROFILE_ID, variant=VARIANT, relationship_reviewer_model=REVIEWER_MODEL)
    (output_dir / "prepare-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return metadata


def collect_review(raw_output: Path, action_conclusion: str, execution_file: Path | None, hook_file: Path | None, started_ms: int, finished_ms: int, model_requested: str, review_input: Path, output_dir: Path) -> dict:
    return relationship.collect_review(raw_output, action_conclusion, execution_file, hook_file, started_ms, finished_ms, model_requested, REVIEWER_MODEL, review_input, output_dir)


def grade_run(case_id: str, attempt: int, model_requested: str, review_output: Path, review_metadata: Path, prepare_metadata: Path, output: Path, github_run_id: str) -> dict:
    profile, _ = validate_preflight(case_id)
    fixture, oracle = held_out._fixture_and_oracle(case_id)
    metadata = _load(review_metadata)
    prepared = _load(prepare_metadata)
    if prepared.get("case_id") != case_id or prepared.get("profile_id") != PROFILE_ID:
        raise CalibrationError("prepare metadata identity mismatch")
    quality = held_out._empty_quality(len(oracle["expected_findings"]))
    quality_status = None
    if metadata.get("action_conclusion") != "success":
        result = "execution_failed"
    elif not metadata.get("output_valid") or not review_output.is_file():
        result = "invalid_output"
    else:
        review = held_out.free.core.measurement.validate_review_output_v2(_load(review_output), set(fixture["changed_paths"]))
        quality = held_out.free.core.legacy._quality_result(oracle, review, fixture)
        quality_status = "pass" if quality["false_negative"] == quality["false_positive"] == quality["review_contract_violation"] == 0 else "quality_failed"
        result = quality_status
    measurement = relationship._measurement_qualification(metadata, model_requested)
    if measurement["state"] != "satisfied" and result in {"pass", "quality_failed"}:
        result = "measurement_incomplete"
    runtime = metadata.get("runtime", {})
    total_tokens = runtime.get("input_tokens") + runtime.get("output_tokens") if runtime.get("input_tokens") is not None and runtime.get("output_tokens") is not None else None
    run = {
        "schema_version": 18, "comparison_revision": COMPARISON_REVISION, "profile_id": PROFILE_ID, "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:{case_id}:{VARIANT}:r1:a{attempt}", "case_id": case_id, "fixture_revision": "r2", "variant": VARIANT, "relationship_reviewer_model": REVIEWER_MODEL,
        "repetition": 1, "attempt": attempt, "base_sha": fixture["pr"]["base_sha"], "head_sha": fixture["pr"]["head_sha"], "model": {"requested": model_requested, "reported": runtime.get("model")},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"], "workflow_revision": WORKFLOW_REVISION, "workflow_trace": metadata.get("workflow_trace", {}), "measurement_qualification": measurement, "github_run_id": github_run_id,
        "timing": {"queue_ms": None, "setup_ms": None, "input_ms": prepared.get("input_ms"), "action_step_ms": metadata.get("action_step_ms"), "review_ms": runtime.get("duration_ms"), "report_ms": None, "execution_ms": metadata.get("action_step_ms"), "e2e_ms": None},
        "runtime": {"turns": runtime.get("turns"), "input_tokens": runtime.get("input_tokens"), "output_tokens": runtime.get("output_tokens"), "total_tokens": total_tokens, "reported_cost_usd": runtime.get("reported_cost_usd")},
        "quality": quality, "quality_score": held_out.free.core.measurement._quality_score(quality_status, quality) if quality_status is not None else None, "result": result,
    }
    held_out.free.core.legacy._write_json_once(output, run)
    return run


def record_terminal(case_id: str, attempt: int, model_requested: str, status: str, output: Path, github_run_id: str) -> dict:
    profile, _ = validate_preflight(case_id)
    fixture, oracle = held_out._fixture_and_oracle(case_id)
    run = {
        "schema_version": 18, "comparison_revision": COMPARISON_REVISION, "profile_id": PROFILE_ID, "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:{case_id}:{VARIANT}:r1:a{attempt}", "case_id": case_id, "fixture_revision": "r2", "variant": VARIANT, "relationship_reviewer_model": REVIEWER_MODEL,
        "repetition": 1, "attempt": attempt, "base_sha": fixture["pr"]["base_sha"], "head_sha": fixture["pr"]["head_sha"], "model": {"requested": model_requested, "reported": None},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"], "workflow_revision": WORKFLOW_REVISION, "workflow_trace": {"complete": False}, "measurement_qualification": {"state": "unsatisfied"}, "github_run_id": github_run_id,
        "timing": {key: None for key in ("queue_ms", "setup_ms", "input_ms", "action_step_ms", "review_ms", "report_ms", "execution_ms", "e2e_ms")},
        "runtime": {key: None for key in ("turns", "input_tokens", "output_tokens", "total_tokens", "reported_cost_usd")}, "quality": held_out._empty_quality(len(oracle["expected_findings"])), "quality_score": None, "result": status,
    }
    held_out.free.core.legacy._write_json_once(output, run)
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
    for name in ("raw-output", "execution-file", "hook-file", "review-input", "output-dir"):
        collect.add_argument(f"--{name}", type=Path, required=name not in {"execution-file", "hook-file"})
    for name in ("action-conclusion", "model-requested"):
        collect.add_argument(f"--{name}", required=True)
    for name in ("started-ms", "finished-ms"):
        collect.add_argument(f"--{name}", required=True, type=int)
    for command in ("grade", "record-terminal"):
        item = sub.add_parser(command)
        item.add_argument("--case-id", required=True, choices=CASES)
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
    try:
        if args.command == "validate-preflight":
            validate_preflight(args.case_id)
            print("C02 finding-admission calibration preflight is valid")
        elif args.command == "prepare":
            print(json.dumps(prepare_input(args.case_id, args.output_dir), ensure_ascii=False))
        elif args.command == "collect":
            print(json.dumps(collect_review(args.raw_output, args.action_conclusion, args.execution_file, args.hook_file, args.started_ms, args.finished_ms, args.model_requested, args.review_input, args.output_dir), ensure_ascii=False))
        elif args.command == "grade":
            print(json.dumps(grade_run(args.case_id, args.attempt, args.model_requested, args.review_output, args.review_metadata, args.prepare_metadata, args.output, args.github_run_id), ensure_ascii=False))
        else:
            print(json.dumps(record_terminal(args.case_id, args.attempt, args.model_requested, args.status, args.output, args.github_run_id), ensure_ascii=False))
    except (CalibrationError, relationship_run.ComparisonError, held_out.QualificationError, relationship.CalibrationError, held_out.free.CalibrationError, held_out.free.core.QualificationError, held_out.free.core.legacy.QualificationError, held_out.free.core.measurement.ValidationError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
