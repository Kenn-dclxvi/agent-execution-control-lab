#!/usr/bin/env python3
"""Run the admitted ChatControlFree baseline at five iterations per fixed case."""

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


MODULE_PATH = Path(__file__).with_name("run_qualification_v4.py")
SPEC = importlib.util.spec_from_file_location("general_chat_qualification_r4", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load qualification runtime r4")
r4 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r4)
base = r4.base
r3 = r4.r3


REPETITION = {
    "iterations": 5,
    "order": "case_id_ascending_then_iteration_ascending",
    "valid_low_quality_policy": "retain",
    "external_failure_policy": "record_and_stop_before_comparison",
}


def validate_profile(profile_path: Path) -> dict[str, Any]:
    profile_path = profile_path.resolve()
    profile = base.load_object(profile_path)
    if profile.get("repetition_condition") != REPETITION:
        raise base.QualificationError("N=5 repetition condition mismatch")
    normalized = copy.deepcopy(profile)
    normalized["repetition_condition"] = {
        "iterations": 1,
        "order": "case_id_ascending",
        "valid_low_quality_policy": "retain",
        "external_failure_policy": "record_and_stop_before_comparison",
    }
    with tempfile.TemporaryDirectory(prefix="general-chat-profile-validation-") as raw_temp:
        normalized_path = Path(raw_temp) / "profile.json"
        normalized_path.write_text(json.dumps(normalized, ensure_ascii=False), encoding="utf-8")
        bound = base.validate_profile(normalized_path)
    bound["profile"] = profile
    bound["profile_path"] = profile_path
    adapter_path = base.verify_reference(profile.get("runtime_adapter_ref") or {}, "runtime adapter")
    if adapter_path != Path(__file__).resolve():
        raise base.QualificationError("runtime adapter path mismatch")
    accounting = (profile.get("runtime_ref") or {}).get("token_accounting") or {}
    if accounting.get("contract_id") != "codex-jsonl-single-agent-all-agent-total-r2":
        raise base.QualificationError("token accounting contract mismatch")
    return bound


