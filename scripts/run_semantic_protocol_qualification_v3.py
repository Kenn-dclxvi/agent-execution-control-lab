#!/usr/bin/env python3
"""Plan and execute missing i002-i005 slots for semantic-protocol N=5 extension."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

try:
    from . import run_semantic_protocol_qualification_v2 as base
except ImportError:
    import run_semantic_protocol_qualification_v2 as base

_base_validate_preflight = base.validate_preflight

QualificationGateError = base.QualificationGateError
canonical_bytes = base.canonical_bytes
load_object = base.load_object
sha256_file = base.sha256_file
write_once = base.write_once


def _reference_compatibility_fields(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "target": plan.get("target"),
        "target_registration": plan.get("target_registration"),
        "prompt_set_identity": plan.get("prompt_set_identity"),
        "evaluation_set_ref": plan.get("evaluation_set_ref"),
        "runtime_ref": plan.get("runtime_ref"),
        "task_spec_ref": plan.get("task_spec_ref"),
        "rating_ref": plan.get("rating_ref"),
        "transcript_ref": plan.get("transcript_ref"),
        "qualification_artifacts": plan.get("qualification_artifacts"),
    }


def bind_existing_iteration_result(
    *, reference_result_path: Path, plan: dict[str, Any], repository_root: Path
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    reference_result_path = reference_result_path.resolve()
    try:
        relative_result = str(reference_result_path.relative_to(repository_root))
    except ValueError as error:
        raise QualificationGateError("existing iteration result escapes repository") from error
    result = load_object(reference_result_path)
    if result.get("schema_version") != "portable-instruction-semantic-qualification-result/v1":
        raise QualificationGateError("existing iteration result schema mismatch")
    result_plan_ref = result.get("plan") or {}
    result_plan_path = base.safe_repository_path(
        repository_root, result_plan_ref.get("path"), "existing iteration plan"
    )
    if sha256_file(result_plan_path) != result_plan_ref.get("sha256"):
        raise QualificationGateError("existing iteration plan hash mismatch")
    result_plan = load_object(result_plan_path)
    if result_plan.get("plan_id") != result_plan_ref.get("plan_id"):
        raise QualificationGateError("existing iteration plan identity mismatch")
    if result_plan.get("plan_sha256") != base.content_identity(result_plan, "plan_sha256"):
        raise QualificationGateError("existing iteration plan content hash mismatch")
    if _reference_compatibility_fields(result_plan) != _reference_compatibility_fields(plan):
        raise QualificationGateError("existing iteration result is incompatible with N=5 plan")
    repetition = result_plan.get("repetition_condition")
    if repetition != {
        "iterations": 1,
        "order": "case_id_ascending",
        "valid_low_quality_policy": "retain",
        "external_failure_policy": "exclude_without_case_change",
    }:
        raise QualificationGateError("existing iteration result is not an N=1 result")
    expected_slots = [
        {
            "slot_id": f"{slot['case_id']}-i001",
            "case_id": slot["case_id"],
            "case_revision": slot["case_revision"],
            "iteration": 1,
        }
        for slot in plan["slots"][::4]
    ]
    rows = result.get("cases")
    if not isinstance(rows, list) or [row.get("slot") for row in rows] != expected_slots:
        raise QualificationGateError("existing iteration result does not cover exact i001 slots")
    if any(
        row.get("status") != "valid"
        or row.get("quality_score") not in {1, 2, 3, 4}
        or not isinstance(row.get("all_agent_total_tokens"), int)
        or not isinstance(row.get("elapsed_seconds"), (int, float))
        for row in rows
    ):
        raise QualificationGateError("existing iteration result contains inadmissible rows")
    summary = result.get("summary") or {}
    if summary.get("valid_results") != 14 or summary.get("external_failures") != 0:
        raise QualificationGateError("existing iteration result summary is incomplete")
    return {
        "path": relative_result,
        "sha256": sha256_file(reference_result_path),
        "result_id": result.get("result_id"),
        "plan": {
            "path": str(result_plan_path.relative_to(repository_root)),
            "sha256": sha256_file(result_plan_path),
            "plan_id": result_plan["plan_id"],
        },
        "reused_slots": expected_slots,
        "reused_slot_count": len(expected_slots),
        "compatibility": "effective_atomic_run_conditions_match",
    }


def generate_plan(
    *, repository_root: Path, profile_path: Path, target_path: Path, bundle_path: Path
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    profile_path = profile_path.resolve()
    target_path = target_path.resolve()
    bundle_path = bundle_path.resolve()
    binding = base.validate_registered_profile(
        profile_path=profile_path,
        target_path=target_path,
        bundle_path=bundle_path,
        repository_root=repository_root,
    )
    profile = base.load_object(profile_path)
    target = base.load_object(target_path)
    paths = base.profile_paths(profile, repository_root)
    evaluation_set = base.load_object(paths["set"])
    set_ref = profile["evaluation_set_ref"]
    if evaluation_set.get("set_id") != set_ref.get("set_id"):
        raise base.QualificationGateError("evaluation set identity mismatch")
    if evaluation_set.get("set_revision") != set_ref.get("set_revision"):
        raise base.QualificationGateError("evaluation set revision mismatch")
    if base.sha256_file(paths["set"]) != set_ref.get("sha256"):
        raise base.QualificationGateError("evaluation set hash mismatch")
    registration = base.validate_target_registration(
        target_path,
        profile=profile,
        evaluation_set=evaluation_set,
        repository_root=repository_root,
    )
    registration["path"] = str(Path(registration["path"]).relative_to(repository_root))
    cases = evaluation_set.get("cases")
    if not isinstance(cases, list) or len(cases) != 14:
        raise base.QualificationGateError("qualification set must contain exactly fourteen cases")
    case_ids = [item.get("case_id") for item in cases if isinstance(item, dict)]
    if case_ids != sorted(case_ids) or len(set(case_ids)) != 14:
        raise base.QualificationGateError("qualification cases must be unique and sorted")
    repetition = profile.get("repetition_condition")
    if repetition != {
        "iterations": 5,
        "order": "case_id_then_iteration_ascending",
        "valid_low_quality_policy": "retain",
        "external_failure_policy": "exclude_without_case_change",
    }:
        raise base.QualificationGateError("N=5 repetition condition mismatch")
    execution = profile.get("execution") or {}
    dispatch_iterations = profile.get("dispatch_iterations")
    if dispatch_iterations != [2, 3, 4, 5]:
        raise base.QualificationGateError("N=5 plan must dispatch exactly missing iterations 2-5")
    slots = [
        {
            "slot_id": f"{item['case_id']}-i{iteration:03d}",
            "case_id": item["case_id"],
            "case_revision": item["case_revision"],
            "iteration": iteration,
        }
        for item in cases
        for iteration in dispatch_iterations
    ]
    plan_id, _ = base.dispatch_plan_identity(profile)
    plan = {
        "schema_version": base.PLAN_SCHEMA,
        "plan_id": plan_id,
        "target": {
            "path": str(target_path.relative_to(repository_root)),
            "sha256": base.sha256_file(target_path),
            "target_id": target["target_id"],
            "target_subject_ref": profile["target_subject_ref"],
        },
        "target_registration": registration,
        "profile": {
            "path": str(profile_path.relative_to(repository_root)),
            "sha256": base.sha256_file(profile_path),
            "profile_id": profile["profile_id"],
        },
        "prompt_set_identity": profile["prompt_set_identity"],
        "evaluation_set_ref": profile["evaluation_set_ref"],
        "runtime_ref": profile["runtime_ref"],
        "task_spec_ref": profile["task_spec_ref"],
        "rating_ref": profile["rating_ref"],
        "transcript_ref": profile["transcript_ref"],
        "repetition_condition": repetition,
        "execution": execution,
        "dispatch_iterations": dispatch_iterations,
        "slots": slots,
        "authorized_slot_count": len(slots),
        "issued_slot_count": 0,
        "binding_receipt": binding,
        "dispatch_state": "planned_missing_iterations_not_issued",
        "existing_iteration_result_required": True,
    }
    if "qualification_artifacts" in registration:
        plan["qualification_artifacts"] = registration["qualification_artifacts"]
    plan["plan_sha256"] = base.content_identity(plan, "plan_sha256")
    return plan


def validate_plan(plan: dict[str, Any], *, repository_root: Path, bundle_path: Path) -> dict[str, Any]:
    if plan.get("schema_version") != base.PLAN_SCHEMA:
        raise base.QualificationGateError("unsupported dispatch plan schema")
    if plan.get("plan_sha256") != base.content_identity(plan, "plan_sha256"):
        raise base.QualificationGateError("dispatch plan content hash mismatch")
    profile_path = base.safe_repository_path(repository_root, (plan.get("profile") or {}).get("path"), "profile")
    target_path = base.safe_repository_path(repository_root, (plan.get("target") or {}).get("path"), "target")
    expected = generate_plan(
        repository_root=repository_root,
        profile_path=profile_path,
        target_path=target_path,
        bundle_path=bundle_path,
    )
    if plan != expected:
        raise base.QualificationGateError("dispatch plan is stale or differs from bound artifacts")
    return expected


def build_preflight(
    *,
    plan_path: Path,
    reference_result_path: Path,
    repository_root: Path,
    bundle_path: Path,
    core_adapter_path: Path,
    runner_path: Path,
    codex_executable: Path,
    observed_version: str | None = None,
) -> dict[str, Any]:
    plan = load_object(plan_path)
    validate_plan(plan, repository_root=repository_root, bundle_path=bundle_path)
    receipt = base.build_preflight(
        plan_path=plan_path,
        repository_root=repository_root,
        bundle_path=bundle_path,
        core_adapter_path=core_adapter_path,
        runner_path=runner_path,
        codex_executable=codex_executable,
        observed_version=observed_version,
    )
    receipt["existing_iteration_result"] = bind_existing_iteration_result(
        reference_result_path=reference_result_path,
        plan=plan,
        repository_root=repository_root,
    )
    receipt["stop_conditions"].append("existing_iteration_result_drift_or_incompatibility")
    receipt["receipt_sha256"] = base.content_identity(receipt, "receipt_sha256")
    return receipt


def validate_preflight(
    *,
    receipt_path: Path,
    repository_root: Path,
    bundle_path: Path,
    observed_version: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt, plan = _base_validate_preflight(
        receipt_path=receipt_path,
        repository_root=repository_root,
        bundle_path=bundle_path,
        observed_version=observed_version,
    )
    reference = receipt.get("existing_iteration_result") or {}
    reference_path = base.safe_repository_path(
        repository_root, reference.get("path"), "existing iteration result"
    )
    expected = bind_existing_iteration_result(
        reference_result_path=reference_path,
        plan=plan,
        repository_root=repository_root,
    )
    if reference != expected:
        raise QualificationGateError("existing iteration result binding mismatch")
    return receipt, plan


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("create-plan")
    plan.add_argument("--repository-root", type=Path, required=True)
    plan.add_argument("--profile", type=Path, required=True)
    plan.add_argument("--target", type=Path, required=True)
    plan.add_argument("--bundle", type=Path, required=True)
    plan.add_argument("--output", type=Path, required=True)
    preflight = commands.add_parser("create-preflight")
    preflight.add_argument("--repository-root", type=Path, required=True)
    preflight.add_argument("--plan", type=Path, required=True)
    preflight.add_argument("--reference-result", type=Path, required=True)
    preflight.add_argument("--bundle", type=Path, required=True)
    preflight.add_argument("--core-adapter", type=Path, required=True)
    preflight.add_argument("--runner", type=Path, required=True)
    preflight.add_argument("--codex", type=Path, required=True)
    preflight.add_argument("--output", type=Path, required=True)
    verify = commands.add_parser("verify-preflight")
    verify.add_argument("--repository-root", type=Path, required=True)
    verify.add_argument("--receipt", type=Path, required=True)
    verify.add_argument("--bundle", type=Path, required=True)
    run = commands.add_parser("run-slot")
    run.add_argument("--repository-root", type=Path, required=True)
    run.add_argument("--receipt", type=Path, required=True)
    run.add_argument("--bundle", type=Path, required=True)
    run.add_argument("--slot-id", required=True)
    run.add_argument("--output-root", type=Path, required=True)
    run.add_argument("--session-root", type=Path, required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "create-plan":
            value = generate_plan(
                repository_root=args.repository_root,
                profile_path=args.profile,
                target_path=args.target,
                bundle_path=args.bundle,
            )
            write_once(args.output.resolve(), canonical_bytes(value))
        elif args.command == "create-preflight":
            value = build_preflight(
                plan_path=args.plan,
                reference_result_path=args.reference_result,
                repository_root=args.repository_root,
                bundle_path=args.bundle,
                core_adapter_path=args.core_adapter,
                runner_path=args.runner,
                codex_executable=args.codex,
            )
            write_once(args.output.resolve(), canonical_bytes(value))
        elif args.command == "verify-preflight":
            receipt, plan = validate_preflight(
                receipt_path=args.receipt,
                repository_root=args.repository_root,
                bundle_path=args.bundle,
            )
            value = {
                "schema_version": "portable-instruction-semantic-profile-preflight-verification/v2",
                "preflight_id": receipt["preflight_id"],
                "plan_id": plan["plan_id"],
                "authorized_slot_count": receipt["authorized_slot_count"],
                "reused_slot_count": receipt["existing_iteration_result"]["reused_slot_count"],
                "dispatch_allowed": True,
            }
        else:
            value = base.execute_slot(
                receipt_path=args.receipt,
                repository_root=args.repository_root,
                bundle_path=args.bundle,
                slot_id=args.slot_id,
                output_root=args.output_root,
                session_root=args.session_root,
            )
    except (
        base.BundleError,
        base.MaterializationError,
        OSError,
        QualificationGateError,
        base.SemanticCodexAdapterError,
    ) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))
    return 0


base.generate_plan = generate_plan
base.validate_plan = validate_plan
base.validate_preflight = validate_preflight


if __name__ == "__main__":
    raise SystemExit(main())
