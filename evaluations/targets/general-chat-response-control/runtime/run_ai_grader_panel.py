#!/usr/bin/env python3
"""Prepare and execute the fixed three-member semantic AI grader panel."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
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
PANEL_SCHEMA_PATH = TARGET / "calibration/ai-grader-panel-r1.schema.json"
CALIBRATION_INPUT_PATH = TARGET / "calibration/calibration-input-core-r1.json"
CALIBRATION_INPUT_SCHEMA_PATH = TARGET / "calibration/calibration-input-r1.schema.json"
CASES_PATH = TARGET / "cases/core-r1/input-cases.json"
CASES_SCHEMA_PATH = TARGET / "cases/core-r1/input-cases.schema.json"
MEMBER_PROMPT_PATH = TARGET / "rating-contracts/general-chat-semantic-panel-member-r1.txt"
PACKET_SCHEMA_PATH = TARGET / "calibration/rater-packet-r1.schema.json"
ORGANIZER_MAP_SCHEMA_PATH = TARGET / "calibration/organizer-map-r1.schema.json"
LABEL_TEMPLATE_SCHEMA_PATH = TARGET / "calibration/ai-grader-label-template-r1.schema.json"
CANONICAL_LABEL_SCHEMA_PATH = TARGET / "calibration/ai-grader-label-r1.schema.json"
PREFLIGHT_SCHEMA_PATH = TARGET / "calibration/ai-grader-run-preflight-r1.schema.json"
PILOT_REPORT_SCHEMA_PATH = TARGET / "calibration/ai-panel-pilot-report-r1.schema.json"
RUN_RESULT_SCHEMA_PATH = TARGET / "calibration/ai-grader-panel-run-result-r1.schema.json"
RECOVERY_RESULT_SCHEMA_PATH = (
    TARGET / "calibration/ai-grader-panel-recovery-result-r1.schema.json"
)
RUNNER_PATH = Path(__file__).resolve()
RUNTIME_VERSION = "0.148.0"
PREFLIGHT_RECEIPT_ID = "general-chat-semantic-pilot-panel-r1-preflight-r3"
DISPATCH_ID = "general-chat-semantic-pilot-panel-r1-dispatch-r2"
RUN_ID = "general-chat-semantic-pilot-panel-r1-run-r2"

CALIBRATION_MODULE_PATH = Path(__file__).with_name("prepare_semantic_calibration.py")
CALIBRATION_SPEC = importlib.util.spec_from_file_location(
    "general_chat_prepare_semantic_calibration", CALIBRATION_MODULE_PATH
)
if CALIBRATION_SPEC is None or CALIBRATION_SPEC.loader is None:
    raise RuntimeError("cannot load semantic calibration module")
calibration_runtime = importlib.util.module_from_spec(CALIBRATION_SPEC)
CALIBRATION_SPEC.loader.exec_module(calibration_runtime)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.codex_runtime_binding import (  # noqa: E402
    CodexRuntimeBindingError,
    resolve_fixed_codex_runtime,
    verify_codex_runtime_binding,
)


class PanelRunError(RuntimeError):
    """The fixed panel cannot be prepared or executed without contract drift."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise PanelRunError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise PanelRunError(f"expected JSON object: {path}")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def content_identity(value: dict[str, Any], field: str) -> str:
    payload = {key: item for key, item in value.items() if key != field}
    return sha256_bytes(
        json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    )


