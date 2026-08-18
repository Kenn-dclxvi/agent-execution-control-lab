#!/usr/bin/env python3
"""P002 candidate-only plan, preflight, and execution entrypoint."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any


def _load_base():
    path = Path(__file__).with_name("runner.py")
    spec = importlib.util.spec_from_file_location("codex_validation_carrier_qualification_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("qualification runner cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = _load_base()
adapter = base.adapter
RuntimeGateError = base.RuntimeGateError
PLAN_SCHEMA = base.PLAN_SCHEMA
PREFLIGHT_SCHEMA = base.PREFLIGHT_SCHEMA
PLAN_ID = "codex-validation-carrier-p002-heldout-r1-n1-dispatch-r1"
PREFLIGHT_ID = "codex-validation-carrier-p002-heldout-r1-n1-preflight-r1"
PROFILE_ID = "codex-validation-carrier-p002-heldout-r1-codex-cli0146-sol-medium-n1-r1"
PROMPT_IDENTITY = "p002-portable-full-agent-codex-validation-carrier-r1"
RUNTIME_REGISTRATION_ID = "codex-validation-carrier-heldout-r1-runtime-registration-r1"
CANDIDATE_BINDING_ID = "p002-portable-full-agent-codex-validation-carrier-composition-binding-r1"
_validate_qualification_profile = base.validate_profile


def validate_profile(*, repository_root: Path, profile_path: Path, target_path: Path) -> dict[str, Any]:
    binding = _validate_qualification_profile(
        repository_root=repository_root,
        profile_path=profile_path,
        target_path=target_path,
    )
    profile = binding["profile"]
    if profile.get("profile_id") != PROFILE_ID:
        raise RuntimeGateError("P002 Profile identity mismatch")
    if profile.get("dispatch_series_id") != "codex-validation-carrier-p002-heldout-r1-n1":
        raise RuntimeGateError("P002 dispatch series mismatch")
    if profile.get("prompt_set_identity", {}).get("name") != PROMPT_IDENTITY:
        raise RuntimeGateError("P002 prompt identity mismatch")
    expected_scope = {
        "profile_class": "candidate_only_p002_gate",
        "candidate_only": True,
        "formal_comparison": False,
        "paired_comparison": "not_authorized",
        "standard14_projection": "not_authorized",
        "adoption": "not_decided",
        "release": "not_decided",
        "runtime_projection": "not_authorized",
    }
    if profile.get("scope") != expected_scope:
        raise RuntimeGateError("P002 Profile scope mismatch")
    runtime_registration_path = base.safe_repository_file(
        repository_root, profile.get("runtime_registration_ref") or {}, "runtime registration"
    )
    runtime_registration = adapter.load_object(runtime_registration_path)
    if (
        runtime_registration.get("registration_id") != RUNTIME_REGISTRATION_ID
        or runtime_registration.get("allowed_next_profile_class") != "candidate_only_p002_gate"
        or runtime_registration.get("state") != "qualified_for_candidate_only_profile_registration"
    ):
        raise RuntimeGateError("runtime registration does not authorize P002 candidate-only Profile")
    candidate_binding_path = base.safe_repository_file(
        repository_root, profile.get("candidate_binding_ref") or {}, "candidate binding"
    )
    candidate_binding = adapter.load_object(candidate_binding_path)
    if (
        candidate_binding.get("binding_id") != CANDIDATE_BINDING_ID
        or candidate_binding.get("candidate_bundle", {}).get("prompt_identity") != PROMPT_IDENTITY
        or candidate_binding.get("state") != "candidate_bundle_bound_not_evaluated"
        or candidate_binding.get("verification", {}).get("bundle_binding") != "verified"
    ):
        raise RuntimeGateError("P002 candidate binding mismatch")
    binding["runtime_registration_path"] = runtime_registration_path
    binding["candidate_binding_path"] = candidate_binding_path
    return binding


def generate_plan(*, repository_root: Path, profile_path: Path, target_path: Path) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    binding = validate_profile(repository_root=repository_root, profile_path=profile_path, target_path=target_path)
    profile, target, evaluation_set = binding["profile"], binding["target"], binding["set"]
    slots = [
        {"slot_id": f"{item['case_id']}-i001", "case_id": item["case_id"], "case_revision": item["case_revision"], "iteration": 1}
        for item in evaluation_set["cases"]
    ]
    plan = {
        "schema_version": PLAN_SCHEMA,
        "plan_id": PLAN_ID,
        "target": {"path": str(target_path.resolve().relative_to(repository_root)), "sha256": base.sha256_file(target_path), "target_id": target["target_id"]},
        "profile": {"path": str(profile_path.resolve().relative_to(repository_root)), "sha256": base.sha256_file(profile_path), "profile_id": profile["profile_id"]},
        "prompt_set_identity": profile["prompt_set_identity"],
        "evaluation_set_ref": profile["evaluation_set_ref"],
        "runtime_ref": profile["runtime_ref"],
        "task_spec_ref": profile["task_spec_ref"],
        "rating_ref": profile["rating_ref"],
        "token_accounting_ref": profile["token_accounting_ref"],
        "capability_catalog_ref": profile["capability_catalog_ref"],
        "schema_transport_ref": profile["schema_transport_ref"],
        "runtime_registration_ref": profile["runtime_registration_ref"],
        "candidate_binding_ref": profile["candidate_binding_ref"],
        "repetition_condition": profile["repetition_condition"],
        "execution": profile["execution"],
        "slots": slots,
        "authorized_slot_count": len(slots),
        "issued_slot_count": 0,
        "dispatch_state": "planned_not_issued",
        "scope": profile["scope"],
    }
    plan["plan_sha256"] = base.content_identity(plan, "plan_sha256")
    return plan


def validate_plan(*, repository_root: Path, plan_path: Path) -> dict[str, Any]:
    plan = adapter.load_object(plan_path.resolve())
    if plan.get("schema_version") != PLAN_SCHEMA or plan.get("plan_sha256") != base.content_identity(plan, "plan_sha256"):
        raise RuntimeGateError("dispatch plan identity mismatch")
    profile_path = base.safe_repository_file(repository_root, plan.get("profile") or {}, "profile")
    target_path = base.safe_repository_file(repository_root, plan.get("target") or {}, "target")
    expected = generate_plan(repository_root=repository_root, profile_path=profile_path, target_path=target_path)
    if plan != expected:
        raise RuntimeGateError("dispatch plan is stale")
    return plan


def build_preflight(*, repository_root: Path, plan_path: Path, codex_executable: Path, observed_version: str | None = None) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    plan = validate_plan(repository_root=repository_root, plan_path=plan_path)
    executable = codex_executable.resolve()
    if not executable.is_file():
        raise RuntimeGateError("Codex executable is unavailable")
    observed = observed_version or base.observe_codex_version(executable)
    if observed != f"codex-cli {plan['runtime_ref']['version']}":
        raise RuntimeGateError("Codex version differs from Profile")
    execution_code = {
        "adapter": {"path": str(Path(adapter.__file__).resolve().relative_to(repository_root)), "sha256": base.sha256_file(Path(adapter.__file__))},
        "runner": {"path": str(Path(__file__).resolve().relative_to(repository_root)), "sha256": base.sha256_file(Path(__file__))},
    }
    receipt = {
        "schema_version": PREFLIGHT_SCHEMA,
        "preflight_id": PREFLIGHT_ID,
        "plan": {"path": str(plan_path.resolve().relative_to(repository_root)), "sha256": base.sha256_file(plan_path), "plan_id": plan["plan_id"], "plan_sha256": plan["plan_sha256"]},
        "profile": plan["profile"],
        "target": plan["target"],
        "execution_code": execution_code,
        "runtime": {"executable": str(executable), "observed_version": observed, "runtime_ref": plan["runtime_ref"]},
        "authorized_slots": plan["slots"],
        "authorized_slot_count": len(plan["slots"]),
        "issued_slot_count": 0,
        "dispatch_allowed": True,
        "profile_class": "candidate_only_p002_gate",
        "stop_conditions": ["plan_hash_mismatch", "profile_or_target_drift", "execution_code_hash_mismatch", "runtime_version_drift", "capability_preflight_denied", "candidate_binding_drift", "slot_not_authorized", "slot_output_exists"],
    }
    receipt["receipt_sha256"] = base.content_identity(receipt, "receipt_sha256")
    return receipt


def validate_preflight(*, repository_root: Path, receipt_path: Path, observed_version: str | None = None):
    repository_root = repository_root.resolve()
    receipt = adapter.load_object(receipt_path.resolve())
    if receipt.get("schema_version") != PREFLIGHT_SCHEMA or receipt.get("receipt_sha256") != base.content_identity(receipt, "receipt_sha256"):
        raise RuntimeGateError("preflight identity mismatch")
    plan_path = base.safe_repository_file(repository_root, receipt.get("plan") or {}, "plan")
    plan = validate_plan(repository_root=repository_root, plan_path=plan_path)
    for reference in receipt.get("execution_code", {}).values():
        base.safe_repository_file(repository_root, reference, "execution code")
    executable = Path(receipt.get("runtime", {}).get("executable", "")).resolve()
    observed = observed_version or base.observe_codex_version(executable)
    if observed != receipt.get("runtime", {}).get("observed_version") or observed != f"codex-cli {plan['runtime_ref']['version']}":
        raise RuntimeGateError("preflight runtime version drift")
    if receipt.get("authorized_slots") != plan["slots"] or receipt.get("dispatch_allowed") is not True or receipt.get("issued_slot_count") != 0:
        raise RuntimeGateError("preflight does not authorize the exact fresh slot set")
    expected = build_preflight(repository_root=repository_root, plan_path=plan_path, codex_executable=executable, observed_version=observed)
    if receipt != expected:
        raise RuntimeGateError("preflight is stale")
    return receipt, plan


def execute_slot(**kwargs):
    base.validate_profile = validate_profile
    base.validate_preflight = validate_preflight
    return base.execute_slot(**kwargs)


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("--repository-root", type=Path, required=True)
    plan_parser.add_argument("--profile", type=Path, required=True)
    plan_parser.add_argument("--target", type=Path, required=True)
    plan_parser.add_argument("--output", type=Path, required=True)
    preflight_parser = subparsers.add_parser("preflight")
    preflight_parser.add_argument("--repository-root", type=Path, required=True)
    preflight_parser.add_argument("--plan", type=Path, required=True)
    preflight_parser.add_argument("--codex", type=Path, required=True)
    preflight_parser.add_argument("--output", type=Path, required=True)
    execute_parser = subparsers.add_parser("execute")
    execute_parser.add_argument("--repository-root", type=Path, required=True)
    execute_parser.add_argument("--preflight", type=Path, required=True)
    execute_parser.add_argument("--slot-id", required=True)
    execute_parser.add_argument("--output-root", type=Path, required=True)
    execute_parser.add_argument("--session-root", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "plan":
        base.write_once(args.output, base.canonical_bytes(generate_plan(repository_root=args.repository_root, profile_path=args.profile, target_path=args.target)))
    elif args.command == "preflight":
        base.write_once(args.output, base.canonical_bytes(build_preflight(repository_root=args.repository_root, plan_path=args.plan, codex_executable=args.codex)))
    else:
        execute_slot(repository_root=args.repository_root, receipt_path=args.preflight, slot_id=args.slot_id, output_root=args.output_root, session_root=args.session_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
