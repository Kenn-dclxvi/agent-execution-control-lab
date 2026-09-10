#!/usr/bin/env python3
"""Preflight and execute the general-chat semantic-protocol qualification."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time
from typing import Any

import jsonschema


class QualificationError(Exception):
    pass


ROOT = Path(__file__).resolve().parents[4]
TARGET_ROOT = ROOT / "evaluations/targets/general-chat-response-control"
TARGET_PATH = TARGET_ROOT / "target.json"
REGISTRATION_PATH = TARGET_ROOT / "registration.json"
ARRAY_FIELDS = (
    "clarification_value_ids",
    "request_evidence_ids",
    "answered_topic_ids",
    "unresolved_topic_ids",
)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def content_identity(value: dict[str, Any], field: str) -> str:
    return hashlib.sha256(canonical_bytes({k: v for k, v in value.items() if k != field})).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise QualificationError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise QualificationError(f"expected JSON object: {path}")
    return value


def safe_path(raw: str, label: str) -> Path:
    path = (ROOT / raw).resolve()
    try:
        path.relative_to(ROOT)
    except ValueError as error:
        raise QualificationError(f"{label} escapes repository") from error
    if not path.is_file() and not path.is_dir():
        raise QualificationError(f"{label} does not exist")
    return path


def verify_reference(reference: dict[str, Any], label: str) -> Path:
    path = safe_path(reference.get("path", ""), label)
    if not path.is_file() or sha256_file(path) != reference.get("sha256"):
        raise QualificationError(f"{label} hash mismatch")
    return path


def verify_bundle(profile: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    prompt = profile.get("prompt_set_identity") or {}
    bundle = safe_path(prompt.get("path", ""), "prompt bundle")
    manifest = load_object(bundle / "manifest.json")
    if manifest.get("schema_version") != "the-caption-prompt.bundle/v1":
        raise QualificationError("prompt bundle schema mismatch")
    if manifest.get("prompt_identity") != prompt.get("name"):
        raise QualificationError("prompt identity mismatch")
    if manifest.get("bundle_sha256") != prompt.get("bundle_sha256"):
        raise QualificationError("prompt bundle hash mismatch")
    entries = manifest.get("files")
    if entries != [
        {
            "git_blob_sha1": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
            "mode": "100644",
            "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "target": "AGENTS.md",
            "type": "file",
        }
    ]:
        raise QualificationError("qualification baseline must contain only empty AGENTS.md")
    instruction = bundle / "files/AGENTS.md.txt"
    if not instruction.is_file() or instruction.read_bytes() != b"":
        raise QualificationError("qualification baseline instruction is not empty")
    return bundle, manifest


def validate_profile(profile_path: Path) -> dict[str, Any]:
    profile_path = profile_path.resolve()
    profile = load_object(profile_path)
    target = load_object(TARGET_PATH)
    registration = load_object(REGISTRATION_PATH)
    if profile.get("schema_version") != "general-chat-response-profile/v1":
        raise QualificationError("profile schema mismatch")
    if profile.get("lifecycle_state") != "registered_not_qualified":
        raise QualificationError("profile lifecycle mismatch")
    if profile.get("target_id") != target.get("target_id") or profile.get("target_id") != registration.get("target_id"):
        raise QualificationError("target identity mismatch")
    expected_subject = dict(target.get("target_subject") or {})
    expected_subject.pop("subject_authority", None)
    if profile.get("target_subject_ref") != expected_subject:
        raise QualificationError("target subject mismatch")
    bundle, manifest = verify_bundle(profile)
    references = {
        "task_spec": profile.get("task_spec_ref") or {},
        "evaluation_set": profile.get("evaluation_set_ref") or {},
        "case_source": profile.get("case_source_ref") or {},
        "oracle": profile.get("oracle_ref") or {},
        "response_schema": profile.get("response_schema_ref") or {},
        "rating": profile.get("rating_ref") or {},
        "capability_catalog": (profile.get("runtime_ref") or {}).get("capability_catalog") or {},
        "token_accounting": (profile.get("runtime_ref") or {}).get("token_accounting") or {},
    }
    paths = {label: verify_reference(reference, label) for label, reference in references.items()}
    if references["oracle"].get("model_visible") is not False:
        raise QualificationError("oracle must be model-invisible")
    wrapper = paths["task_spec"].read_text(encoding="utf-8")
    if wrapper.count("{{MODEL_PACKET_JSON}}") != 1:
        raise QualificationError("TaskSpec wrapper placeholder mismatch")
    cases = load_object(paths["case_source"])
    oracle = load_object(paths["oracle"])
    evaluation_set = load_object(paths["evaluation_set"])
    response_schema = load_object(paths["response_schema"])
    input_schema = load_object(TARGET_ROOT / "cases/core-r1/input-cases.schema.json")
    oracle_schema = load_object(TARGET_ROOT / "cases/core-r1/oracle.schema.json")
    jsonschema.Draft202012Validator(input_schema).validate(cases)
    jsonschema.Draft202012Validator(oracle_schema).validate(oracle)
    case_ids = [item["case_id"] for item in cases.get("cases", [])]
    oracle_ids = [item["case_id"] for item in oracle.get("cases", [])]
    set_ids = [item["case_id"] for item in evaluation_set.get("cases", [])]
    if case_ids != sorted(case_ids) or case_ids != oracle_ids or case_ids != set_ids or len(case_ids) != 8:
        raise QualificationError("case, oracle, and set membership mismatch")
    runtime = profile.get("runtime_ref") or {}
    if runtime.get("runtime") != "codex-cli" or runtime.get("version") != "0.146.0":
        raise QualificationError("runtime identity mismatch")
    observed_version = subprocess.run(
        ["codex", "--version"], check=True, capture_output=True, text=True
    ).stdout.strip()
    if observed_version != "codex-cli 0.146.0":
        raise QualificationError("installed Codex CLI version mismatch")
    if profile.get("repetition_condition") != {
        "iterations": 1,
        "order": "case_id_ascending",
        "valid_low_quality_policy": "retain",
        "external_failure_policy": "record_and_stop_before_comparison",
    }:
        raise QualificationError("repetition condition mismatch")
    if profile.get("execution") != {
        "max_workers": 24,
        "schedule_policy": "global_queue",
        "max_attempts_per_slot": 1,
        "dispatch_gate": "saved_preflight_receipt_required",
    }:
        raise QualificationError("execution contract mismatch")
    return {
        "profile": profile,
        "profile_path": profile_path,
        "target": target,
        "bundle": bundle,
        "manifest": manifest,
        "paths": paths,
        "cases": cases,
        "oracle": oracle,
        "response_schema": response_schema,
        "wrapper": wrapper,
    }


def make_preflight(profile_path: Path) -> dict[str, Any]:
    bound = validate_profile(profile_path)
    slots = [
        {"slot_id": f"{item['case_id']}-i001", "case_id": item["case_id"], "case_revision": "r1", "iteration": 1}
        for item in bound["cases"]["cases"]
    ]
    receipt = {
        "schema_version": "general-chat-response-preflight/v1",
        "receipt_id": "chat-control-free-core-r1-n1-preflight-r1",
        "target": {"path": str(TARGET_PATH.relative_to(ROOT)), "sha256": sha256_file(TARGET_PATH)},
        "registration": {"path": str(REGISTRATION_PATH.relative_to(ROOT)), "sha256": sha256_file(REGISTRATION_PATH)},
        "profile": {
            "path": str(bound["profile_path"].relative_to(ROOT)),
            "sha256": sha256_file(bound["profile_path"]),
            "profile_id": bound["profile"]["profile_id"],
        },
        "prompt_set_identity": bound["profile"]["prompt_set_identity"],
        "target_subject_ref": bound["profile"]["target_subject_ref"],
        "evaluation_set_ref": bound["profile"]["evaluation_set_ref"],
        "runtime_ref": bound["profile"]["runtime_ref"],
        "task_spec_ref": bound["profile"]["task_spec_ref"],
        "rating_ref": bound["profile"]["rating_ref"],
        "slots": slots,
        "authorized_slot_count": len(slots),
        "issued_slot_count": 0,
        "state": "ready_not_issued",
    }
    receipt["receipt_sha256"] = content_identity(receipt, "receipt_sha256")
    return receipt


def write_once(path: Path, value: dict[str, Any]) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
    except FileExistsError as error:
        raise QualificationError(f"refusing to overwrite artifact: {path}") from error


def projected_schema(schema: dict[str, Any]) -> dict[str, Any]:
    unsupported = {"$schema", "$id", "title", "minLength", "uniqueItems"}
    if isinstance(schema, dict):
        return {key: projected_schema(value) for key, value in schema.items() if key not in unsupported}
    if isinstance(schema, list):
        return [projected_schema(value) for value in schema]
    return schema


def parse_usage(stdout: bytes) -> tuple[str, int]:
    thread_ids: list[str] = []
    usages: list[dict[str, Any]] = []
    failures: list[str] = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("type") == "thread.started":
            thread_ids.append(event.get("thread_id"))
        elif event.get("type") == "turn.completed":
            usages.append(event.get("usage") or {})
        elif event.get("type") in {"error", "turn.failed"}:
            failures.append(event.get("type"))
    if failures or len(thread_ids) != 1 or len(usages) != 1:
        raise QualificationError("Codex JSONL terminal identity is incomplete")
    total = usages[0].get("total_tokens")
    if not isinstance(total, int) or total < 0:
        raise QualificationError("Codex usage.total_tokens is unavailable")
    return thread_ids[0], total


def grade(response: dict[str, Any], oracle: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    expected = oracle["expected"]
    arrays_exact = all(set(response[field]) == set(expected[field]) for field in ARRAY_FIELDS)
    message = response["assistant_message"]
    constraints = oracle["message_constraints"]
    missing_all = [value for value in constraints["required_all"] if value not in message]
    missing_any = [group for group in constraints["required_any"] if not any(value in message for value in group)]
    forbidden_present = [value for value in constraints["forbidden"] if value in message]
    major_hits = []
    for rule in oracle["major_violations"]:
        hits = sorted(set(response[rule["field"]]) & set(rule["ids"]))
        if hits:
            major_hits.append({"field": rule["field"], "ids": hits})
    message_passed = not missing_all and not missing_any and not forbidden_present
    if major_hits:
        score = 1
    elif arrays_exact and message_passed:
        score = 4
    elif arrays_exact:
        score = 3
    else:
        score = 2
    return score, {
        "arrays_exact": arrays_exact,
        "message_passed": message_passed,
        "missing_required_all": missing_all,
        "missing_required_any_groups": missing_any,
        "forbidden_present": forbidden_present,
        "major_violation_hits": major_hits,
        "mechanism_predicates": oracle["mechanism_predicates"],
    }


def run_slot(bound: dict[str, Any], case: dict[str, Any], oracle: dict[str, Any]) -> dict[str, Any]:
    runtime = bound["profile"]["runtime_ref"]
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="general-chat-eval-") as raw_workspace:
        workspace = Path(raw_workspace)
        (workspace / "AGENTS.md").write_bytes(b"")
        response_schema_path = workspace / "response-schema.json"
        response_schema_path.write_text(
            json.dumps(projected_schema(bound["response_schema"]), ensure_ascii=False), encoding="utf-8"
        )
        final_path = workspace / "final.json"
        prompt = bound["wrapper"].replace(
            "{{MODEL_PACKET_JSON}}", json.dumps(case, ensure_ascii=False, sort_keys=True, indent=2)
        )
        command = [
            "codex", "exec", "--skip-git-repo-check", "--cd", str(workspace),
            "--ignore-user-config", "--ignore-rules", "--strict-config", "--ephemeral",
            "--disable", "multi_agent", "--disable", "memories", "--disable", "apps",
            "--disable", "plugins", "--disable", "plugin_sharing",
            "-c", 'approval_policy="never"', "--model", runtime["model"],
            "-c", f'model_reasoning_effort="{runtime["reasoning_effort"]}"',
            "--sandbox", "read-only", "--output-schema", str(response_schema_path),
            "--json", "--output-last-message", str(final_path), "-",
        ]
        completed = subprocess.run(command, input=prompt.encode(), capture_output=True, check=False)
        elapsed = time.monotonic() - started
        if completed.returncode != 0:
            return {
                "slot_id": f"{case['case_id']}-i001",
                "case_id": case["case_id"],
                "case_revision": case["case_revision"],
                "iteration": 1,
                "status": "external_failure",
                "returncode": completed.returncode,
                "elapsed_seconds": round(elapsed, 6),
                "stderr_tail": completed.stderr.decode(errors="replace")[-1000:],
            }
        try:
            thread_id, total_tokens = parse_usage(completed.stdout)
            response = load_object(final_path)
            jsonschema.Draft202012Validator(bound["response_schema"]).validate(response)
            if response.get("case_id") != case["case_id"]:
                raise QualificationError("response case identity mismatch")
            score, diagnostics = grade(response, oracle)
        except (QualificationError, json.JSONDecodeError, jsonschema.ValidationError) as error:
            return {
                "slot_id": f"{case['case_id']}-i001",
                "case_id": case["case_id"],
                "case_revision": case["case_revision"],
                "iteration": 1,
                "status": "unrateable",
                "elapsed_seconds": round(elapsed, 6),
                "error": str(error),
            }
        return {
            "slot_id": f"{case['case_id']}-i001",
            "case_id": case["case_id"],
            "case_revision": case["case_revision"],
            "iteration": 1,
            "status": "valid",
            "quality_score": score,
            "all_agent_total_tokens": total_tokens,
            "elapsed_seconds": round(elapsed, 6),
            "root_thread_id": thread_id,
            "response": response,
            "diagnostics": diagnostics,
        }


def validate_preflight(path: Path, profile_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = load_object(path)
    if receipt.get("schema_version") != "general-chat-response-preflight/v1":
        raise QualificationError("preflight schema mismatch")
    if receipt.get("receipt_sha256") != content_identity(receipt, "receipt_sha256"):
        raise QualificationError("preflight receipt hash mismatch")
    if receipt.get("state") != "ready_not_issued" or receipt.get("issued_slot_count") != 0:
        raise QualificationError("preflight is not ready")
    expected = make_preflight(profile_path)
    if receipt != expected:
        raise QualificationError("preflight receipt is stale")
    return receipt, validate_profile(profile_path)


def execute(profile_path: Path, preflight_path: Path, dispatch_path: Path, result_path: Path) -> dict[str, Any]:
    receipt, bound = validate_preflight(preflight_path, profile_path)
    dispatch = {
        "schema_version": "general-chat-response-dispatch/v1",
        "dispatch_id": "chat-control-free-core-r1-n1-dispatch-r1",
        "preflight": {
            "path": str(preflight_path.resolve().relative_to(ROOT)),
            "sha256": sha256_file(preflight_path),
            "receipt_id": receipt["receipt_id"],
        },
        "slots": receipt["slots"],
        "issued_slot_count": len(receipt["slots"]),
        "state": "issued_once",
    }
    dispatch["dispatch_sha256"] = content_identity(dispatch, "dispatch_sha256")
    write_once(dispatch_path, dispatch)
    cases = {item["case_id"]: item for item in bound["cases"]["cases"]}
    oracles = {item["case_id"]: item for item in bound["oracle"]["cases"]}
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=24) as executor:
        futures = {
            executor.submit(run_slot, bound, cases[slot["case_id"]], oracles[slot["case_id"]]): slot
            for slot in receipt["slots"]
        }
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda item: item["slot_id"])
    valid = [row for row in rows if row["status"] == "valid"]
    result = {
        "schema_version": "general-chat-response-qualification-result/v1",
        "result_id": "chat-control-free-core-r1-n1-qualification-r1",
        "target_id": "general-chat-response-control",
        "profile": receipt["profile"],
        "preflight": dispatch["preflight"],
        "dispatch": {
            "path": str(dispatch_path.resolve().relative_to(ROOT)),
            "sha256": sha256_file(dispatch_path),
            "dispatch_id": dispatch["dispatch_id"],
        },
        "cases": rows,
        "summary": {
            "authorized_slots": len(rows),
            "valid_results": len(valid),
            "unrateable_results": sum(row["status"] == "unrateable" for row in rows),
            "external_failures": sum(row["status"] == "external_failure" for row in rows),
            "score_distribution": {
                str(score): sum(row.get("quality_score") == score for row in valid) for score in (1, 2, 3, 4)
            },
            "all_kpis_complete": len(valid) == len(rows) and all(
                isinstance(row.get("all_agent_total_tokens"), int)
                and isinstance(row.get("elapsed_seconds"), (int, float)) for row in valid
            ),
            "qualification_state": "measurement_established" if len(valid) == len(rows) else "measurement_not_established",
        },
        "lifecycle": {
            "evaluation": "qualification_n1_completed",
            "candidate": "not_created",
            "adoption": "not_decided",
            "release": "not_created",
            "projection": "not_authorized",
        },
    }
    result["result_sha256"] = content_identity(result, "result_sha256")
    write_once(result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    preflight_parser = subparsers.add_parser("preflight")
    preflight_parser.add_argument("--profile", type=Path, required=True)
    preflight_parser.add_argument("--output", type=Path, required=True)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--profile", type=Path, required=True)
    run_parser.add_argument("--preflight", type=Path, required=True)
    run_parser.add_argument("--dispatch-output", type=Path, required=True)
    run_parser.add_argument("--result-output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            receipt = make_preflight(args.profile)
            write_once(args.output, receipt)
            print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
        else:
            result = execute(args.profile, args.preflight, args.dispatch_output, args.result_output)
            print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
    except QualificationError as error:
        print(str(error), file=__import__("sys").stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
