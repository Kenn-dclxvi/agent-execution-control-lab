#!/usr/bin/env python3
"""Prepare, collect, and grade held-out Opus relationship-reviewer runs."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

import pr_review_held_out_control_free as held_out
import pr_review_relationship_role_calibration as relationship


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-held-out-relationship-reviewer-opus-three-n1-r1"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-measure-held-out-relationship-reviewer-opus.yml"
WORKFLOW_REVISION = "pr-review-measure-held-out-relationship-reviewer-opus-r1"
COMPARISON_REVISION = "pr-review-held-out-workflow-topology-comparison-r1"
RATING_ID = "pr-review-finding-quality-v9"
VARIANT = "held-out-relationship-reviewer-opus"
ROOT_MODEL = "claude-sonnet-5"
REVIEWER_MODEL = "opus"
CASES = held_out.CASES


class ComparisonError(ValueError):
    pass


def _load(path: Path) -> dict:
    return held_out._load(path)


def _sha(path: Path) -> str:
    return held_out._sha(path)


def _artifact_path(relative_path: str) -> Path:
    return REPOSITORY_ROOT / relative_path if relative_path.startswith(".github/") else INSTANCE_ROOT / relative_path


def validate_preflight(case_id: str) -> tuple[dict, dict]:
    held_out._fixture_and_oracle(case_id)
    profile = _load(PROFILE_PATH)
    preflight = _load(PREFLIGHT_PATH)
    expected_cases = [{"id": item, "revision": "r2"} for item in CASES]
    if profile.get("profile_id") != PROFILE_ID or profile.get("state") != "frozen_not_executed":
        raise ComparisonError("profile identity mismatch")
    if profile.get("purpose") != "held_out_workflow_topology_comparison" or profile.get("cases") != expected_cases:
        raise ComparisonError("profile scope mismatch")
    conditions = profile.get("comparison_conditions", {})
    if conditions.get("variant") != VARIANT or conditions.get("relationship_reviewer_model") != REVIEWER_MODEL:
        raise ComparisonError("profile variant mismatch")
    if conditions.get("model", {}).get("requested") != ROOT_MODEL or conditions.get("model", {}).get("relationship_reviewer") != REVIEWER_MODEL:
        raise ComparisonError("model role mismatch")
    executor = conditions.get("executor_parameters", {})
    if executor.get("max_workers") != 24 or executor.get("dispatch_concurrency") != 3:
        raise ComparisonError("executor concurrency mismatch")
    prompt = conditions.get("prompt", {})
    template_path = _artifact_path(prompt.get("template_path", ""))
    effective = template_path.read_text(encoding="utf-8").replace("{{RELATIONSHIP_REVIEWER_MODEL}}", REVIEWER_MODEL)
    if _sha(template_path) != prompt.get("template_sha256"):
        raise ComparisonError("prompt template mismatch")
    if hashlib.sha256(effective.encode("utf-8")).hexdigest() != prompt.get("effective_content_sha256"):
        raise ComparisonError("effective prompt mismatch")
    for artifact in conditions.get("bound_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise ComparisonError(f"profile artifact mismatch: {artifact.get('path')}")
    binding = conditions.get("case_bindings", {}).get(case_id)
    if not isinstance(binding, dict):
        raise ComparisonError("case binding is missing")
    for key in ("input", "oracle", "snapshot", "authority", "eligibility"):
        artifact = binding.get(key, {})
        path = _artifact_path(artifact.get("path", ""))
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise ComparisonError(f"case artifact mismatch: {case_id}.{key}")
    expected_profile = {"profile_id": PROFILE_ID, "path": f"profiles/{PROFILE_PATH.name}", "sha256": _sha(PROFILE_PATH)}
    if preflight.get("state") != "ready_not_executed" or preflight.get("profile") != expected_profile:
        raise ComparisonError("preflight profile receipt mismatch")
    slot = {"case_id": case_id, "fixture_revision": "r2", "variant": VARIANT, "repetition": 1}
    if slot not in preflight.get("planned_slots", []):
        raise ComparisonError("slot is not in the fixed plan")
    for artifact in preflight.get("verified_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise ComparisonError(f"preflight artifact mismatch: {artifact.get('path')}")
    admission = _load(INSTANCE_ROOT / "contracts/pr-review-held-out-control-free-three-admission-r2.json")
    if admission.get("state") != "satisfied_for_comparison_preflight":
        raise ComparisonError("Control-Free admission mismatch")
    baseline = _load(INSTANCE_ROOT / "profiles/pr-review-held-out-control-free-three-n1-r1.json")
    baseline_conditions = baseline.get("comparison_conditions", {})
    common_pairs = (
        (profile.get("cases"), baseline.get("cases"), "cases"),
        (profile.get("evaluation_set"), baseline.get("evaluation_set"), "evaluation set"),
        (conditions.get("target_repository_ref"), baseline_conditions.get("target_repository_ref"), "target repository ref"),
        (conditions.get("case_bindings"), baseline_conditions.get("case_bindings"), "case bindings"),
        (conditions.get("task_spec", {}).get("source"), baseline_conditions.get("task_spec", {}).get("source"), "TaskSpec source"),
        (conditions.get("task_spec", {}).get("functional_specification"), baseline_conditions.get("task_spec", {}).get("functional_specification"), "functional specification"),
        (conditions.get("task_spec", {}).get("required_outcome"), baseline_conditions.get("task_spec", {}).get("required_outcome"), "required outcome"),
        ({key: conditions.get("review_contract", {}).get(key) for key in ("revision", "path", "sha256")}, {"revision": baseline_conditions.get("review_contract", {}).get("revision"), "path": baseline_conditions.get("review_contract", {}).get("path"), "sha256": _sha(INSTANCE_ROOT / baseline_conditions.get("review_contract", {}).get("path", ""))}, "review contract"),
        ({key: conditions.get("review_output_schema", {}).get(key) for key in ("revision", "path", "sha256")}, {"revision": baseline_conditions.get("review_output_schema", {}).get("revision"), "path": baseline_conditions.get("review_output_schema", {}).get("path"), "sha256": _sha(INSTANCE_ROOT / baseline_conditions.get("review_output_schema", {}).get("path", ""))}, "review output schema"),
        (conditions.get("quality_rating", {}).get("contract_id"), baseline_conditions.get("quality_rating", {}).get("contract_id"), "quality rating"),
        (conditions.get("model", {}).get("requested"), baseline_conditions.get("model", {}).get("requested"), "root model"),
        (conditions.get("agent_environment", {}).get("action_revision"), baseline_conditions.get("agent_environment", {}).get("action_revision"), "Action revision"),
        (conditions.get("agent_environment", {}).get("runner"), baseline_conditions.get("agent_environment", {}).get("runner"), "runner"),
        (conditions.get("agent_environment", {}).get("authentication"), baseline_conditions.get("agent_environment", {}).get("authentication"), "authentication"),
        (conditions.get("permission", {}).get("github"), baseline_conditions.get("permission", {}).get("github"), "GitHub permission"),
        (conditions.get("permission", {}).get("repository_write"), baseline_conditions.get("permission", {}).get("repository_write"), "repository write permission"),
        (conditions.get("permission", {}).get("github_comment_write"), baseline_conditions.get("permission", {}).get("github_comment_write"), "comment permission"),
        (executor.get("max_workers"), baseline_conditions.get("executor_parameters", {}).get("max_workers"), "max_workers"),
        (executor.get("dispatch_concurrency"), baseline_conditions.get("executor_parameters", {}).get("dispatch_concurrency"), "dispatch concurrency"),
        (executor.get("action_timeout_seconds"), baseline_conditions.get("executor_parameters", {}).get("action_timeout_seconds"), "Action timeout"),
        (executor.get("reviewer_job_timeout_seconds"), baseline_conditions.get("executor_parameters", {}).get("reviewer_job_timeout_seconds"), "reviewer timeout"),
        (executor.get("token_accounting"), baseline_conditions.get("executor_parameters", {}).get("token_accounting"), "token accounting"),
        (conditions.get("repetition_condition", {}).get("iterations_per_case"), baseline_conditions.get("repetition_condition", {}).get("iterations_per_case"), "iterations per case"),
    )
    for observed, expected, label in common_pairs:
        if observed != expected:
            raise ComparisonError(f"comparison compatibility mismatch: {label}")
    if preflight.get("compatibility", {}).get("mechanical_diff_state") != "satisfied":
        raise ComparisonError("comparison compatibility receipt mismatch")
    for result in conditions.get("reused_control_free_results", []):
        path = _artifact_path(result["path"])
        if not path.is_file() or _sha(path) != result.get("sha256"):
            raise ComparisonError(f"saved Control-Free result mismatch: {result.get('case_id')}")
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
    prompt_path = output_dir / "core-prompt.md"
    prompt_path.write_text(prompt_path.read_text(encoding="utf-8").replace("{{RELATIONSHIP_REVIEWER_MODEL}}", REVIEWER_MODEL), encoding="utf-8")
    shutil.copyfile(INSTANCE_ROOT / "tools/pr_review_held_out_control_free.py", output_dir / "pr_review_held_out_control_free.py")
    shutil.copyfile(INSTANCE_ROOT / "tools/pr_review_relationship_role_calibration.py", output_dir / "pr_review_relationship_role_calibration.py")
    metadata.update(profile_id=PROFILE_ID, variant=VARIANT, relationship_reviewer_model=REVIEWER_MODEL, prompt_sha256=_sha(prompt_path))
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
        raise ComparisonError("prepare metadata identity mismatch")
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
        "schema_version": 17,
        "comparison_revision": COMPARISON_REVISION,
        "profile_id": PROFILE_ID,
        "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:{case_id}:{VARIANT}:r1:a{attempt}",
        "case_id": case_id,
        "fixture_revision": "r2",
        "variant": VARIANT,
        "relationship_reviewer_model": REVIEWER_MODEL,
        "repetition": 1,
        "attempt": attempt,
        "base_sha": fixture["pr"]["base_sha"],
        "head_sha": fixture["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": runtime.get("model")},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"],
        "workflow_revision": WORKFLOW_REVISION,
        "workflow_trace": metadata.get("workflow_trace", {}),
        "measurement_qualification": measurement,
        "github_run_id": github_run_id,
        "timing": {"queue_ms": None, "setup_ms": None, "input_ms": prepared.get("input_ms"), "action_step_ms": metadata.get("action_step_ms"), "review_ms": runtime.get("duration_ms"), "report_ms": None, "execution_ms": metadata.get("action_step_ms"), "e2e_ms": None},
        "runtime": {"turns": runtime.get("turns"), "input_tokens": runtime.get("input_tokens"), "output_tokens": runtime.get("output_tokens"), "total_tokens": total_tokens, "reported_cost_usd": runtime.get("reported_cost_usd")},
        "quality": quality,
        "quality_score": held_out.free.core.measurement._quality_score(quality_status, quality) if quality_status is not None else None,
        "result": result,
    }
    held_out.free.core.legacy._write_json_once(output, run)
    return run


def record_terminal(case_id: str, attempt: int, model_requested: str, status: str, output: Path, github_run_id: str) -> dict:
    profile, _ = validate_preflight(case_id)
    fixture, oracle = held_out._fixture_and_oracle(case_id)
    run = {
        "schema_version": 17, "comparison_revision": COMPARISON_REVISION, "profile_id": PROFILE_ID, "quality_rating_contract": RATING_ID,
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
            print("held-out Opus relationship-reviewer preflight is valid")
        elif args.command == "prepare":
            print(json.dumps(prepare_input(args.case_id, args.output_dir), ensure_ascii=False))
        elif args.command == "collect":
            print(json.dumps(collect_review(args.raw_output, args.action_conclusion, args.execution_file, args.hook_file, args.started_ms, args.finished_ms, args.model_requested, args.review_input, args.output_dir), ensure_ascii=False))
        elif args.command == "grade":
            print(json.dumps(grade_run(args.case_id, args.attempt, args.model_requested, args.review_output, args.review_metadata, args.prepare_metadata, args.output, args.github_run_id), ensure_ascii=False))
        else:
            print(json.dumps(record_terminal(args.case_id, args.attempt, args.model_requested, args.status, args.output, args.github_run_id), ensure_ascii=False))
    except (ComparisonError, held_out.QualificationError, relationship.CalibrationError, held_out.free.CalibrationError, held_out.free.core.QualificationError, held_out.free.core.legacy.QualificationError, held_out.free.core.measurement.ValidationError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
