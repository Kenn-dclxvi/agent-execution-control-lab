#!/usr/bin/env python3
"""Prepare and execute the fixed non-member AI panel adjudicator."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[4]
TARGET = ROOT / "evaluations/targets/general-chat-response-control"
PANEL_PATH = TARGET / "calibration/ai-grader-panel-r1.json"
CALIBRATION_PATH = TARGET / "calibration/calibration-input-core-r1.json"
CASES_PATH = TARGET / "cases/core-r1/input-cases.json"
PROMPT_PATH = TARGET / "rating-contracts/general-chat-semantic-panel-adjudicator-r1.txt"
CANONICAL_SCHEMA_PATH = TARGET / "calibration/ai-panel-adjudication-r1.schema.json"
PREFLIGHT_SCHEMA_PATH = TARGET / "calibration/ai-adjudicator-run-preflight-r1.schema.json"
RESULT_SCHEMA_PATH = TARGET / "calibration/ai-adjudicator-run-result-r1.schema.json"
RUNNER_PATH = Path(__file__).resolve()
RUNTIME_VERSION = "0.148.0"

PANEL_RUNNER_PATH = Path(__file__).with_name("run_ai_grader_panel.py")
SPEC = importlib.util.spec_from_file_location("general_chat_ai_panel_runner", PANEL_RUNNER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("cannot load AI panel runner")
panel_runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(panel_runtime)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.codex_runtime_binding import (  # noqa: E402
    CodexRuntimeBindingError,
    resolve_fixed_codex_runtime,
    verify_codex_runtime_binding,
)


class AdjudicatorRunError(RuntimeError):
    """The fixed adjudication cannot proceed without contract drift."""


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise AdjudicatorRunError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise AdjudicatorRunError(f"expected JSON object: {path}")
    return value


def _repo_ref(path: Path) -> dict[str, str]:
    resolved = path.resolve()
    return {
        "path": str(resolved.relative_to(ROOT)),
        "sha256": panel_runtime.sha256_file(resolved),
    }


def _external_ref(path: Path) -> dict[str, str]:
    resolved = path.resolve()
    if not resolved.is_file():
        raise AdjudicatorRunError(f"external file is unavailable: {resolved}")
    return {"path": str(resolved), "sha256": panel_runtime.sha256_file(resolved)}


def _external_root(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        return resolved
    raise AdjudicatorRunError("run root must be outside the repository")


def _find_panel_rating(
    recovery: dict[str, Any], calibration_item_id: str, assertion_id: str
) -> list[dict[str, Any]]:
    ratings: list[dict[str, Any]] = []
    for slot in recovery["slots"]:
        label = _load(Path(slot["label"]["path"]))
        run_root = Path(recovery["source_run"]["path"]).parent
        map_path = (
            run_root
            / "material"
            / slot["grader_execution_id"]
            / "organizer-map.json"
        )
        organizer_map = _load(map_path)
        opaque = next(
            item["rating_item_id"]
            for item in organizer_map["mappings"]
            if item["calibration_item_id"] == calibration_item_id
        )
        row = next(
            item
            for item in label["labels"]
            if item["rating_item_id"] == opaque and item["assertion_id"] == assertion_id
        )
        ratings.append(
            {
                "grader_execution_id": slot["grader_execution_id"],
                "label": row["label"],
                "evidence_spans": row["evidence_spans"],
                "reason": row["reason"],
            }
        )
    if len(ratings) != 3:
        raise AdjudicatorRunError("disagreement does not have three fixed ratings")
    return ratings


def _make_packet(recovery_path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    recovery = _load(recovery_path)
    jsonschema.Draft202012Validator(
        _load(panel_runtime.RECOVERY_RESULT_SCHEMA_PATH)
    ).validate(recovery)
    if recovery["result_sha256"] != panel_runtime.content_identity(
        recovery, "result_sha256"
    ):
        raise AdjudicatorRunError("recovery result hash mismatch")
    report_path = Path(recovery["pilot_report"]["path"])
    if _external_ref(report_path) != recovery["pilot_report"]:
        raise AdjudicatorRunError("pilot report drifted")
    report = _load(report_path)
    disagreements = report["disagreements"]
    if report["reference_state"] != "ai_adjudication_required" or len(disagreements) != 1:
        raise AdjudicatorRunError("pilot report is not the fixed one-item disagreement")
    disagreement = disagreements[0]
    calibration = _load(CALIBRATION_PATH)
    cases = _load(CASES_PATH)
    source_item = next(
        item
        for item in calibration["items"]
        if item["calibration_item_id"] == disagreement["calibration_item_id"]
    )
    case = next(item for item in cases["cases"] if item["case_id"] == source_item["case_id"])
    assertion = next(
        item
        for item in source_item["assertions"]
        if item["assertion_id"] == disagreement["assertion_id"]
    )
    panel = _load(PANEL_PATH)
    adjudicator = panel["adjudicator"]
    packet = {
        "schema_version": "general-chat-ai-adjudication-packet/v1",
        "calibration_set_id": report["calibration_set_id"],
        "panel_report_sha256": panel_runtime.sha256_file(report_path),
        "adjudicator_identity": adjudicator["grader_execution_id"],
        "panel_member": False,
        "items": [
            {
                "calibration_item_id": source_item["calibration_item_id"],
                "conversation": case["conversation"],
                "available_evidence": case["available_evidence"],
                "received_evidence": case["received_evidence"],
                "assistant_message": source_item["assistant_message"],
                "assertion": assertion,
                "panel_ratings": _find_panel_rating(
                    recovery, source_item["calibration_item_id"], assertion["assertion_id"]
                ),
            }
        ],
    }
    output_identity = {
        "schema_version": "general-chat-ai-panel-adjudication/v1",
        "calibration_set_id": report["calibration_set_id"],
        "panel_report_sha256": packet["panel_report_sha256"],
        "adjudicator_identity": adjudicator["grader_execution_id"],
        "panel_member": False,
        "reference_type": "multi_grader_consensus_reference",
        "human_alignment_state": "unmeasured",
        "qualification_effect": "none",
    }
    return packet, output_identity


def make_preflight(run_root: Path, recovery_path: Path) -> dict[str, Any]:
    run_root = _external_root(run_root)
    if run_root.exists() and any(run_root.iterdir()):
        raise AdjudicatorRunError("preflight run root must be absent or empty")
    run_root.mkdir(parents=True, exist_ok=True)
    panel = _load(PANEL_PATH)
    adjudicator = panel["adjudicator"]
    if adjudicator["prompt_sha256"] != panel_runtime.sha256_file(PROMPT_PATH):
        raise AdjudicatorRunError("adjudicator prompt hash mismatch")
    if adjudicator["schema_sha256"] != panel_runtime.sha256_file(CANONICAL_SCHEMA_PATH):
        raise AdjudicatorRunError("adjudicator schema hash mismatch")
    try:
        binding = resolve_fixed_codex_runtime(RUNTIME_VERSION)
        verify_codex_runtime_binding(binding)
    except CodexRuntimeBindingError as error:
        raise AdjudicatorRunError(str(error)) from error
    packet, output_identity = _make_packet(recovery_path.resolve())
    transport_schema = panel_runtime.project_transport_schema(_load(CANONICAL_SCHEMA_PATH))
    panel_runtime.validate_transport_schema(transport_schema)
    stdin = (
        PROMPT_PATH.read_text(encoding="utf-8").rstrip()
        + "\n\n以下の固定packetにある不一致だけを裁定してください。\n"
        + json.dumps(
            {"packet": packet, "required_output_identity": output_identity},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")
    material = run_root / "material"
    packet_path = material / "packet.json"
    schema_path = material / "transport-schema.json"
    stdin_path = material / "stdin.txt"
    panel_runtime.write_once(packet_path, packet)
    panel_runtime.write_once(schema_path, transport_schema)
    panel_runtime.write_bytes_once(stdin_path, stdin)
    receipt = {
        "schema_version": "general-chat-ai-adjudicator-run-preflight/v1",
        "receipt_id": "general-chat-semantic-pilot-adjudication-r1-preflight-r1",
        "state": "ready_not_issued",
        "issued_slot_count": 0,
        "runtime_binding": binding,
        "adjudicator": {
            "grader_execution_id": adjudicator["grader_execution_id"],
            "model": adjudicator["model"],
            "reasoning_effort": adjudicator["reasoning_effort"],
        },
        "fixed_sources": {
            "panel": _repo_ref(PANEL_PATH),
            "calibration": _repo_ref(CALIBRATION_PATH),
            "cases": _repo_ref(CASES_PATH),
            "prompt": _repo_ref(PROMPT_PATH),
            "canonical_schema": _repo_ref(CANONICAL_SCHEMA_PATH),
            "preflight_schema": _repo_ref(PREFLIGHT_SCHEMA_PATH),
            "result_schema": _repo_ref(RESULT_SCHEMA_PATH),
            "runner": _repo_ref(RUNNER_PATH),
            "panel_runner": _repo_ref(PANEL_RUNNER_PATH),
            "recovery_result": _external_ref(recovery_path.resolve()),
        },
        "storage": {"run_root": str(run_root), "repository_external": True},
        "material": {
            "packet": _external_ref(packet_path),
            "transport_schema": _external_ref(schema_path),
            "stdin": _external_ref(stdin_path),
        },
    }
    receipt["receipt_sha256"] = panel_runtime.content_identity(receipt, "receipt_sha256")
    jsonschema.Draft202012Validator(_load(PREFLIGHT_SCHEMA_PATH)).validate(receipt)
    panel_runtime.write_once(run_root / "preflight.json", receipt)
    return receipt


def validate_preflight(path: Path) -> dict[str, Any]:
    receipt = _load(path.resolve())
    jsonschema.Draft202012Validator(_load(PREFLIGHT_SCHEMA_PATH)).validate(receipt)
    if receipt["receipt_sha256"] != panel_runtime.content_identity(receipt, "receipt_sha256"):
        raise AdjudicatorRunError("preflight receipt hash mismatch")
    if Path(receipt["storage"]["run_root"]).resolve() != path.resolve().parent:
        raise AdjudicatorRunError("preflight run root mismatch")
    for reference in receipt["fixed_sources"].values():
        resolved = Path(reference["path"])
        if not resolved.is_absolute():
            resolved = ROOT / resolved
        if _external_ref(resolved) != {"path": str(resolved.resolve()), "sha256": reference["sha256"]}:
            raise AdjudicatorRunError("preflight fixed source drifted")
    for reference in receipt["material"].values():
        if _external_ref(Path(reference["path"])) != reference:
            raise AdjudicatorRunError("preflight material drifted")
    try:
        verify_codex_runtime_binding(receipt["runtime_binding"])
    except CodexRuntimeBindingError as error:
        raise AdjudicatorRunError(str(error)) from error
    return receipt


def execute(path: Path) -> dict[str, Any]:
    receipt = validate_preflight(path)
    run_root = Path(receipt["storage"]["run_root"])
    issued_path = run_root / "issued.json"
    result_path = run_root / "run-result.json"
    if issued_path.exists() or result_path.exists() or (run_root / "output").exists():
        raise AdjudicatorRunError("adjudicator was already issued")
    issued = {
        "dispatch_id": "general-chat-semantic-pilot-adjudication-r1-dispatch-r1",
        "preflight_sha256": panel_runtime.sha256_file(path),
        "issued_slot_count": 1,
        "state": "issued_once",
    }
    issued["dispatch_sha256"] = panel_runtime.content_identity(issued, "dispatch_sha256")
    panel_runtime.write_once(issued_path, issued)
    output_dir = run_root / "output"
    output_dir.mkdir()
    stdout_path = output_dir / "stdout.jsonl"
    stderr_path = output_dir / "stderr.log"
    adjudication_path = output_dir / "adjudication.json"
    host_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve()
    host_auth = host_home / "auth.json"
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="general-chat-adjudicator-workspace-") as raw_workspace, tempfile.TemporaryDirectory(prefix="general-chat-adjudicator-home-") as raw_home:
        workspace = Path(raw_workspace)
        codex_home = Path(raw_home)
        os.symlink(host_auth, codex_home / "auth.json")
        (workspace / "AGENTS.md").write_bytes(b"")
        final_path = workspace / "final.json"
        adjudicator = receipt["adjudicator"]
        command = [
            receipt["runtime_binding"]["executable"], "exec", "--skip-git-repo-check",
            "--cd", str(workspace), "--ignore-user-config", "--ignore-rules",
            "--strict-config", "--ephemeral", "--disable", "multi_agent",
            "--disable", "memories", "--disable", "apps", "--disable", "plugins",
            "--disable", "plugin_sharing", "-c", 'approval_policy="never"',
            "--model", adjudicator["model"], "-c",
            f'model_reasoning_effort="{adjudicator["reasoning_effort"]}"',
            "--sandbox", "read-only", "--output-schema",
            receipt["material"]["transport_schema"]["path"], "--json",
            "--output-last-message", str(final_path), "-",
        ]
        environment = dict(os.environ)
        environment["CODEX_HOME"] = str(codex_home)
        completed = subprocess.run(
            command,
            input=Path(receipt["material"]["stdin"]["path"]).read_bytes(),
            capture_output=True,
            check=False,
            env=environment,
        )
        elapsed = round(time.monotonic() - started, 6)
        panel_runtime.write_bytes_once(stdout_path, completed.stdout)
        panel_runtime.write_bytes_once(stderr_path, completed.stderr)
        status = "external_failure"
        thread_id = None
        usage = None
        adjudication_ref = None
        if completed.returncode == 0:
            try:
                thread_id, raw_usage = panel_runtime.parse_jsonl(completed.stdout)
                document = _load(final_path)
                jsonschema.Draft202012Validator(_load(CANONICAL_SCHEMA_PATH)).validate(document)
                packet = _load(Path(receipt["material"]["packet"]["path"]))
                expected = packet["items"][0]
                identity = {
                    "calibration_set_id": packet["calibration_set_id"],
                    "panel_report_sha256": packet["panel_report_sha256"],
                    "adjudicator_identity": packet["adjudicator_identity"],
                    "panel_member": False,
                    "reference_type": "multi_grader_consensus_reference",
                    "human_alignment_state": "unmeasured",
                    "qualification_effect": "none",
                }
                if any(document[key] != value for key, value in identity.items()):
                    raise AdjudicatorRunError("adjudication identity mismatch")
                if [(item["calibration_item_id"], item["assertion_id"]) for item in document["items"]] != [(expected["calibration_item_id"], expected["assertion"]["assertion_id"])]:
                    raise AdjudicatorRunError("adjudication item mismatch")
                if any(span not in expected["assistant_message"] for span in document["items"][0]["evidence_spans"]):
                    raise AdjudicatorRunError("adjudication evidence span is not verbatim")
                panel_runtime.write_once(adjudication_path, document)
                usage = {**raw_usage, "total_tokens": raw_usage["input_tokens"] + raw_usage["output_tokens"]}
                adjudication_ref = _external_ref(adjudication_path)
                status = "valid"
            except (AdjudicatorRunError, panel_runtime.PanelRunError, jsonschema.ValidationError):
                status = "unrateable"
    result = {
        "schema_version": "general-chat-ai-adjudicator-run-result/v1",
        "run_id": "general-chat-semantic-pilot-adjudication-r1-run-r1",
        "status": status,
        "process_exit_code": completed.returncode,
        "elapsed_seconds": elapsed,
        "root_thread_id": thread_id,
        "usage": usage,
        "preflight": _external_ref(path),
        "dispatch": _external_ref(issued_path),
        "stdout": _external_ref(stdout_path),
        "stderr": _external_ref(stderr_path),
        "adjudication": adjudication_ref,
    }
    result["result_sha256"] = panel_runtime.content_identity(result, "result_sha256")
    jsonschema.Draft202012Validator(_load(RESULT_SCHEMA_PATH)).validate(result)
    panel_runtime.write_once(result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    preflight = commands.add_parser("preflight")
    preflight.add_argument("--run-root", type=Path, required=True)
    preflight.add_argument("--recovery-result", type=Path, required=True)
    run = commands.add_parser("run")
    run.add_argument("--preflight", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            output = make_preflight(args.run_root, args.recovery_result)
        else:
            output = execute(args.preflight)
    except (AdjudicatorRunError, panel_runtime.PanelRunError, jsonschema.ValidationError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
