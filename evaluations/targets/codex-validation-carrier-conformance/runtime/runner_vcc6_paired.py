#!/usr/bin/env python3
"""VCC6 P001/P002 paired N=5 plan, preflight, and execution entrypoint."""

from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
import subprocess
import time
from typing import Any


def _load_base():
    path = Path(__file__).with_name("runner.py")
    spec = importlib.util.spec_from_file_location("codex_validation_carrier_base_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("base runner cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


base = _load_base()
adapter = base.adapter
RuntimeGateError = base.RuntimeGateError
PLAN_SCHEMA = "codex-validation-carrier-paired-plan/v1"
PREFLIGHT_SCHEMA = "codex-validation-carrier-paired-preflight/v1"
EXECUTION_SCHEMA = "codex-validation-carrier-paired-execution-observation/v1"
FAILURE_SCHEMA = "codex-validation-carrier-paired-external-failure/v1"
PROFILE_ID = "vcc6-p001-p002-codex-cli0146-sol-medium-n5-r1"
PLAN_ID = "vcc6-p001-p002-n5-dispatch-r1"
PREFLIGHT_ID = "vcc6-p001-p002-n5-preflight-r1"
ARM_IDENTITIES = {
    "P001": ("portable-semantic-c147-portable-full-agent-r1", "6152e6ca546ef778eb59ad6ff0fe6883748ece469309ff627945777978e4faf0"),
    "P002": ("p002-portable-full-agent-codex-validation-carrier-r1", "2fa8a0d70c8f72788f58906bd4bde1c627ba00260c1db12f97cc6171b0dce66d"),
}


def _load_reference(repository_root: Path, reference: dict[str, Any], label: str):
    path = base.safe_repository_file(repository_root, reference, label)
    return path, adapter.load_object(path)


def validate_profile(*, repository_root: Path, profile_path: Path, target_path: Path) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    profile = adapter.load_object(profile_path.resolve())
    target = adapter.load_object(target_path.resolve())
    if profile.get("schema_version") != "codex-validation-carrier-paired-profile/v1":
        raise RuntimeGateError("unsupported paired Profile schema")
    if profile.get("profile_id") != PROFILE_ID or profile.get("dispatch_series_id") != "vcc6-p001-p002-n5-r1":
        raise RuntimeGateError("paired Profile identity mismatch")
    if profile.get("lifecycle_state") != "registered_not_compared":
        raise RuntimeGateError("paired Profile lifecycle state mismatch")
    if profile.get("target_id") != target.get("target_id") or target.get("target_id") != "codex-validation-carrier-conformance":
        raise RuntimeGateError("paired Profile target mismatch")
    if profile.get("target_repository_ref") != target.get("target_repository"):
        raise RuntimeGateError("paired Profile repository ref mismatch")

    common_refs = {
        "evaluation_set": profile.get("evaluation_set_ref"),
        "task_spec": profile.get("task_spec_ref"),
        "rating": profile.get("rating_ref"),
        "token_accounting": profile.get("token_accounting_ref"),
        "capability_catalog": profile.get("capability_catalog_ref"),
        "schema_transport": profile.get("schema_transport_ref"),
        "gate_registration": profile.get("gate_registration_ref"),
    }
    paths: dict[str, Path] = {}
    objects: dict[str, dict[str, Any]] = {}
    for name, reference in common_refs.items():
        paths[name] = base.safe_repository_file(repository_root, reference or {}, name)
        if name in {"evaluation_set", "capability_catalog", "gate_registration"}:
            objects[name] = adapter.load_object(paths[name])
    evaluation_set = objects["evaluation_set"]
    if evaluation_set.get("set_id") != "codex-validation-carrier-heldout-r1":
        raise RuntimeGateError("VCC6 evaluation set mismatch")
    if [item.get("case_id") for item in evaluation_set.get("cases", [])] != [f"VCC-H0{index}" for index in range(1, 7)]:
        raise RuntimeGateError("VCC6 case membership mismatch")
    if profile.get("runtime_ref") != base.RUNTIME_EXPECTED:
        raise RuntimeGateError("paired runtime differs from qualification contract")
    if profile.get("repetition_condition") != {
        "iterations_per_case_per_arm": 5,
        "order": "global_queue_arm_case_iteration",
        "valid_low_quality_policy": "retain",
        "external_failure_policy": "exclude_without_case_change",
    }:
        raise RuntimeGateError("paired repetition contract mismatch")
    if profile.get("execution") != {
        "max_workers": 24,
        "schedule_policy": "shared_global_queue",
        "max_attempts_per_slot": 1,
        "dispatch_gate": "paired_comparison_preflight_required",
    }:
        raise RuntimeGateError("paired execution contract mismatch")
    if profile.get("comparison_contract") != {
        "required_logical_slots": 60,
        "reused_slots": 6,
        "new_dispatch_slots": 54,
        "primary_cost_aggregate": "sum_over_30_valid_runs_per_arm",
        "quality_gate": "P002_all_30_score4",
        "cost_improvement_gate": "P002_tokens_sum_lt_P001_tokens_sum_and_P002_elapsed_sum_lt_P001_elapsed_sum",
        "per_case_reporting": True,
        "standard14_next_gate": "quality_gate_and_cost_improvement_gate",
    }:
        raise RuntimeGateError("paired comparison contract mismatch")
    if profile.get("scope") != {
        "profile_class": "p001_p002_paired_targeted_n5",
        "formal_comparison": True,
        "standard14_projection": "not_authorized_until_result_gate",
        "n20_extension": "not_authorized",
        "adoption": "not_decided",
        "release": "not_decided",
        "runtime_projection": "not_authorized",
    }:
        raise RuntimeGateError("paired scope mismatch")
    gate = objects["gate_registration"]
    if (
        gate.get("registration_id") != "codex-validation-carrier-p002-candidate-gate-registration-r1"
        or gate.get("allowed_next_profile_class") != "p001_p002_paired_targeted_n5"
        or gate.get("state") != "candidate_gate_passed_paired_targeted_n5_allowed"
    ):
        raise RuntimeGateError("candidate gate does not authorize paired N=5")

    capability = objects["capability_catalog"]
    cases = adapter.load_object(repository_root / "evaluations/targets/codex-validation-carrier-conformance/cases/heldout-r1/input-cases.json")
    if capability.get("carrier_capabilities") != cases["runtime_contract"]["carrier_capabilities"]:
        raise RuntimeGateError("capability catalog differs from VCC6 runtime contract")
    capability_preflight = adapter.capability_preflight(cases["runtime_contract"])
    if capability_preflight["dispatch_state"] != "allowed":
        raise RuntimeGateError("VCC6 capability preflight denied")

    arms = profile.get("arms")
    if not isinstance(arms, dict) or set(arms) != set(ARM_IDENTITIES):
        raise RuntimeGateError("paired arms mismatch")
    bundles: dict[str, Path] = {}
    manifests: dict[str, dict[str, Any]] = {}
    for arm, (identity, bundle_sha) in ARM_IDENTITIES.items():
        arm_value = arms[arm]
        prompt = arm_value.get("prompt_set_identity") or {}
        bundle_path = (repository_root / prompt.get("path", "")).resolve()
        try:
            manifest = base.verify_bundle(bundle_path)
        except Exception as error:
            raise RuntimeGateError(f"{arm} prompt bundle is invalid") from error
        if prompt.get("name") != identity or prompt.get("sha256") != bundle_sha:
            raise RuntimeGateError(f"{arm} prompt reference mismatch")
        if manifest.get("prompt_identity") != identity or manifest.get("bundle_sha256") != bundle_sha:
            raise RuntimeGateError(f"{arm} prompt manifest mismatch")
        if arm_value.get("requested_iterations") != [1, 2, 3, 4, 5]:
            raise RuntimeGateError(f"{arm} iteration set mismatch")
        bundles[arm] = bundle_path
        manifests[arm] = manifest
    if arms["P001"].get("reuse") != []:
        raise RuntimeGateError("P001 must not reuse a missing VCC6 result")
    p002_reuse = arms["P002"].get("reuse")
    if not isinstance(p002_reuse, list) or len(p002_reuse) != 1 or p002_reuse[0].get("iteration") != 1:
        raise RuntimeGateError("P002 reuse declaration mismatch")
    reuse_path, reuse_result = _load_reference(repository_root, p002_reuse[0], "P002 reuse result")
    if (
        reuse_result.get("result_id") != p002_reuse[0].get("result_id")
        or reuse_result.get("result_sha256") != p002_reuse[0].get("result_sha256")
        or reuse_result.get("prompt_set_identity") != arms["P002"]["prompt_set_identity"]
        or reuse_result.get("runtime_ref") != profile.get("runtime_ref")
        or reuse_result.get("rating_ref") != profile.get("rating_ref")
        or reuse_result.get("token_accounting_ref") != profile.get("token_accounting_ref")
    ):
        raise RuntimeGateError("P002 reuse result compatibility mismatch")
    result_set_ref = reuse_result.get("evaluation_set_ref") or {}
    profile_set_ref = profile.get("evaluation_set_ref") or {}
    if any(result_set_ref.get(key) != profile_set_ref.get(key) for key in ("set_id", "set_revision", "path", "sha256")):
        raise RuntimeGateError("P002 reuse evaluation set mismatch")
    reuse_slots = [row.get("slot") for row in reuse_result.get("cases", [])]
    expected_reuse = [
        {"slot_id": f"VCC-H0{index}-i001", "case_id": f"VCC-H0{index}", "case_revision": "r1", "iteration": 1}
        for index in range(1, 7)
    ]
    if reuse_slots != expected_reuse or any(row.get("status") != "valid" for row in reuse_result.get("cases", [])):
        raise RuntimeGateError("P002 reuse slots are incomplete or invalid")
    return {
        "profile": profile,
        "target": target,
        "set": evaluation_set,
        "paths": paths,
        "bundles": bundles,
        "manifests": manifests,
        "reuse_path": reuse_path,
        "reuse_result": reuse_result,
        "capability_preflight": capability_preflight,
    }


def generate_plan(*, repository_root: Path, profile_path: Path, target_path: Path) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    binding = validate_profile(repository_root=repository_root, profile_path=profile_path, target_path=target_path)
    profile, target, evaluation_set = binding["profile"], binding["target"], binding["set"]
    logical_slots = []
    reused_slots = []
    dispatch_slots = []
    for arm in ("P001", "P002"):
        for case in evaluation_set["cases"]:
            for iteration in range(1, 6):
                slot = {
                    "slot_id": f"{arm}-{case['case_id']}-i{iteration:03d}",
                    "arm": arm,
                    "case_id": case["case_id"],
                    "case_revision": case["case_revision"],
                    "iteration": iteration,
                }
                logical_slots.append(slot)
                (reused_slots if arm == "P002" and iteration == 1 else dispatch_slots).append(slot)
    plan = {
        "schema_version": PLAN_SCHEMA,
        "plan_id": PLAN_ID,
        "target": {"path": str(target_path.resolve().relative_to(repository_root)), "sha256": base.sha256_file(target_path), "target_id": target["target_id"]},
        "profile": {"path": str(profile_path.resolve().relative_to(repository_root)), "sha256": base.sha256_file(profile_path), "profile_id": profile["profile_id"]},
        "arms": profile["arms"],
        "evaluation_set_ref": profile["evaluation_set_ref"],
        "runtime_ref": profile["runtime_ref"],
        "task_spec_ref": profile["task_spec_ref"],
        "rating_ref": profile["rating_ref"],
        "token_accounting_ref": profile["token_accounting_ref"],
        "capability_catalog_ref": profile["capability_catalog_ref"],
        "schema_transport_ref": profile["schema_transport_ref"],
        "gate_registration_ref": profile["gate_registration_ref"],
        "repetition_condition": profile["repetition_condition"],
        "execution": profile["execution"],
        "comparison_contract": profile["comparison_contract"],
        "scope": profile["scope"],
        "logical_slots": logical_slots,
        "reused_slots": reused_slots,
        "dispatch_slots": dispatch_slots,
        "logical_slot_count": len(logical_slots),
        "reused_slot_count": len(reused_slots),
        "authorized_dispatch_slot_count": len(dispatch_slots),
        "issued_slot_count": 0,
        "dispatch_state": "planned_not_issued",
    }
    plan["plan_sha256"] = base.content_identity(plan, "plan_sha256")
    return plan


def validate_plan(*, repository_root: Path, plan_path: Path) -> dict[str, Any]:
    plan = adapter.load_object(plan_path.resolve())
    if plan.get("schema_version") != PLAN_SCHEMA or plan.get("plan_sha256") != base.content_identity(plan, "plan_sha256"):
        raise RuntimeGateError("paired dispatch plan identity mismatch")
    profile_path = base.safe_repository_file(repository_root, plan.get("profile") or {}, "paired profile")
    target_path = base.safe_repository_file(repository_root, plan.get("target") or {}, "target")
    expected = generate_plan(repository_root=repository_root, profile_path=profile_path, target_path=target_path)
    if plan != expected:
        raise RuntimeGateError("paired dispatch plan is stale")
    return plan


def build_preflight(*, repository_root: Path, plan_path: Path, codex_executable: Path, observed_version: str | None = None) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    plan = validate_plan(repository_root=repository_root, plan_path=plan_path)
    executable = codex_executable.resolve()
    if not executable.is_file():
        raise RuntimeGateError("Codex executable is unavailable")
    observed = observed_version or base.observe_codex_version(executable)
    if observed != f"codex-cli {plan['runtime_ref']['version']}":
        raise RuntimeGateError("Codex version differs from paired Profile")
    receipt = {
        "schema_version": PREFLIGHT_SCHEMA,
        "preflight_id": PREFLIGHT_ID,
        "plan": {"path": str(plan_path.resolve().relative_to(repository_root)), "sha256": base.sha256_file(plan_path), "plan_id": plan["plan_id"], "plan_sha256": plan["plan_sha256"]},
        "profile": plan["profile"],
        "target": plan["target"],
        "execution_code": {
            "adapter": {"path": str(Path(adapter.__file__).resolve().relative_to(repository_root)), "sha256": base.sha256_file(Path(adapter.__file__))},
            "runner": {"path": str(Path(__file__).resolve().relative_to(repository_root)), "sha256": base.sha256_file(Path(__file__))},
        },
        "runtime": {"executable": str(executable), "observed_version": observed, "runtime_ref": plan["runtime_ref"]},
        "prompt_difference_only": True,
        "logical_slot_count": plan["logical_slot_count"],
        "reused_slots": plan["reused_slots"],
        "reused_slot_count": plan["reused_slot_count"],
        "authorized_dispatch_slots": plan["dispatch_slots"],
        "authorized_dispatch_slot_count": plan["authorized_dispatch_slot_count"],
        "issued_slot_count": 0,
        "dispatch_allowed": True,
        "stop_conditions": ["plan_hash_mismatch", "profile_or_target_drift", "prompt_or_reuse_drift", "non_prompt_compatibility_mismatch", "execution_code_hash_mismatch", "runtime_version_drift", "capability_preflight_denied", "slot_not_authorized", "slot_output_exists"],
    }
    receipt["receipt_sha256"] = base.content_identity(receipt, "receipt_sha256")
    return receipt


def validate_preflight(*, repository_root: Path, receipt_path: Path, observed_version: str | None = None):
    repository_root = repository_root.resolve()
    receipt = adapter.load_object(receipt_path.resolve())
    if receipt.get("schema_version") != PREFLIGHT_SCHEMA or receipt.get("receipt_sha256") != base.content_identity(receipt, "receipt_sha256"):
        raise RuntimeGateError("paired preflight identity mismatch")
    plan_path = base.safe_repository_file(repository_root, receipt.get("plan") or {}, "paired plan")
    plan = validate_plan(repository_root=repository_root, plan_path=plan_path)
    for reference in receipt.get("execution_code", {}).values():
        base.safe_repository_file(repository_root, reference, "execution code")
    executable = Path(receipt.get("runtime", {}).get("executable", "")).resolve()
    observed = observed_version or base.observe_codex_version(executable)
    if observed != receipt.get("runtime", {}).get("observed_version") or observed != f"codex-cli {plan['runtime_ref']['version']}":
        raise RuntimeGateError("paired preflight runtime drift")
    if (
        receipt.get("prompt_difference_only") is not True
        or receipt.get("authorized_dispatch_slots") != plan["dispatch_slots"]
        or receipt.get("reused_slots") != plan["reused_slots"]
        or receipt.get("dispatch_allowed") is not True
        or receipt.get("issued_slot_count") != 0
    ):
        raise RuntimeGateError("paired preflight does not authorize exact fresh slots")
    expected = build_preflight(repository_root=repository_root, plan_path=plan_path, codex_executable=executable, observed_version=observed)
    if receipt != expected:
        raise RuntimeGateError("paired preflight is stale")
    return receipt, plan


def execute_slot(*, repository_root: Path, receipt_path: Path, slot_id: str, output_root: Path, session_root: Path):
    repository_root = repository_root.resolve()
    receipt, plan = validate_preflight(repository_root=repository_root, receipt_path=receipt_path)
    selected = [slot for slot in plan["dispatch_slots"] if slot["slot_id"] == slot_id]
    if len(selected) != 1:
        raise RuntimeGateError("paired slot is not authorized exactly once")
    slot = selected[0]
    slot_root = output_root.resolve() / slot_id
    if slot_root.exists():
        raise RuntimeGateError(f"paired slot output already exists: {slot_root}")
    profile_path = base.safe_repository_file(repository_root, plan["profile"], "paired profile")
    target_path = base.safe_repository_file(repository_root, plan["target"], "target")
    binding = validate_profile(repository_root=repository_root, profile_path=profile_path, target_path=target_path)
    base.write_once(slot_root / "private/dispatch-receipt.json", base.canonical_bytes({"slot": slot, "plan_sha256": plan["plan_sha256"], "preflight_sha256": base.sha256_file(receipt_path), "status": "issued"}))
    try:
        materialized = slot_root / "materialized"
        adapter.materialize_case(target_path.parent, slot["case_id"], materialized)
        workspace = materialized / "workspace"
        manifest = binding["manifests"][slot["arm"]]
        prompt_file = base.bundle_stored_path(binding["bundles"][slot["arm"]] / "files", "AGENTS.md", manifest["storage_format"])
        instruction = workspace / "AGENTS.md"
        if instruction.exists():
            raise RuntimeGateError("materialized fixture already contains AGENTS.md")
        instruction.write_bytes(prompt_file.read_bytes())
        os.chmod(instruction, 0o600)
        model_input = adapter.render_model_input(binding["paths"]["task_spec"], materialized / "model-visible/input.json")
        canonical_schema = target_path.parent / "schemas/response.schema.json"
        transport_schema = slot_root / "private/transport-response.schema.json"
        projection = base.project_response_schema(canonical_schema, transport_schema)
        base.write_once(slot_root / "private/schema-projection-receipt.json", base.canonical_bytes(projection))
        final_response = slot_root / "private/final-response.json"
        command = base.build_command(executable=Path(receipt["runtime"]["executable"]), workspace=workspace, profile=binding["profile"], response_schema=transport_schema, final_response=final_response)
        started_wall = time.time()
        started_ns = time.monotonic_ns()
        completed = subprocess.run(command, input=model_input, capture_output=True, check=False)
        elapsed = (time.monotonic_ns() - started_ns) / 1_000_000_000
        base.write_once(slot_root / "private/codex-events.jsonl", completed.stdout)
        base.write_once(slot_root / "private/codex-stderr.bin", completed.stderr)
        if completed.returncode != 0:
            raise RuntimeGateError("Codex process did not exit successfully")
        identity = base.parse_codex_jsonl_identity(completed.stdout)
        usage = base.collect_workspace_usage_by_root(session_root.resolve(), workspace.resolve(), identity["root_thread_id"], modified_since=started_wall - 60)
        root_sessions = [item for item in usage["sessions"] if item["thread_id"] == identity["root_thread_id"]]
        if len(root_sessions) != 1:
            raise RuntimeGateError("persisted root rollout is not uniquely bound")
        grade = adapter.grade_case(target_root=target_path.parent, case_id=slot["case_id"], materialized_root=materialized, final_response_path=final_response, rollout_path=Path(root_sessions[0]["rollout_file"]))
        base.write_once(slot_root / "private/grade.json", base.canonical_bytes(grade))
        observation = {
            "schema_version": EXECUTION_SCHEMA,
            "slot": slot,
            "status": "valid",
            "process_exit_code": completed.returncode,
            "quality_score": grade["quality_score"],
            "mechanism_passed": grade["mechanism_passed"],
            "all_agent_total_tokens": usage["all_agent_total_tokens"],
            "elapsed_seconds": elapsed,
            "token_accounting": usage["token_accounting"],
            "artifacts": {"final_response_sha256": base.sha256_file(final_response), "grade_sha256": base.sha256_file(slot_root / "private/grade.json")},
        }
        base.write_once(slot_root / "private/execution-observation.json", base.canonical_bytes(observation))
        return observation
    except Exception as error:
        base.write_once(slot_root / "private/execution-failure.json", base.canonical_bytes({"schema_version": FAILURE_SCHEMA, "slot": slot, "status": "excluded_external_failure", "reason": str(error)}))
        raise


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
