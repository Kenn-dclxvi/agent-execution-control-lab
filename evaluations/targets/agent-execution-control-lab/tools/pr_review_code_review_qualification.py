#!/usr/bin/env python3
"""Run the Claude Code code-review workflow against PRR-C01/r4."""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
from pathlib import Path

import pr_review_measurement as measurement
import pr_review_qualification as legacy


INSTANCE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PROFILE_ID = "pr-review-claude-code-core-c01-r4-qualification-n2-r1"
PROFILE_PATH = INSTANCE_ROOT / "profiles" / f"{PROFILE_ID}.json"
PREFLIGHT_PATH = INSTANCE_ROOT / "contracts" / f"{PROFILE_ID}-preflight.json"
SNAPSHOT_PATH = INSTANCE_ROOT / "contracts" / "baseline-repository-snapshot-prr-c01-r4-r1.json"
WORKFLOW_PATH = REPOSITORY_ROOT / ".github/workflows/pr-review-qualify-claude-code-core.yml"
WORKFLOW_REVISION = "pr-review-qualify-claude-code-core-r1"
COMPARISON_REVISION = "pr-review-claude-code-core-qualification-r1"
RATING_ID = "pr-review-finding-quality-v5"
VARIANT = "claude-code-review-core"


class QualificationError(ValueError):
    pass


def _fixture_and_oracle() -> tuple[dict, dict]:
    fixture = legacy._load_json(INSTANCE_ROOT / "cases/PRR-C01/r4/input.json")
    oracle = legacy._load_json(INSTANCE_ROOT / "cases/PRR-C01/r4/oracle.json")
    compatible_fixture = copy.deepcopy(fixture)
    compatible_fixture.update(schema_version=3, fixture_revision="r3")
    measurement.validate_fixture_input(compatible_fixture, "PRR-C01")
    compatible_oracle = copy.deepcopy(oracle)
    compatible_oracle.update(schema_version=3, fixture_revision="r3")
    measurement.validate_fixture_oracle(compatible_oracle, compatible_fixture)
    if fixture.get("schema_version") != 4 or fixture.get("fixture_revision") != "r4":
        raise QualificationError("fixture identity mismatch")
    return fixture, oracle


def _workflow_trace(path: Path | None) -> dict:
    groups: list[list[str]] = []
    input_tokens = 0
    output_tokens = 0
    usage_records = 0
    subagent_usage_records = 0
    if path and path.is_file():
        try:
            documents = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            documents = []
        if not isinstance(documents, list):
            documents = [documents]
        for message in documents:
            if not isinstance(message, dict) or message.get("type") != "assistant":
                continue
            body = message.get("message")
            usage = body.get("usage") if isinstance(body, dict) else None
            observed_input, observed_output = measurement._usage_totals(usage)
            if observed_input is not None or observed_output is not None:
                input_tokens += observed_input or 0
                output_tokens += observed_output or 0
                usage_records += 1
                if message.get("parent_tool_use_id") is not None:
                    subagent_usage_records += 1
            if message.get("parent_tool_use_id") is not None:
                continue
            content = body.get("content", []) if isinstance(body, dict) else []
            models = []
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                if block.get("name") not in {"Agent", "Task"}:
                    continue
                tool_input = block.get("input", {})
                model = tool_input.get("model") if isinstance(tool_input, dict) else None
                models.append(model if model in {"haiku", "sonnet", "opus"} else "unknown")
            if models:
                groups.append(models)
    first = len(groups) >= 1 and groups[0] == ["haiku"]
    second = len(groups) >= 2 and groups[1] == ["haiku"]
    third = len(groups) >= 3 and groups[2] == ["sonnet"]
    reviewers = (
        len(groups) >= 4
        and sorted(groups[3]) == ["opus", "opus", "sonnet", "sonnet"]
    )
    validators = [model for group in groups[4:] for model in group]
    validation = bool(validators) and set(validators) <= {"sonnet", "opus"}
    subagent_usage = subagent_usage_records > 0
    return {
        "agent_model_groups": groups,
        "eligibility_haiku": first,
        "authority_haiku": second,
        "summary_sonnet": third,
        "parallel_reviewers_2_sonnet_2_opus": reviewers,
        "separate_validation_agents": validation,
        "subagent_usage_observed": subagent_usage,
        "usage_records": usage_records,
        "all_agent_input_tokens": input_tokens if usage_records else None,
        "all_agent_output_tokens": output_tokens if usage_records else None,
        "complete": all((first, second, third, reviewers, validation, subagent_usage)),
    }


