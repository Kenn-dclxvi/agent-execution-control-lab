#!/usr/bin/env python3
"""VCC6 prompt-only single-arm plan, preflight, and execution entrypoint."""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any


def _load_base():
    path = Path(__file__).with_name("runner.py")
    spec = importlib.util.spec_from_file_location("codex_validation_carrier_prompt_only_base", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("base runner cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = _load_base()
adapter = base.adapter
RuntimeGateError = base.RuntimeGateError
PLAN_SCHEMA = base.PLAN_SCHEMA
PREFLIGHT_SCHEMA = base.PREFLIGHT_SCHEMA
GATE_SCHEMA = "codex-validation-carrier-prompt-only-execution-gate/v1"


def _load_gate(repository_root: Path, profile: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    path = base.safe_repository_file(
        repository_root,
        profile.get("execution_gate_ref") or {},
        "prompt-only execution gate",
    )
    value = adapter.load_object(path)
    if (
        value.get("schema_version") != GATE_SCHEMA
        or value.get("target_id") != "codex-validation-carrier-conformance"
        or value.get("dispatch_allowed") is not True
        or value.get("state") != "prompt_only_execution_gate_registered_not_executed"
    ):
        raise RuntimeGateError("prompt-only execution gate does not authorize dispatch")
    return path, value


def validate_profile(*, repository_root: Path, profile_path: Path, target_path: Path) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    profile = adapter.load_object(profile_path.resolve())
    target = adapter.load_object(target_path.resolve())
    if profile.get("schema_version") != "codex-validation-carrier-profile/v1":
        raise RuntimeGateError("unsupported prompt-only Profile schema")
    if profile.get("lifecycle_state") != "registered_not_qualified":
        raise RuntimeGateError("prompt-only Profile lifecycle state is invalid")
    if profile.get("target_id") != target.get("target_id") or target.get("target_id") != "codex-validation-carrier-conformance":
        raise RuntimeGateError("prompt-only Profile target identity mismatch")
    if profile.get("target_repository_ref") != target.get("target_repository"):
        raise RuntimeGateError("prompt-only Profile target repository ref mismatch")
    if profile.get("dispatch_series_id") != f"{profile.get('profile_id')}-dispatch":
        raise RuntimeGateError("prompt-only dispatch series must derive from Profile identity")

    references = {
        "evaluation_set": profile.get("evaluation_set_ref"),
        "task_spec": profile.get("task_spec_ref"),
        "rating": profile.get("rating_ref"),
        "token_accounting": profile.get("token_accounting_ref"),
        "capability_catalog": profile.get("capability_catalog_ref"),
        "schema_transport": profile.get("schema_transport_ref"),
    }
    paths = {name: base.safe_repository_file(repository_root, reference or {}, name) for name, reference in references.items()}
    evaluation_set = adapter.load_object(paths["evaluation_set"])
    if evaluation_set.get("set_id") != "codex-validation-carrier-heldout-r1":
        raise RuntimeGateError("VCC6 evaluation set mismatch")
    if [item.get("case_id") for item in evaluation_set.get("cases", [])] != [f"VCC-H0{index}" for index in range(1, 7)]:
        raise RuntimeGateError("VCC6 case membership mismatch")

    gate_path, gate = _load_gate(repository_root, profile)
    contract = gate.get("profile_contract") or {}
    fixed = gate.get("fixed_conditions") or {}
    target_fixed = fixed.get("target") or {}
    if (
        target_fixed.get("path") != str(target_path.resolve().relative_to(repository_root))
        or target_fixed.get("sha256") != base.sha256_file(target_path)
    ):
        raise RuntimeGateError("target differs from prompt-only execution gate")
    for name, reference in references.items():
        expected_reference = fixed.get(name) or {}
        if any(reference.get(key) != expected_reference.get(key) for key in ("path", "sha256")):
            raise RuntimeGateError(f"{name} differs from prompt-only execution gate")
    execution_paths = {
        "adapter": Path(adapter.__file__).resolve(),
        "base_runner": Path(base.__file__).resolve(),
        "prompt_only_runner": Path(__file__).resolve(),
    }
    for name, path in execution_paths.items():
        reference = gate.get("execution_code", {}).get(name) or {}
        if (
            reference.get("path") != str(path.relative_to(repository_root))
            or reference.get("sha256") != base.sha256_file(path)
        ):
            raise RuntimeGateError(f"{name} differs from prompt-only execution gate")
    if profile.get("runtime_ref") != gate.get("runtime_ref") or profile.get("runtime_ref") != base.RUNTIME_EXPECTED:
        raise RuntimeGateError("prompt-only runtime differs from execution gate")
    for field in ("repetition_condition", "execution", "scope"):
        if profile.get(field) != contract.get(field):
            raise RuntimeGateError(f"prompt-only {field} differs from execution gate")
    iterations = profile.get("repetition_condition", {}).get("iterations")
    if not isinstance(iterations, int) or iterations < 1:
        raise RuntimeGateError("prompt-only iteration count must be positive")

    capability = adapter.load_object(paths["capability_catalog"])
    cases_path = repository_root / "evaluations/targets/codex-validation-carrier-conformance/cases/heldout-r1/input-cases.json"
    case_contract = adapter.load_object(cases_path)["runtime_contract"]
    if capability.get("carrier_capabilities") != case_contract["carrier_capabilities"]:
        raise RuntimeGateError("capability catalog differs from VCC6 runtime contract")
    capability_preflight = adapter.capability_preflight(case_contract)
    if capability_preflight["dispatch_state"] != "allowed":
        raise RuntimeGateError(f"capability preflight denied: {capability_preflight['reason']}")

    prompt = profile.get("prompt_set_identity") or {}
    allowed = gate.get("allowed_prompt_set_identities")
    if not isinstance(allowed, list) or prompt not in allowed:
        raise RuntimeGateError("prompt identity is not registered for the shared-runner series")
    bundle_path = (repository_root / prompt.get("path", "")).resolve()
    try:
        manifest = base.verify_bundle(bundle_path)
    except Exception as error:
        raise RuntimeGateError("prompt bundle is invalid") from error
    if manifest.get("prompt_identity") != prompt.get("name") or manifest.get("bundle_sha256") != prompt.get("sha256"):
        raise RuntimeGateError("prompt bundle identity mismatch")
    return {
        "profile": profile,
        "target": target,
        "set": evaluation_set,
        "paths": paths,
        "bundle_path": bundle_path,
        "capability_preflight": capability_preflight,
        "gate_path": gate_path,
        "gate": gate,
    }


def generate_plan(*, repository_root: Path, profile_path: Path, target_path: Path) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    binding = validate_profile(
        repository_root=repository_root,
        profile_path=profile_path,
        target_path=target_path,
    )
    profile, target, evaluation_set = binding["profile"], binding["target"], binding["set"]
    iterations = profile["repetition_condition"]["iterations"]
    slots = [
        {
            "slot_id": f"{item['case_id']}-i{iteration:03d}",
            "case_id": item["case_id"],
            "case_revision": item["case_revision"],
            "iteration": iteration,
        }
        for item in evaluation_set["cases"]
        for iteration in range(1, iterations + 1)
    ]
    plan = {
        "schema_version": PLAN_SCHEMA,
        "plan_id": f"{profile['dispatch_series_id']}-plan-r1",
        "target": {
            "path": str(target_path.resolve().relative_to(repository_root)),
            "sha256": base.sha256_file(target_path),
            "target_id": target["target_id"],
        },
        "profile": {
            "path": str(profile_path.resolve().relative_to(repository_root)),
            "sha256": base.sha256_file(profile_path),
            "profile_id": profile["profile_id"],
        },
        "prompt_set_identity": profile["prompt_set_identity"],
        "evaluation_set_ref": profile["evaluation_set_ref"],
        "runtime_ref": profile["runtime_ref"],
        "task_spec_ref": profile["task_spec_ref"],
        "rating_ref": profile["rating_ref"],
        "token_accounting_ref": profile["token_accounting_ref"],
        "capability_catalog_ref": profile["capability_catalog_ref"],
        "schema_transport_ref": profile["schema_transport_ref"],
        "execution_gate_ref": profile["execution_gate_ref"],
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
    if (
        plan.get("schema_version") != PLAN_SCHEMA
        or plan.get("plan_sha256") != base.content_identity(plan, "plan_sha256")
    ):
        raise RuntimeGateError("prompt-only dispatch plan identity mismatch")
    profile_path = base.safe_repository_file(repository_root, plan.get("profile") or {}, "profile")
    target_path = base.safe_repository_file(repository_root, plan.get("target") or {}, "target")
    expected = generate_plan(
        repository_root=repository_root,
        profile_path=profile_path,
        target_path=target_path,
    )
    if plan != expected:
        raise RuntimeGateError("prompt-only dispatch plan is stale")
    return plan


def build_preflight(
    *,
    repository_root: Path,
    plan_path: Path,
    codex_executable: Path,
    observed_version: str | None = None,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    plan = validate_plan(repository_root=repository_root, plan_path=plan_path)
    executable = codex_executable.resolve()
    if not executable.is_file():
        raise RuntimeGateError("Codex executable is unavailable")
    observed = observed_version or base.observe_codex_version(executable)
    if observed != f"codex-cli {plan['runtime_ref']['version']}":
        raise RuntimeGateError("Codex version differs from prompt-only Profile")
    receipt = {
        "schema_version": PREFLIGHT_SCHEMA,
        "preflight_id": f"{plan['plan_id']}-preflight-r1",
        "plan": {
            "path": str(plan_path.resolve().relative_to(repository_root)),
            "sha256": base.sha256_file(plan_path),
            "plan_id": plan["plan_id"],
            "plan_sha256": plan["plan_sha256"],
        },
        "profile": plan["profile"],
        "target": plan["target"],
        "execution_code": {
            "adapter": {
                "path": str(Path(adapter.__file__).resolve().relative_to(repository_root)),
                "sha256": base.sha256_file(Path(adapter.__file__)),
            },
            "base_runner": {
                "path": str(Path(base.__file__).resolve().relative_to(repository_root)),
                "sha256": base.sha256_file(Path(base.__file__)),
            },
            "prompt_only_runner": {
                "path": str(Path(__file__).resolve().relative_to(repository_root)),
                "sha256": base.sha256_file(Path(__file__)),
            },
        },
        "runtime": {
            "executable": str(executable),
            "observed_version": observed,
            "runtime_ref": plan["runtime_ref"],
        },
        "prompt_difference_only": True,
        "saved_result_reuse": False,
        "authorized_slots": plan["slots"],
        "authorized_slot_count": len(plan["slots"]),
        "issued_slot_count": 0,
        "dispatch_allowed": True,
        "profile_class": plan["scope"]["profile_class"],
        "stop_conditions": [
            "plan_hash_mismatch",
            "profile_or_target_drift",
            "prompt_foundation_drift",
            "non_prompt_compatibility_mismatch",
            "execution_code_hash_mismatch",
            "runtime_version_drift",
            "capability_preflight_denied",
            "slot_not_authorized",
            "slot_output_exists",
        ],
    }
    receipt["receipt_sha256"] = base.content_identity(receipt, "receipt_sha256")
    return receipt


def validate_preflight(
    *,
    repository_root: Path,
    receipt_path: Path,
    observed_version: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    repository_root = repository_root.resolve()
    receipt = adapter.load_object(receipt_path.resolve())
    if (
        receipt.get("schema_version") != PREFLIGHT_SCHEMA
        or receipt.get("receipt_sha256") != base.content_identity(receipt, "receipt_sha256")
    ):
        raise RuntimeGateError("prompt-only preflight identity mismatch")
    plan_path = base.safe_repository_file(repository_root, receipt.get("plan") or {}, "plan")
    plan = validate_plan(repository_root=repository_root, plan_path=plan_path)
    for reference in receipt.get("execution_code", {}).values():
        base.safe_repository_file(repository_root, reference, "execution code")
    executable = Path(receipt.get("runtime", {}).get("executable", "")).resolve()
    observed = observed_version or base.observe_codex_version(executable)
    if (
        observed != receipt.get("runtime", {}).get("observed_version")
        or observed != f"codex-cli {plan['runtime_ref']['version']}"
    ):
        raise RuntimeGateError("prompt-only preflight runtime drift")
    if (
        receipt.get("prompt_difference_only") is not True
        or receipt.get("saved_result_reuse") is not False
        or receipt.get("authorized_slots") != plan["slots"]
        or receipt.get("dispatch_allowed") is not True
        or receipt.get("issued_slot_count") != 0
    ):
        raise RuntimeGateError("prompt-only preflight does not authorize the exact fresh slots")
    expected = build_preflight(
        repository_root=repository_root,
        plan_path=plan_path,
        codex_executable=executable,
        observed_version=observed,
    )
    if receipt != expected:
        raise RuntimeGateError("prompt-only preflight is stale")
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
        base.write_once(
            args.output,
            base.canonical_bytes(
                generate_plan(
                    repository_root=args.repository_root,
                    profile_path=args.profile,
                    target_path=args.target,
                )
            ),
        )
    elif args.command == "preflight":
        base.write_once(
            args.output,
            base.canonical_bytes(
                build_preflight(
                    repository_root=args.repository_root,
                    plan_path=args.plan,
                    codex_executable=args.codex,
                )
            ),
        )
    else:
        execute_slot(
            repository_root=args.repository_root,
            receipt_path=args.preflight,
            slot_id=args.slot_id,
            output_root=args.output_root,
            session_root=args.session_root,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
