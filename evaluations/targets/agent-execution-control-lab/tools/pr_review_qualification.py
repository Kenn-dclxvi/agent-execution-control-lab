#!/usr/bin/env python3
"""Prepare, collect, and grade the PRR-C01/r3 Core Baseline qualification."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any

import pr_review_measurement as measurement


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-agentic-retrieval-c01-r3-qualification-n2-r1"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = (
    INSTANCE_ROOT
    / "contracts"
    / "pr-review-agentic-retrieval-c01-r3-qualification-n2-r1-preflight.json"
)
SNAPSHOT_RECEIPT_PATH = (
    INSTANCE_ROOT
    / "contracts"
    / "baseline-repository-snapshot-prr-c01-r3-r1.json"
)
WORKFLOW_REVISION = "pr-review-qualify-core-r1"
COMPARISON_REVISION = "pr-review-core-baseline-qualification-r1"


class QualificationError(ValueError):
    pass


def _load_json(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise QualificationError(f"unable to read JSON {path}: {exc}") from exc


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json_once(path: Path, value: Any) -> None:
    if path.exists():
        raise QualificationError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def validate_preflight(repetition: int, prior_admission: Path | None = None) -> tuple[dict, dict]:
    if repetition not in {1, 2}:
        raise QualificationError("repetition must be 1 or 2")
    profile = _load_json(PROFILE_PATH)
    validation = measurement.validate_qualification_profile(profile)
    preflight = _load_json(PREFLIGHT_PATH)
    if preflight.get("state") != "ready_not_executed":
        raise QualificationError("qualification preflight is not ready")
    if preflight.get("profile") != {
        "profile_id": PROFILE_ID,
        "path": f"profiles/{PROFILE_PATH.name}",
        "sha256": _sha256(PROFILE_PATH),
    }:
        raise QualificationError("qualification profile receipt mismatch")
    if preflight.get("validation_tool") != {
        "path": "tools/pr_review_measurement.py",
        "sha256": _sha256(Path(measurement.__file__)),
    }:
        raise QualificationError("qualification validator receipt mismatch")
    for artifact in preflight.get("verified_artifacts", []):
        path = (
            REPOSITORY_ROOT / artifact["path"]
            if artifact["path"].startswith(".github/")
            else INSTANCE_ROOT / artifact["path"]
        )
        if not path.is_file() or _sha256(path) != artifact.get("sha256"):
            raise QualificationError(f"preflight artifact mismatch: {artifact.get('path')}")
    slot = {
        "case_id": "PRR-C01",
        "fixture_revision": "r3",
        "variant": "agentic-retrieval",
        "repetition": repetition,
    }
    if slot not in validation["planned_slots"] or slot not in preflight.get(
        "planned_slots", []
    ):
        raise QualificationError("requested slot is not in the fixed plan")
    if repetition == 2:
        if prior_admission is None:
            raise QualificationError("repetition 2 requires repetition 1 admission")
        admission = _load_json(prior_admission)
        if admission.get("state") != "satisfied" or admission.get(
            "admitted_repetition"
        ) != 2:
            raise QualificationError("repetition 1 admission is not satisfied")
    return profile, preflight


def prepare_input(
    repetition: int, output_dir: Path, prior_admission: Path | None = None
) -> dict:
    from pr_review_authority_packet import materialize_authority_packet
    from pr_review_repository_snapshot import _make_cleanup_writable
    from pr_review_repository_snapshot_r2 import materialize_snapshot

    profile, preflight = validate_preflight(repetition, prior_admission)
    if output_dir.exists() and any(output_dir.iterdir()):
        raise QualificationError(f"output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter_ns()
    conditions = profile["comparison_conditions"]
    fixture_path = INSTANCE_ROOT / conditions["fixture_identity"]["input_path"]
    snapshot_root = output_dir / "repository"
    try:
        observed_snapshot = materialize_snapshot(
            REPOSITORY_ROOT,
            conditions["target_repository_ref"]["commit"],
            fixture_path,
            output_dir,
        )
        if observed_snapshot != _load_json(SNAPSHOT_RECEIPT_PATH):
            raise QualificationError("materialized snapshot receipt mismatch")
        authority = materialize_authority_packet(
            REPOSITORY_ROOT,
            INSTANCE_ROOT / conditions["authority_selection"]["path"],
        )
        copies = {
            fixture_path: output_dir / "review-input.json",
            INSTANCE_ROOT / conditions["review_contract"]["path"]: output_dir
            / "review-contract.md",
            INSTANCE_ROOT / conditions["review_output_schema"]["path"]: output_dir
            / "review-output-schema.json",
            INSTANCE_ROOT / conditions["permission"]["fixture_tool_path"]: output_dir
            / "fixture-tool",
            INSTANCE_ROOT / conditions["prompt"]["content_path"]: output_dir
            / "core-prompt.md",
            Path(__file__): output_dir / "pr-review-qualification.py",
            Path(measurement.__file__): output_dir / "pr-review-measurement.py",
        }
        for source, destination in copies.items():
            shutil.copyfile(source, destination)
        (output_dir / "authority-input.json").write_text(
            json.dumps(authority, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (output_dir / "fixture-tool").chmod(0o755)
        metadata = {
            "schema_version": 2,
            "profile_id": PROFILE_ID,
            "preflight_id": preflight["preflight_id"],
            "case_id": "PRR-C01",
            "fixture_revision": "r3",
            "variant": "agentic-retrieval",
            "repetition": repetition,
            "input_sha256": _sha256(output_dir / "review-input.json"),
            "authority_sha256": _sha256(output_dir / "authority-input.json"),
            "review_contract_sha256": _sha256(output_dir / "review-contract.md"),
            "review_output_schema_sha256": _sha256(
                output_dir / "review-output-schema.json"
            ),
            "prompt_sha256": _sha256(output_dir / "core-prompt.md"),
            "snapshot_sha256": observed_snapshot["snapshot_sha256"],
            "input_ms": (time.perf_counter_ns() - started) // 1_000_000,
        }
        _write_json_once(output_dir / "prepare-metadata.json", metadata)
        return metadata
    except Exception:
        _make_cleanup_writable(snapshot_root)
        raise


def collect_review(
    raw_output: Path,
    action_conclusion: str,
    execution_file: Path | None,
    started_ms: int,
    finished_ms: int,
    model_requested: str,
    review_input: Path,
    output_dir: Path,
) -> dict:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise QualificationError(f"output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_valid = False
    validation_error = None
    if action_conclusion == "success":
        try:
            changed_paths = set(_load_json(review_input)["changed_paths"])
            review = measurement.validate_review_output_v2(
                _load_json(raw_output), changed_paths
            )
            _write_json_once(output_dir / "review-output.json", review)
            output_valid = True
        except (QualificationError, measurement.ValidationError) as exc:
            validation_error = str(exc)
    metadata = {
        "schema_version": 1,
        "action_conclusion": action_conclusion,
        "output_valid": output_valid,
        "validation_error": validation_error,
        "model_requested": model_requested,
        "action_step_ms": max(0, finished_ms - started_ms),
        "runtime": measurement._parse_execution_file(execution_file),
    }
    measurement.validate_review_metadata(metadata, model_requested)
    _write_json_once(output_dir / "review-metadata.json", metadata)
    return metadata


def _quality_result(oracle: dict, review: dict, fixture: dict) -> dict:
    expected = oracle["expected_findings"]
    actual = review["findings"]
    matched: set[int] = set()
    for expected_finding in expected:
        for index, actual_finding in enumerate(actual):
            if index not in matched and measurement._finding_identity_matches_v2(
                expected_finding, actual_finding
            ):
                matched.add(index)
                break
    true_positive = len(matched)
    false_negative = len(expected) - true_positive
    false_positive = len(actual) - true_positive
    finding_categories = {finding["category"] for finding in actual}
    rule_ids = {
        rule["rule_id"] for source in fixture["rules"] for rule in source["rules"]
    }
    scope_violation = sum(1 for finding in actual if finding["rule_id"] not in rule_ids)
    contract_violation = scope_violation + sum(
        1
        for category in measurement.CATEGORIES
        if review["summary"][category]
        != ("fail" if category in finding_categories else "pass")
    )
    return {
        "observed": True,
        "expected_findings": len(expected),
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "path_accuracy": true_positive,
        "line_accuracy": true_positive,
        "category_accuracy": true_positive,
        "clean_control_major_false_positive": 0,
        "scope_violation_count": scope_violation,
        "review_contract_violation": contract_violation,
        "summary_complete": set(review["summary"]) == set(measurement.CATEGORIES),
    }


def validate_run_result(value: Any) -> dict:
    measurement.validate_run_result({
        **value,
        "schema_version": 2,
        "comparison_revision": "pr-review-core-r2",
        "quality_rating_contract": "pr-review-finding-quality-v1",
        "fixture_revision": "r1",
    })
    if value.get("schema_version") != 3:
        raise QualificationError("qualification result schema mismatch")
    if value.get("comparison_revision") != COMPARISON_REVISION:
        raise QualificationError("qualification comparison identity mismatch")
    if value.get("profile_id") != PROFILE_ID:
        raise QualificationError("qualification profile identity mismatch")
    if value.get("quality_rating_contract") != "pr-review-finding-quality-v3":
        raise QualificationError("qualification rating identity mismatch")
    if value.get("fixture_revision") != "r3" or value.get("variant") != "agentic-retrieval":
        raise QualificationError("qualification fixture or variant mismatch")
    if value.get("workflow_revision") != WORKFLOW_REVISION:
        raise QualificationError("qualification workflow revision mismatch")
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
    fixture_path, oracle_path = measurement._fixture_paths("PRR-C01", "r3")
    fixture = measurement.validate_fixture_input(_load_json(fixture_path), "PRR-C01")
    oracle = measurement.validate_fixture_oracle(_load_json(oracle_path), fixture)
    prepared = _load_json(prepare_metadata)
    if prepared.get("profile_id") != PROFILE_ID or prepared.get("repetition") != repetition:
        raise QualificationError("prepare metadata identity mismatch")
    metadata = measurement.validate_review_metadata(
        _load_json(review_metadata), model_requested
    )
    quality = {
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
    if metadata["action_conclusion"] != "success":
        result = "execution_failed"
    elif not metadata["output_valid"] or not review_output.is_file():
        result = "invalid_output"
    else:
        review = measurement.validate_review_output_v2(
            _load_json(review_output), set(fixture["changed_paths"])
        )
        quality = _quality_result(oracle, review, fixture)
        result = (
            "pass"
            if quality["false_negative"] == 0
            and quality["false_positive"] == 0
            and quality["review_contract_violation"] == 0
            else "quality_failed"
        )
    runtime = metadata["runtime"]
    reported_model = runtime.get("model")
    if result == "pass" and reported_model != model_requested:
        result = "measurement_incomplete"
    quality_score = measurement._quality_score(result, quality)
    input_tokens = runtime.get("input_tokens")
    output_tokens = runtime.get("output_tokens")
    total_tokens = (
        input_tokens + output_tokens
        if input_tokens is not None and output_tokens is not None
        else None
    )
    conditions = profile["comparison_conditions"]
    run = {
        "schema_version": 3,
        "comparison_revision": COMPARISON_REVISION,
        "profile_id": PROFILE_ID,
        "quality_rating_contract": "pr-review-finding-quality-v3",
        "result_id": f"{COMPARISON_REVISION}:PRR-C01:agentic-retrieval:r{repetition}:a{attempt}",
        "case_id": "PRR-C01",
        "fixture_revision": "r3",
        "variant": "agentic-retrieval",
        "repetition": repetition,
        "attempt": attempt,
        "base_sha": fixture["pr"]["base_sha"],
        "head_sha": fixture["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": reported_model},
        "reviewer_executor": conditions["agent_environment"],
        "workflow_revision": WORKFLOW_REVISION,
        "github_run_id": github_run_id,
        "timing": {
            "queue_ms": None,
            "setup_ms": None,
            "input_ms": prepared["input_ms"],
            "action_step_ms": metadata["action_step_ms"],
            "review_ms": runtime.get("duration_ms"),
            "report_ms": None,
            "execution_ms": metadata["action_step_ms"],
            "e2e_ms": None,
        },
        "runtime": {
            "turns": runtime.get("turns"),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "reported_cost_usd": runtime.get("reported_cost_usd"),
        },
        "quality": quality,
        "quality_score": quality_score,
        "result": result,
    }
    validate_run_result(run)
    _write_json_once(output, run)
    return run


def record_terminal(
    repetition: int,
    attempt: int,
    model_requested: str,
    status: str,
    output: Path,
    github_run_id: str,
) -> dict:
    if status not in {
        "execution_failed",
        "timeout",
        "cancelled",
        "measurement_incomplete",
    }:
        raise QualificationError("terminal status is invalid")
    profile, _ = validate_preflight(repetition)
    fixture_path, _ = measurement._fixture_paths("PRR-C01", "r3")
    fixture = measurement.validate_fixture_input(_load_json(fixture_path), "PRR-C01")
    run = {
        "schema_version": 3,
        "comparison_revision": COMPARISON_REVISION,
        "profile_id": PROFILE_ID,
        "quality_rating_contract": "pr-review-finding-quality-v3",
        "result_id": f"{COMPARISON_REVISION}:PRR-C01:agentic-retrieval:r{repetition}:a{attempt}",
        "case_id": "PRR-C01",
        "fixture_revision": "r3",
        "variant": "agentic-retrieval",
        "repetition": repetition,
        "attempt": attempt,
        "base_sha": fixture["pr"]["base_sha"],
        "head_sha": fixture["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": None},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"],
        "workflow_revision": WORKFLOW_REVISION,
        "github_run_id": github_run_id,
        "timing": {
            "queue_ms": None,
            "setup_ms": None,
            "input_ms": None,
            "action_step_ms": None,
            "review_ms": None,
            "report_ms": None,
            "execution_ms": None,
            "e2e_ms": None,
        },
        "runtime": {
            "turns": None,
            "input_tokens": None,
            "output_tokens": None,
            "total_tokens": None,
            "reported_cost_usd": None,
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
    validate_run_result(run)
    _write_json_once(output, run)
    return run


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate-preflight")
    validate.add_argument("--repetition", required=True, type=int)
    prepare = subparsers.add_parser("prepare")
    prepare.add_argument("--repetition", required=True, type=int)
    prepare.add_argument("--output-dir", required=True, type=Path)
    collect = subparsers.add_parser("collect")
    collect.add_argument("--raw-output", required=True, type=Path)
    collect.add_argument("--action-conclusion", required=True)
    collect.add_argument("--execution-file", type=Path)
    collect.add_argument("--started-ms", required=True, type=int)
    collect.add_argument("--finished-ms", required=True, type=int)
    collect.add_argument("--model-requested", required=True)
    collect.add_argument("--review-input", required=True, type=Path)
    collect.add_argument("--output-dir", required=True, type=Path)
    grade = subparsers.add_parser("grade")
    grade.add_argument("--repetition", required=True, type=int)
    grade.add_argument("--attempt", required=True, type=int)
    grade.add_argument("--model-requested", required=True)
    grade.add_argument("--review-output", required=True, type=Path)
    grade.add_argument("--review-metadata", required=True, type=Path)
    grade.add_argument("--prepare-metadata", required=True, type=Path)
    grade.add_argument("--output", required=True, type=Path)
    grade.add_argument("--github-run-id", required=True)
    terminal = subparsers.add_parser("record-terminal")
    terminal.add_argument("--repetition", required=True, type=int)
    terminal.add_argument("--attempt", required=True, type=int)
    terminal.add_argument("--model-requested", required=True)
    terminal.add_argument(
        "--status",
        required=True,
        choices=("execution_failed", "timeout", "cancelled", "measurement_incomplete"),
    )
    terminal.add_argument("--output", required=True, type=Path)
    terminal.add_argument("--github-run-id", required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate-preflight":
            validate_preflight(args.repetition)
            print("qualification preflight is valid")
        elif args.command == "prepare":
            print(json.dumps(prepare_input(args.repetition, args.output_dir), ensure_ascii=False))
        elif args.command == "collect":
            print(json.dumps(collect_review(
                args.raw_output, args.action_conclusion, args.execution_file,
                args.started_ms, args.finished_ms, args.model_requested,
                args.review_input, args.output_dir,
            ), ensure_ascii=False))
        elif args.command == "grade":
            print(json.dumps(grade_run(
                args.repetition, args.attempt, args.model_requested,
                args.review_output, args.review_metadata, args.prepare_metadata,
                args.output, args.github_run_id,
            ), ensure_ascii=False))
        elif args.command == "record-terminal":
            print(json.dumps(record_terminal(
                args.repetition, args.attempt, args.model_requested, args.status,
                args.output, args.github_run_id,
            ), ensure_ascii=False))
    except (QualificationError, measurement.ValidationError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
