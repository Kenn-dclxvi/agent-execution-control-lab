#!/usr/bin/env python3
"""Measure Candidate171 on the fixed C02 development case."""

from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from pathlib import Path

import pr_review_measurement_c02_evidence_diagnostic_r3 as base


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-measurement-c02-consumer-bound-evidence-n3-r1"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
BASELINE_PROFILE_PATH = INSTANCE_ROOT / "profiles/pr-review-measurement-c02-evidence-diagnostic-n1-r4.json"
BASELINE_RESULT_PATH = INSTANCE_ROOT / "results/pr-review-measurement-c02-evidence-diagnostic-r4-prr-c02-prompt-evidence-scope-r1-a31300109132.json"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-measure-c02-consumer-bound-evidence.yml"
WORKFLOW_REVISION = "pr-review-measure-c02-consumer-bound-evidence-r1"
COMPARISON_REVISION = "pr-review-measurement-c02-consumer-bound-evidence-r1"
VARIANT = "consumer-bound-evidence"
SCHEMA_VERSION = 23
REPETITIONS = (1, 2, 3)
_ACTIVE_REPETITION: int | None = None


class MeasurementError(ValueError):
    pass


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha(path: Path) -> str:
    return base.base.base.held_out._sha(path)


def _artifact_path(relative_path: str) -> Path:
    return (
        REPOSITORY_ROOT / relative_path
        if relative_path.startswith(".github/") or relative_path.startswith("prompts/releases/")
        else INSTANCE_ROOT / relative_path
    )


