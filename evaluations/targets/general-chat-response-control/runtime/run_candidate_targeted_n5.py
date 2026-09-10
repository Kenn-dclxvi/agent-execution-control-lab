#!/usr/bin/env python3
"""Evaluate RequiredValueCarrier r1 on the one observed failing case at N=5."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
from typing import Any

import jsonschema


MODULE_PATH = Path(__file__).with_name("run_baseline_n5.py")
SPEC = importlib.util.spec_from_file_location("general_chat_baseline_n5", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load baseline N=5 runtime")
n5 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(n5)
base, r4, r3 = n5.base, n5.r4, n5.r3

CANDIDATE_PATH = base.ROOT / "evaluations/targets/general-chat-response-control/prompts/candidates/required-value-carrier-r1"
BASELINE_PROMPT = {
    "name": "chat-control-free-r1",
    "revision": "r1",
    "bundle_sha256": "7806831a2dae4e9c4debdd6d8316c12a76699012992cf8360f756da87e1797a9",
    "path": "evaluations/targets/general-chat-response-control/prompts/baselines/chat-control-free-r1",
}


def verify_candidate() -> tuple[dict[str, Any], bytes]:
    manifest = base.load_object(CANDIDATE_PATH / "manifest.json")
    instruction = (CANDIDATE_PATH / "files/AGENTS.md.txt").read_bytes()
    if manifest.get("prompt_identity") != "required-value-carrier-r1":
        raise base.QualificationError("candidate identity mismatch")
    entries = manifest.get("files")
    if entries != [{
        "git_blob_sha1": "78201bc86e9d94b9fa0aaead34881b0d32bf12fa",
        "mode": "100644",
        "sha256": hashlib.sha256(instruction).hexdigest(),
        "target": "AGENTS.md",
        "type": "file",
    }]:
        raise base.QualificationError("candidate file identity mismatch")
    identity = {"files": entries, "schema_version": manifest.get("schema_version")}
    if hashlib.sha256(json.dumps(identity, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest() != manifest.get("bundle_sha256"):
        raise base.QualificationError("candidate bundle hash mismatch")
    return manifest, instruction


def validate_profile(profile_path: Path) -> dict[str, Any]:
    profile_path = profile_path.resolve()
    profile = base.load_object(profile_path)
    manifest, instruction = verify_candidate()
    prompt = profile.get("prompt_set_identity") or {}
    if prompt.get("name") != manifest.get("prompt_identity") or prompt.get("bundle_sha256") != manifest.get("bundle_sha256"):
        raise base.QualificationError("candidate profile identity mismatch")
    normalized = copy.deepcopy(profile)
    normalized["prompt_set_identity"] = BASELINE_PROMPT
    normalized["repetition_condition"] = {
        "iterations": 1,
        "order": "case_id_ascending",
        "valid_low_quality_policy": "retain",
        "external_failure_policy": "record_and_stop_before_comparison",
    }
    with tempfile.TemporaryDirectory(prefix="general-chat-candidate-profile-") as raw_temp:
        normalized_path = Path(raw_temp) / "profile.json"
        normalized_path.write_text(json.dumps(normalized, ensure_ascii=False), encoding="utf-8")
        bound = base.validate_profile(normalized_path)
    bound["profile"], bound["profile_path"] = profile, profile_path
    bound["candidate_instruction"] = instruction
    adapter_path = base.verify_reference(profile.get("runtime_adapter_ref") or {}, "runtime adapter")
    if adapter_path != Path(__file__).resolve():
        raise base.QualificationError("runtime adapter path mismatch")
    return bound


def make_preflight(profile_path: Path) -> dict[str, Any]:
    bound = validate_profile(profile_path)
    case = next(item for item in bound["cases"]["cases"] if item["case_id"] == "GCR-Q02")
    slots = [{"slot_id": f"GCR-Q02-i{i:03d}", "case_id": "GCR-Q02", "case_revision": case["case_revision"], "iteration": i} for i in range(1, 6)]
    reference_path = base.ROOT / "evaluations/targets/general-chat-response-control/results/chat-control-free-core-r1-n5-baseline-r1.json"
    receipt = {
        "schema_version": "general-chat-response-preflight/v1",
        "receipt_id": "required-value-carrier-core-r1-q02-n5-preflight-r1",
        "reference_result": {"path": str(reference_path.relative_to(base.ROOT)), "sha256": base.sha256_file(reference_path), "baseline_state": "measured"},
        "target": {"path": str(base.TARGET_PATH.relative_to(base.ROOT)), "sha256": base.sha256_file(base.TARGET_PATH)},
        "registration": {"path": str(base.REGISTRATION_PATH.relative_to(base.ROOT)), "sha256": base.sha256_file(base.REGISTRATION_PATH)},
        "profile": {"path": str(bound["profile_path"].relative_to(base.ROOT)), "sha256": base.sha256_file(bound["profile_path"]), "profile_id": bound["profile"]["profile_id"]},
        "prompt_set_identity": bound["profile"]["prompt_set_identity"],
        "target_subject_ref": bound["profile"]["target_subject_ref"],
        "evaluation_set_ref": bound["profile"]["evaluation_set_ref"],
        "runtime_ref": bound["profile"]["runtime_ref"],
        "task_spec_ref": bound["profile"]["task_spec_ref"],
        "rating_ref": bound["profile"]["rating_ref"],
        "allowed_delta": "prompt_set_identity only",
        "slots": slots, "authorized_slot_count": 5, "issued_slot_count": 0, "state": "ready_not_issued",
    }
    receipt["receipt_sha256"] = base.content_identity(receipt, "receipt_sha256")
    return receipt


def run_slot(bound: dict[str, Any], case: dict[str, Any], oracle: dict[str, Any], iteration: int) -> dict[str, Any]:
    runtime = bound["profile"]["runtime_ref"]
    started = time.monotonic()
    host_auth = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve() / "auth.json"
    slot_id = f"{case['case_id']}-i{iteration:03d}"
    with tempfile.TemporaryDirectory(prefix="general-chat-eval-") as raw_workspace, tempfile.TemporaryDirectory(prefix="general-chat-codex-home-") as raw_home:
        workspace, codex_home = Path(raw_workspace), Path(raw_home)
        os.symlink(host_auth, codex_home / "auth.json")
        (workspace / "AGENTS.md").write_bytes(bound["candidate_instruction"])
        schema_path = workspace / "response-schema.json"
        schema_path.write_text(json.dumps(r3.api_schema(bound["response_schema"]), ensure_ascii=False), encoding="utf-8")
        final_path = workspace / "final.json"
        prompt = bound["wrapper"].replace("{{MODEL_PACKET_JSON}}", json.dumps(case, ensure_ascii=False, sort_keys=True, indent=2))
        command = ["codex", "exec", "--skip-git-repo-check", "--cd", str(workspace), "--ignore-user-config", "--ignore-rules", "--strict-config", "--ephemeral", "--disable", "multi_agent", "--disable", "memories", "--disable", "apps", "--disable", "plugins", "--disable", "plugin_sharing", "-c", 'approval_policy="never"', "--model", runtime["model"], "-c", f'model_reasoning_effort="{runtime["reasoning_effort"]}"', "--sandbox", "read-only", "--output-schema", str(schema_path), "--json", "--output-last-message", str(final_path), "-"]
        environment = dict(os.environ); environment["CODEX_HOME"] = str(codex_home)
        completed = subprocess.run(command, input=prompt.encode(), capture_output=True, check=False, env=environment)
        elapsed = round(time.monotonic() - started, 6)
        if completed.returncode != 0:
            return {"slot_id": slot_id, "case_id": case["case_id"], "case_revision": case["case_revision"], "iteration": iteration, "status": "external_failure", "returncode": completed.returncode, "elapsed_seconds": elapsed, "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(), "stderr_tail": completed.stderr.decode(errors="replace")[-1000:]}
        try:
            thread_id, total_tokens = r4.parse_usage(completed.stdout)
            response = base.load_object(final_path)
            jsonschema.Draft202012Validator(bound["response_schema"]).validate(response)
            if response.get("case_id") != case["case_id"]: raise base.QualificationError("response case identity mismatch")
            score, diagnostics = base.grade(response, oracle)
        except (base.QualificationError, json.JSONDecodeError, jsonschema.ValidationError) as error:
            return {"slot_id": slot_id, "case_id": case["case_id"], "case_revision": case["case_revision"], "iteration": iteration, "status": "unrateable", "elapsed_seconds": elapsed, "error": str(error)}
        return {"slot_id": slot_id, "case_id": case["case_id"], "case_revision": case["case_revision"], "iteration": iteration, "status": "valid", "quality_score": score, "all_agent_total_tokens": total_tokens, "elapsed_seconds": elapsed, "root_thread_id": thread_id, "response": response, "diagnostics": diagnostics}


def validate_preflight(path: Path, profile_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = base.load_object(path)
    if receipt.get("receipt_sha256") != base.content_identity(receipt, "receipt_sha256") or receipt.get("state") != "ready_not_issued" or receipt.get("issued_slot_count") != 0:
        raise base.QualificationError("preflight is invalid")
    expected = make_preflight(profile_path)
    if receipt != expected: raise base.QualificationError("preflight receipt is stale")
    return receipt, validate_profile(profile_path)


def execute(profile_path: Path, preflight_path: Path, dispatch_path: Path, result_path: Path) -> dict[str, Any]:
    receipt, bound = validate_preflight(preflight_path, profile_path)
    dispatch = {"schema_version": "general-chat-response-dispatch/v1", "dispatch_id": "required-value-carrier-core-r1-q02-n5-dispatch-r1", "preflight": {"path": str(preflight_path.resolve().relative_to(base.ROOT)), "sha256": base.sha256_file(preflight_path), "receipt_id": receipt["receipt_id"]}, "slots": receipt["slots"], "issued_slot_count": 5, "state": "issued_once"}
    dispatch["dispatch_sha256"] = base.content_identity(dispatch, "dispatch_sha256"); base.write_once(dispatch_path, dispatch)
    case = next(item for item in bound["cases"]["cases"] if item["case_id"] == "GCR-Q02")
    oracle = next(item for item in bound["oracle"]["cases"] if item["case_id"] == "GCR-Q02")
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(run_slot, bound, case, oracle, i) for i in range(1, 6)]
        for future in as_completed(futures): rows.append(future.result())
    rows.sort(key=lambda item: item["slot_id"]); valid = [row for row in rows if row["status"] == "valid"]
    gate_passed = len(valid) == 5 and all(row["quality_score"] == 4 and not row["response"]["clarification_value_ids"] and not row["response"]["request_evidence_ids"] and not row["response"]["unresolved_topic_ids"] for row in valid)
    result = {"schema_version": "general-chat-response-candidate-result/v1", "result_id": "required-value-carrier-core-r1-q02-n5-r1", "target_id": "general-chat-response-control", "profile": receipt["profile"], "reference_result": receipt["reference_result"], "preflight": dispatch["preflight"], "dispatch": {"path": str(dispatch_path.resolve().relative_to(base.ROOT)), "sha256": base.sha256_file(dispatch_path), "dispatch_id": dispatch["dispatch_id"]}, "cases": rows, "summary": {"authorized_slots": 5, "valid_results": len(valid), "unrateable_results": sum(row["status"] == "unrateable" for row in rows), "external_failures": sum(row["status"] == "external_failure" for row in rows), "score_distribution": {str(score): sum(row.get("quality_score") == score for row in valid) for score in (1,2,3,4)}, "targeted_gate_passed": gate_passed}, "lifecycle": {"evaluation": "targeted_n5_completed", "candidate": "evaluated" if len(valid) == 5 else "measurement_not_established", "adoption": "not_decided", "release": "not_created", "projection": "not_authorized"}}
    result["result_sha256"] = base.content_identity(result, "result_sha256"); base.write_once(result_path, result); return result


def main() -> int:
    parser = argparse.ArgumentParser(); subs = parser.add_subparsers(dest="command", required=True)
    pre = subs.add_parser("preflight"); pre.add_argument("--profile", type=Path, required=True); pre.add_argument("--output", type=Path, required=True)
    run = subs.add_parser("run"); run.add_argument("--profile", type=Path, required=True); run.add_argument("--preflight", type=Path, required=True); run.add_argument("--dispatch-output", type=Path, required=True); run.add_argument("--result-output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            receipt = make_preflight(args.profile); base.write_once(args.output, receipt); print(json.dumps({"authorized_slot_count": 5, "state": receipt["state"]}, sort_keys=True))
        else:
            result = execute(args.profile, args.preflight, args.dispatch_output, args.result_output); print(json.dumps(result["summary"], sort_keys=True))
    except base.QualificationError as error:
        print(str(error), file=__import__("sys").stderr); return 1
    return 0


if __name__ == "__main__": raise SystemExit(main())