def write_once(path: Path, value: dict[str, Any]) -> None:
    if path.exists():
        raise PanelRunError(f"refusing to overwrite artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_bytes_once(path: Path, value: bytes) -> None:
    if path.exists():
        raise PanelRunError(f"refusing to overwrite artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def repository_reference(path: Path) -> dict[str, str]:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(ROOT)
    except ValueError as error:
        raise PanelRunError(f"repository source escapes root: {resolved}") from error
    if not resolved.is_file():
        raise PanelRunError(f"repository source is unavailable: {resolved}")
    return {"path": str(relative), "sha256": sha256_file(resolved)}


def external_reference(path: Path) -> dict[str, str]:
    resolved = path.resolve()
    if not resolved.is_file():
        raise PanelRunError(f"external material is unavailable: {resolved}")
    return {"path": str(resolved), "sha256": sha256_file(resolved)}


def ensure_external_run_root(run_root: Path) -> Path:
    resolved = run_root.resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        return resolved
    raise PanelRunError("run root must be outside the repository")


def _json_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    raise PanelRunError("cannot infer JSON type for transport schema")


def project_transport_schema(value: Any) -> Any:
    """Project the canonical contract into the model transport schema subset."""
    if isinstance(value, dict):
        projected = {
            key: project_transport_schema(item)
            for key, item in value.items()
            if key not in {"$schema", "$id", "uniqueItems"}
        }
        if "type" not in projected and "const" in projected:
            projected["type"] = _json_type(projected["const"])
        if "type" not in projected and "enum" in projected:
            enum_types = {_json_type(item) for item in projected["enum"]}
            if len(enum_types) != 1:
                raise PanelRunError("transport schema enum has mixed JSON types")
            projected["type"] = enum_types.pop()
        return projected
    if isinstance(value, list):
        return [project_transport_schema(item) for item in value]
    return value


def validate_transport_schema(schema: dict[str, Any]) -> None:
    """Reject a known-invalid model transport schema before any slot is issued."""
    def visit(node: Any, location: tuple[str, ...]) -> None:
        if isinstance(node, list):
            for index, item in enumerate(node):
                visit(item, (*location, str(index)))
            return
        if not isinstance(node, dict):
            return
        if any(key in node for key in ("$schema", "$id", "uniqueItems")):
            raise PanelRunError(
                "transport schema retains unsupported annotation at "
                + "/".join(location)
            )
        if ("const" in node or "enum" in node) and "type" not in node:
            raise PanelRunError(
                "transport schema fixed-value node lacks type at "
                + "/".join(location)
            )
        properties = node.get("properties")
        if isinstance(properties, dict):
            required = node.get("required")
            if not isinstance(required, list) or set(required) != set(properties):
                raise PanelRunError(
                    "transport schema object does not require every property at "
                    + "/".join(location)
                )
        for key, item in node.items():
            visit(item, (*location, key))

    visit(schema, ("$",))


def make_stdin(member_prompt: str, packet: dict[str, Any], template: dict[str, Any]) -> bytes:
    payload = {
        "packet": packet,
        "required_output_identity": {
            "schema_version": "general-chat-ai-grader-label/v1",
            "packet_id": template["packet_id"],
            "calibration_set_id": template["calibration_set_id"],
            "grader_execution_id": template["grader_execution_id"],
            "independent_context": True,
        },
        "required_label_rows": template["labels"],
    }
    return (
        member_prompt.rstrip()
        + "\n\n以下の固定packetだけを判定し、required_label_rowsの全行を同じ順序で完成させてください。\n"
        + json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _validate_fixed_panel(panel: dict[str, Any]) -> None:
    panel_schema = load_object(PANEL_SCHEMA_PATH)
    jsonschema.Draft202012Validator(panel_schema).validate(panel)
    if not calibration_runtime.ai_panel_is_bound(
        panel, model_under_test="gpt-5.6-sol"
    ):
        raise PanelRunError("AI panel identity is not bound")
    if panel["runtime_identity"] != f"codex-cli {RUNTIME_VERSION}":
        raise PanelRunError("AI panel runtime identity mismatch")
    if len(panel["members"]) != 3:
        raise PanelRunError("pilot runner requires exactly three fixed panel members")
    if {item["prompt_sha256"] for item in panel["members"]} != {
        sha256_file(MEMBER_PROMPT_PATH)
    }:
        raise PanelRunError("panel member prompt hash mismatch")
    if {item["schema_sha256"] for item in panel["members"]} != {
        sha256_file(CANONICAL_LABEL_SCHEMA_PATH)
    }:
        raise PanelRunError("panel member label schema hash mismatch")


def make_preflight(run_root: Path) -> dict[str, Any]:
    run_root = ensure_external_run_root(run_root)
    receipt_path = run_root / "preflight.json"
    if run_root.exists() and any(run_root.iterdir()):
        raise PanelRunError("preflight run root must be absent or empty")
    run_root.mkdir(parents=True, exist_ok=True)

    panel = load_object(PANEL_PATH)
    _validate_fixed_panel(panel)
    calibration = load_object(CALIBRATION_INPUT_PATH)
    cases = load_object(CASES_PATH)
    canonical_schema = load_object(CANONICAL_LABEL_SCHEMA_PATH)
    jsonschema.Draft202012Validator(
        load_object(CALIBRATION_INPUT_SCHEMA_PATH)
    ).validate(calibration)
    jsonschema.Draft202012Validator(load_object(CASES_SCHEMA_PATH)).validate(cases)
    member_prompt = MEMBER_PROMPT_PATH.read_text(encoding="utf-8")
    try:
        runtime_binding = resolve_fixed_codex_runtime(RUNTIME_VERSION)
        verify_codex_runtime_binding(runtime_binding)
    except CodexRuntimeBindingError as error:
        raise PanelRunError(str(error)) from error

    slots: list[dict[str, Any]] = []
    for index, member in enumerate(panel["members"], start=1):
        slot_dir = run_root / "material" / member["grader_execution_id"]
        packet, organizer_map, template = calibration_runtime.make_ai_grader_material(
            calibration,
            cases,
            grader_execution_id=member["grader_execution_id"],
            calibration_input_sha256=sha256_file(CALIBRATION_INPUT_PATH),
            cases_sha256=sha256_file(CASES_PATH),
        )
        transport_schema = project_transport_schema(canonical_schema)
        validate_transport_schema(transport_schema)
        stdin = make_stdin(member_prompt, packet, template)
        packet_path = slot_dir / "packet.json"
        map_path = slot_dir / "organizer-map.json"
        template_path = slot_dir / "label-template.json"
        transport_schema_path = slot_dir / "transport-schema.json"
        stdin_path = slot_dir / "stdin.txt"
        for path, value in (
            (packet_path, packet),
            (map_path, organizer_map),
            (template_path, template),
            (transport_schema_path, transport_schema),
        ):
            write_once(path, value)
        write_bytes_once(stdin_path, stdin)
        jsonschema.Draft202012Validator(load_object(PACKET_SCHEMA_PATH)).validate(packet)
        jsonschema.Draft202012Validator(load_object(ORGANIZER_MAP_SCHEMA_PATH)).validate(
            organizer_map
        )
        jsonschema.Draft202012Validator(load_object(LABEL_TEMPLATE_SCHEMA_PATH)).validate(
            template
        )
        slots.append(
            {
                "slot_id": f"ai-panel-slot-{index:02d}",
                "grader_execution_id": member["grader_execution_id"],
                "model": member["model"],
                "reasoning_effort": member["reasoning_effort"],
                "packet": external_reference(packet_path),
                "organizer_map": external_reference(map_path),
                "label_template": external_reference(template_path),
                "transport_schema": external_reference(transport_schema_path),
                "stdin": external_reference(stdin_path),
            }
        )

    receipt = {
        "schema_version": "general-chat-ai-grader-run-preflight/v1",
        "receipt_id": PREFLIGHT_RECEIPT_ID,
        "panel_id": panel["panel_id"],
        "state": "ready_not_issued",
        "issued_slot_count": 0,
        "runtime_binding": runtime_binding,
        "fixed_sources": {
            "panel": repository_reference(PANEL_PATH),
            "panel_schema": repository_reference(PANEL_SCHEMA_PATH),
            "calibration_input": repository_reference(CALIBRATION_INPUT_PATH),
            "calibration_input_schema": repository_reference(CALIBRATION_INPUT_SCHEMA_PATH),
            "cases": repository_reference(CASES_PATH),
            "cases_schema": repository_reference(CASES_SCHEMA_PATH),
            "member_prompt": repository_reference(MEMBER_PROMPT_PATH),
            "packet_schema": repository_reference(PACKET_SCHEMA_PATH),
            "organizer_map_schema": repository_reference(ORGANIZER_MAP_SCHEMA_PATH),
            "label_template_schema": repository_reference(LABEL_TEMPLATE_SCHEMA_PATH),
            "canonical_label_schema": repository_reference(CANONICAL_LABEL_SCHEMA_PATH),
            "preflight_schema": repository_reference(PREFLIGHT_SCHEMA_PATH),
            "pilot_report_schema": repository_reference(PILOT_REPORT_SCHEMA_PATH),
            "run_result_schema": repository_reference(RUN_RESULT_SCHEMA_PATH),
            "runner": repository_reference(RUNNER_PATH),
        },
        "instruction_isolation": {
            "ephemeral": True,
            "ignore_user_config": True,
            "ignore_rules": True,
            "multi_agent": False,
            "memories": False,
            "apps": False,
            "plugins": False,
            "plugin_sharing": False,
            "sandbox": "read-only",
            "approval_policy": "never",
        },
        "storage": {
            "run_root": str(run_root),
            "repository_external": True,
            "codex_home": "per_slot_temporary",
            "auth_transport": "host_auth_symlink_not_persisted",
            "raw_output_policy": "external_run_root_only",
        },
        "slots": slots,
    }
    receipt["receipt_sha256"] = content_identity(receipt, "receipt_sha256")
    schema = load_object(PREFLIGHT_SCHEMA_PATH)
    jsonschema.Draft202012Validator(schema).validate(receipt)
    write_once(receipt_path, receipt)
    return receipt


def validate_preflight(preflight_path: Path) -> dict[str, Any]:
    receipt = load_object(preflight_path.resolve())
    schema = load_object(PREFLIGHT_SCHEMA_PATH)
    jsonschema.Draft202012Validator(schema).validate(receipt)
    if receipt["receipt_sha256"] != content_identity(receipt, "receipt_sha256"):
        raise PanelRunError("preflight receipt hash mismatch")
    if Path(receipt["storage"]["run_root"]).resolve() != preflight_path.resolve().parent:
        raise PanelRunError("preflight path does not match bound run root")
    ensure_external_run_root(preflight_path.resolve().parent)
    panel = load_object(PANEL_PATH)
    _validate_fixed_panel(panel)
    expected_members = [
        {
            "slot_id": f"ai-panel-slot-{index:02d}",
            "grader_execution_id": member["grader_execution_id"],
            "model": member["model"],
            "reasoning_effort": member["reasoning_effort"],
        }
        for index, member in enumerate(panel["members"], start=1)
    ]
    observed_members = [
        {key: slot[key] for key in expected_members[0]}
        for slot in receipt["slots"]
    ]
    if observed_members != expected_members:
        raise PanelRunError("preflight slot identity differs from the fixed panel")
    expected_sources = {
        "panel": repository_reference(PANEL_PATH),
        "panel_schema": repository_reference(PANEL_SCHEMA_PATH),
        "calibration_input": repository_reference(CALIBRATION_INPUT_PATH),
        "calibration_input_schema": repository_reference(CALIBRATION_INPUT_SCHEMA_PATH),
        "cases": repository_reference(CASES_PATH),
        "cases_schema": repository_reference(CASES_SCHEMA_PATH),
        "member_prompt": repository_reference(MEMBER_PROMPT_PATH),
        "packet_schema": repository_reference(PACKET_SCHEMA_PATH),
        "organizer_map_schema": repository_reference(ORGANIZER_MAP_SCHEMA_PATH),
        "label_template_schema": repository_reference(LABEL_TEMPLATE_SCHEMA_PATH),
        "canonical_label_schema": repository_reference(CANONICAL_LABEL_SCHEMA_PATH),
        "preflight_schema": repository_reference(PREFLIGHT_SCHEMA_PATH),
        "pilot_report_schema": repository_reference(PILOT_REPORT_SCHEMA_PATH),
        "run_result_schema": repository_reference(RUN_RESULT_SCHEMA_PATH),
        "runner": repository_reference(RUNNER_PATH),
    }
    if receipt["fixed_sources"] != expected_sources:
        raise PanelRunError("preflight repository source drifted")
    calibration = load_object(CALIBRATION_INPUT_PATH)
    cases = load_object(CASES_PATH)
    canonical_schema = load_object(CANONICAL_LABEL_SCHEMA_PATH)
    expected_transport_schema = project_transport_schema(canonical_schema)
    validate_transport_schema(expected_transport_schema)
    member_prompt = MEMBER_PROMPT_PATH.read_text(encoding="utf-8")
    for slot in receipt["slots"]:
        for field in ("packet", "organizer_map", "label_template", "transport_schema", "stdin"):
            reference = slot[field]
            path = Path(reference["path"]).resolve()
            try:
                path.relative_to(preflight_path.resolve().parent)
            except ValueError as error:
                raise PanelRunError("preflight material escapes run root") from error
            if external_reference(path) != reference:
                raise PanelRunError(f"preflight material drifted: {field}")
        expected_packet, expected_map, expected_template = (
            calibration_runtime.make_ai_grader_material(
                calibration,
                cases,
                grader_execution_id=slot["grader_execution_id"],
                calibration_input_sha256=sha256_file(CALIBRATION_INPUT_PATH),
                cases_sha256=sha256_file(CASES_PATH),
            )
        )
        if load_object(Path(slot["packet"]["path"])) != expected_packet:
            raise PanelRunError("preflight packet differs from fixed sources")
        if load_object(Path(slot["organizer_map"]["path"])) != expected_map:
            raise PanelRunError("preflight organizer map differs from fixed sources")
        if load_object(Path(slot["label_template"]["path"])) != expected_template:
            raise PanelRunError("preflight label template differs from fixed sources")
        observed_transport_schema = load_object(Path(slot["transport_schema"]["path"]))
        validate_transport_schema(observed_transport_schema)
        if observed_transport_schema != expected_transport_schema:
            raise PanelRunError("preflight transport schema differs from canonical projection")
        if Path(slot["stdin"]["path"]).read_bytes() != make_stdin(
            member_prompt, expected_packet, expected_template
        ):
            raise PanelRunError("preflight stdin differs from fixed sources")
    try:
        verify_codex_runtime_binding(receipt["runtime_binding"])
        current_binding = resolve_fixed_codex_runtime(RUNTIME_VERSION)
    except CodexRuntimeBindingError as error:
        raise PanelRunError(str(error)) from error
    if current_binding != receipt["runtime_binding"]:
        raise PanelRunError("preflight Codex runtime binding drifted")
    return receipt


def build_command(
    receipt: dict[str, Any], slot: dict[str, Any], workspace: Path, final_path: Path
) -> list[str]:
    return [
        receipt["runtime_binding"]["executable"],
        "exec",
        "--skip-git-repo-check",
        "--cd",
        str(workspace.resolve()),
        "--ignore-user-config",
        "--ignore-rules",
        "--strict-config",
        "--ephemeral",
        "--disable",
        "multi_agent",
        "--disable",
        "memories",
        "--disable",
        "apps",
        "--disable",
        "plugins",
        "--disable",
        "plugin_sharing",
        "-c",
        'approval_policy="never"',
        "--model",
        slot["model"],
        "-c",
        f'model_reasoning_effort="{slot["reasoning_effort"]}"',
        "--sandbox",
        "read-only",
        "--output-schema",
        slot["transport_schema"]["path"],
        "--json",
        "--output-last-message",
        str(final_path.resolve()),
        "-",
    ]


def parse_jsonl(stdout: bytes) -> tuple[str, dict[str, int]]:
    thread_ids: list[str] = []
    usages: list[dict[str, Any]] = []
    failures: list[str] = []
    for raw_line in stdout.splitlines():
        if not raw_line.strip():
            continue
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as error:
            raise PanelRunError("Codex stdout contains non-JSONL data") from error
        if not isinstance(event, dict):
            raise PanelRunError("Codex JSONL event is not an object")
        event_type = event.get("type")
        if event_type == "thread.started" and isinstance(event.get("thread_id"), str):
            thread_ids.append(event["thread_id"])
        elif event_type == "turn.completed" and isinstance(event.get("usage"), dict):
            usages.append(event["usage"])
        elif event_type in {"error", "turn.failed"}:
            failures.append(str(event_type))
    if failures or len(thread_ids) != 1 or len(usages) != 1:
        raise PanelRunError("Codex JSONL terminal identity is incomplete")
    usage = usages[0]
    expected_fields = (
        "input_tokens",
        "cached_input_tokens",
        "cache_write_input_tokens",
        "output_tokens",
        "reasoning_output_tokens",
    )
    if set(usage) != set(expected_fields):
        raise PanelRunError("Codex terminal usage fields differ from the fixed contract")
    if any(
        not isinstance(usage[field], int)
        or isinstance(usage[field], bool)
        or usage[field] < 0
        for field in expected_fields
    ):
        raise PanelRunError("Codex terminal usage value is unavailable")
    if usage["cached_input_tokens"] > usage["input_tokens"]:
        raise PanelRunError("Codex cached input tokens exceed input tokens")
    if usage["cache_write_input_tokens"] > usage["input_tokens"]:
        raise PanelRunError("Codex cache-write input tokens exceed input tokens")
    if usage["reasoning_output_tokens"] > usage["output_tokens"]:
        raise PanelRunError("Codex reasoning tokens exceed output tokens")
    return thread_ids[0], {field: usage[field] for field in expected_fields}


def extract_final_label_from_jsonl(stdout: bytes) -> dict[str, Any]:
    messages: list[str] = []
    for raw_line in stdout.splitlines():
        if not raw_line.strip():
            continue
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as error:
            raise PanelRunError("Codex stdout contains non-JSONL data") from error
        item = event.get("item") if isinstance(event, dict) else None
        if (
            event.get("type") == "item.completed"
            and isinstance(item, dict)
            and item.get("type") == "agent_message"
            and isinstance(item.get("text"), str)
        ):
            messages.append(item["text"])
    if not messages:
        raise PanelRunError("Codex final agent message is unavailable")
    try:
        label = json.loads(messages[-1])
    except json.JSONDecodeError as error:
        raise PanelRunError("Codex final agent message is not JSON") from error
    if not isinstance(label, dict):
        raise PanelRunError("Codex final agent message is not a JSON object")
    return label


def validate_member_label(
    label: dict[str, Any], template: dict[str, Any], canonical_schema: dict[str, Any]
) -> None:
    jsonschema.Draft202012Validator(canonical_schema).validate(label)
    for field in ("packet_id", "calibration_set_id", "grader_execution_id"):
        if label[field] != template[field]:
            raise PanelRunError(f"AI label identity mismatch: {field}")
    if label.get("independent_context") is not True:
        raise PanelRunError("AI label independence identity mismatch")
    expected = [
        (item["rating_item_id"], item["assertion_id"])
        for item in template["labels"]
    ]
    observed = [
        (item["rating_item_id"], item["assertion_id"])
        for item in label["labels"]
    ]
    if observed != expected:
        raise PanelRunError("AI label rows differ from the fixed template")


def run_slot(receipt: dict[str, Any], slot: dict[str, Any], host_auth: Path) -> dict[str, Any]:
    run_root = Path(receipt["storage"]["run_root"])
    output_dir = run_root / "output" / slot["grader_execution_id"]
    output_dir.mkdir(parents=True, exist_ok=False)
    stdout_path = output_dir / "stdout.jsonl"
    stderr_path = output_dir / "stderr.log"
    label_path = output_dir / "label.json"
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="general-chat-ai-grader-workspace-") as raw_workspace, tempfile.TemporaryDirectory(
        prefix="general-chat-ai-grader-home-"
    ) as raw_home:
        workspace = Path(raw_workspace)
        codex_home = Path(raw_home)
        os.symlink(host_auth, codex_home / "auth.json")
        (workspace / "AGENTS.md").write_bytes(b"")
        temporary_final = workspace / "final.json"
        command = build_command(receipt, slot, workspace, temporary_final)
        environment = dict(os.environ)
        environment["CODEX_HOME"] = str(codex_home)
        completed = subprocess.run(
            command,
            input=Path(slot["stdin"]["path"]).read_bytes(),
            capture_output=True,
            check=False,
            env=environment,
        )
        elapsed = round(time.monotonic() - started, 6)
        write_bytes_once(stdout_path, completed.stdout)
        write_bytes_once(stderr_path, completed.stderr)
        base = {
            "slot_id": slot["slot_id"],
            "grader_execution_id": slot["grader_execution_id"],
            "process_exit_code": completed.returncode,
            "elapsed_seconds": elapsed,
            "stdout_sha256": sha256_file(stdout_path),
            "stderr_sha256": sha256_file(stderr_path),
            "root_thread_id": None,
            "total_tokens": None,
            "label": None,
        }
        if completed.returncode != 0:
            return {**base, "status": "external_failure"}
        try:
            thread_id, usage = parse_jsonl(completed.stdout)
            label = load_object(temporary_final)
            template = load_object(Path(slot["label_template"]["path"]))
            canonical_schema = load_object(CANONICAL_LABEL_SCHEMA_PATH)
            validate_member_label(label, template, canonical_schema)
            write_once(label_path, label)
        except (PanelRunError, jsonschema.ValidationError):
            return {**base, "status": "unrateable"}
        return {
            **base,
            "status": "valid",
            "root_thread_id": thread_id,
            "total_tokens": usage["input_tokens"] + usage["output_tokens"],
            "label": external_reference(label_path),
        }


def recover_completed_run(source_result_path: Path) -> dict[str, Any]:
    source_result_path = source_result_path.resolve()
    source_result = load_object(source_result_path)
    jsonschema.Draft202012Validator(load_object(RUN_RESULT_SCHEMA_PATH)).validate(
        source_result
    )
    if source_result["result_sha256"] != content_identity(
        source_result, "result_sha256"
    ):
        raise PanelRunError("source run result hash mismatch")
    if source_result["summary"] != {
        "authorized_slots": 3,
        "valid_results": 0,
        "external_failures": 0,
        "unrateable_results": 3,
        "measurement_state": "pilot_measurement_not_established",
    }:
        raise PanelRunError("source run is not the fixed recoverable state")
    run_root = source_result_path.parent
    recovery_path = run_root / "recovery-result.json"
    report_path = run_root / "recovered-pilot-report.json"
    if recovery_path.exists() or report_path.exists():
        raise PanelRunError("recovery artifacts already exist")
    preflight_path = Path(source_result["preflight"]["path"]).resolve()
    if external_reference(preflight_path) != source_result["preflight"]:
        raise PanelRunError("source preflight artifact drifted")
    receipt = load_object(preflight_path)
    jsonschema.Draft202012Validator(load_object(PREFLIGHT_SCHEMA_PATH)).validate(receipt)
    if receipt["receipt_sha256"] != content_identity(receipt, "receipt_sha256"):
        raise PanelRunError("source preflight receipt hash mismatch")
    slots_by_id = {slot["slot_id"]: slot for slot in receipt["slots"]}
    canonical_schema = load_object(CANONICAL_LABEL_SCHEMA_PATH)
    recovered_slots: list[dict[str, Any]] = []
    maps: list[dict[str, Any]] = []
    labels: list[dict[str, Any]] = []
    for source_row in source_result["slots"]:
        if source_row["status"] != "unrateable" or source_row["process_exit_code"] != 0:
            raise PanelRunError("source slot is not a completed unrateable result")
        slot = slots_by_id.get(source_row["slot_id"])
        if slot is None or slot["grader_execution_id"] != source_row["grader_execution_id"]:
            raise PanelRunError("source slot identity mismatch")
        output_dir = run_root / "output" / slot["grader_execution_id"]
        stdout_path = output_dir / "stdout.jsonl"
        stderr_path = output_dir / "stderr.log"
        if sha256_file(stdout_path) != source_row["stdout_sha256"]:
            raise PanelRunError("source slot stdout drifted")
        if sha256_file(stderr_path) != source_row["stderr_sha256"]:
            raise PanelRunError("source slot stderr drifted")
        stdout = stdout_path.read_bytes()
        thread_id, usage = parse_jsonl(stdout)
        label = extract_final_label_from_jsonl(stdout)
        template = load_object(Path(slot["label_template"]["path"]))
        validate_member_label(label, template, canonical_schema)
        label_path = output_dir / "recovered-label.json"
        write_once(label_path, label)
        labels.append(label)
        maps.append(load_object(Path(slot["organizer_map"]["path"])))
        recovered_slots.append(
            {
                "slot_id": slot["slot_id"],
                "grader_execution_id": slot["grader_execution_id"],
                "root_thread_id": thread_id,
                "usage": {
                    **usage,
                    "total_tokens": usage["input_tokens"] + usage["output_tokens"],
                },
                "stdout": external_reference(stdout_path),
                "label": external_reference(label_path),
            }
        )
    pilot_report = calibration_runtime.analyze_ai_panel(maps, labels)
    jsonschema.Draft202012Validator(load_object(PILOT_REPORT_SCHEMA_PATH)).validate(
        pilot_report
    )
    write_once(report_path, pilot_report)
    recovery = {
        "schema_version": "general-chat-ai-grader-panel-recovery-result/v1",
        "recovery_id": "general-chat-semantic-pilot-panel-r1-attempt-r2-recovery-r1",
        "source_run": external_reference(source_result_path),
        "source_preflight": external_reference(preflight_path),
        "recovery_method": "codex-cli-jsonl-terminal-recovery-r1",
        "recovery_runner": repository_reference(RUNNER_PATH),
        "recovery_schema": repository_reference(RECOVERY_RESULT_SCHEMA_PATH),
        "slots": recovered_slots,
        "pilot_report": external_reference(report_path),
        "summary": {
            "recovered_results": len(recovered_slots),
            "valid_results": len(recovered_slots),
            "measurement_state": "pilot_measurement_established",
        },
    }
    recovery["result_sha256"] = content_identity(recovery, "result_sha256")
    jsonschema.Draft202012Validator(load_object(RECOVERY_RESULT_SCHEMA_PATH)).validate(
        recovery
    )
    write_once(recovery_path, recovery)
    return recovery


def execute(preflight_path: Path) -> dict[str, Any]:
    receipt = validate_preflight(preflight_path)
    run_root = Path(receipt["storage"]["run_root"])
    dispatch_path = run_root / "issued.json"
    result_path = run_root / "run-result.json"
    if dispatch_path.exists() or result_path.exists() or (run_root / "output").exists():
        raise PanelRunError("panel slots were already issued or partially issued")
    host_codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve()
    host_auth = host_codex_home / "auth.json"
    if not host_auth.is_file():
        raise PanelRunError("host Codex auth identity is unavailable")
    dispatch = {
        "schema_version": "general-chat-ai-grader-panel-dispatch/v1",
        "dispatch_id": DISPATCH_ID,
        "preflight_sha256": sha256_file(preflight_path),
        "slots": [slot["slot_id"] for slot in receipt["slots"]],
        "issued_slot_count": len(receipt["slots"]),
        "state": "issued_once",
    }
    dispatch["dispatch_sha256"] = content_identity(dispatch, "dispatch_sha256")
    write_once(dispatch_path, dispatch)

    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=len(receipt["slots"])) as executor:
        futures = {
            executor.submit(run_slot, receipt, slot, host_auth): slot
            for slot in receipt["slots"]
        }
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda item: item["slot_id"])
    valid = [row for row in rows if row["status"] == "valid"]
    pilot_reference: dict[str, str] | None = None
    if len(valid) == len(rows):
        maps = [load_object(Path(slot["organizer_map"]["path"])) for slot in receipt["slots"]]
        labels = [load_object(Path(row["label"]["path"])) for row in valid]
        pilot_report = calibration_runtime.analyze_ai_panel(maps, labels)
        jsonschema.Draft202012Validator(load_object(PILOT_REPORT_SCHEMA_PATH)).validate(
            pilot_report
        )
        pilot_path = run_root / "pilot-report.json"
        write_once(pilot_path, pilot_report)
        pilot_reference = external_reference(pilot_path)

    result = {
        "schema_version": "general-chat-ai-grader-panel-run-result/v1",
        "run_id": RUN_ID,
        "panel_id": receipt["panel_id"],
        "preflight": external_reference(preflight_path),
        "dispatch": external_reference(dispatch_path),
        "slots": rows,
        "pilot_report": pilot_reference,
        "summary": {
            "authorized_slots": len(rows),
            "valid_results": len(valid),
            "external_failures": sum(row["status"] == "external_failure" for row in rows),
            "unrateable_results": sum(row["status"] == "unrateable" for row in rows),
            "measurement_state": (
                "pilot_measurement_established"
                if len(valid) == len(rows)
                else "pilot_measurement_not_established"
            ),
        },
    }
    result["result_sha256"] = content_identity(result, "result_sha256")
    jsonschema.Draft202012Validator(load_object(RUN_RESULT_SCHEMA_PATH)).validate(result)
    write_once(result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    preflight = commands.add_parser("preflight")
    preflight.add_argument("--run-root", type=Path, required=True)
    run = commands.add_parser("run")
    run.add_argument("--preflight", type=Path, required=True)
    recover = commands.add_parser("recover")
    recover.add_argument("--run-result", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            receipt = make_preflight(args.run_root)
            output = {
                "receipt_id": receipt["receipt_id"],
                "authorized_slot_count": len(receipt["slots"]),
                "state": receipt["state"],
            }
        elif args.command == "run":
            output = execute(args.preflight)["summary"]
        else:
            output = recover_completed_run(args.run_result)["summary"]
    except (PanelRunError, jsonschema.ValidationError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
