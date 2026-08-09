#!/usr/bin/env python3
"""Prepare, collect, and grade held-out Control-Free qualification runs."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

import pr_review_workflow_free_calibration as free


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-held-out-control-free-three-n1-r1"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-qualify-held-out-control-free.yml"
WORKFLOW_REVISION = "pr-review-qualify-held-out-control-free-r1"
COMPARISON_REVISION = "pr-review-held-out-control-free-qualification-r1"
RATING_ID = "pr-review-finding-quality-v9"
VARIANT = "held-out-control-free"
ROOT_MODEL = "claude-sonnet-5"
CASES = ("PRR-C02", "PRR-C03", "PRR-C06")
CASE_SLUGS = {case_id: case_id.lower() for case_id in CASES}


class QualificationError(ValueError):
    pass


def _load(path: Path) -> dict:
    return free.core.legacy._load_json(path)


def _sha(path: Path) -> str:
    return free.core.legacy._sha256(path)


def _artifact_path(relative_path: str) -> Path:
    return (
        REPOSITORY_ROOT / relative_path
        if relative_path.startswith(".github/")
        else INSTANCE_ROOT / relative_path
    )


def _fixture_and_oracle(case_id: str) -> tuple[dict, dict]:
    if case_id not in CASES:
        raise QualificationError("case is not in the fixed held-out set")
    fixture = _load(INSTANCE_ROOT / f"cases/{case_id}/r2/input.json")
    oracle = _load(INSTANCE_ROOT / f"cases/{case_id}/r2/oracle.json")
    if (
        fixture.get("schema_version") != 5
        or fixture.get("case_id") != case_id
        or fixture.get("fixture_revision") != "r2"
        or fixture.get("review_contract_revision") != "pr-review-contract-r2"
    ):
        raise QualificationError("fixture identity mismatch")
    if fixture.get("changed_paths") != [item.get("path") for item in fixture.get("changes", [])]:
        raise QualificationError("fixture changed paths mismatch")
    if (
        oracle.get("schema_version") != 5
        or oracle.get("case_id") != case_id
        or oracle.get("fixture_revision") != "r2"
        or not isinstance(oracle.get("expected_findings"), list)
    ):
        raise QualificationError("oracle identity mismatch")
    return fixture, oracle


def validate_preflight(case_id: str) -> tuple[dict, dict]:
    fixture, _ = _fixture_and_oracle(case_id)
    profile = _load(PROFILE_PATH)
    preflight = _load(PREFLIGHT_PATH)
    expected_cases = [{"id": item, "revision": "r2"} for item in CASES]
    if (
        profile.get("profile_id") != PROFILE_ID
        or profile.get("state") != "frozen_not_executed"
        or profile.get("purpose") != "held_out_control_free_qualification"
        or profile.get("cases") != expected_cases
    ):
        raise QualificationError("profile identity mismatch")
    conditions = profile.get("comparison_conditions", {})
    if conditions.get("variant") != VARIANT:
        raise QualificationError("profile variant mismatch")
    if conditions.get("model", {}).get("requested") != ROOT_MODEL:
        raise QualificationError("profile model mismatch")
    executor = conditions.get("executor_parameters", {})
    if executor.get("max_workers") != 24 or executor.get("dispatch_concurrency") != 3:
        raise QualificationError("profile concurrency mismatch")
    for artifact in conditions.get("bound_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise QualificationError(f"profile artifact mismatch: {artifact.get('path')}")
    case_binding = conditions.get("case_bindings", {}).get(case_id)
    if not isinstance(case_binding, dict):
        raise QualificationError("case binding is missing")
    for key in ("input", "oracle", "snapshot", "authority", "eligibility"):
        artifact = case_binding.get(key, {})
        path = _artifact_path(artifact.get("path", ""))
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise QualificationError(f"case artifact mismatch: {case_id}.{key}")
    if _sha(INSTANCE_ROOT / f"cases/{case_id}/r2/input.json") != case_binding["input"]["sha256"]:
        raise QualificationError("fixture input binding mismatch")
    expected_profile = {
        "profile_id": PROFILE_ID,
        "path": f"profiles/{PROFILE_PATH.name}",
        "sha256": _sha(PROFILE_PATH),
    }
    if preflight.get("state") != "ready_not_executed" or preflight.get("profile") != expected_profile:
        raise QualificationError("preflight profile receipt mismatch")
    slot = {"case_id": case_id, "fixture_revision": "r2", "variant": VARIANT, "repetition": 1}
    if slot not in preflight.get("planned_slots", []):
        raise QualificationError("slot is not in the fixed plan")
    for artifact in preflight.get("verified_artifacts", []):
        path = _artifact_path(artifact["path"])
        if not path.is_file() or _sha(path) != artifact.get("sha256"):
            raise QualificationError(f"preflight artifact mismatch: {artifact.get('path')}")
    audit = _load(INSTANCE_ROOT / "contracts/pr-review-held-out-three-case-design-audit-r1.json")
    rating = _load(INSTANCE_ROOT / "rating-contracts/pr-review-finding-quality-v9.json")
    if audit.get("decision", {}).get("state") != "satisfied":
        raise QualificationError("independent case audit is not satisfied")
    if rating.get("state") != "independent_case_design_audit_satisfied":
        raise QualificationError("rating admission mismatch")
    if fixture["case_id"] != case_id:
        raise QualificationError("fixture case mismatch")
    return profile, preflight


def prepare_input(case_id: str, output_dir: Path) -> dict:
    from pr_review_authority_packet import materialize_authority_packet
    from pr_review_repository_snapshot import _make_cleanup_writable
    from pr_review_repository_snapshot_r4 import materialize_snapshot

    profile, preflight = validate_preflight(case_id)
    if output_dir.exists() and any(output_dir.iterdir()):
        raise QualificationError(f"output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter_ns()
    conditions = profile["comparison_conditions"]
    binding = conditions["case_bindings"][case_id]
    fixture_path = INSTANCE_ROOT / binding["input"]["path"]
    snapshot_root = output_dir / "repository"
    try:
        observed_snapshot = materialize_snapshot(
            REPOSITORY_ROOT,
            conditions["target_repository_ref"]["commit"],
            fixture_path,
            output_dir,
        )
        if observed_snapshot != _load(INSTANCE_ROOT / binding["snapshot"]["path"]):
            raise QualificationError("materialized snapshot receipt mismatch")
        authority = materialize_authority_packet(
            REPOSITORY_ROOT, INSTANCE_ROOT / binding["authority"]["path"]
        )
        copies = {
            fixture_path: output_dir / "review-input.json",
            INSTANCE_ROOT / conditions["review_contract"]["path"]: output_dir / "review-contract.md",
            INSTANCE_ROOT / conditions["review_output_schema"]["path"]: output_dir / "review-output-schema.json",
            INSTANCE_ROOT / conditions["permission"]["fixture_tool_path"]: output_dir / "fixture-tool",
            INSTANCE_ROOT / conditions["prompt"]["content_path"]: output_dir / "core-prompt.md",
            INSTANCE_ROOT / binding["eligibility"]["path"]: output_dir / "review-eligibility.json",
            Path(__file__): output_dir / Path(__file__).name,
        }
        dependencies = (
            "pr_review_measurement.py",
            "pr_review_qualification.py",
            "pr_review_code_review_qualification.py",
            "pr_review_workflow_free_calibration.py",
            "pr_review_subagent_hook.py",
        )
        for filename in dependencies:
            copies[INSTANCE_ROOT / "tools" / filename] = output_dir / filename
        for source, destination in copies.items():
            shutil.copyfile(source, destination)
        (output_dir / "authority-input.json").write_text(
            json.dumps(authority, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (output_dir / "claude-project-settings.json").write_text(
            json.dumps(free._hook_settings(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (output_dir / "fixture-tool").chmod(0o755)
        metadata = {
            "schema_version": 3,
            "profile_id": PROFILE_ID,
            "preflight_id": preflight["preflight_id"],
            "case_id": case_id,
            "fixture_revision": "r2",
            "variant": VARIANT,
            "repetition": 1,
            "input_sha256": _sha(output_dir / "review-input.json"),
            "authority_sha256": _sha(output_dir / "authority-input.json"),
            "review_contract_sha256": _sha(output_dir / "review-contract.md"),
            "review_output_schema_sha256": _sha(output_dir / "review-output-schema.json"),
            "prompt_sha256": _sha(output_dir / "core-prompt.md"),
            "snapshot_sha256": observed_snapshot["snapshot_sha256"],
            "input_ms": (time.perf_counter_ns() - started) // 1_000_000,
        }
        free.core.legacy._write_json_once(output_dir / "prepare-metadata.json", metadata)
        return metadata
    except Exception:
        _make_cleanup_writable(snapshot_root)
        raise


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
    return free.collect_review(
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


def _empty_quality(expected: int) -> dict:
    return {
        "observed": False,
        "expected_findings": expected,
        "true_positive": 0,
        "false_positive": 0,
        "false_negative": expected,
        "path_accuracy": 0,
        "line_accuracy": 0,
        "category_accuracy": 0,
        "clean_control_major_false_positive": 0,
        "scope_violation_count": 0,
        "review_contract_violation": 0,
        "summary_complete": False,
    }


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
    fixture, oracle = _fixture_and_oracle(case_id)
    metadata = _load(review_metadata)
    prepared = _load(prepare_metadata)
    if prepared.get("case_id") != case_id or prepared.get("profile_id") != PROFILE_ID:
        raise QualificationError("prepare metadata identity mismatch")
    quality = _empty_quality(len(oracle["expected_findings"]))
    quality_status = None
    if metadata.get("action_conclusion") != "success":
        result = "execution_failed"
    elif not metadata.get("output_valid") or not review_output.is_file():
        result = "invalid_output"
    else:
        review = free.core.measurement.validate_review_output_v2(
            _load(review_output), set(fixture["changed_paths"])
        )
        quality = free.core.legacy._quality_result(oracle, review, fixture)
        quality_status = (
            "pass"
            if quality["false_negative"] == quality["false_positive"] == quality["review_contract_violation"] == 0
            else "quality_failed"
        )
        result = quality_status
    measurement = free._measurement_qualification(metadata, model_requested)
    if measurement["state"] != "satisfied" and result in {"pass", "quality_failed"}:
        result = "measurement_incomplete"
    runtime = metadata.get("runtime", {})
    total_tokens = None
    if runtime.get("input_tokens") is not None and runtime.get("output_tokens") is not None:
        total_tokens = runtime["input_tokens"] + runtime["output_tokens"]
    run = {
        "schema_version": 16,
        "comparison_revision": COMPARISON_REVISION,
        "profile_id": PROFILE_ID,
        "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:{case_id}:{VARIANT}:r1:a{attempt}",
        "case_id": case_id,
        "fixture_revision": "r2",
        "variant": VARIANT,
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
        "timing": {
            "queue_ms": None,
            "setup_ms": None,
            "input_ms": prepared.get("input_ms"),
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
        "quality_score": (
            free.core.measurement._quality_score(quality_status, quality)
            if quality_status is not None
            else None
        ),
        "result": result,
    }
    free.core.legacy._write_json_once(output, run)
    return run


def record_terminal(
    case_id: str,
    attempt: int,
    model_requested: str,
    status: str,
    output: Path,
    github_run_id: str,
) -> dict:
    profile, _ = validate_preflight(case_id)
    fixture, oracle = _fixture_and_oracle(case_id)
    run = {
        "schema_version": 16,
        "comparison_revision": COMPARISON_REVISION,
        "profile_id": PROFILE_ID,
        "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:{case_id}:{VARIANT}:r1:a{attempt}",
        "case_id": case_id,
        "fixture_revision": "r2",
        "variant": VARIANT,
        "repetition": 1,
        "attempt": attempt,
        "base_sha": fixture["pr"]["base_sha"],
        "head_sha": fixture["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": None},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"],
        "workflow_revision": WORKFLOW_REVISION,
        "workflow_trace": {"complete": False},
        "measurement_qualification": {"state": "unsatisfied"},
        "github_run_id": github_run_id,
        "timing": {key: None for key in ("queue_ms", "setup_ms", "input_ms", "action_step_ms", "review_ms", "report_ms", "execution_ms", "e2e_ms")},
        "runtime": {key: None for key in ("turns", "input_tokens", "output_tokens", "total_tokens", "reported_cost_usd")},
        "quality": _empty_quality(len(oracle["expected_findings"])),
        "quality_score": None,
        "result": status,
    }
    free.core.legacy._write_json_once(output, run)
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
            print("held-out Control-Free qualification preflight is valid")
        elif args.command == "prepare":
            print(json.dumps(prepare_input(args.case_id, args.output_dir), ensure_ascii=False))
        elif args.command == "collect":
            print(json.dumps(collect_review(args.raw_output, args.action_conclusion, args.execution_file, args.hook_file, args.started_ms, args.finished_ms, args.model_requested, args.review_input, args.output_dir), ensure_ascii=False))
        elif args.command == "grade":
            print(json.dumps(grade_run(args.case_id, args.attempt, args.model_requested, args.review_output, args.review_metadata, args.prepare_metadata, args.output, args.github_run_id), ensure_ascii=False))
        else:
            print(json.dumps(record_terminal(args.case_id, args.attempt, args.model_requested, args.status, args.output, args.github_run_id), ensure_ascii=False))
    except (QualificationError, free.CalibrationError, free.core.QualificationError, free.core.legacy.QualificationError, free.core.measurement.ValidationError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