def validate_preflight(
    repetition: int, prior_admission: Path | None = None
) -> tuple[dict, dict]:
    if repetition not in {1, 2}:
        raise QualificationError("repetition must be 1 or 2")
    profile = legacy._load_json(PROFILE_PATH)
    preflight = legacy._load_json(PREFLIGHT_PATH)
    if profile.get("profile_id") != PROFILE_ID or profile.get("state") != "frozen_not_executed":
        raise QualificationError("profile identity mismatch")
    if profile.get("cases") != [{"id": "PRR-C01", "revision": "r4"}]:
        raise QualificationError("profile case mismatch")
    conditions = profile.get("comparison_conditions", {})
    if conditions.get("variant") != VARIANT:
        raise QualificationError("profile variant mismatch")
    if preflight.get("state") != "ready_not_executed" or preflight.get("profile") != {
        "profile_id": PROFILE_ID,
        "path": f"profiles/{PROFILE_PATH.name}",
        "sha256": legacy._sha256(PROFILE_PATH),
    }:
        raise QualificationError("preflight profile receipt mismatch")
    for artifact in preflight.get("verified_artifacts", []):
        artifact_path = (
            REPOSITORY_ROOT / artifact["path"]
            if artifact["path"].startswith(".github/")
            else INSTANCE_ROOT / artifact["path"]
        )
        if not artifact_path.is_file() or legacy._sha256(artifact_path) != artifact.get("sha256"):
            raise QualificationError(f"preflight artifact mismatch: {artifact.get('path')}")
    audit = legacy._load_json(INSTANCE_ROOT / conditions["fixture_identity"]["case_design_audit_path"])
    rating = legacy._load_json(INSTANCE_ROOT / conditions["quality_rating"]["path"])
    mapping = legacy._load_json(INSTANCE_ROOT / conditions["workflow_mapping"]["path"])
    boundary = legacy._load_json(INSTANCE_ROOT / conditions["measurement_boundary"]["path"])
    if audit.get("decision") != "satisfied" or rating.get("state") != "independent_qualification_satisfied":
        raise QualificationError("case admission mismatch")
    if mapping.get("state") != "satisfied_not_executed" or boundary.get("state") != "satisfied":
        raise QualificationError("workflow mapping mismatch")
    if conditions.get("workflow", {}).get("revision") != WORKFLOW_REVISION:
        raise QualificationError("workflow revision mismatch")
    if conditions.get("model", {}).get("requested") != "claude-sonnet-5":
        raise QualificationError("root model mismatch")
    executor = conditions.get("executor_parameters", {})
    if executor.get("max_workers") != 24 or executor.get("internal_review_concurrency") != 4:
        raise QualificationError("executor concurrency mismatch")
    planned = {"case_id": "PRR-C01", "fixture_revision": "r4", "variant": VARIANT, "repetition": repetition}
    if planned not in preflight.get("planned_slots", []):
        raise QualificationError("slot is not in the fixed plan")
    if repetition == 2:
        if prior_admission is None:
            raise QualificationError("repetition 2 requires repetition 1 admission")
        admission = legacy._load_json(prior_admission)
        if admission.get("state") != "satisfied" or admission.get(
            "admitted_repetition"
        ) != 2:
            raise QualificationError("repetition 1 admission is not satisfied")
    _fixture_and_oracle()
    return profile, preflight


