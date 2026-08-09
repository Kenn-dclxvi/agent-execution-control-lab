#!/usr/bin/env python3
"""Measure the C02 Prompt Variant Evidence Scope development slot."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

import pr_review_c02_finding_admission as base
import pr_review_held_out_control_free as held_out
import pr_review_relationship_role_calibration as relationship


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-measurement-c02-evidence-scope-n1-r1"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
BASELINE_PROFILE_PATH = INSTANCE_ROOT / "profiles/pr-review-c02-relationship-reviewer-opus-finding-admission-n1-r1.json"
BASELINE_RESULT_PATH = INSTANCE_ROOT / "results/pr-review-c02-finding-admission-calibration-r1-prr-c02-c02-relationship-reviewer-opus-finding-admission-r1-a31295440716.json"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-measure-c02-evidence-scope.yml"
WORKFLOW_REVISION = "pr-review-measure-c02-evidence-scope-r1"
COMPARISON_REVISION = "pr-review-measurement-c02-evidence-scope-r1"
RATING_ID = "pr-review-finding-quality-v9"
VARIANT = "prompt-evidence-scope"
ROOT_MODEL = "claude-sonnet-5"
REVIEWER_MODEL = "opus"
CASES = ("PRR-C02",)
REQUIRED_INITIAL_READS = 7


class MeasurementError(ValueError):
    pass


def _load(path: Path) -> dict:
    return held_out._load(path)


def _sha(path: Path) -> str:
    return held_out._sha(path)


def _artifact_path(relative_path: str) -> Path:
    return REPOSITORY_ROOT / relative_path if relative_path.startswith(".github/") else INSTANCE_ROOT / relative_path


def validate_preflight(case_id: str) -> tuple[dict, dict]:
    if case_id != "PRR-C02":
        raise MeasurementError("only Case PRR-C02 is allowed")
    held_out._fixture_and_oracle(case_id)
    profile = _load(PROFILE_PATH)
    baseline_profile = _load(BASELINE_PROFILE_PATH)
    baseline_result = _load(BASELINE_RESULT_PATH)
    preflight = _load(PREFLIGHT_PATH)
    if profile.get("profile_id") != PROFILE_ID or profile.get("state") != "frozen_not_executed":
        raise MeasurementError("Profile identity mismatch")
    if profile.get("purpose") != "c02_evidence_scope_development_measurement" or profile.get("cases") != [{"id": case_id, "revision": "r2"}]:
        raise MeasurementError("Measurement Series scope mismatch")
    conditions = profile.get("comparison_conditions", {})
    baseline = baseline_profile.get("comparison_conditions", {})
    if conditions.get("variant") != VARIANT or conditions.get("relationship_reviewer_model") != REVIEWER_MODEL:
        raise MeasurementError("Prompt Variant mismatch")
    if conditions.get("model", {}).get("requested") != ROOT_MODEL or conditions.get("model", {}).get("relationship_reviewer") != REVIEWER_MODEL:
        raise MeasurementError("model role mismatch")
    executor = conditions.get("executor_parameters", {})
    if executor.get("max_workers") != 24 or executor.get("dispatch_concurrency") != 1:
        raise MeasurementError("executor concurrency mismatch")
    for artifact in conditions.get("bound_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise MeasurementError(f"Profile artifact mismatch: {artifact.get('path')}")
    binding = conditions.get("case_bindings", {}).get(case_id)
    if not isinstance(binding, dict):
        raise MeasurementError("Case binding is missing")
    for key in ("input", "oracle", "snapshot", "authority", "eligibility"):
        artifact = binding.get(key, {})
        path = _artifact_path(artifact.get("path", ""))
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise MeasurementError(f"Case artifact mismatch: {case_id}.{key}")
    common_pairs = (
        (conditions.get("target_repository_ref"), baseline.get("target_repository_ref"), "target repository ref"),
        (binding, baseline.get("case_bindings", {}).get(case_id), "Case binding"),
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
            raise MeasurementError(f"comparison compatibility mismatch: {label}")
    expected_baseline = conditions.get("baseline_result", {})
    if baseline_result.get("result_id") != expected_baseline.get("result_id") or _sha(BASELINE_RESULT_PATH) != expected_baseline.get("sha256"):
        raise MeasurementError("saved baseline Run Result mismatch")
    if baseline_result.get("measurement_qualification", {}).get("state") != "satisfied" or baseline_result.get("quality_score") != 4:
        raise MeasurementError("saved baseline Run Result is not the fixed quality reference")
    expected_profile = {"profile_id": PROFILE_ID, "path": f"profiles/{PROFILE_PATH.name}", "sha256": _sha(PROFILE_PATH)}
    if preflight.get("state") != "ready_not_executed" or preflight.get("profile") != expected_profile:
        raise MeasurementError("preflight Profile receipt mismatch")
    slot = {"case_id": case_id, "fixture_revision": "r2", "variant": VARIANT, "repetition": 1}
    if preflight.get("planned_slots") != [slot] or preflight.get("compatibility", {}).get("mechanical_diff_state") != "satisfied":
        raise MeasurementError("fixed Measurement Series slot mismatch")
    for artifact in preflight.get("verified_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise MeasurementError(f"preflight artifact mismatch: {artifact.get('path')}")
    return profile, preflight


def _patch_base() -> dict:
    original = {
        "PROFILE_ID": base.PROFILE_ID,
        "PROFILE_PATH": base.PROFILE_PATH,
        "PREFLIGHT_PATH": base.PREFLIGHT_PATH,
        "WORKFLOW_PATH": base.WORKFLOW_PATH,
        "WORKFLOW_REVISION": base.WORKFLOW_REVISION,
        "COMPARISON_REVISION": base.COMPARISON_REVISION,
        "VARIANT": base.VARIANT,
        "file": base.__file__,
        "validate": base.validate_preflight,
    }
    base.PROFILE_ID = PROFILE_ID
    base.PROFILE_PATH = PROFILE_PATH
    base.PREFLIGHT_PATH = PREFLIGHT_PATH
    base.WORKFLOW_PATH = WORKFLOW_PATH
    base.WORKFLOW_REVISION = WORKFLOW_REVISION
    base.COMPARISON_REVISION = COMPARISON_REVISION
    base.VARIANT = VARIANT
    base.__file__ = __file__
    base.validate_preflight = validate_preflight
    return original


def _restore_base(original: dict) -> None:
    for key in ("PROFILE_ID", "PROFILE_PATH", "PREFLIGHT_PATH", "WORKFLOW_PATH", "WORKFLOW_REVISION", "COMPARISON_REVISION", "VARIANT"):
        setattr(base, key, original[key])
    base.__file__ = original["file"]
    base.validate_preflight = original["validate"]


def prepare_input(case_id: str, output_dir: Path) -> dict:
    original = _patch_base()
    try:
        metadata = base.prepare_input(case_id, output_dir)
    finally:
        _restore_base(original)
    shutil.copyfile(INSTANCE_ROOT / "tools/pr_review_c02_finding_admission.py", output_dir / "pr_review_c02_finding_admission.py")
    metadata.update(profile_id=PROFILE_ID, variant=VARIANT, prompt_variant="pr-review-prompt-evidence-scope-r1")
    (output_dir / "prepare-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return metadata


def _fixture_batch_metrics(events: list[dict]) -> dict:
    reviewer_ids = {
        event["agent_id"] for event in events
        if event.get("event") == "SubagentStart" and isinstance(event.get("agent_id"), str)
    }
    fixture_ids = {
        event["tool_use_id"] for event in events
        if event.get("event") == "PostToolUse"
        and event.get("agent_id") in reviewer_ids
        and event.get("tool_name") == "Bash"
        and event.get("fixture_tool_command") is True
        and isinstance(event.get("tool_use_id"), str)
    }
    batches = []
    for event in events:
        if event.get("event") != "PostToolBatch" or event.get("agent_id") not in reviewer_ids:
            continue
        ids = event.get("tool_use_ids", [])
        if not isinstance(ids, list):
            continue
        size = len(fixture_ids.intersection(item for item in ids if isinstance(item, str)))
        if size:
            batches.append(size)
    maximum = max(batches, default=0)
    return {
        "fixture_tool_batch_count": len(batches),
        "fixture_tool_batch_sizes": batches,
        "fixture_tool_max_batch_size": maximum,
        "required_initial_read_count": REQUIRED_INITIAL_READS,
        "joint_initial_read_observed": maximum >= REQUIRED_INITIAL_READS,
        "additional_fixture_read_count": max(0, len(fixture_ids) - REQUIRED_INITIAL_READS),
    }


def collect_review(raw_output: Path, action_conclusion: str, execution_file: Path | None, hook_file: Path | None, started_ms: int, finished_ms: int, model_requested: str, review_input: Path, output_dir: Path) -> dict:
    metadata = relationship.collect_review(raw_output, action_conclusion, execution_file, hook_file, started_ms, finished_ms, model_requested, REVIEWER_MODEL, review_input, output_dir)
    events = relationship.free._read_hook_events(hook_file)
    metadata["workflow_trace"].update(_fixture_batch_metrics(events))
    (output_dir / "review-metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return metadata


def _mechanism_qualification(metadata: dict) -> dict:
    trace = metadata.get("workflow_trace", {})
    observed = trace.get("fixture_tool_batch_count", 0) > 0
    satisfied = bool(
        observed
        and trace.get("joint_initial_read_observed") is True
        and trace.get("additional_fixture_read_count") == 0
        and trace.get("relationship_reviewer_fixture_access_count") == REQUIRED_INITIAL_READS
        and trace.get("root_fixture_tool_access_count") == 0
    )
    return {
        "state": "satisfied" if satisfied else ("unsatisfied" if observed else "unobserved"),
        "required_initial_read_count": REQUIRED_INITIAL_READS,
        "joint_initial_read_observed": trace.get("joint_initial_read_observed") is True,
        "additional_fixture_read_count": trace.get("additional_fixture_read_count"),
        "fixture_tool_max_batch_size": trace.get("fixture_tool_max_batch_size"),
    }


def grade_run(case_id: str, attempt: int, model_requested: str, review_output: Path, review_metadata: Path, prepare_metadata: Path, output: Path, github_run_id: str) -> dict:
    original = _patch_base()
    try:
        with tempfile.TemporaryDirectory() as directory:
            intermediate = Path(directory) / "run-result.json"
            run = base.grade_run(case_id, attempt, model_requested, review_output, review_metadata, prepare_metadata, intermediate, github_run_id)
    finally:
        _restore_base(original)
    run["schema_version"] = 19
    run["mechanism_qualification"] = _mechanism_qualification(_load(review_metadata))
    held_out.free.core.legacy._write_json_once(output, run)
    return run


def record_terminal(case_id: str, attempt: int, model_requested: str, status: str, output: Path, github_run_id: str) -> dict:
    original = _patch_base()
    try:
        with tempfile.TemporaryDirectory() as directory:
            intermediate = Path(directory) / "run-result.json"
            run = base.record_terminal(case_id, attempt, model_requested, status, intermediate, github_run_id)
    finally:
        _restore_base(original)
    run["schema_version"] = 19
    run["mechanism_qualification"] = {
        "state": "unobserved",
        "required_initial_read_count": REQUIRED_INITIAL_READS,
        "joint_initial_read_observed": False,
        "additional_fixture_read_count": None,
        "fixture_tool_max_batch_size": None,
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
            print("Measurement Series C02 Evidence Scope preflight is valid")
        elif args.command == "prepare":
            print(json.dumps(prepare_input(args.case_id, args.output_dir), ensure_ascii=False))
        elif args.command == "collect":
            print(json.dumps(collect_review(args.raw_output, args.action_conclusion, args.execution_file, args.hook_file, args.started_ms, args.finished_ms, args.model_requested, args.review_input, args.output_dir), ensure_ascii=False))
        elif args.command == "grade":
            print(json.dumps(grade_run(args.case_id, args.attempt, args.model_requested, args.review_output, args.review_metadata, args.prepare_metadata, args.output, args.github_run_id), ensure_ascii=False))
        else:
            print(json.dumps(record_terminal(args.case_id, args.attempt, args.model_requested, args.status, args.output, args.github_run_id), ensure_ascii=False))
    except (MeasurementError, base.CalibrationError, held_out.QualificationError, relationship.CalibrationError, held_out.free.CalibrationError, held_out.free.core.QualificationError, held_out.free.core.legacy.QualificationError, held_out.free.core.measurement.ValidationError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