def validate_preflight(case_id: str, repetition: int | None = None) -> tuple[dict, dict]:
    repetition = _ACTIVE_REPETITION if repetition is None else repetition
    if case_id != "PRR-C02" or repetition not in REPETITIONS:
        raise MeasurementError("only PRR-C02 repetitions 1-3 are allowed")
    base.base.base.held_out._fixture_and_oracle(case_id)
    profile = _load(PROFILE_PATH)
    baseline_profile = _load(BASELINE_PROFILE_PATH)
    baseline_result = _load(BASELINE_RESULT_PATH)
    preflight = _load(PREFLIGHT_PATH)
    if profile.get("profile_id") != PROFILE_ID or profile.get("state") != "frozen_not_executed":
        raise MeasurementError("Profile identity mismatch")
    if profile.get("purpose") != "c02_consumer_bound_evidence_development_measurement":
        raise MeasurementError("Measurement Series scope mismatch")
    conditions = profile.get("comparison_conditions", {})
    baseline = baseline_profile.get("comparison_conditions", {})
    if conditions.get("variant") != VARIANT or conditions.get("candidate_number") != 171:
        raise MeasurementError("Candidate171 variant mismatch")
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
    executor = conditions.get("executor_parameters", {})
    baseline_executor = baseline.get("executor_parameters", {})
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
        (executor.get("max_attempts_per_case"), baseline_executor.get("max_attempts_per_case"), "max attempts"),
        (executor.get("max_turns"), baseline_executor.get("max_turns"), "max turns"),
        (executor.get("turn_limit_source"), baseline_executor.get("turn_limit_source"), "turn limit source"),
        (executor.get("max_workers"), baseline_executor.get("max_workers"), "max workers"),
        (executor.get("internal_review_topology"), baseline_executor.get("internal_review_topology"), "review topology"),
        (executor.get("action_timeout_seconds"), baseline_executor.get("action_timeout_seconds"), "Action timeout"),
        (executor.get("reviewer_job_timeout_seconds"), baseline_executor.get("reviewer_job_timeout_seconds"), "reviewer timeout"),
        (executor.get("token_accounting"), baseline_executor.get("token_accounting"), "token accounting"),
        (conditions.get("measurement_gate"), baseline.get("measurement_gate"), "measurement gate"),
        (conditions.get("kpis"), baseline.get("kpis"), "KPIs"),
    )
    for observed, expected, label in common_pairs:
        if observed != expected:
            raise MeasurementError(f"comparison compatibility mismatch: {label}")
    expected_baseline = conditions.get("baseline_result", {})
    if (
        baseline_result.get("result_id") != expected_baseline.get("result_id")
        or _sha(BASELINE_RESULT_PATH) != expected_baseline.get("sha256")
        or baseline_result.get("measurement_qualification", {}).get("state") != "satisfied"
    ):
        raise MeasurementError("saved Candidate170 baseline mismatch")
    expected_profile = {
        "profile_id": PROFILE_ID,
        "path": f"profiles/{PROFILE_PATH.name}",
        "sha256": _sha(PROFILE_PATH),
    }
    if preflight.get("state") != "ready_not_executed" or preflight.get("profile") != expected_profile:
        raise MeasurementError("preflight Profile receipt mismatch")
    expected_slots = [
        {
            "case_id": case_id,
            "fixture_revision": "r2",
            "variant": VARIANT,
            "repetition": item,
        }
        for item in REPETITIONS
    ]
    if (
        preflight.get("planned_slots") != expected_slots
        or preflight.get("compatibility", {}).get("mechanical_diff_state") != "satisfied"
    ):
        raise MeasurementError("fixed Candidate171 slots mismatch")
    for artifact in preflight.get("verified_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise MeasurementError(f"preflight artifact mismatch: {artifact.get('path')}")
    return profile, preflight


def _patch_base(repetition: int) -> dict:
    global _ACTIVE_REPETITION
    original = {
        "PROFILE_ID": base.PROFILE_ID,
        "PROFILE_PATH": base.PROFILE_PATH,
        "PREFLIGHT_PATH": base.PREFLIGHT_PATH,
        "WORKFLOW_PATH": base.WORKFLOW_PATH,
        "WORKFLOW_REVISION": base.WORKFLOW_REVISION,
        "COMPARISON_REVISION": base.COMPARISON_REVISION,
        "file": base.__file__,
        "validate": base.base.base.validate_preflight,
        "active_repetition": _ACTIVE_REPETITION,
    }
    base.PROFILE_ID = PROFILE_ID
    base.PROFILE_PATH = PROFILE_PATH
    base.PREFLIGHT_PATH = PREFLIGHT_PATH
    base.WORKFLOW_PATH = WORKFLOW_PATH
    base.WORKFLOW_REVISION = WORKFLOW_REVISION
    base.COMPARISON_REVISION = COMPARISON_REVISION
    base.__file__ = __file__
    base.base.base.validate_preflight = validate_preflight
    _ACTIVE_REPETITION = repetition
    return original


def _restore_base(original: dict) -> None:
    global _ACTIVE_REPETITION
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
    base.base.base.validate_preflight = original["validate"]
    _ACTIVE_REPETITION = original["active_repetition"]


def _call(repetition: int, function, *args):
    original = _patch_base(repetition)
    try:
        return function(*args)
    finally:
        _restore_base(original)


def prepare_input(case_id: str, repetition: int, output_dir: Path) -> dict:
    validate_preflight(case_id, repetition)
    metadata = _call(repetition, base.prepare_input, case_id, output_dir)
    shutil.copyfile(
        INSTANCE_ROOT / "tools/pr_review_measurement_c02_evidence_diagnostic_r3.py",
        output_dir / "pr_review_measurement_c02_evidence_diagnostic_r3.py",
    )
    shutil.copyfile(__file__, output_dir / Path(__file__).name)
    metadata.update(
        profile_id=PROFILE_ID,
        repetition=repetition,
        variant=VARIANT,
        prompt_variant="pr-review-consumer-bound-evidence-r1",
    )
    (output_dir / "prepare-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def collect_review(*args) -> dict:
    return _call(1, base.collect_review, *args)


def _evidence_control_diagnostics(run: dict) -> dict:
    trace = run.get("workflow_trace", {})
    operation_counts = trace.get("evidence_diagnostics", {}).get("operation_counts", {})
    recognized = sum(
        count
        for outcomes in operation_counts.values()
        if isinstance(outcomes, dict)
        for count in outcomes.values()
        if isinstance(count, int) and not isinstance(count, bool)
    )
    access_count = trace.get("fixture_tool_access_count")
    unclassified = (
        max(0, access_count - recognized)
        if isinstance(access_count, int) and not isinstance(access_count, bool)
        else None
    )
    return {
        "state": "observed_not_machine_qualified" if trace.get("complete") else "unobserved",
        "fixed_read_count_gate": False,
        "consumer_binding_machine_verifiable": False,
        "fixture_tool_access_count": access_count,
        "recognized_operation_access_count": recognized,
        "unclassified_access_count": unclassified,
    }


def grade_run(
    case_id: str,
    repetition: int,
    attempt: int,
    model_requested: str,
    review_output: Path,
    review_metadata: Path,
    prepare_metadata: Path,
    output: Path,
    github_run_id: str,
) -> dict:
    validate_preflight(case_id, repetition)
    with tempfile.TemporaryDirectory() as directory:
        intermediate = Path(directory) / "run-result.json"
        run = _call(
            repetition,
            base.grade_run,
            case_id,
            attempt,
            model_requested,
            review_output,
            review_metadata,
            prepare_metadata,
            intermediate,
            github_run_id,
        )
    run.update(
        schema_version=SCHEMA_VERSION,
        comparison_revision=COMPARISON_REVISION,
        profile_id=PROFILE_ID,
        workflow_revision=WORKFLOW_REVISION,
        variant=VARIANT,
        repetition=repetition,
        result_id=f"{COMPARISON_REVISION}:{case_id}:{VARIANT}:r{repetition}:a{attempt}",
    )
    run["evidence_control_diagnostics"] = _evidence_control_diagnostics(run)
    run.pop("mechanism_qualification", None)
    base.base.base.base.held_out.free.core.legacy._write_json_once(output, run)
    return run


def record_terminal(
    case_id: str,
    repetition: int,
    attempt: int,
    model_requested: str,
    status: str,
    output: Path,
    github_run_id: str,
) -> dict:
    validate_preflight(case_id, repetition)
    with tempfile.TemporaryDirectory() as directory:
        intermediate = Path(directory) / "run-result.json"
        run = _call(
            repetition,
            base.record_terminal,
            case_id,
            attempt,
            model_requested,
            status,
            intermediate,
            github_run_id,
        )
    run.update(
        schema_version=SCHEMA_VERSION,
        comparison_revision=COMPARISON_REVISION,
        profile_id=PROFILE_ID,
        workflow_revision=WORKFLOW_REVISION,
        variant=VARIANT,
        repetition=repetition,
        result_id=f"{COMPARISON_REVISION}:{case_id}:{VARIANT}:r{repetition}:a{attempt}",
    )
    run["evidence_control_diagnostics"] = _evidence_control_diagnostics(run)
    run.pop("mechanism_qualification", None)
    base.base.base.base.held_out.free.core.legacy._write_json_once(output, run)
    return run


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate-preflight", "prepare"):
        item = sub.add_parser(name)
        item.add_argument("--case-id", required=True, choices=("PRR-C02",))
        item.add_argument("--repetition", required=True, type=int, choices=REPETITIONS)
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
        item.add_argument("--case-id", required=True, choices=("PRR-C02",))
        item.add_argument("--repetition", required=True, type=int, choices=REPETITIONS)
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
        validate_preflight(args.case_id, args.repetition)
        print("Candidate171 C02 N=3 preflight is valid")
    elif args.command == "prepare":
        print(json.dumps(prepare_input(args.case_id, args.repetition, args.output_dir), ensure_ascii=False))
    elif args.command == "collect":
        print(json.dumps(collect_review(
            args.raw_output, args.action_conclusion, args.execution_file, args.hook_file,
            args.started_ms, args.finished_ms, args.model_requested, args.review_input,
            args.output_dir,
        ), ensure_ascii=False))
    elif args.command == "grade":
        print(json.dumps(grade_run(
            args.case_id, args.repetition, args.attempt, args.model_requested,
            args.review_output, args.review_metadata, args.prepare_metadata,
            args.output, args.github_run_id,
        ), ensure_ascii=False))
    else:
        print(json.dumps(record_terminal(
            args.case_id, args.repetition, args.attempt, args.model_requested,
            args.status, args.output, args.github_run_id,
        ), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