def prepare_input(repetition: int, output_dir: Path) -> dict:
    import pr_review_repository_snapshot_r3 as snapshot_r3

    # The legacy preparer imports the r2 module name internally. Bind that name
    # to the r3 materializer required by the r4 new-file overlay.
    sys.modules["pr_review_repository_snapshot_r2"] = snapshot_r3
    legacy.PROFILE_ID = PROFILE_ID
    legacy.PROFILE_PATH = PROFILE_PATH
    legacy.PREFLIGHT_PATH = PREFLIGHT_PATH
    legacy.SNAPSHOT_RECEIPT_PATH = SNAPSHOT_PATH
    legacy.validate_preflight = validate_preflight
    legacy.__file__ = __file__
    metadata = legacy.prepare_input(repetition, output_dir)
    (output_dir / "pr-review-qualification.py").replace(
        output_dir / "pr_review_code_review_qualification.py"
    )
    shutil.copyfile(
        INSTANCE_ROOT / "contracts/prr-c01-r4-review-eligibility-r1.json",
        output_dir / "review-eligibility.json",
    )
    metadata.update(fixture_revision="r4", variant=VARIANT)
    (output_dir / "prepare-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def collect_review(*args, **kwargs) -> dict:
    metadata = legacy.collect_review(*args, **kwargs)
    execution_file = args[2] if len(args) > 2 else kwargs.get("execution_file")
    metadata["workflow_trace"] = _workflow_trace(execution_file)
    trace = metadata["workflow_trace"]
    if trace["subagent_usage_observed"]:
        metadata["runtime"]["input_tokens"] = trace["all_agent_input_tokens"]
        metadata["runtime"]["output_tokens"] = trace["all_agent_output_tokens"]
    output_dir = args[-1] if args else kwargs["output_dir"]
    (Path(output_dir) / "review-metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def grade_run(repetition: int, attempt: int, model_requested: str, review_output: Path,
              review_metadata: Path, prepare_metadata: Path, output: Path,
              github_run_id: str) -> dict:
    profile, _ = validate_preflight(repetition)
    fixture, oracle = _fixture_and_oracle()
    metadata = legacy._load_json(review_metadata)
    prepared = legacy._load_json(prepare_metadata)
    quality = {"observed": False, "expected_findings": 1, "true_positive": 0,
               "false_positive": 0, "false_negative": 1, "path_accuracy": 0,
               "line_accuracy": 0, "category_accuracy": 0,
               "clean_control_major_false_positive": 0, "scope_violation_count": 0,
               "review_contract_violation": 0, "summary_complete": False}
    if metadata.get("action_conclusion") != "success":
        result = "execution_failed"
    elif not metadata.get("output_valid") or not review_output.is_file():
        result = "invalid_output"
    else:
        review = measurement.validate_review_output_v2(
            legacy._load_json(review_output), set(fixture["changed_paths"])
        )
        quality = legacy._quality_result(oracle, review, fixture)
        result = "pass" if quality["false_negative"] == quality["false_positive"] == quality["review_contract_violation"] == 0 else "quality_failed"
    runtime = metadata.get("runtime", {})
    trace = metadata.get("workflow_trace", {})
    if result == "pass" and (runtime.get("model") != model_requested or not trace.get("complete")):
        result = "measurement_incomplete"
    total = None
    if runtime.get("input_tokens") is not None and runtime.get("output_tokens") is not None:
        total = runtime["input_tokens"] + runtime["output_tokens"]
    run = {
        "schema_version": 7, "comparison_revision": COMPARISON_REVISION,
        "profile_id": PROFILE_ID, "quality_rating_contract": RATING_ID,
        "result_id": f"{COMPARISON_REVISION}:PRR-C01:{VARIANT}:r{repetition}:a{attempt}",
        "case_id": "PRR-C01", "fixture_revision": "r4", "variant": VARIANT,
        "repetition": repetition, "attempt": attempt, "base_sha": fixture["pr"]["base_sha"],
        "head_sha": fixture["pr"]["head_sha"],
        "model": {"requested": model_requested, "reported": runtime.get("model")},
        "reviewer_executor": profile["comparison_conditions"]["agent_environment"],
        "workflow_revision": WORKFLOW_REVISION, "workflow_trace": trace,
        "github_run_id": github_run_id,
        "timing": {"queue_ms": None, "setup_ms": None, "input_ms": prepared["input_ms"],
                   "action_step_ms": metadata["action_step_ms"], "review_ms": runtime.get("duration_ms"),
                   "report_ms": None, "execution_ms": metadata["action_step_ms"], "e2e_ms": None},
        "runtime": {"turns": runtime.get("turns"), "input_tokens": runtime.get("input_tokens"),
                    "output_tokens": runtime.get("output_tokens"), "total_tokens": total,
                    "reported_cost_usd": runtime.get("reported_cost_usd")},
        "quality": quality, "quality_score": measurement._quality_score(result, quality), "result": result,
    }
    legacy._write_json_once(output, run)
    return run


def record_terminal(repetition: int, attempt: int, model_requested: str, status: str,
                    output: Path, github_run_id: str) -> dict:
    profile, _ = validate_preflight(repetition)
    fixture, _ = _fixture_and_oracle()
    run = {"schema_version": 7, "comparison_revision": COMPARISON_REVISION,
           "profile_id": PROFILE_ID, "quality_rating_contract": RATING_ID,
           "result_id": f"{COMPARISON_REVISION}:PRR-C01:{VARIANT}:r{repetition}:a{attempt}",
           "case_id": "PRR-C01", "fixture_revision": "r4", "variant": VARIANT,
           "repetition": repetition, "attempt": attempt, "base_sha": fixture["pr"]["base_sha"],
           "head_sha": fixture["pr"]["head_sha"], "model": {"requested": model_requested, "reported": None},
           "reviewer_executor": profile["comparison_conditions"]["agent_environment"],
           "workflow_revision": WORKFLOW_REVISION, "workflow_trace": {"complete": False},
           "github_run_id": github_run_id, "timing": {key: None for key in ("queue_ms", "setup_ms", "input_ms", "action_step_ms", "review_ms", "report_ms", "execution_ms", "e2e_ms")},
           "runtime": {key: None for key in ("turns", "input_tokens", "output_tokens", "total_tokens", "reported_cost_usd")},
           "quality": {"observed": False, "expected_findings": 1, "true_positive": 0, "false_positive": 0, "false_negative": 0, "path_accuracy": 0, "line_accuracy": 0, "category_accuracy": 0, "clean_control_major_false_positive": 0, "scope_violation_count": 0, "review_contract_violation": 0, "summary_complete": False},
           "quality_score": None, "result": status}
    legacy._write_json_once(output, run)
    return run


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate-preflight", "prepare"):
        item = sub.add_parser(name); item.add_argument("--repetition", required=True, type=int)
        if name == "prepare": item.add_argument("--output-dir", required=True, type=Path)
    collect = sub.add_parser("collect")
    for name in ("raw-output", "execution-file", "review-input", "output-dir"): collect.add_argument(f"--{name}", type=Path, required=name != "execution-file")
    for name in ("action-conclusion", "model-requested"): collect.add_argument(f"--{name}", required=True)
    for name in ("started-ms", "finished-ms"): collect.add_argument(f"--{name}", required=True, type=int)
    for command in ("grade", "record-terminal"):
        item = sub.add_parser(command)
        for name in ("repetition", "attempt"): item.add_argument(f"--{name}", required=True, type=int)
        for name in ("model-requested", "github-run-id"): item.add_argument(f"--{name}", required=True)
        item.add_argument("--output", required=True, type=Path)
        if command == "grade":
            for name in ("review-output", "review-metadata", "prepare-metadata"): item.add_argument(f"--{name}", required=True, type=Path)
        else: item.add_argument("--status", required=True)
    args = parser.parse_args()
    try:
        if args.command == "validate-preflight": validate_preflight(args.repetition); print("qualification preflight is valid")
        elif args.command == "prepare": print(json.dumps(prepare_input(args.repetition, args.output_dir), ensure_ascii=False))
        elif args.command == "collect": print(json.dumps(collect_review(args.raw_output, args.action_conclusion, args.execution_file, args.started_ms, args.finished_ms, args.model_requested, args.review_input, args.output_dir), ensure_ascii=False))
        elif args.command == "grade": print(json.dumps(grade_run(args.repetition, args.attempt, args.model_requested, args.review_output, args.review_metadata, args.prepare_metadata, args.output, args.github_run_id), ensure_ascii=False))
        else: print(json.dumps(record_terminal(args.repetition, args.attempt, args.model_requested, args.status, args.output, args.github_run_id), ensure_ascii=False))
    except (QualificationError, legacy.QualificationError, measurement.ValidationError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr); return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
