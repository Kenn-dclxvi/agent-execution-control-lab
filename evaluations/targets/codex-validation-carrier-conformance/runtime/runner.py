#!/usr/bin/env python3
"""Qualification-only plan, preflight, and Codex execution entrypoint."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.all_agent_usage import AllAgentUsageError, collect_workspace_usage_by_root
from scripts.export_prompt_bundle import BundleError, bundle_stored_path, verify_bundle
from scripts.semantic_protocol_codex_adapter import parse_codex_jsonl_identity


def _load_adapter():
    path = Path(__file__).with_name("adapter.py")
    spec = importlib.util.spec_from_file_location("codex_validation_carrier_adapter", path)
    if spec is None or spec.loader is None:
        raise RuntimeGateError("target adapter cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


adapter = _load_adapter()

PLAN_SCHEMA = "codex-validation-carrier-qualification-plan/v1"
PREFLIGHT_SCHEMA = "codex-validation-carrier-qualification-preflight/v1"
EXECUTION_SCHEMA = "codex-validation-carrier-execution-observation/v1"
FAILURE_SCHEMA = "codex-validation-carrier-external-failure/v1"
RUNTIME_EXPECTED = {
    "runtime": "codex-cli",
    "version": "0.146.0",
    "model": "gpt-5.6-sol",
    "reasoning_effort": "medium",
    "permission": {"sandbox": "workspace-write", "approval_policy": "never"},
    "session_mode": "persisted_for_usage_collection",
    "token_accounting": {
        "scope": "all_agents",
        "revision": "v2",
        "source": "codex_rollout_final_usage_by_thread_bound_workspace",
    },
    "instruction_isolation": {
        "ignore_user_config": True,
        "ignore_rules": True,
        "memory": False,
        "apps": False,
        "plugins": False,
        "plugin_sharing": False,
        "multi_agent": False,
    },
    "elapsed_boundary": "adapter_start_to_terminal_process_result_monotonic",
}


class RuntimeGateError(Exception):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def identity_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def content_identity(value: dict[str, Any], field: str) -> str:
    return hashlib.sha256(identity_bytes({key: item for key, item in value.items() if key != field})).hexdigest()


def write_once(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(value)
    except FileExistsError as error:
        raise RuntimeGateError(f"refusing to overwrite: {path}") from error


def safe_repository_file(repository_root: Path, reference: dict[str, Any], label: str) -> Path:
    raw = reference.get("path") if isinstance(reference, dict) else None
    if not isinstance(raw, str) or not raw:
        raise RuntimeGateError(f"{label} path is unbound")
    path = (repository_root.resolve() / raw).resolve()
    try:
        path.relative_to(repository_root.resolve())
    except ValueError as error:
        raise RuntimeGateError(f"{label} path escapes repository") from error
    if not path.is_file() or sha256_file(path) != reference.get("sha256"):
        raise RuntimeGateError(f"{label} hash mismatch")
    return path


def validate_profile(*, repository_root: Path, profile_path: Path, target_path: Path) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    profile = adapter.load_object(profile_path.resolve())
    target = adapter.load_object(target_path.resolve())
    if profile.get("schema_version") != "codex-validation-carrier-profile/v1":
        raise RuntimeGateError("unsupported Profile schema")
    if profile.get("lifecycle_state") != "registered_not_qualified":
        raise RuntimeGateError("Profile lifecycle state is invalid")
    if profile.get("target_id") != target.get("target_id") or target.get("target_id") != "codex-validation-carrier-conformance":
        raise RuntimeGateError("Profile target identity mismatch")
    if profile.get("target_repository_ref") != target.get("target_repository"):
        raise RuntimeGateError("Profile target repository ref mismatch")

    references = {
        "evaluation_set": profile.get("evaluation_set_ref"),
        "task_spec": profile.get("task_spec_ref"),
        "rating": profile.get("rating_ref"),
        "token_accounting": profile.get("token_accounting_ref"),
        "capability_catalog": profile.get("capability_catalog_ref"),
        "schema_transport": profile.get("schema_transport_ref"),
    }
    bound = {name: safe_repository_file(repository_root, reference, name) for name, reference in references.items()}
    evaluation_set = adapter.load_object(bound["evaluation_set"])
    if evaluation_set.get("set_id") != profile["evaluation_set_ref"].get("set_id"):
        raise RuntimeGateError("evaluation set identity mismatch")
    if [item.get("case_id") for item in evaluation_set.get("cases", [])] != [f"VCC-H0{index}" for index in range(1, 7)]:
        raise RuntimeGateError("qualification case membership mismatch")

    runtime = copy.deepcopy(profile.get("runtime_ref") or {})
    runtime.pop("capability_catalog", None)
    runtime.pop("output_schema_transport", None)
    if runtime != RUNTIME_EXPECTED:
        raise RuntimeGateError("Profile runtime differs from qualification contract")
    capability = adapter.load_object(bound["capability_catalog"])
    cases_path = repository_root / "evaluations/targets/codex-validation-carrier-conformance/cases/heldout-r1/input-cases.json"
    case_contract = adapter.load_object(cases_path)["runtime_contract"]
    if capability.get("carrier_capabilities") != case_contract["carrier_capabilities"]:
        raise RuntimeGateError("capability catalog differs from case contract")
    preflight = adapter.capability_preflight(case_contract)
    if preflight["dispatch_state"] != "allowed":
        raise RuntimeGateError(f"capability preflight denied: {preflight['reason']}")

    prompt = profile.get("prompt_set_identity") or {}
    bundle_raw = prompt.get("path")
    if not isinstance(bundle_raw, str):
        raise RuntimeGateError("prompt bundle path is unbound")
    bundle_path = (repository_root / bundle_raw).resolve()
    try:
        manifest = verify_bundle(bundle_path)
    except (BundleError, OSError) as error:
        raise RuntimeGateError("prompt bundle is invalid") from error
    if prompt.get("name") != manifest.get("prompt_identity") or prompt.get("sha256") != manifest.get("bundle_sha256"):
        raise RuntimeGateError("prompt bundle identity mismatch")
    if profile.get("repetition_condition") != {
        "iterations": 1,
        "order": "case_id_ascending",
        "valid_low_quality_policy": "retain",
        "external_failure_policy": "exclude_without_case_change",
    }:
        raise RuntimeGateError("qualification repetition condition mismatch")
    if profile.get("execution") != {
        "max_workers": 24,
        "schedule_policy": "global_queue",
        "max_attempts_per_slot": 1,
        "dispatch_gate": "qualification_preflight_required",
    }:
        raise RuntimeGateError("qualification execution contract mismatch")
    return {
        "profile": profile,
        "target": target,
        "set": evaluation_set,
        "paths": bound,
        "bundle_path": bundle_path,
        "capability_preflight": preflight,
    }


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
        "plan_id": "codex-validation-carrier-control-free-heldout-r1-n1-dispatch-r1",
        "target": {"path": str(target_path.resolve().relative_to(repository_root)), "sha256": sha256_file(target_path), "target_id": target["target_id"]},
        "profile": {"path": str(profile_path.resolve().relative_to(repository_root)), "sha256": sha256_file(profile_path), "profile_id": profile["profile_id"]},
        "prompt_set_identity": profile["prompt_set_identity"],
        "evaluation_set_ref": profile["evaluation_set_ref"],
        "runtime_ref": profile["runtime_ref"],
        "task_spec_ref": profile["task_spec_ref"],
        "rating_ref": profile["rating_ref"],
        "token_accounting_ref": profile["token_accounting_ref"],
        "capability_catalog_ref": profile["capability_catalog_ref"],
        "schema_transport_ref": profile["schema_transport_ref"],
        "repetition_condition": profile["repetition_condition"],
        "execution": profile["execution"],
        "slots": slots,
        "authorized_slot_count": len(slots),
        "issued_slot_count": 0,
        "dispatch_state": "planned_not_issued",
        "scope": profile["scope"],
    }
    plan["plan_sha256"] = content_identity(plan, "plan_sha256")
    return plan


def validate_plan(*, repository_root: Path, plan_path: Path) -> dict[str, Any]:
    plan = adapter.load_object(plan_path.resolve())
    if plan.get("schema_version") != PLAN_SCHEMA or plan.get("plan_sha256") != content_identity(plan, "plan_sha256"):
        raise RuntimeGateError("dispatch plan identity mismatch")
    profile_path = safe_repository_file(repository_root, plan.get("profile") or {}, "profile")
    target_path = safe_repository_file(repository_root, plan.get("target") or {}, "target")
    expected = generate_plan(repository_root=repository_root, profile_path=profile_path, target_path=target_path)
    if plan != expected:
        raise RuntimeGateError("dispatch plan is stale")
    return plan


def observe_codex_version(executable: Path) -> str:
    completed = subprocess.run([str(executable.resolve()), "--version"], capture_output=True, check=False, text=True)
    if completed.returncode != 0 or not completed.stdout.strip():
        raise RuntimeGateError("Codex version observation failed")
    return completed.stdout.strip()


def build_preflight(*, repository_root: Path, plan_path: Path, codex_executable: Path, observed_version: str | None = None) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    plan = validate_plan(repository_root=repository_root, plan_path=plan_path)
    executable = codex_executable.resolve()
    if not executable.is_file():
        raise RuntimeGateError("Codex executable is unavailable")
    observed = observed_version or observe_codex_version(executable)
    if observed != f"codex-cli {plan['runtime_ref']['version']}":
        raise RuntimeGateError("Codex version differs from Profile")
    execution_code = {
        "adapter": {"path": str(Path(adapter.__file__).resolve().relative_to(repository_root)), "sha256": sha256_file(Path(adapter.__file__))},
        "runner": {"path": str(Path(__file__).resolve().relative_to(repository_root)), "sha256": sha256_file(Path(__file__))},
    }
    receipt = {
        "schema_version": PREFLIGHT_SCHEMA,
        "preflight_id": "codex-validation-carrier-control-free-heldout-r1-n1-preflight-r1",
        "plan": {"path": str(plan_path.resolve().relative_to(repository_root)), "sha256": sha256_file(plan_path), "plan_id": plan["plan_id"], "plan_sha256": plan["plan_sha256"]},
        "profile": plan["profile"], "target": plan["target"],
        "execution_code": execution_code,
        "runtime": {"executable": str(executable), "observed_version": observed, "runtime_ref": plan["runtime_ref"]},
        "authorized_slots": plan["slots"], "authorized_slot_count": len(plan["slots"]),
        "issued_slot_count": 0, "dispatch_allowed": True,
        "stop_conditions": ["plan_hash_mismatch", "profile_or_target_drift", "execution_code_hash_mismatch", "runtime_version_drift", "capability_preflight_denied", "slot_not_authorized", "slot_output_exists"],
    }
    receipt["receipt_sha256"] = content_identity(receipt, "receipt_sha256")
    return receipt


def validate_preflight(*, repository_root: Path, receipt_path: Path, observed_version: str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    repository_root = repository_root.resolve()
    receipt = adapter.load_object(receipt_path.resolve())
    if receipt.get("schema_version") != PREFLIGHT_SCHEMA or receipt.get("receipt_sha256") != content_identity(receipt, "receipt_sha256"):
        raise RuntimeGateError("preflight identity mismatch")
    plan_path = safe_repository_file(repository_root, receipt.get("plan") or {}, "plan")
    plan = validate_plan(repository_root=repository_root, plan_path=plan_path)
    for reference in receipt.get("execution_code", {}).values():
        safe_repository_file(repository_root, reference, "execution code")
    executable = Path(receipt.get("runtime", {}).get("executable", "")).resolve()
    observed = observed_version or observe_codex_version(executable)
    if observed != receipt.get("runtime", {}).get("observed_version") or observed != f"codex-cli {plan['runtime_ref']['version']}":
        raise RuntimeGateError("preflight runtime version drift")
    if receipt.get("authorized_slots") != plan["slots"] or receipt.get("dispatch_allowed") is not True or receipt.get("issued_slot_count") != 0:
        raise RuntimeGateError("preflight does not authorize the exact fresh slot set")
    expected = build_preflight(repository_root=repository_root, plan_path=plan_path, codex_executable=executable, observed_version=observed)
    if receipt != expected:
        raise RuntimeGateError("preflight is stale")
    return receipt, plan


def project_response_schema(canonical_path: Path, output_path: Path) -> dict[str, Any]:
    canonical = adapter.load_object(canonical_path)
    projected = copy.deepcopy(canonical)
    removed: list[str] = []

    def visit(value: Any, location: str = "") -> None:
        if isinstance(value, dict):
            for key in list(value):
                child_location = f"{location}.{key}" if location else key
                if key in {"$schema", "$id", "title", "uniqueItems", "pattern", "minLength"}:
                    value.pop(key)
                    removed.append(child_location)
                else:
                    visit(value[key], child_location)
            if "const" in value:
                constant = value.pop("const")
                if isinstance(constant, str):
                    value.setdefault("type", "string")
                elif isinstance(constant, bool):
                    value.setdefault("type", "boolean")
                elif isinstance(constant, int):
                    value.setdefault("type", "integer")
                value["enum"] = [constant]
                removed.append(f"{location}.const" if location else "const")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit(item, f"{location}[{index}]")

    visit(projected)
    write_once(output_path, canonical_bytes(projected))
    return {"canonical_sha256": sha256_file(canonical_path), "projected_sha256": sha256_file(output_path), "removed_or_transformed": removed}


def build_command(*, executable: Path, workspace: Path, profile: dict[str, Any], response_schema: Path, final_response: Path) -> list[str]:
    runtime = profile["runtime_ref"]
    return [
        str(executable.resolve()), "exec", "--skip-git-repo-check", "--cd", str(workspace.resolve()),
        "--ignore-user-config", "--ignore-rules", "--strict-config",
        "--disable", "multi_agent", "--disable", "memories", "--disable", "apps",
        "--disable", "plugins", "--disable", "plugin_sharing",
        "-c", 'approval_policy="never"', "--model", runtime["model"],
        "-c", f'model_reasoning_effort="{runtime["reasoning_effort"]}"',
        "--sandbox", "workspace-write", "--output-schema", str(response_schema.resolve()),
        "--json", "--output-last-message", str(final_response.resolve()), "-",
    ]


def execute_slot(*, repository_root: Path, receipt_path: Path, slot_id: str, output_root: Path, session_root: Path) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    receipt, plan = validate_preflight(repository_root=repository_root, receipt_path=receipt_path)
    selected = [slot for slot in plan["slots"] if slot["slot_id"] == slot_id]
    if len(selected) != 1:
        raise RuntimeGateError("slot is not authorized exactly once")
    slot = selected[0]
    slot_root = output_root.resolve() / slot_id
    if slot_root.exists():
        raise RuntimeGateError(f"slot output already exists: {slot_root}")
    profile_path = safe_repository_file(repository_root, plan["profile"], "profile")
    target_path = safe_repository_file(repository_root, plan["target"], "target")
    binding = validate_profile(repository_root=repository_root, profile_path=profile_path, target_path=target_path)
    profile = binding["profile"]
    write_once(slot_root / "private/dispatch-receipt.json", canonical_bytes({"slot": slot, "plan_sha256": plan["plan_sha256"], "preflight_sha256": sha256_file(receipt_path), "status": "issued"}))
    try:
        materialized = slot_root / "materialized"
        adapter.materialize_case(target_path.parent, slot["case_id"], materialized)
        workspace = materialized / "workspace"
        manifest = verify_bundle(binding["bundle_path"])
        prompt_file = bundle_stored_path(binding["bundle_path"] / "files", "AGENTS.md", manifest["storage_format"])
        instruction = workspace / "AGENTS.md"
        if instruction.exists():
            raise RuntimeGateError("materialized fixture already contains AGENTS.md")
        instruction.write_bytes(prompt_file.read_bytes())
        os.chmod(instruction, 0o600)
        model_input = adapter.render_model_input(binding["paths"]["task_spec"], materialized / "model-visible/input.json")
        canonical_schema = target_path.parent / "schemas/response.schema.json"
        transport_schema = slot_root / "private/transport-response.schema.json"
        projection = project_response_schema(canonical_schema, transport_schema)
        write_once(slot_root / "private/schema-projection-receipt.json", canonical_bytes(projection))
        final_response = slot_root / "private/final-response.json"
        command = build_command(executable=Path(receipt["runtime"]["executable"]), workspace=workspace, profile=profile, response_schema=transport_schema, final_response=final_response)
        started_wall = time.time()
        started_ns = time.monotonic_ns()
        completed = subprocess.run(command, input=model_input, capture_output=True, check=False)
        elapsed = (time.monotonic_ns() - started_ns) / 1_000_000_000
        write_once(slot_root / "private/codex-events.jsonl", completed.stdout)
        write_once(slot_root / "private/codex-stderr.bin", completed.stderr)
        if completed.returncode != 0:
            raise RuntimeGateError("Codex process did not exit successfully")
        identity = parse_codex_jsonl_identity(completed.stdout)
        usage = collect_workspace_usage_by_root(session_root.resolve(), workspace.resolve(), identity["root_thread_id"], modified_since=started_wall - 60)
        root_sessions = [item for item in usage["sessions"] if item["thread_id"] == identity["root_thread_id"]]
        if len(root_sessions) != 1:
            raise RuntimeGateError("persisted root rollout is not uniquely bound")
        grade = adapter.grade_case(target_root=target_path.parent, case_id=slot["case_id"], materialized_root=materialized, final_response_path=final_response, rollout_path=Path(root_sessions[0]["rollout_file"]))
        write_once(slot_root / "private/grade.json", canonical_bytes(grade))
        observation = {
            "schema_version": EXECUTION_SCHEMA, "slot": slot, "status": "valid",
            "process_exit_code": completed.returncode, "quality_score": grade["quality_score"],
            "mechanism_passed": grade["mechanism_passed"],
            "all_agent_total_tokens": usage["all_agent_total_tokens"], "elapsed_seconds": elapsed,
            "token_accounting": usage["token_accounting"],
            "artifacts": {"final_response_sha256": sha256_file(final_response), "grade_sha256": sha256_file(slot_root / "private/grade.json")},
        }
        write_once(slot_root / "private/execution-observation.json", canonical_bytes(observation))
        return observation
    except Exception as error:
        write_once(slot_root / "private/execution-failure.json", canonical_bytes({"schema_version": FAILURE_SCHEMA, "slot": slot, "status": "excluded_external_failure", "reason": str(error)}))
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
        write_once(args.output, canonical_bytes(generate_plan(repository_root=args.repository_root, profile_path=args.profile, target_path=args.target)))
    elif args.command == "preflight":
        write_once(args.output, canonical_bytes(build_preflight(repository_root=args.repository_root, plan_path=args.plan, codex_executable=args.codex)))
    else:
        execute_slot(repository_root=args.repository_root, receipt_path=args.preflight, slot_id=args.slot_id, output_root=args.output_root, session_root=args.session_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
