#!/usr/bin/env python3
"""Qualification runtime r3 with isolated state and API-compatible schema projection."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
from typing import Any

import jsonschema


MODULE_PATH = Path(__file__).with_name("run_qualification_v2.py")
SPEC = importlib.util.spec_from_file_location("general_chat_qualification_r2", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load qualification runtime r2")
r2 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(r2)
base = r2.base


def api_schema(schema: Any) -> Any:
    """Project canonical JSON Schema to the response-format subset without changing its meaning."""
    unsupported = {"$schema", "$id", "title", "minLength", "uniqueItems"}
    if isinstance(schema, dict):
        projected = {key: api_schema(value) for key, value in schema.items() if key not in unsupported}
        if "const" in projected and "type" not in projected:
            value = projected["const"]
            inferred = (
                "boolean" if isinstance(value, bool)
                else "integer" if isinstance(value, int)
                else "number" if isinstance(value, float)
                else "string" if isinstance(value, str)
                else "array" if isinstance(value, list)
                else "object" if isinstance(value, dict)
                else "null"
            )
            projected["type"] = inferred
        return projected
    if isinstance(schema, list):
        return [api_schema(value) for value in schema]
    return schema


def validate_profile(profile_path: Path) -> dict[str, Any]:
    bound = base.validate_profile(profile_path)
    adapter_path = base.verify_reference(bound["profile"].get("runtime_adapter_ref") or {}, "runtime adapter")
    if adapter_path != Path(__file__).resolve():
        raise base.QualificationError("runtime adapter path mismatch")
    isolation = (bound["profile"].get("runtime_ref") or {}).get("runtime_state_isolation")
    if isolation != {
        "codex_home": "per_slot_temporary",
        "auth_transport": "host_auth_symlink_not_persisted",
        "skills_cache": "not_shared",
        "models_cache": "not_shared",
    }:
        raise base.QualificationError("runtime state isolation contract mismatch")
    return bound


def make_preflight(profile_path: Path) -> dict[str, Any]:
    validate_profile(profile_path)
    receipt = base.make_preflight(profile_path)
    receipt["receipt_id"] = "chat-control-free-core-r1-n1-preflight-r3"
    receipt["receipt_sha256"] = base.content_identity(receipt, "receipt_sha256")
    return receipt


def run_slot(bound: dict[str, Any], case: dict[str, Any], oracle: dict[str, Any]) -> dict[str, Any]:
    runtime = bound["profile"]["runtime_ref"]
    started = time.monotonic()
    host_codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve()
    host_auth = host_codex_home / "auth.json"
    if not host_auth.is_file():
        raise base.QualificationError("host Codex auth identity is unavailable")
    with tempfile.TemporaryDirectory(prefix="general-chat-eval-") as raw_workspace, tempfile.TemporaryDirectory(
        prefix="general-chat-codex-home-"
    ) as raw_codex_home:
        workspace = Path(raw_workspace)
        codex_home = Path(raw_codex_home)
        os.symlink(host_auth, codex_home / "auth.json")
        (workspace / "AGENTS.md").write_bytes(b"")
        response_schema_path = workspace / "response-schema.json"
        response_schema_path.write_text(json.dumps(api_schema(bound["response_schema"]), ensure_ascii=False), encoding="utf-8")
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
        elapsed = time.monotonic() - started
        if completed.returncode != 0:
            diagnostics = r2.__dict__.get("parse_jsonl_diagnostics")
            return {
                "slot_id": f"{case['case_id']}-i001",
                "case_id": case["case_id"],
                "case_revision": case["case_revision"],
                "iteration": 1,
                "status": "external_failure",
                "returncode": completed.returncode,
                "elapsed_seconds": round(elapsed, 6),
                "stdout_sha256": base.hashlib.sha256(completed.stdout).hexdigest(),
                "stderr_tail": completed.stderr.decode(errors="replace")[-1000:],
                **({"diagnostics": diagnostics(completed.stdout)} if diagnostics else {}),
            }
        try:
            thread_id, total_tokens = base.parse_usage(completed.stdout)
            response = base.load_object(final_path)
            jsonschema.Draft202012Validator(bound["response_schema"]).validate(response)
            if response.get("case_id") != case["case_id"]:
                raise base.QualificationError("response case identity mismatch")
            score, diagnostics = base.grade(response, oracle)
        except (base.QualificationError, json.JSONDecodeError, jsonschema.ValidationError) as error:
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
    receipt = base.load_object(path)
    if receipt.get("schema_version") != "general-chat-response-preflight/v1":
        raise base.QualificationError("preflight schema mismatch")
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
        "dispatch_id": "chat-control-free-core-r1-n1-dispatch-r3",
        "preflight": {
            "path": str(preflight_path.resolve().relative_to(base.ROOT)),
            "sha256": base.sha256_file(preflight_path),
            "receipt_id": receipt["receipt_id"],
        },
        "slots": receipt["slots"],
        "issued_slot_count": len(receipt["slots"]),
        "state": "issued_once",
    }
    dispatch["dispatch_sha256"] = base.content_identity(dispatch, "dispatch_sha256")
    base.write_once(dispatch_path, dispatch)
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
        "result_id": "chat-control-free-core-r1-n1-qualification-r3",
        "target_id": "general-chat-response-control",
        "profile": receipt["profile"],
        "preflight": dispatch["preflight"],
        "dispatch": {
            "path": str(dispatch_path.resolve().relative_to(base.ROOT)),
            "sha256": base.sha256_file(dispatch_path),
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
            print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
        else:
            result = execute(args.profile, args.preflight, args.dispatch_output, args.result_output)
            print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
    except base.QualificationError as error:
        print(str(error), file=__import__("sys").stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