def make_preflight(profile_path: Path) -> dict[str, Any]:
    bound = validate_profile(profile_path)
    slots = [
        {
            "slot_id": f"{item['case_id']}-i{iteration:03d}",
            "case_id": item["case_id"],
            "case_revision": item["case_revision"],
            "iteration": iteration,
        }
        for item in bound["cases"]["cases"]
        for iteration in range(1, 6)
    ]
    receipt = {
        "schema_version": "general-chat-response-preflight/v1",
        "receipt_id": "chat-control-free-core-r1-n5-preflight-r1",
        "reference_result": {
            "path": "evaluations/targets/general-chat-response-control/results/chat-control-free-core-r1-n1-qualification-r4.json",
            "sha256": base.sha256_file(
                base.ROOT / "evaluations/targets/general-chat-response-control/results/chat-control-free-core-r1-n1-qualification-r4.json"
            ),
            "qualification_state": "measurement_established",
        },
        "target": {"path": str(base.TARGET_PATH.relative_to(base.ROOT)), "sha256": base.sha256_file(base.TARGET_PATH)},
        "registration": {
            "path": str(base.REGISTRATION_PATH.relative_to(base.ROOT)),
            "sha256": base.sha256_file(base.REGISTRATION_PATH),
        },
        "profile": {
            "path": str(bound["profile_path"].relative_to(base.ROOT)),
            "sha256": base.sha256_file(bound["profile_path"]),
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
    receipt["receipt_sha256"] = base.content_identity(receipt, "receipt_sha256")
    return receipt


def run_slot(bound: dict[str, Any], case: dict[str, Any], oracle: dict[str, Any], iteration: int) -> dict[str, Any]:
    runtime = bound["profile"]["runtime_ref"]
    started = time.monotonic()
    host_codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve()
    host_auth = host_codex_home / "auth.json"
    if not host_auth.is_file():
        raise base.QualificationError("host Codex auth identity is unavailable")
    slot_id = f"{case['case_id']}-i{iteration:03d}"
    with tempfile.TemporaryDirectory(prefix="general-chat-eval-") as raw_workspace, tempfile.TemporaryDirectory(
        prefix="general-chat-codex-home-"
    ) as raw_codex_home:
        workspace = Path(raw_workspace)
        codex_home = Path(raw_codex_home)
        os.symlink(host_auth, codex_home / "auth.json")
        (workspace / "AGENTS.md").write_bytes(b"")
        response_schema_path = workspace / "response-schema.json"
        response_schema_path.write_text(
            json.dumps(r3.api_schema(bound["response_schema"]), ensure_ascii=False), encoding="utf-8"
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
        environment = dict(os.environ)
        environment["CODEX_HOME"] = str(codex_home)
        completed = subprocess.run(command, input=prompt.encode(), capture_output=True, check=False, env=environment)
        elapsed = round(time.monotonic() - started, 6)
        if completed.returncode != 0:
            return {
                "slot_id": slot_id, "case_id": case["case_id"], "case_revision": case["case_revision"],
                "iteration": iteration, "status": "external_failure", "returncode": completed.returncode,
                "elapsed_seconds": elapsed, "stdout_sha256": hashlib.sha256(completed.stdout).hexdigest(),
                "stderr_tail": completed.stderr.decode(errors="replace")[-1000:],
            }
        try:
            thread_id, total_tokens = r4.parse_usage(completed.stdout)
            response = base.load_object(final_path)
            jsonschema.Draft202012Validator(bound["response_schema"]).validate(response)
            if response.get("case_id") != case["case_id"]:
                raise base.QualificationError("response case identity mismatch")
            score, diagnostics = base.grade(response, oracle)
        except (base.QualificationError, json.JSONDecodeError, jsonschema.ValidationError) as error:
            return {
                "slot_id": slot_id, "case_id": case["case_id"], "case_revision": case["case_revision"],
                "iteration": iteration, "status": "unrateable", "elapsed_seconds": elapsed, "error": str(error),
            }
        return {
            "slot_id": slot_id, "case_id": case["case_id"], "case_revision": case["case_revision"],
            "iteration": iteration, "status": "valid", "quality_score": score,
            "all_agent_total_tokens": total_tokens, "elapsed_seconds": elapsed, "root_thread_id": thread_id,
            "response": response, "diagnostics": diagnostics,
        }


def validate_preflight(path: Path, profile_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    receipt = base.load_object(path)
    if receipt.get("receipt_sha256") != base.content_identity(receipt, "receipt_sha256"):
        raise base.QualificationError("preflight receipt hash mismatch")
    if receipt.get("state") != "ready_not_issued" or receipt.get("issued_slot_count") != 0:
        raise base.QualificationError("preflight is not ready")
    expected = make_preflight(profile_path)
    if receipt != expected:
        raise base.QualificationError("preflight receipt is stale")
    return receipt, validate_profile(profile_path)


def execute(profile_path: Path, preflight_path: Path, dispatch_path: Path, result_path: Path) -> dict[str, Any]:
    receipt, bound = validate_preflight(preflight_path, profile_path)
    dispatch = {
        "schema_version": "general-chat-response-dispatch/v1",
        "dispatch_id": "chat-control-free-core-r1-n5-dispatch-r1",
        "preflight": {"path": str(preflight_path.resolve().relative_to(base.ROOT)), "sha256": base.sha256_file(preflight_path), "receipt_id": receipt["receipt_id"]},
        "slots": receipt["slots"], "issued_slot_count": len(receipt["slots"]), "state": "issued_once",
    }
    dispatch["dispatch_sha256"] = base.content_identity(dispatch, "dispatch_sha256")
    base.write_once(dispatch_path, dispatch)
    cases = {item["case_id"]: item for item in bound["cases"]["cases"]}
    oracles = {item["case_id"]: item for item in bound["oracle"]["cases"]}
    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=24) as executor:
        futures = {
            executor.submit(run_slot, bound, cases[slot["case_id"]], oracles[slot["case_id"]], slot["iteration"]): slot
            for slot in receipt["slots"]
        }
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda item: item["slot_id"])
    valid = [row for row in rows if row["status"] == "valid"]
    result = {
        "schema_version": "general-chat-response-baseline-result/v1",
        "result_id": "chat-control-free-core-r1-n5-baseline-r1",
        "target_id": "general-chat-response-control",
        "profile": receipt["profile"], "reference_result": receipt["reference_result"],
        "preflight": dispatch["preflight"],
        "dispatch": {"path": str(dispatch_path.resolve().relative_to(base.ROOT)), "sha256": base.sha256_file(dispatch_path), "dispatch_id": dispatch["dispatch_id"]},
        "cases": rows,
        "summary": {
            "authorized_slots": len(rows), "valid_results": len(valid),
            "unrateable_results": sum(row["status"] == "unrateable" for row in rows),
            "external_failures": sum(row["status"] == "external_failure" for row in rows),
            "score_distribution": {str(score): sum(row.get("quality_score") == score for row in valid) for score in (1, 2, 3, 4)},
            "all_kpis_complete": len(valid) == len(rows) and all(isinstance(row.get("all_agent_total_tokens"), int) and isinstance(row.get("elapsed_seconds"), (int, float)) for row in valid),
            "baseline_state": "measured" if len(valid) == len(rows) else "measurement_not_established",
        },
        "lifecycle": {"evaluation": "baseline_n5_completed", "candidate": "not_created", "adoption": "not_decided", "release": "not_created", "projection": "not_authorized"},
    }
    result["result_sha256"] = base.content_identity(result, "result_sha256")
    base.write_once(result_path, result)
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
            base.write_once(args.output, receipt)
            print(json.dumps({"receipt_id": receipt["receipt_id"], "authorized_slot_count": receipt["authorized_slot_count"], "state": receipt["state"]}, ensure_ascii=False, sort_keys=True))
        else:
            result = execute(args.profile, args.preflight, args.dispatch_output, args.result_output)
            print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
    except base.QualificationError as error:
        print(str(error), file=__import__("sys").stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
