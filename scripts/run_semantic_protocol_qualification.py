#!/usr/bin/env python3
"""Plan, preflight, and execute one authorized semantic-protocol qualification slot."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from typing import Any

try:
    from .export_prompt_bundle import BundleError, bundle_stored_path, verify_bundle
    from .materialize_semantic_protocol_case import MaterializationError, materialize
    from .semantic_protocol_codex_adapter import (
        SemanticCodexAdapterError,
        build_command,
        collect_accounted_usage,
        collect_accounted_usage_persisted,
        load_object,
        parse_codex_jsonl_identity,
        prepare_instruction_workspace,
        validate_final_response,
        validate_registered_profile,
    )
except ImportError:
    from export_prompt_bundle import BundleError, bundle_stored_path, verify_bundle
    from materialize_semantic_protocol_case import MaterializationError, materialize
    from semantic_protocol_codex_adapter import (
        SemanticCodexAdapterError,
        build_command,
        collect_accounted_usage,
        collect_accounted_usage_persisted,
        load_object,
        parse_codex_jsonl_identity,
        prepare_instruction_workspace,
        validate_final_response,
        validate_registered_profile,
    )


PLAN_SCHEMA = "portable-instruction-semantic-dispatch-plan/v1"
PREFLIGHT_SCHEMA = "portable-instruction-semantic-profile-preflight/v1"
DISPATCH_SCHEMA = "portable-instruction-semantic-dispatch-receipt/v1"
EXECUTION_SCHEMA = "portable-instruction-semantic-execution-observation/v1"
FAILURE_SUMMARY_SCHEMA = "portable-instruction-semantic-external-failure-summary/v1"
CONTROL_FREE_DISPATCH_SERIES_ID = "portable-semantic-control-free-heldout-r1-n1"


class QualificationGateError(Exception):
    pass


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def identity_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def content_identity(value: dict[str, Any], field: str) -> str:
    return sha256_bytes(identity_bytes({key: item for key, item in value.items() if key != field}))


def safe_repository_path(repository_root: Path, raw_path: object, label: str) -> Path:
    if not isinstance(raw_path, str) or not raw_path:
        raise QualificationGateError(f"{label} path is unbound")
    path = (repository_root.resolve() / raw_path).resolve()
    try:
        path.relative_to(repository_root.resolve())
    except ValueError as error:
        raise QualificationGateError(f"{label} path escapes repository") from error
    if not path.is_file():
        raise QualificationGateError(f"{label} path is unavailable")
    return path


def write_once(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(value)
    except FileExistsError as error:
        raise QualificationGateError(f"refusing to overwrite: {path}") from error


def profile_paths(profile: dict[str, Any], repository_root: Path) -> dict[str, Path]:
    runtime = profile.get("runtime_ref") or {}
    return {
        "set": safe_repository_path(repository_root, (profile.get("evaluation_set_ref") or {}).get("path"), "set"),
        "task_spec": safe_repository_path(repository_root, (profile.get("task_spec_ref") or {}).get("path"), "TaskSpec"),
        "rating": safe_repository_path(repository_root, (profile.get("rating_ref") or {}).get("path"), "rating"),
        "transcript": safe_repository_path(repository_root, (profile.get("transcript_ref") or {}).get("path"), "transcript"),
        "capability": safe_repository_path(repository_root, (runtime.get("capability_catalog") or {}).get("path"), "capability catalog"),
    }


def validate_target_registration(target_path: Path) -> dict[str, Any]:
    target_path = target_path.resolve()
    registration_path = target_path.parent / "registration.json"
    registration = load_object(registration_path)
    target = load_object(target_path)
    if registration.get("schema_version") != "portable-instruction-semantic-target-registration/v1":
        raise QualificationGateError("unsupported target registration schema")
    if registration.get("target_id") != target.get("target_id"):
        raise QualificationGateError("target registration identity mismatch")
    artifacts = registration.get("registered_artifacts")
    if not isinstance(artifacts, dict) or not artifacts:
        raise QualificationGateError("target registration artifacts are unbound")
    required = {
        "cases/heldout-r1/input-cases.json",
        "cases/heldout-r1/oracle.json",
        "cases/heldout-r1/response.schema.json",
        "rating-contracts/portable-instruction-semantic-exact-v1.json",
    }
    if not required.issubset(artifacts):
        raise QualificationGateError("target registration omits qualification artifacts")
    for relative, expected in artifacts.items():
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise QualificationGateError("target registration artifact binding is invalid")
        artifact = (target_path.parent / relative).resolve()
        try:
            artifact.relative_to(target_path.parent)
        except ValueError as error:
            raise QualificationGateError("target registration artifact escapes target") from error
        if not artifact.is_file() or sha256_file(artifact) != expected:
            raise QualificationGateError(f"target registration artifact hash mismatch: {relative}")
    return {
        "path": str(registration_path),
        "sha256": sha256_file(registration_path),
        "registration_id": registration["registration_id"],
        "registered_artifacts": artifacts,
    }


def dispatch_plan_identity(profile: dict[str, Any]) -> tuple[str, str]:
    profile_id = profile.get("profile_id")
    if not isinstance(profile_id, str) or not profile_id:
        raise QualificationGateError("qualification Profile identity is unbound")
    revision = profile_id.rsplit("-", 1)[-1]
    if re.fullmatch(r"r[1-9][0-9]*", revision) is None:
        raise QualificationGateError("unsupported qualification Profile revision")
    series_id = profile.get("dispatch_series_id", CONTROL_FREE_DISPATCH_SERIES_ID)
    if not isinstance(series_id, str) or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", series_id) is None:
        raise QualificationGateError("qualification dispatch series identity is invalid")
    return f"{series_id}-dispatch-{revision}", revision


def generate_plan(
    *,
    repository_root: Path,
    profile_path: Path,
    target_path: Path,
    bundle_path: Path,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    profile_path = profile_path.resolve()
    target_path = target_path.resolve()
    bundle_path = bundle_path.resolve()
    binding = validate_registered_profile(
        profile_path=profile_path,
        target_path=target_path,
        bundle_path=bundle_path,
        repository_root=repository_root,
    )
    profile = load_object(profile_path)
    target = load_object(target_path)
    registration = validate_target_registration(target_path)
    registration["path"] = str(Path(registration["path"]).relative_to(repository_root))
    paths = profile_paths(profile, repository_root)
    evaluation_set = load_object(paths["set"])
    set_ref = profile["evaluation_set_ref"]
    if evaluation_set.get("set_id") != set_ref.get("set_id"):
        raise QualificationGateError("evaluation set identity mismatch")
    if evaluation_set.get("set_revision") != set_ref.get("set_revision"):
        raise QualificationGateError("evaluation set revision mismatch")
    if sha256_file(paths["set"]) != set_ref.get("sha256"):
        raise QualificationGateError("evaluation set hash mismatch")
    cases = evaluation_set.get("cases")
    if not isinstance(cases, list) or len(cases) != 14:
        raise QualificationGateError("qualification set must contain exactly fourteen cases")
    case_ids = [item.get("case_id") for item in cases if isinstance(item, dict)]
    if case_ids != sorted(case_ids) or len(set(case_ids)) != 14:
        raise QualificationGateError("qualification cases must be unique and sorted")
    repetition = profile.get("repetition_condition")
    if repetition != {
        "iterations": 1,
        "order": "case_id_ascending",
        "valid_low_quality_policy": "retain",
        "external_failure_policy": "exclude_without_case_change",
    }:
        raise QualificationGateError("qualification repetition condition mismatch")
    slots = [
        {
            "slot_id": f"{item['case_id']}-i001",
            "case_id": item["case_id"],
            "case_revision": item["case_revision"],
            "iteration": 1,
        }
        for item in cases
    ]
    plan_id, _profile_revision = dispatch_plan_identity(profile)
    plan = {
        "schema_version": PLAN_SCHEMA,
        "plan_id": plan_id,
        "target": {
            "path": str(target_path.relative_to(repository_root)),
            "sha256": sha256_file(target_path),
            "target_id": target["target_id"],
            "target_subject_ref": profile["target_subject_ref"],
        },
        "target_registration": registration,
        "profile": {
            "path": str(profile_path.relative_to(repository_root)),
            "sha256": sha256_file(profile_path),
            "profile_id": profile["profile_id"],
        },
        "prompt_set_identity": profile["prompt_set_identity"],
        "evaluation_set_ref": profile["evaluation_set_ref"],
        "runtime_ref": profile["runtime_ref"],
        "task_spec_ref": profile["task_spec_ref"],
        "rating_ref": profile["rating_ref"],
        "transcript_ref": profile["transcript_ref"],
        "repetition_condition": repetition,
        "execution": profile["execution"],
        "slots": slots,
        "authorized_slot_count": len(slots),
        "issued_slot_count": 0,
        "binding_receipt": binding,
        "dispatch_state": "planned_not_issued",
    }
    plan["plan_sha256"] = content_identity(plan, "plan_sha256")
    return plan


def validate_plan(
    plan: dict[str, Any],
    *,
    repository_root: Path,
    bundle_path: Path,
) -> dict[str, Any]:
    if plan.get("schema_version") != PLAN_SCHEMA:
        raise QualificationGateError("unsupported dispatch plan schema")
    if plan.get("plan_sha256") != content_identity(plan, "plan_sha256"):
        raise QualificationGateError("dispatch plan content hash mismatch")
    profile_path = safe_repository_path(repository_root, (plan.get("profile") or {}).get("path"), "profile")
    target_path = safe_repository_path(repository_root, (plan.get("target") or {}).get("path"), "target")
    expected = generate_plan(
        repository_root=repository_root,
        profile_path=profile_path,
        target_path=target_path,
        bundle_path=bundle_path,
    )
    if plan != expected:
        raise QualificationGateError("dispatch plan is stale or differs from bound artifacts")
    return expected


def observe_codex_version(executable: Path) -> str:
    executable = executable.resolve()
    completed = subprocess.run(
        [str(executable), "--version"],
        capture_output=True,
        check=False,
        text=True,
    )
    if completed.returncode != 0:
        raise QualificationGateError("Codex version observation failed")
    observed = completed.stdout.strip()
    if not observed:
        raise QualificationGateError("Codex version observation is empty")
    return observed


def build_preflight(
    *,
    plan_path: Path,
    repository_root: Path,
    bundle_path: Path,
    core_adapter_path: Path,
    runner_path: Path,
    codex_executable: Path,
    observed_version: str | None = None,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    plan_path = plan_path.resolve()
    core_adapter_path = core_adapter_path.resolve()
    runner_path = runner_path.resolve()
    plan = load_object(plan_path)
    validate_plan(plan, repository_root=repository_root, bundle_path=bundle_path)
    if not core_adapter_path.is_file():
        raise QualificationGateError("core adapter source is unavailable")
    if not runner_path.is_file():
        raise QualificationGateError("qualification runner source is unavailable")
    executable = codex_executable.resolve()
    if not executable.is_file():
        raise QualificationGateError("Codex executable is unavailable")
    observed = observed_version or observe_codex_version(executable)
    expected_version = plan["runtime_ref"]["version"]
    if observed != f"codex-cli {expected_version}":
        raise QualificationGateError("Codex version differs from Profile")
    receipt = {
        "schema_version": PREFLIGHT_SCHEMA,
        "preflight_id": plan["plan_id"].replace("dispatch", "preflight"),
        "plan": {
            "path": str(plan_path.relative_to(repository_root)),
            "sha256": sha256_file(plan_path),
            "plan_id": plan["plan_id"],
            "plan_sha256": plan["plan_sha256"],
        },
        "profile": plan["profile"],
        "target": plan["target"],
        "execution_code": {
            "core_adapter": {
                "path": str(core_adapter_path.relative_to(repository_root)),
                "sha256": sha256_file(core_adapter_path),
            },
            "runner": {
                "path": str(runner_path.relative_to(repository_root)),
                "sha256": sha256_file(runner_path),
            },
        },
        "runtime": {
            "executable": str(executable),
            "observed_version": observed,
            "runtime_ref": plan["runtime_ref"],
        },
        "authorized_slots": plan["slots"],
        "authorized_slot_count": plan["authorized_slot_count"],
        "issued_slot_count": 0,
        "dispatch_allowed": True,
        "stop_conditions": [
            "plan_hash_mismatch",
            "profile_or_target_drift",
            "execution_code_hash_mismatch",
            "runtime_version_drift",
            "slot_not_authorized",
            "slot_output_exists",
        ],
    }
    receipt["receipt_sha256"] = content_identity(receipt, "receipt_sha256")
    return receipt


def validate_preflight(
    *,
    receipt_path: Path,
    repository_root: Path,
    bundle_path: Path,
    observed_version: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    repository_root = repository_root.resolve()
    receipt_path = receipt_path.resolve()
    receipt = load_object(receipt_path)
    if receipt.get("schema_version") != PREFLIGHT_SCHEMA:
        raise QualificationGateError("unsupported Profile preflight schema")
    if receipt.get("receipt_sha256") != content_identity(receipt, "receipt_sha256"):
        raise QualificationGateError("Profile preflight content hash mismatch")
    plan_path = safe_repository_path(repository_root, (receipt.get("plan") or {}).get("path"), "plan")
    if sha256_file(plan_path) != receipt["plan"].get("sha256"):
        raise QualificationGateError("Profile preflight plan file hash mismatch")
    plan = load_object(plan_path)
    validate_plan(plan, repository_root=repository_root, bundle_path=bundle_path)
    if receipt.get("plan") != {
        "path": str(plan_path.relative_to(repository_root)),
        "sha256": sha256_file(plan_path),
        "plan_id": plan["plan_id"],
        "plan_sha256": plan["plan_sha256"],
    }:
        raise QualificationGateError("Profile preflight plan binding mismatch")
    if receipt.get("profile") != plan.get("profile") or receipt.get("target") != plan.get("target"):
        raise QualificationGateError("Profile preflight artifact binding mismatch")
    execution_code = receipt.get("execution_code") or {}
    for key, label in (("core_adapter", "core adapter"), ("runner", "qualification runner")):
        reference = execution_code.get(key) or {}
        source_path = safe_repository_path(repository_root, reference.get("path"), label)
        if sha256_file(source_path) != reference.get("sha256"):
            raise QualificationGateError(f"Profile preflight {label} hash mismatch")
    executable = Path((receipt.get("runtime") or {}).get("executable", "")).resolve()
    if not executable.is_file():
        raise QualificationGateError("Profile preflight Codex executable is unavailable")
    observed = observed_version or observe_codex_version(executable)
    if observed != receipt["runtime"].get("observed_version"):
        raise QualificationGateError("Profile preflight runtime version drift")
    if receipt["runtime"].get("runtime_ref") != plan.get("runtime_ref"):
        raise QualificationGateError("Profile preflight runtime binding mismatch")
    if observed != f"codex-cli {plan['runtime_ref']['version']}":
        raise QualificationGateError("Profile preflight runtime differs from Profile")
    if receipt.get("authorized_slots") != plan.get("slots"):
        raise QualificationGateError("Profile preflight slot set differs from plan")
    if receipt.get("authorized_slot_count") != len(plan.get("slots", [])):
        raise QualificationGateError("Profile preflight slot count differs from plan")
    if receipt.get("dispatch_allowed") is not True or receipt.get("issued_slot_count") != 0:
        raise QualificationGateError("Profile preflight does not authorize fresh dispatch")
    return receipt, plan


def authorize_slot(
    *,
    receipt_path: Path,
    repository_root: Path,
    bundle_path: Path,
    slot_id: str,
    output_root: Path,
    observed_version: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], Path]:
    receipt, plan = validate_preflight(
        receipt_path=receipt_path,
        repository_root=repository_root,
        bundle_path=bundle_path,
        observed_version=observed_version,
    )
    selected = [slot for slot in receipt["authorized_slots"] if slot.get("slot_id") == slot_id]
    if len(selected) != 1:
        raise QualificationGateError(f"slot is not authorized exactly once: {slot_id}")
    slot_root = output_root.resolve() / slot_id
    if slot_root.exists():
        raise QualificationGateError(f"slot output already exists: {slot_root}")
    return receipt, plan, selected[0], slot_root


def render_model_input(wrapper_path: Path, packet_path: Path) -> bytes:
    wrapper = wrapper_path.read_text(encoding="utf-8")
    if wrapper.count("{{MODEL_PACKET_JSON}}") != 1:
        raise QualificationGateError("TaskSpec wrapper must contain one packet placeholder")
    packet = packet_path.read_text(encoding="utf-8").rstrip("\n")
    return wrapper.replace("{{MODEL_PACKET_JSON}}", packet).encode("utf-8")


def project_response_schema(
    canonical_path: Path,
    output_path: Path,
    transport_contract: dict[str, Any],
) -> dict[str, Any]:
    r2_contract = {
        "revision": "codex-structured-output-projection-r2",
        "api_schema_projection": "remove_uniqueItems_only",
        "canonical_post_validation": True,
    }
    r3_contract = {
        "revision": "codex-structured-output-supported-subset-r3",
        "api_schema_projection": "supported_subset_semantic_equivalence",
        "canonical_post_validation": True,
    }
    if transport_contract not in (r2_contract, r3_contract):
        raise QualificationGateError("unsupported output schema transport contract")
    canonical = load_object(canonical_path)
    projected = copy.deepcopy(canonical)
    unique_ids = (projected.get("$defs") or {}).get("unique_ids")
    if not isinstance(unique_ids, dict) or unique_ids.get("uniqueItems") is not True:
        raise QualificationGateError("canonical uniqueItems transport boundary is unavailable")
    removed = unique_ids.pop("uniqueItems")
    removed_keywords = ["$defs.unique_ids.uniqueItems"]
    transformations: list[str] = []
    if transport_contract == r3_contract:
        for key in ("$schema", "$id", "title"):
            if key not in projected:
                raise QualificationGateError(f"canonical schema metadata is unavailable: {key}")
            projected.pop(key)
            removed_keywords.append(key)
        for path, node in (
            ("$defs.unique_ids.items.minLength", unique_ids.get("items")),
            ("properties.case_id.minLength", (projected.get("properties") or {}).get("case_id")),
        ):
            if not isinstance(node, dict) or node.pop("minLength", None) != 1:
                raise QualificationGateError(f"canonical string boundary is unavailable: {path}")
            removed_keywords.append(path)
        schema_id = (projected.get("properties") or {}).get("schema_id")
        expected_schema_id = "portable-instruction-control-response/r2"
        if not isinstance(schema_id, dict) or schema_id != {"const": expected_schema_id}:
            raise QualificationGateError("canonical schema_id const boundary is unavailable")
        schema_id.clear()
        schema_id.update({"type": "string", "enum": [expected_schema_id]})
        transformations.append("properties.schema_id.const_to_typed_single_enum")
    if removed is not True or projected == canonical:
        raise QualificationGateError("output schema transport projection made no change")
    write_once(output_path, canonical_bytes(projected))
    return {
        "contract": transport_contract,
        "canonical_sha256": sha256_file(canonical_path),
        "projected_sha256": sha256_file(output_path),
        "removed_keywords": removed_keywords,
        "transformations": transformations,
    }


def execute_slot(
    *,
    receipt_path: Path,
    repository_root: Path,
    bundle_path: Path,
    slot_id: str,
    output_root: Path,
    session_root: Path,
) -> dict[str, Any]:
    repository_root = repository_root.resolve()
    receipt, plan, slot, slot_root = authorize_slot(
        receipt_path=receipt_path,
        repository_root=repository_root,
        bundle_path=bundle_path,
        slot_id=slot_id,
        output_root=output_root,
    )
    profile_path = repository_root / plan["profile"]["path"]
    profile = load_object(profile_path)
    target_path = repository_root / plan["target"]["path"]
    bundle = verify_bundle(bundle_path.resolve())
    bundle_file = bundle_stored_path(bundle_path.resolve() / "files", "AGENTS.md", bundle["storage_format"])
    set_path = repository_root / profile["evaluation_set_ref"]["path"]
    target_root = target_path.parent
    cases_path = target_root / "cases/heldout-r1/input-cases.json"
    response_schema_path = target_root / "cases/heldout-r1/response.schema.json"
    wrapper_path = repository_root / profile["task_spec_ref"]["path"]

    slot_root.mkdir(parents=True, mode=0o700)
    dispatch_receipt = {
        "schema_version": DISPATCH_SCHEMA,
        "slot": slot,
        "plan_sha256": receipt["plan"]["sha256"],
        "preflight_sha256": sha256_file(receipt_path),
        "profile_sha256": plan["profile"]["sha256"],
        "status": "issued",
    }
    write_once(slot_root / "private/dispatch-receipt.json", canonical_bytes(dispatch_receipt))
    try:
        materialize(
            target_path,
            cases_path,
            response_schema_path,
            slot["case_id"],
            slot_root / "materialized",
        )
        workspace = slot_root / "workspace"
        prepare_instruction_workspace(workspace, bundle_file.read_bytes())
        model_input = render_model_input(
            wrapper_path,
            slot_root / "materialized/model-visible/input.json",
        )
        final_response = slot_root / "private/final-response.json"
        command_schema_path = response_schema_path
        schema_transport = profile["runtime_ref"].get("output_schema_transport")
        if schema_transport:
            command_schema_path = slot_root / "private/transport-response.schema.json"
            projection = project_response_schema(response_schema_path, command_schema_path, schema_transport)
            write_once(slot_root / "private/schema-projection-receipt.json", canonical_bytes(projection))
        command = build_command(
            codex=receipt["runtime"]["executable"],
            workspace=workspace,
            model=profile["runtime_ref"]["model"],
            reasoning_effort=profile["runtime_ref"]["reasoning_effort"],
            response_schema=command_schema_path,
            final_response=final_response,
        )
        started_wall = time.time()
        started_monotonic = time.monotonic_ns()
        completed = subprocess.run(command, input=model_input, capture_output=True, check=False)
        elapsed_ns = time.monotonic_ns() - started_monotonic
        write_once(slot_root / "private/codex-events.jsonl", completed.stdout)
        write_once(slot_root / "private/codex-stderr.bin", completed.stderr)
        if completed.returncode != 0:
            raise QualificationGateError("Codex process did not exit successfully")
        validate_final_response(final_response, response_schema_path)
        usage_collector = (
            collect_accounted_usage_persisted
            if profile["runtime_ref"]["token_accounting"].get("revision") == "v2"
            else collect_accounted_usage
        )
        usage = usage_collector(
            session_root=session_root,
            workspace=workspace,
            codex_jsonl=completed.stdout,
            modified_since=started_wall - 60,
        )
        observation = {
            "schema_version": EXECUTION_SCHEMA,
            "slot": slot,
            "status": "executor_complete_unrated",
            "process_exit_code": completed.returncode,
            "elapsed_seconds": elapsed_ns / 1_000_000_000,
            "token_accounting": usage,
            "final_response": {
                "path": "private/final-response.json",
                "sha256": sha256_file(final_response),
            },
            "quality_rating": "not_started",
        }
        write_once(slot_root / "private/execution-observation.json", canonical_bytes(observation))
        return observation
    except Exception as error:
        failure = {
            "schema_version": EXECUTION_SCHEMA,
            "slot": slot,
            "status": "excluded_external_failure",
            "reason": str(error),
            "quality_rating": "not_started",
        }
        try:
            write_once(slot_root / "private/execution-failure.json", canonical_bytes(failure))
        except QualificationGateError:
            pass
        raise


def summarize_schema_transport_failure(
    *,
    plan_path: Path,
    preflight_path: Path,
    output_root: Path,
) -> dict[str, Any]:
    plan_path = plan_path.resolve()
    output_root = output_root.resolve()
    plan = load_object(plan_path)
    preflight_path = preflight_path.resolve()
    preflight = load_object(preflight_path)
    if preflight.get("plan", {}).get("plan_id") != plan.get("plan_id"):
        raise QualificationGateError("failure summary preflight and plan differ")
    observations = []
    for slot in plan.get("slots", []):
        slot_id = slot["slot_id"]
        private = output_root / slot_id / "private"
        if not private.parent.exists():
            continue
        dispatch_path = private / "dispatch-receipt.json"
        failure_path = private / "execution-failure.json"
        events_path = private / "codex-events.jsonl"
        if not all(path.is_file() for path in (dispatch_path, failure_path, events_path)):
            raise QualificationGateError(f"failure evidence is incomplete: {slot_id}")
        dispatch = load_object(dispatch_path)
        failure = load_object(failure_path)
        if dispatch.get("slot") != slot or failure.get("slot") != slot:
            raise QualificationGateError(f"failure evidence slot binding mismatch: {slot_id}")
        if failure.get("status") != "excluded_external_failure":
            raise QualificationGateError(f"slot is not an excluded external failure: {slot_id}")
        messages = []
        for line in events_path.read_text(encoding="utf-8").splitlines():
            event = json.loads(line)
            if event.get("type") in {"error", "turn.failed"}:
                messages.append(json.dumps(event, ensure_ascii=False, sort_keys=True))
        joined = "\n".join(messages)
        if "invalid_json_schema" not in joined:
            raise QualificationGateError(f"slot failure does not match schema transport signature: {slot_id}")
        if "'uniqueItems' is not permitted" in joined:
            reason_code = "codex_output_schema_unique_items_unsupported"
        elif "schema must have a 'type' key" in joined:
            reason_code = "codex_output_schema_untyped_const_unsupported"
        else:
            raise QualificationGateError(f"slot failure has an unknown schema transport signature: {slot_id}")
        if (private / "final-response.json").exists() or (private / "execution-observation.json").exists():
            raise QualificationGateError(f"failed slot unexpectedly contains a valid observation: {slot_id}")
        observations.append(
            {
                "slot_id": slot_id,
                "status": "excluded_external_failure",
                "reason_code": reason_code,
                "dispatch_receipt_sha256": sha256_file(dispatch_path),
                "failure_receipt_sha256": sha256_file(failure_path),
                "events_sha256": sha256_file(events_path),
            }
        )
    if not observations:
        raise QualificationGateError("failure summary has no issued slots")
    revision = plan["plan_id"].rsplit("-", 1)[-1]
    summary = {
        "schema_version": FAILURE_SUMMARY_SCHEMA,
        "summary_id": f"portable-semantic-control-free-heldout-r1-n1-attempt-{revision}-external-failure",
        "plan": {"path": str(plan_path), "sha256": sha256_file(plan_path), "plan_id": plan["plan_id"]},
        "preflight": {
            "path": str(preflight_path),
            "sha256": sha256_file(preflight_path),
            "preflight_id": preflight["preflight_id"],
        },
        "private_output_root": str(output_root),
        "observations": observations,
        "issued_slot_count": len(observations),
        "valid_result_count": 0,
        "classification": "profile_transport_incompatible",
        "raw_artifacts_private": True,
        "case_or_oracle_change_authorized": False,
    }
    summary["summary_sha256"] = content_identity(summary, "summary_sha256")
    return summary


def summarize_token_accounting_failure(
    *,
    plan_path: Path,
    preflight_path: Path,
    output_root: Path,
) -> dict[str, Any]:
    plan_path = plan_path.resolve()
    preflight_path = preflight_path.resolve()
    output_root = output_root.resolve()
    plan = load_object(plan_path)
    preflight = load_object(preflight_path)
    if preflight.get("plan", {}).get("plan_id") != plan.get("plan_id"):
        raise QualificationGateError("token failure preflight and plan differ")
    target_path = safe_repository_path(
        Path.cwd(),
        (plan.get("target") or {}).get("path"),
        "target",
    )
    canonical_schema = target_path.parent / "cases/heldout-r1/response.schema.json"
    observations = []
    for slot in plan.get("slots", []):
        private = output_root / slot["slot_id"] / "private"
        if not private.parent.exists():
            continue
        dispatch_path = private / "dispatch-receipt.json"
        failure_path = private / "execution-failure.json"
        events_path = private / "codex-events.jsonl"
        response_path = private / "final-response.json"
        if not all(path.is_file() for path in (dispatch_path, failure_path, events_path, response_path)):
            raise QualificationGateError(f"token failure evidence is incomplete: {slot['slot_id']}")
        failure = load_object(failure_path)
        if failure.get("status") != "excluded_external_failure" or failure.get("reason") != "Codex usage lacks primary total_tokens":
            raise QualificationGateError(f"slot is not the expected token accounting failure: {slot['slot_id']}")
        identity = parse_codex_jsonl_identity(events_path.read_bytes())
        if identity["raw_usage"].get("total_tokens") is not None:
            raise QualificationGateError(f"exec event unexpectedly has primary total_tokens: {slot['slot_id']}")
        validate_final_response(response_path, canonical_schema)
        if (private / "execution-observation.json").exists():
            raise QualificationGateError(f"token-failed slot unexpectedly contains a valid observation: {slot['slot_id']}")
        observations.append(
            {
                "slot_id": slot["slot_id"],
                "status": "excluded_external_failure",
                "reason_code": "codex_exec_usage_primary_total_missing",
                "root_thread_id": identity["root_thread_id"],
                "dispatch_receipt_sha256": sha256_file(dispatch_path),
                "failure_receipt_sha256": sha256_file(failure_path),
                "events_sha256": sha256_file(events_path),
                "schema_valid_response_sha256": sha256_file(response_path),
            }
        )
    if not observations:
        raise QualificationGateError("token failure summary has no issued slots")
    revision = plan["plan_id"].rsplit("-", 1)[-1]
    summary = {
        "schema_version": FAILURE_SUMMARY_SCHEMA,
        "summary_id": f"portable-semantic-control-free-heldout-r1-n1-attempt-{revision}-external-failure",
        "plan": {"path": str(plan_path), "sha256": sha256_file(plan_path), "plan_id": plan["plan_id"]},
        "preflight": {
            "path": str(preflight_path),
            "sha256": sha256_file(preflight_path),
            "preflight_id": preflight["preflight_id"],
        },
        "private_output_root": str(output_root),
        "observations": observations,
        "issued_slot_count": len(observations),
        "valid_result_count": 0,
        "classification": "profile_token_accounting_incompatible",
        "raw_artifacts_private": True,
        "case_or_oracle_change_authorized": False,
    }
    summary["summary_sha256"] = content_identity(summary, "summary_sha256")
    return summary


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
    summarize = commands.add_parser("summarize-schema-transport-failure")
    summarize.add_argument("--plan", type=Path, required=True)
    summarize.add_argument("--preflight", type=Path, required=True)
    summarize.add_argument("--output-root", type=Path, required=True)
    summarize.add_argument("--output", type=Path, required=True)
    token_failure = commands.add_parser("summarize-token-accounting-failure")
    token_failure.add_argument("--plan", type=Path, required=True)
    token_failure.add_argument("--preflight", type=Path, required=True)
    token_failure.add_argument("--output-root", type=Path, required=True)
    token_failure.add_argument("--output", type=Path, required=True)
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
                "schema_version": "portable-instruction-semantic-profile-preflight-verification/v1",
                "preflight_id": receipt["preflight_id"],
                "plan_id": plan["plan_id"],
                "authorized_slot_count": receipt["authorized_slot_count"],
                "dispatch_allowed": True,
            }
        elif args.command == "run-slot":
            value = execute_slot(
                receipt_path=args.receipt,
                repository_root=args.repository_root,
                bundle_path=args.bundle,
                slot_id=args.slot_id,
                output_root=args.output_root,
                session_root=args.session_root,
            )
        elif args.command == "summarize-schema-transport-failure":
            value = summarize_schema_transport_failure(
                plan_path=args.plan,
                preflight_path=args.preflight,
                output_root=args.output_root,
            )
            write_once(args.output.resolve(), canonical_bytes(value))
        else:
            value = summarize_token_accounting_failure(
                plan_path=args.plan,
                preflight_path=args.preflight,
                output_root=args.output_root,
            )
            write_once(args.output.resolve(), canonical_bytes(value))
    except (
        BundleError,
        MaterializationError,
        OSError,
        QualificationGateError,
        SemanticCodexAdapterError,
    ) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(value, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
