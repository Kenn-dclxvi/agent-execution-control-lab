#!/usr/bin/env python3
"""Prepare, validate, grade, and summarize PR review measurements."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import statistics
import sys
import time
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MEASUREMENT_ROOT = REPOSITORY_ROOT / "pr-review-measurements"
FIXTURE_ROOT = MEASUREMENT_ROOT / "fixtures" / "r1"
CONTRACT_PATH = MEASUREMENT_ROOT / "contracts" / "pr-review-core-r1.json"
REVIEW_CONTRACT_PATH = MEASUREMENT_ROOT / "contracts" / "review-contract-r1.md"
REVIEW_SCHEMA_PATH = MEASUREMENT_ROOT / "schemas" / "review-output-r1.schema.json"
FIXTURE_TOOL_PATH = REPOSITORY_ROOT / "scripts" / "pr_review_fixture_tool.py"

CASE_IDS = tuple(f"PRR-C0{number}" for number in range(1, 7))
VARIANTS = ("agentic-retrieval", "deterministic-input")
CATEGORIES = (
    "repository_discipline",
    "evaluation_artifact_integrity",
    "secret_or_private_log",
    "document_quality",
)
SUMMARY_STATES = ("pass", "fail", "unknown")
SEVERITIES = ("major", "minor")
RESULT_STATUSES = (
    "pass",
    "quality_failed",
    "invalid_output",
    "execution_failed",
    "timeout",
    "cancelled",
    "measurement_incomplete",
)
FINDING_KEYS = {
    "category",
    "rule_id",
    "path",
    "line_start",
    "line_end",
    "severity",
    "message",
}


class ValidationError(ValueError):
    pass


def _load_json(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"unable to read JSON {path}: {exc}") from exc


def _write_json_once(path: Path, value: Any) -> None:
    if path.exists():
        raise ValidationError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_exact_keys(value: dict, expected: set[str], label: str) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValidationError(f"{label} keys mismatch: missing={missing} extra={extra}")


def _relative_path(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValidationError(f"{label} must be a non-empty string")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise ValidationError(f"{label} must be a normalized repository-relative path")
    return value


def _positive_int(value: Any, label: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise ValidationError(f"{label} must be a positive integer")
    return value


def _validate_finding(value: Any, label: str, changed_paths: set[str] | None = None) -> dict:
    if not isinstance(value, dict):
        raise ValidationError(f"{label} must be an object")
    _require_exact_keys(value, FINDING_KEYS, label)
    if value["category"] not in CATEGORIES:
        raise ValidationError(f"{label}.category is invalid")
    if not isinstance(value["rule_id"], str) or not value["rule_id"]:
        raise ValidationError(f"{label}.rule_id must be a non-empty string")
    path = _relative_path(value["path"], f"{label}.path")
    if changed_paths is not None and path not in changed_paths:
        raise ValidationError(f"{label}.path is not a changed path")
    start = _positive_int(value["line_start"], f"{label}.line_start")
    end = _positive_int(value["line_end"], f"{label}.line_end")
    if end < start:
        raise ValidationError(f"{label} line range is reversed")
    if value["severity"] not in SEVERITIES:
        raise ValidationError(f"{label}.severity is invalid")
    if not isinstance(value["message"], str) or not value["message"].strip():
        raise ValidationError(f"{label}.message must be non-empty")
    return value


def validate_fixture_input(value: Any, expected_case_id: str | None = None) -> dict:
    if not isinstance(value, dict):
        raise ValidationError("fixture input must be an object")
    _require_exact_keys(
        value,
        {
            "schema_version",
            "case_id",
            "fixture_revision",
            "review_contract_revision",
            "pr",
            "changed_paths",
            "changes",
            "rules",
        },
        "fixture input",
    )
    if value["schema_version"] != 1:
        raise ValidationError("fixture input schema_version must be 1")
    if value["case_id"] not in CASE_IDS or (
        expected_case_id is not None and value["case_id"] != expected_case_id
    ):
        raise ValidationError("fixture input case_id is invalid")
    if value["fixture_revision"] != "r1":
        raise ValidationError("fixture_revision must be r1")
    if value["review_contract_revision"] != "pr-review-contract-r1":
        raise ValidationError("review_contract_revision is invalid")

    pr = value["pr"]
    if not isinstance(pr, dict):
        raise ValidationError("pr must be an object")
    _require_exact_keys(pr, {"title", "body", "base_sha", "head_sha"}, "pr")
    if not all(isinstance(pr[key], str) for key in ("title", "body")):
        raise ValidationError("pr title and body must be strings")
    for key in ("base_sha", "head_sha"):
        if not isinstance(pr[key], str) or re.fullmatch(r"[0-9a-f]{40}", pr[key]) is None:
            raise ValidationError(f"pr.{key} must be a 40-character lowercase SHA")
    if pr["base_sha"] == pr["head_sha"]:
        raise ValidationError("base_sha and head_sha must differ")

    paths = value["changed_paths"]
    if not isinstance(paths, list) or not paths:
        raise ValidationError("changed_paths must be a non-empty list")
    normalized_paths = [_relative_path(path, "changed_paths entry") for path in paths]
    if len(set(normalized_paths)) != len(normalized_paths):
        raise ValidationError("changed_paths must be unique")

    changes = value["changes"]
    if not isinstance(changes, list) or not changes:
        raise ValidationError("changes must be a non-empty list")
    change_paths: list[str] = []
    for index, change in enumerate(changes):
        if not isinstance(change, dict):
            raise ValidationError(f"changes[{index}] must be an object")
        _require_exact_keys(change, {"path", "patch", "content_after"}, f"changes[{index}]")
        change_paths.append(_relative_path(change["path"], f"changes[{index}].path"))
        if not isinstance(change["patch"], str) or not change["patch"]:
            raise ValidationError(f"changes[{index}].patch must be non-empty")
        if not isinstance(change["content_after"], str):
            raise ValidationError(f"changes[{index}].content_after must be a string")
    if set(change_paths) != set(normalized_paths) or len(change_paths) != len(normalized_paths):
        raise ValidationError("changes paths must exactly match changed_paths")

    rules = value["rules"]
    if not isinstance(rules, list) or not rules:
        raise ValidationError("rules must be a non-empty list")
    seen_rule_ids: set[str] = set()
    for source_index, source in enumerate(rules):
        if not isinstance(source, dict):
            raise ValidationError(f"rules[{source_index}] must be an object")
        _require_exact_keys(source, {"source", "scope", "rules"}, f"rules[{source_index}]")
        _relative_path(source["source"], f"rules[{source_index}].source")
        if not isinstance(source["scope"], str) or not source["scope"]:
            raise ValidationError(f"rules[{source_index}].scope must be non-empty")
        if not isinstance(source["rules"], list) or not source["rules"]:
            raise ValidationError(f"rules[{source_index}].rules must be non-empty")
        for rule_index, rule in enumerate(source["rules"]):
            label = f"rules[{source_index}].rules[{rule_index}]"
            if not isinstance(rule, dict):
                raise ValidationError(f"{label} must be an object")
            _require_exact_keys(rule, {"rule_id", "text"}, label)
            if not all(isinstance(rule[key], str) and rule[key] for key in ("rule_id", "text")):
                raise ValidationError(f"{label} values must be non-empty strings")
            if rule["rule_id"] in seen_rule_ids:
                raise ValidationError(f"duplicate rule_id: {rule['rule_id']}")
            seen_rule_ids.add(rule["rule_id"])

    serialized = json.dumps(value, ensure_ascii=False)
    if '"expected_findings"' in serialized or '"clean_control"' in serialized:
        raise ValidationError("model-visible input contains oracle fields")
    return value


def validate_fixture_oracle(value: Any, fixture_input: dict) -> dict:
    if not isinstance(value, dict):
        raise ValidationError("fixture oracle must be an object")
    _require_exact_keys(
        value,
        {"schema_version", "case_id", "fixture_revision", "clean_control", "expected_findings"},
        "fixture oracle",
    )
    if value["schema_version"] != 1:
        raise ValidationError("fixture oracle schema_version must be 1")
    if value["case_id"] != fixture_input["case_id"]:
        raise ValidationError("fixture oracle case_id mismatch")
    if value["fixture_revision"] != fixture_input["fixture_revision"]:
        raise ValidationError("fixture oracle revision mismatch")
    if not isinstance(value["clean_control"], bool):
        raise ValidationError("clean_control must be boolean")
    expected = value["expected_findings"]
    if not isinstance(expected, list):
        raise ValidationError("expected_findings must be a list")
    changed_paths = set(fixture_input["changed_paths"])
    for index, finding in enumerate(expected):
        _validate_finding(finding, f"expected_findings[{index}]", changed_paths)
    if value["clean_control"] != (len(expected) == 0):
        raise ValidationError("clean_control must be true exactly when expected_findings is empty")
    return value


def validate_review_output(value: Any) -> dict:
    if not isinstance(value, dict):
        raise ValidationError("review output must be an object")
    _require_exact_keys(value, {"findings", "summary"}, "review output")
    if not isinstance(value["findings"], list):
        raise ValidationError("findings must be a list")
    for index, finding in enumerate(value["findings"]):
        _validate_finding(finding, f"findings[{index}]")
    summary = value["summary"]
    if not isinstance(summary, dict):
        raise ValidationError("summary must be an object")
    _require_exact_keys(summary, set(CATEGORIES), "summary")
    for category, state in summary.items():
        if state not in SUMMARY_STATES:
            raise ValidationError(f"summary.{category} is invalid")
    return value


def validate_run_result(value: Any) -> dict:
    if not isinstance(value, dict):
        raise ValidationError("run result must be an object")
    _require_exact_keys(
        value,
        {
            "schema_version",
            "comparison_revision",
            "result_id",
            "case_id",
            "fixture_revision",
            "variant",
            "repetition",
            "attempt",
            "base_sha",
            "head_sha",
            "model",
            "reviewer_executor",
            "workflow_revision",
            "github_run_id",
            "timing",
            "runtime",
            "quality",
            "result",
        },
        "run result",
    )
    if value["schema_version"] != 1 or value["comparison_revision"] != "pr-review-core-r1":
        raise ValidationError("run result identity is invalid")
    if not isinstance(value["result_id"], str) or not value["result_id"]:
        raise ValidationError("result_id must be non-empty")
    if value["case_id"] not in CASE_IDS or value["fixture_revision"] != "r1":
        raise ValidationError("run result fixture identity is invalid")
    if value["variant"] not in VARIANTS:
        raise ValidationError("run result variant is invalid")
    _positive_int(value["repetition"], "run result repetition")
    _positive_int(value["attempt"], "run result attempt")
    for key in ("base_sha", "head_sha"):
        if not isinstance(value[key], str) or re.fullmatch(r"[0-9a-f]{40}", value[key]) is None:
            raise ValidationError(f"run result {key} is invalid")
    model = value["model"]
    if not isinstance(model, dict):
        raise ValidationError("run result model must be an object")
    _require_exact_keys(model, {"requested", "reported"}, "run result model")
    if not isinstance(model["requested"], str) or not model["requested"]:
        raise ValidationError("run result requested model is invalid")
    if model["reported"] is not None and not isinstance(model["reported"], str):
        raise ValidationError("run result reported model is invalid")
    if not isinstance(value["reviewer_executor"], dict) or not value["reviewer_executor"]:
        raise ValidationError("run result reviewer_executor is invalid")
    if not isinstance(value["workflow_revision"], str) or not value["workflow_revision"]:
        raise ValidationError("run result workflow_revision is invalid")
    if value["github_run_id"] is not None and not isinstance(value["github_run_id"], str):
        raise ValidationError("run result github_run_id is invalid")
    timing_keys = {
        "queue_ms",
        "setup_ms",
        "input_ms",
        "action_step_ms",
        "review_ms",
        "report_ms",
        "execution_ms",
        "e2e_ms",
    }
    if not isinstance(value["timing"], dict):
        raise ValidationError("run result timing must be an object")
    _require_exact_keys(value["timing"], timing_keys, "run result timing")
    for key, item in value["timing"].items():
        if item is not None and (not isinstance(item, (int, float)) or isinstance(item, bool) or item < 0):
            raise ValidationError(f"run result timing.{key} is invalid")
    runtime_keys = {"turns", "input_tokens", "output_tokens", "reported_cost_usd"}
    if not isinstance(value["runtime"], dict):
        raise ValidationError("run result runtime must be an object")
    _require_exact_keys(value["runtime"], runtime_keys, "run result runtime")
    for key, item in value["runtime"].items():
        if item is not None and (not isinstance(item, (int, float)) or isinstance(item, bool) or item < 0):
            raise ValidationError(f"run result runtime.{key} is invalid")
    quality_keys = {
        "observed",
        "expected_findings",
        "true_positive",
        "false_positive",
        "false_negative",
        "path_accuracy",
        "line_accuracy",
        "category_accuracy",
        "clean_control_major_false_positive",
        "scope_violation_count",
        "review_contract_violation",
        "summary_complete",
    }
    if not isinstance(value["quality"], dict):
        raise ValidationError("run result quality must be an object")
    _require_exact_keys(value["quality"], quality_keys, "run result quality")
    for key in quality_keys - {"observed", "summary_complete"}:
        item = value["quality"][key]
        if not isinstance(item, int) or isinstance(item, bool) or item < 0:
            raise ValidationError(f"run result quality.{key} is invalid")
    if not isinstance(value["quality"]["summary_complete"], bool):
        raise ValidationError("run result quality.summary_complete is invalid")
    if not isinstance(value["quality"]["observed"], bool):
        raise ValidationError("run result quality.observed is invalid")
    if value["result"] not in RESULT_STATUSES:
        raise ValidationError("run result status is invalid")
    return value


def _fixture_paths(case_id: str) -> tuple[Path, Path]:
    if case_id not in CASE_IDS:
        raise ValidationError(f"unknown case_id: {case_id}")
    case_dir = FIXTURE_ROOT / case_id
    return case_dir / "input.json", case_dir / "oracle.json"


def validate_all_fixtures() -> list[dict]:
    validated: list[dict] = []
    existing_dirs = sorted(path.name for path in FIXTURE_ROOT.iterdir() if path.is_dir())
    if existing_dirs != list(CASE_IDS):
        raise ValidationError(f"fixture cases mismatch: {existing_dirs}")
    for case_id in CASE_IDS:
        input_path, oracle_path = _fixture_paths(case_id)
        fixture_input = validate_fixture_input(_load_json(input_path), case_id)
        oracle = validate_fixture_oracle(_load_json(oracle_path), fixture_input)
        validated.append(
            {
                "case_id": case_id,
                "input_sha256": _sha256(input_path),
                "oracle_sha256": _sha256(oracle_path),
                "expected_findings": len(oracle["expected_findings"]),
                "clean_control": oracle["clean_control"],
            }
        )
    return validated


def prepare_input(case_id: str, variant: str, output_dir: Path) -> dict:
    if variant not in VARIANTS:
        raise ValidationError(f"unknown variant: {variant}")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValidationError(f"output directory is not empty: {output_dir}")
    started = time.perf_counter_ns()
    input_path, oracle_path = _fixture_paths(case_id)
    fixture_input = validate_fixture_input(_load_json(input_path), case_id)
    validate_fixture_oracle(_load_json(oracle_path), fixture_input)
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(input_path, output_dir / "review-input.json")
    shutil.copyfile(REVIEW_CONTRACT_PATH, output_dir / "review-contract.md")
    shutil.copyfile(REVIEW_SCHEMA_PATH, output_dir / "review-output-schema.json")
    shutil.copyfile(FIXTURE_TOOL_PATH, output_dir / "fixture-tool")
    shutil.copyfile(Path(__file__), output_dir / "pr-review-measurement.py")
    (output_dir / "fixture-tool").chmod(0o755)
    elapsed_ms = (time.perf_counter_ns() - started) // 1_000_000
    metadata = {
        "schema_version": 1,
        "case_id": case_id,
        "fixture_revision": fixture_input["fixture_revision"],
        "review_contract_revision": fixture_input["review_contract_revision"],
        "variant": variant,
        "input_sha256": _sha256(output_dir / "review-input.json"),
        "review_contract_sha256": _sha256(output_dir / "review-contract.md"),
        "review_output_schema_sha256": _sha256(output_dir / "review-output-schema.json"),
        "collector_sha256": _sha256(output_dir / "pr-review-measurement.py"),
        "input_ms": elapsed_ms,
    }
    _write_json_once(output_dir / "prepare-metadata.json", metadata)
    return metadata


def validate_prepare_metadata(value: Any, case_id: str, variant: str) -> dict:
    if not isinstance(value, dict):
        raise ValidationError("prepare metadata must be an object")
    _require_exact_keys(
        value,
        {
            "schema_version",
            "case_id",
            "fixture_revision",
            "review_contract_revision",
            "variant",
            "input_sha256",
            "review_contract_sha256",
            "review_output_schema_sha256",
            "collector_sha256",
            "input_ms",
        },
        "prepare metadata",
    )
    input_path, _ = _fixture_paths(case_id)
    expected = {
        "schema_version": 1,
        "case_id": case_id,
        "fixture_revision": "r1",
        "review_contract_revision": "pr-review-contract-r1",
        "variant": variant,
        "input_sha256": _sha256(input_path),
        "review_contract_sha256": _sha256(REVIEW_CONTRACT_PATH),
        "review_output_schema_sha256": _sha256(REVIEW_SCHEMA_PATH),
        "collector_sha256": _sha256(Path(__file__)),
    }
    for key, expected_value in expected.items():
        if value[key] != expected_value:
            raise ValidationError(f"prepare metadata {key} mismatch")
    if not isinstance(value["input_ms"], (int, float)) or isinstance(value["input_ms"], bool) or value["input_ms"] < 0:
        raise ValidationError("prepare metadata input_ms is invalid")
    return value


def _iter_json_values(value: Any) -> Iterable[dict]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _iter_json_values(child)
    elif isinstance(value, list):
        for child in value:
            yield from _iter_json_values(child)


def _parse_execution_file(path: Path | None) -> dict:
    runtime = {
        "duration_ms": None,
        "turns": None,
        "input_tokens": None,
        "output_tokens": None,
        "reported_cost_usd": None,
        "model": None,
    }
    if path is None or not path.is_file():
        return runtime
    text = path.read_text(encoding="utf-8", errors="replace")
    documents: list[Any] = []
    try:
        documents.append(json.loads(text))
    except json.JSONDecodeError:
        for line in text.splitlines():
            try:
                documents.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    aliases = {
        "duration_ms": ("duration_ms",),
        "turns": ("num_turns", "turns"),
        "input_tokens": ("input_tokens",),
        "output_tokens": ("output_tokens",),
        "reported_cost_usd": ("total_cost_usd", "reported_cost_usd"),
        "model": ("model", "model_name"),
    }
    for document in documents:
        for mapping in _iter_json_values(document):
            for destination, keys in aliases.items():
                if runtime[destination] is not None:
                    continue
                for key in keys:
                    candidate = mapping.get(key)
                    if destination == "model" and isinstance(candidate, str) and candidate:
                        runtime[destination] = candidate
                        break
                    if destination != "model" and isinstance(candidate, (int, float)) and not isinstance(candidate, bool):
                        runtime[destination] = candidate
                        break
    return runtime


def collect_review(
    raw_output_path: Path,
    action_conclusion: str,
    action_execution_file: Path | None,
    started_ms: int,
    finished_ms: int,
    model_requested: str,
    output_dir: Path,
) -> dict:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValidationError(f"output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_valid = False
    validation_error: str | None = None
    if action_conclusion == "success":
        try:
            review_output = validate_review_output(_load_json(raw_output_path))
            _write_json_once(output_dir / "review-output.json", review_output)
            output_valid = True
        except ValidationError as exc:
            validation_error = str(exc)
    runtime = _parse_execution_file(action_execution_file)
    metadata = {
        "schema_version": 1,
        "action_conclusion": action_conclusion,
        "output_valid": output_valid,
        "validation_error": validation_error,
        "model_requested": model_requested,
        "action_step_ms": max(0, finished_ms - started_ms),
        "runtime": runtime,
    }
    _write_json_once(output_dir / "review-metadata.json", metadata)
    return metadata


def validate_review_metadata(value: Any, model_requested: str) -> dict:
    if not isinstance(value, dict):
        raise ValidationError("review metadata must be an object")
    _require_exact_keys(
        value,
        {
            "schema_version",
            "action_conclusion",
            "output_valid",
            "validation_error",
            "model_requested",
            "action_step_ms",
            "runtime",
        },
        "review metadata",
    )
    if value["schema_version"] != 1:
        raise ValidationError("review metadata schema_version is invalid")
    if not isinstance(value["action_conclusion"], str) or not value["action_conclusion"]:
        raise ValidationError("review metadata action_conclusion is invalid")
    if not isinstance(value["output_valid"], bool):
        raise ValidationError("review metadata output_valid is invalid")
    if value["validation_error"] is not None and not isinstance(value["validation_error"], str):
        raise ValidationError("review metadata validation_error is invalid")
    if value["model_requested"] != model_requested:
        raise ValidationError("review metadata model_requested mismatch")
    if not isinstance(value["action_step_ms"], (int, float)) or isinstance(value["action_step_ms"], bool) or value["action_step_ms"] < 0:
        raise ValidationError("review metadata action_step_ms is invalid")
    runtime = value["runtime"]
    if not isinstance(runtime, dict):
        raise ValidationError("review metadata runtime must be an object")
    _require_exact_keys(
        runtime,
        {"duration_ms", "turns", "input_tokens", "output_tokens", "reported_cost_usd", "model"},
        "review metadata runtime",
    )
    for key in ("duration_ms", "turns", "input_tokens", "output_tokens", "reported_cost_usd"):
        item = runtime[key]
        if item is not None and (not isinstance(item, (int, float)) or isinstance(item, bool) or item < 0):
            raise ValidationError(f"review metadata runtime.{key} is invalid")
    if runtime["model"] is not None and not isinstance(runtime["model"], str):
        raise ValidationError("review metadata runtime.model is invalid")
    return value


def _line_ranges_overlap(left: dict, right: dict) -> bool:
    return left["line_start"] <= right["line_end"] and right["line_start"] <= left["line_end"]


def _finding_identity_matches(expected: dict, actual: dict) -> bool:
    return (
        expected["category"] == actual["category"]
        and expected["rule_id"] == actual["rule_id"]
        and expected["path"] == actual["path"]
        and _line_ranges_overlap(expected, actual)
    )


def _quality_result(oracle: dict, review_output: dict, fixture_input: dict) -> dict:
    expected = oracle["expected_findings"]
    actual = review_output["findings"]
    matched_actual: set[int] = set()
    true_positive = 0
    for expected_finding in expected:
        for index, actual_finding in enumerate(actual):
            if index not in matched_actual and _finding_identity_matches(expected_finding, actual_finding):
                matched_actual.add(index)
                true_positive += 1
                break
    false_negative = len(expected) - true_positive
    false_positive = len(actual) - len(matched_actual)
    path_accuracy = sum(
        1
        for expected_finding in expected
        if any(expected_finding["path"] == finding["path"] for finding in actual)
    )
    line_accuracy = sum(
        1
        for expected_finding in expected
        if any(
            expected_finding["path"] == finding["path"]
            and _line_ranges_overlap(expected_finding, finding)
            for finding in actual
        )
    )
    category_accuracy = sum(
        1
        for expected_finding in expected
        if any(
            expected_finding["path"] == finding["path"]
            and _line_ranges_overlap(expected_finding, finding)
            and expected_finding["category"] == finding["category"]
            for finding in actual
        )
    )
    clean_major_false_positive = 0
    if oracle["clean_control"]:
        clean_major_false_positive = sum(
            1 for finding in actual if finding["severity"] == "major"
        )
    finding_categories = {finding["category"] for finding in actual}
    applicable_rule_ids = {
        rule["rule_id"]
        for source in fixture_input["rules"]
        for rule in source["rules"]
    }
    scope_violation_count = sum(
        1 for finding in actual if finding["rule_id"] not in applicable_rule_ids
    )
    review_contract_violation = scope_violation_count + sum(
        1
        for category in CATEGORIES
        if review_output["summary"][category]
        != ("fail" if category in finding_categories else "pass")
    )
    return {
        "observed": True,
        "expected_findings": len(expected),
        "true_positive": true_positive,
        "false_positive": false_positive,
        "false_negative": false_negative,
        "path_accuracy": path_accuracy,
        "line_accuracy": line_accuracy,
        "category_accuracy": category_accuracy,
        "clean_control_major_false_positive": clean_major_false_positive,
        "scope_violation_count": scope_violation_count,
        "review_contract_violation": review_contract_violation,
        "summary_complete": set(review_output["summary"]) == set(CATEGORIES),
    }


def grade_run(
    case_id: str,
    variant: str,
    repetition: int,
    attempt: int,
    model_requested: str,
    review_output_path: Path,
    review_metadata_path: Path,
    prepare_metadata_path: Path,
    output_path: Path,
    github_run_id: str | None = None,
) -> dict:
    if variant not in VARIANTS:
        raise ValidationError(f"unknown variant: {variant}")
    _positive_int(repetition, "repetition")
    _positive_int(attempt, "attempt")
    input_path, oracle_path = _fixture_paths(case_id)
    fixture_input = validate_fixture_input(_load_json(input_path), case_id)
    oracle = validate_fixture_oracle(_load_json(oracle_path), fixture_input)
    contract = _load_json(CONTRACT_PATH)
    prepare_metadata = validate_prepare_metadata(_load_json(prepare_metadata_path), case_id, variant)
    review_metadata = validate_review_metadata(_load_json(review_metadata_path), model_requested)

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
    if review_metadata.get("action_conclusion") != "success":
        result = "execution_failed"
    elif not review_metadata.get("output_valid") or not review_output_path.is_file():
        result = "invalid_output"
    else:
        review_output = validate_review_output(_load_json(review_output_path))
        quality = _quality_result(oracle, review_output, fixture_input)
        hard_gate_failed = (
            quality["false_negative"] != 0
            or quality["clean_control_major_false_positive"] != 0
            or quality["review_contract_violation"] != 0
        )
        result = "quality_failed" if hard_gate_failed else "pass"

    runtime = review_metadata.get("runtime", {})
    model_reported = runtime.get("model")
    if result == "pass" and (not model_reported or model_reported != model_requested):
        result = "measurement_incomplete"

    run_result = {
        "schema_version": 1,
        "comparison_revision": contract["comparison_revision"],
        "result_id": f"{contract['comparison_revision']}:{case_id}:{variant}:r{repetition}:a{attempt}",
        "case_id": case_id,
        "fixture_revision": fixture_input["fixture_revision"],
        "variant": variant,
        "repetition": repetition,
        "attempt": attempt,
        "base_sha": fixture_input["pr"]["base_sha"],
        "head_sha": fixture_input["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": model_reported},
        "reviewer_executor": contract["reviewer_executor"],
        "workflow_revision": contract["workflow_revision"],
        "github_run_id": github_run_id,
        "timing": {
            "queue_ms": None,
            "setup_ms": None,
            "input_ms": prepare_metadata.get("input_ms"),
            "action_step_ms": review_metadata.get("action_step_ms"),
            "review_ms": runtime.get("duration_ms"),
            "report_ms": None,
            "execution_ms": review_metadata.get("action_step_ms"),
            "e2e_ms": None,
        },
        "runtime": {
            "turns": runtime.get("turns"),
            "input_tokens": runtime.get("input_tokens"),
            "output_tokens": runtime.get("output_tokens"),
            "reported_cost_usd": runtime.get("reported_cost_usd"),
        },
        "quality": quality,
        "result": result,
    }
    validate_run_result(run_result)
    _write_json_once(output_path, run_result)
    return run_result


def record_terminal_run(
    case_id: str,
    variant: str,
    repetition: int,
    attempt: int,
    model_requested: str,
    status: str,
    output_path: Path,
    github_run_id: str | None = None,
) -> dict:
    if variant not in VARIANTS:
        raise ValidationError(f"unknown variant: {variant}")
    if status not in {"execution_failed", "timeout", "cancelled", "measurement_incomplete"}:
        raise ValidationError(f"invalid terminal status: {status}")
    _positive_int(repetition, "repetition")
    _positive_int(attempt, "attempt")
    input_path, oracle_path = _fixture_paths(case_id)
    fixture_input = validate_fixture_input(_load_json(input_path), case_id)
    oracle = validate_fixture_oracle(_load_json(oracle_path), fixture_input)
    contract = _load_json(CONTRACT_PATH)
    run_result = {
        "schema_version": 1,
        "comparison_revision": contract["comparison_revision"],
        "result_id": f"{contract['comparison_revision']}:{case_id}:{variant}:r{repetition}:a{attempt}",
        "case_id": case_id,
        "fixture_revision": fixture_input["fixture_revision"],
        "variant": variant,
        "repetition": repetition,
        "attempt": attempt,
        "base_sha": fixture_input["pr"]["base_sha"],
        "head_sha": fixture_input["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": None},
        "reviewer_executor": contract["reviewer_executor"],
        "workflow_revision": contract["workflow_revision"],
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
            "reported_cost_usd": None,
        },
        "quality": {
            "observed": False,
            "expected_findings": len(oracle["expected_findings"]),
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
        "result": status,
    }
    validate_run_result(run_result)
    _write_json_once(output_path, run_result)
    return run_result


def summarize_results(paths: list[Path]) -> dict:
    if not paths:
        raise ValidationError("at least one result is required")
    results = [validate_run_result(_load_json(path)) for path in paths]
    seen_ids: set[str] = set()
    by_variant: dict[str, list[dict]] = {variant: [] for variant in VARIANTS}
    for result in results:
        result_id = result.get("result_id")
        if not isinstance(result_id, str) or result_id in seen_ids:
            raise ValidationError("result_id is missing or duplicated")
        seen_ids.add(result_id)
        variant = result.get("variant")
        if variant not in by_variant:
            raise ValidationError(f"unknown result variant: {variant}")
        by_variant[variant].append(result)
    summary: dict[str, Any] = {
        "schema_version": 1,
        "comparison_revision": "pr-review-core-r1",
        "result_count": len(results),
        "variants": {},
    }
    for variant, variant_results in by_variant.items():
        passed = [result for result in variant_results if result.get("result") == "pass"]
        execution_values = [
            result["timing"]["execution_ms"]
            for result in passed
            if isinstance(result.get("timing", {}).get("execution_ms"), (int, float))
        ]
        review_values = [
            result["timing"]["review_ms"]
            for result in passed
            if isinstance(result.get("timing", {}).get("review_ms"), (int, float))
        ]
        summary["variants"][variant] = {
            "result_count": len(variant_results),
            "pass_count": len(passed),
            "status_counts": {
                status: sum(1 for result in variant_results if result.get("result") == status)
                for status in RESULT_STATUSES
            },
            "median_execution_ms": statistics.median(execution_values) if execution_values else None,
            "median_review_ms": statistics.median(review_values) if review_values else None,
        }
    return summary


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-fixtures")

    prepare = subparsers.add_parser("prepare-input")
    prepare.add_argument("--case-id", required=True, choices=CASE_IDS)
    prepare.add_argument("--variant", required=True, choices=VARIANTS)
    prepare.add_argument("--output-dir", required=True, type=Path)

    validate_output = subparsers.add_parser("validate-review-output")
    validate_output.add_argument("--input", required=True, type=Path)

    collect = subparsers.add_parser("collect-review")
    collect.add_argument("--raw-output", required=True, type=Path)
    collect.add_argument("--action-conclusion", required=True)
    collect.add_argument("--action-execution-file", type=Path)
    collect.add_argument("--started-ms", required=True, type=int)
    collect.add_argument("--finished-ms", required=True, type=int)
    collect.add_argument("--model-requested", required=True)
    collect.add_argument("--output-dir", required=True, type=Path)

    grade = subparsers.add_parser("grade")
    grade.add_argument("--case-id", required=True, choices=CASE_IDS)
    grade.add_argument("--variant", required=True, choices=VARIANTS)
    grade.add_argument("--repetition", required=True, type=int)
    grade.add_argument("--attempt", required=True, type=int)
    grade.add_argument("--model-requested", required=True)
    grade.add_argument("--review-output", required=True, type=Path)
    grade.add_argument("--review-metadata", required=True, type=Path)
    grade.add_argument("--prepare-metadata", required=True, type=Path)
    grade.add_argument("--output", required=True, type=Path)
    grade.add_argument("--github-run-id")

    terminal = subparsers.add_parser("record-terminal")
    terminal.add_argument("--case-id", required=True, choices=CASE_IDS)
    terminal.add_argument("--variant", required=True, choices=VARIANTS)
    terminal.add_argument("--repetition", required=True, type=int)
    terminal.add_argument("--attempt", required=True, type=int)
    terminal.add_argument("--model-requested", required=True)
    terminal.add_argument(
        "--status",
        required=True,
        choices=("execution_failed", "timeout", "cancelled", "measurement_incomplete"),
    )
    terminal.add_argument("--output", required=True, type=Path)
    terminal.add_argument("--github-run-id")

    summarize = subparsers.add_parser("summarize")
    summarize.add_argument("--result", action="append", required=True, type=Path)
    summarize.add_argument("--output", required=True, type=Path)
    return parser


def main() -> int:
    args = _build_parser().parse_args()
    try:
        if args.command == "validate-fixtures":
            print(json.dumps(validate_all_fixtures(), ensure_ascii=False, indent=2))
        elif args.command == "prepare-input":
            metadata = prepare_input(args.case_id, args.variant, args.output_dir)
            print(json.dumps(metadata, ensure_ascii=False, indent=2))
        elif args.command == "validate-review-output":
            validate_review_output(_load_json(args.input))
            print("review output is valid")
        elif args.command == "collect-review":
            metadata = collect_review(
                args.raw_output,
                args.action_conclusion,
                args.action_execution_file,
                args.started_ms,
                args.finished_ms,
                args.model_requested,
                args.output_dir,
            )
            print(json.dumps(metadata, ensure_ascii=False, indent=2))
        elif args.command == "grade":
            result = grade_run(
                args.case_id,
                args.variant,
                args.repetition,
                args.attempt,
                args.model_requested,
                args.review_output,
                args.review_metadata,
                args.prepare_metadata,
                args.output,
                args.github_run_id,
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.command == "record-terminal":
            result = record_terminal_run(
                args.case_id,
                args.variant,
                args.repetition,
                args.attempt,
                args.model_requested,
                args.status,
                args.output,
                args.github_run_id,
            )
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.command == "summarize":
            summary = summarize_results(args.result)
            _write_json_once(args.output, summary)
            print(json.dumps(summary, ensure_ascii=False, indent=2))
    except ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
