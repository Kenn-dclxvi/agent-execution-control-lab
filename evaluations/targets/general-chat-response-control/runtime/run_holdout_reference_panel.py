#!/usr/bin/env python3
"""Prepare the fixed holdout-reference panel without issuing model slots."""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[4]
TARGET = ROOT / "evaluations/targets/general-chat-response-control"
CALIBRATION = TARGET / "calibration"
PLAN_PATH = CALIBRATION / "qualification-holdout-plan-r1.json"
PLAN_SCHEMA_PATH = CALIBRATION / "qualification-holdout-plan-r1.schema.json"
HOLDOUT_PATH = CALIBRATION / "qualification-holdout-r1.json"
HOLDOUT_SCHEMA_PATH = CALIBRATION / "qualification-holdout-r1.schema.json"
THRESHOLD_PATH = CALIBRATION / "qualification-threshold-r1.json"
MEMBER_PROMPT_PATH = TARGET / "rating-contracts/general-chat-semantic-panel-member-r1.txt"
PACKET_SCHEMA_PATH = CALIBRATION / "rater-packet-r1.schema.json"
ORGANIZER_MAP_SCHEMA_PATH = CALIBRATION / "holdout-organizer-map-r1.schema.json"
LABEL_TEMPLATE_SCHEMA_PATH = CALIBRATION / "ai-grader-label-template-r1.schema.json"
CANONICAL_LABEL_SCHEMA_PATH = CALIBRATION / "ai-grader-label-r1.schema.json"
PREFLIGHT_SCHEMA_PATH = CALIBRATION / "holdout-reference-preflight-r1.schema.json"
DISPATCH_SCHEMA_PATH = CALIBRATION / "holdout-reference-panel-dispatch-r1.schema.json"
REFERENCE_REPORT_SCHEMA_PATH = CALIBRATION / "holdout-reference-panel-report-r1.schema.json"
RUN_RESULT_SCHEMA_PATH = CALIBRATION / "holdout-reference-panel-run-result-r1.schema.json"
REFERENCE_PATH = CALIBRATION / "qualification-reference-r1.json"
RUNNER_PATH = Path(__file__).resolve()
RUNTIME_VERSION = "0.148.0"
RECEIPT_ID = "general-chat-semantic-holdout-reference-r1-preflight-r1"
DISPATCH_ID = "general-chat-semantic-holdout-reference-r1-dispatch-r1"
RUN_ID = "general-chat-semantic-holdout-reference-r1-run-r1"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


panel_runtime = _load_module(
    "general_chat_ai_panel_runtime", Path(__file__).with_name("run_ai_grader_panel.py")
)
calibration_runtime = _load_module(
    "general_chat_calibration_runtime",
    Path(__file__).with_name("prepare_semantic_calibration.py"),
)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.codex_runtime_binding import (  # noqa: E402
    CodexRuntimeBindingError,
    resolve_fixed_codex_runtime,
    verify_codex_runtime_binding,
)


class HoldoutReferenceError(RuntimeError):
    """The holdout-reference preflight cannot be fixed without drift."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise HoldoutReferenceError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise HoldoutReferenceError(f"expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _digest(*parts: str) -> str:
    return hashlib.sha256("\0".join(parts).encode("utf-8")).hexdigest()


def content_identity(value: dict[str, Any], field: str) -> str:
    payload = {key: item for key, item in value.items() if key != field}
    return hashlib.sha256(
        json.dumps(
            payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def repository_reference(path: Path) -> dict[str, str]:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(ROOT)
    except ValueError as error:
        raise HoldoutReferenceError(f"repository source escapes root: {resolved}") from error
    if not resolved.is_file():
        raise HoldoutReferenceError(f"repository source is unavailable: {resolved}")
    return {"path": str(relative), "sha256": sha256_file(resolved)}


def external_reference(path: Path) -> dict[str, str]:
    resolved = path.resolve()
    if not resolved.is_file():
        raise HoldoutReferenceError(f"external material is unavailable: {resolved}")
    return {"path": str(resolved), "sha256": sha256_file(resolved)}


def ensure_external_run_root(run_root: Path) -> Path:
    resolved = run_root.resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        return resolved
    raise HoldoutReferenceError("run root must be outside the repository")


def write_once(path: Path, value: dict[str, Any]) -> None:
    if path.exists():
        raise HoldoutReferenceError(f"refusing to overwrite artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_bytes_once(path: Path, value: bytes) -> None:
    if path.exists():
        raise HoldoutReferenceError(f"refusing to overwrite artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def make_holdout_material(
    holdout: dict[str, Any], *, grader_execution_id: str, source_sha256: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Return one blinded packet, organizer-only map, and blank AI label template."""
    if not grader_execution_id.strip():
        raise HoldoutReferenceError("grader_execution_id must not be empty")
    holdout_set_id = holdout["holdout_set_id"]
    packet_id = f"packet-{_digest(holdout_set_id, grader_execution_id)[:16]}"
    prepared: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for source_item in holdout["items"]:
        opaque = f"item-{_digest(packet_id, source_item['holdout_item_id'])[:16]}"
        packet_item = {
            "rating_item_id": opaque,
            "conversation": source_item["conversation"],
            "available_evidence": source_item["available_evidence"],
            "received_evidence": source_item["received_evidence"],
            "assistant_message": source_item["assistant_message"],
            "assertions": source_item["assertions"],
        }
        mapping = {
            "rating_item_id": opaque,
            "holdout_item_id": source_item["holdout_item_id"],
            "assertion_ids": [
                assertion["assertion_id"] for assertion in source_item["assertions"]
            ],
        }
        prepared.append(
            (
                _digest(packet_id, "order", source_item["holdout_item_id"]),
                packet_item,
                mapping,
            )
        )
    prepared.sort(key=lambda row: row[0])
    packet_items = [row[1] for row in prepared]
    mappings = [row[2] for row in prepared]
    packet = {
        "schema_version": "general-chat-rater-packet/v1",
        "packet_id": packet_id,
        "calibration_set_id": holdout_set_id,
        "rater_id": grader_execution_id,
        "independent": True,
        "instructions": {
            "labels": {
                "pass": "回答がcriterionを意味として満たす",
                "fail": "回答がcriterionに反する、または必要内容を欠く",
                "unknown": "提示情報だけでは判定できない",
                "not_applicable": "criterionをこの回答へ適用できない",
            },
            "unit": "各回答の各assertionを独立に判定する",
            "do_not_infer_missing_facts": True,
            "do_not_compare_items": True,
        },
        "items": packet_items,
    }
    organizer_map = {
        "schema_version": "general-chat-holdout-organizer-map/v1",
        "packet_id": packet_id,
        "holdout_set_id": holdout_set_id,
        "grader_execution_id": grader_execution_id,
        "source_sha256": source_sha256,
        "mappings": mappings,
    }
    template = {
        "schema_version": "general-chat-ai-grader-label-template/v1",
        "packet_id": packet_id,
        "calibration_set_id": holdout_set_id,
        "grader_execution_id": grader_execution_id,
        "independent_context": True,
        "labels": [
            {
                "rating_item_id": item["rating_item_id"],
                "assertion_id": assertion["assertion_id"],
                "label": None,
                "evidence_spans": [],
                "reason": "",
            }
            for item in packet_items
            for assertion in item["assertions"]
        ],
    }
    return packet, organizer_map, template


def _validate_fixed_sources() -> tuple[dict[str, Any], dict[str, Any]]:
    plan = load_object(PLAN_PATH)
    holdout = load_object(HOLDOUT_PATH)
    jsonschema.Draft202012Validator(load_object(PLAN_SCHEMA_PATH)).validate(plan)
    jsonschema.Draft202012Validator(load_object(HOLDOUT_SCHEMA_PATH)).validate(holdout)
    threshold = load_object(THRESHOLD_PATH)
    if not calibration_runtime.threshold_is_bound(threshold):
        raise HoldoutReferenceError("qualification threshold is not bound")
    if plan["threshold"]["sha256"] != sha256_file(THRESHOLD_PATH):
        raise HoldoutReferenceError("threshold identity differs from holdout plan")
    if plan["holdout"]["sha256"] != sha256_file(HOLDOUT_PATH):
        raise HoldoutReferenceError("holdout identity differs from holdout plan")
    if plan["reference_generation"]["issued"] is not False:
        raise HoldoutReferenceError("reference generation is already marked issued")
    if plan["qualification_grader"]["issued"] is not False:
        raise HoldoutReferenceError("qualification grader is already marked issued")
    if REFERENCE_PATH.exists():
        raise HoldoutReferenceError("qualification reference already exists")
    members = plan["reference_generation"]["panel_members"]
    if len(members) != 3 or len(set(members)) != 3:
        raise HoldoutReferenceError("reference panel must have three unique members")
    forbidden = {plan["reference_generation"]["adjudicator"]}
    forbidden.add(plan["qualification_grader"]["execution_id"])
    if set(members) & forbidden:
        raise HoldoutReferenceError("reference execution identities are not independent")
    qualifier = plan["qualification_grader"]
    if qualifier["runtime_identity"] != f"codex-cli {RUNTIME_VERSION}":
        raise HoldoutReferenceError("qualification runtime identity mismatch")
    if qualifier["prompt_sha256"] != sha256_file(MEMBER_PROMPT_PATH):
        raise HoldoutReferenceError("member prompt hash mismatch")
    if qualifier["output_schema_sha256"] != sha256_file(CANONICAL_LABEL_SCHEMA_PATH):
        raise HoldoutReferenceError("canonical label schema hash mismatch")
    return plan, holdout


def _fixed_source_references() -> dict[str, dict[str, str]]:
    return {
        "plan": repository_reference(PLAN_PATH),
        "plan_schema": repository_reference(PLAN_SCHEMA_PATH),
        "holdout": repository_reference(HOLDOUT_PATH),
        "holdout_schema": repository_reference(HOLDOUT_SCHEMA_PATH),
        "threshold": repository_reference(THRESHOLD_PATH),
        "member_prompt": repository_reference(MEMBER_PROMPT_PATH),
        "packet_schema": repository_reference(PACKET_SCHEMA_PATH),
        "organizer_map_schema": repository_reference(ORGANIZER_MAP_SCHEMA_PATH),
        "label_template_schema": repository_reference(LABEL_TEMPLATE_SCHEMA_PATH),
        "canonical_label_schema": repository_reference(CANONICAL_LABEL_SCHEMA_PATH),
        "dispatch_schema": repository_reference(DISPATCH_SCHEMA_PATH),
        "reference_report_schema": repository_reference(REFERENCE_REPORT_SCHEMA_PATH),
        "run_result_schema": repository_reference(RUN_RESULT_SCHEMA_PATH),
        "preflight_schema": repository_reference(PREFLIGHT_SCHEMA_PATH),
        "runner": repository_reference(RUNNER_PATH),
    }


def make_preflight(run_root: Path) -> dict[str, Any]:
    run_root = ensure_external_run_root(run_root)
    if run_root.exists() and any(run_root.iterdir()):
        raise HoldoutReferenceError("preflight run root must be absent or empty")
    run_root.mkdir(parents=True, exist_ok=True)
    plan, holdout = _validate_fixed_sources()
    canonical_schema = load_object(CANONICAL_LABEL_SCHEMA_PATH)
    transport_schema = panel_runtime.project_transport_schema(canonical_schema)
    panel_runtime.validate_transport_schema(transport_schema)
    prompt = MEMBER_PROMPT_PATH.read_text(encoding="utf-8")
    try:
        runtime_binding = resolve_fixed_codex_runtime(RUNTIME_VERSION)
        verify_codex_runtime_binding(runtime_binding)
    except CodexRuntimeBindingError as error:
        raise HoldoutReferenceError(str(error)) from error

    slots: list[dict[str, Any]] = []
    for index, execution_id in enumerate(
        plan["reference_generation"]["panel_members"], start=1
    ):
        slot_dir = run_root / "material" / execution_id
        packet, organizer_map, template = make_holdout_material(
            holdout,
            grader_execution_id=execution_id,
            source_sha256=sha256_file(HOLDOUT_PATH),
        )
        stdin = panel_runtime.make_stdin(prompt, packet, template)
        paths = {
            "packet": slot_dir / "packet.json",
            "organizer_map": slot_dir / "organizer-map.json",
            "label_template": slot_dir / "label-template.json",
            "transport_schema": slot_dir / "transport-schema.json",
        }
        for name, value in (
            ("packet", packet),
            ("organizer_map", organizer_map),
            ("label_template", template),
            ("transport_schema", transport_schema),
        ):
            write_once(paths[name], value)
        stdin_path = slot_dir / "stdin.txt"
        write_bytes_once(stdin_path, stdin)
        jsonschema.Draft202012Validator(load_object(PACKET_SCHEMA_PATH)).validate(packet)
        jsonschema.Draft202012Validator(load_object(ORGANIZER_MAP_SCHEMA_PATH)).validate(
            organizer_map
        )
        jsonschema.Draft202012Validator(
            load_object(LABEL_TEMPLATE_SCHEMA_PATH)
        ).validate(template)
        slots.append(
            {
                "slot_id": f"holdout-reference-slot-{index:02d}",
                "grader_execution_id": execution_id,
                "model": "gpt-5.6-terra",
                "reasoning_effort": "medium",
                "packet": external_reference(paths["packet"]),
                "organizer_map": external_reference(paths["organizer_map"]),
                "label_template": external_reference(paths["label_template"]),
                "transport_schema": external_reference(paths["transport_schema"]),
                "stdin": external_reference(stdin_path),
            }
        )

    receipt = {
        "schema_version": "general-chat-holdout-reference-preflight/v1",
        "receipt_id": RECEIPT_ID,
        "plan_id": plan["plan_id"],
        "state": "ready_not_issued",
        "issued_slot_count": 0,
        "runtime_binding": runtime_binding,
        "fixed_sources": _fixed_source_references(),
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
        "reference_labels_forbidden_between_slots": True,
        "qualification_grader_issued": False,
        "slots": slots,
    }
    receipt["receipt_sha256"] = content_identity(receipt, "receipt_sha256")
    jsonschema.Draft202012Validator(load_object(PREFLIGHT_SCHEMA_PATH)).validate(receipt)
    write_once(run_root / "preflight.json", receipt)
    return receipt


def validate_preflight(preflight_path: Path) -> dict[str, Any]:
    preflight_path = preflight_path.resolve()
    receipt = load_object(preflight_path)
    jsonschema.Draft202012Validator(load_object(PREFLIGHT_SCHEMA_PATH)).validate(receipt)
    if receipt["receipt_sha256"] != content_identity(receipt, "receipt_sha256"):
        raise HoldoutReferenceError("preflight receipt hash mismatch")
    if Path(receipt["storage"]["run_root"]).resolve() != preflight_path.parent:
        raise HoldoutReferenceError("preflight path does not match run root")
    ensure_external_run_root(preflight_path.parent)
    plan, holdout = _validate_fixed_sources()
    if receipt["fixed_sources"] != _fixed_source_references():
        raise HoldoutReferenceError("preflight repository source drifted")
    expected_ids = plan["reference_generation"]["panel_members"]
    if [slot["grader_execution_id"] for slot in receipt["slots"]] != expected_ids:
        raise HoldoutReferenceError("preflight slot identity differs from plan")
    canonical_schema = load_object(CANONICAL_LABEL_SCHEMA_PATH)
    expected_transport = panel_runtime.project_transport_schema(canonical_schema)
    panel_runtime.validate_transport_schema(expected_transport)
    prompt = MEMBER_PROMPT_PATH.read_text(encoding="utf-8")
    for slot in receipt["slots"]:
        for field in (
            "packet",
            "organizer_map",
            "label_template",
            "transport_schema",
            "stdin",
        ):
            reference = slot[field]
            path = Path(reference["path"]).resolve()
            try:
                path.relative_to(preflight_path.parent)
            except ValueError as error:
                raise HoldoutReferenceError("preflight material escapes run root") from error
            if external_reference(path) != reference:
                raise HoldoutReferenceError(f"preflight material drifted: {field}")
        packet, organizer_map, template = make_holdout_material(
            holdout,
            grader_execution_id=slot["grader_execution_id"],
            source_sha256=sha256_file(HOLDOUT_PATH),
        )
        if load_object(Path(slot["packet"]["path"])) != packet:
            raise HoldoutReferenceError("preflight packet differs from holdout")
        if load_object(Path(slot["organizer_map"]["path"])) != organizer_map:
            raise HoldoutReferenceError("preflight organizer map differs from holdout")
        if load_object(Path(slot["label_template"]["path"])) != template:
            raise HoldoutReferenceError("preflight label template differs from holdout")
        if load_object(Path(slot["transport_schema"]["path"])) != expected_transport:
            raise HoldoutReferenceError("preflight transport schema drifted")
        expected_stdin = panel_runtime.make_stdin(prompt, packet, template)
        if Path(slot["stdin"]["path"]).read_bytes() != expected_stdin:
            raise HoldoutReferenceError("preflight stdin differs from fixed material")
    verify_codex_runtime_binding(receipt["runtime_binding"])
    return receipt


def analyze_reference_panel(
    holdout: dict[str, Any],
    organizer_maps: list[dict[str, Any]],
    labels: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return consensus labels and disagreements without sealing a reference."""
    if len(organizer_maps) != 3 or len(labels) != 3:
        raise HoldoutReferenceError("reference panel requires exactly three results")
    execution_ids = [document["grader_execution_id"] for document in labels]
    if len(set(execution_ids)) != 3:
        raise HoldoutReferenceError("reference grader identities must be unique")
    severity_by_key = {
        (item["holdout_item_id"], assertion["assertion_id"]): assertion["severity"]
        for item in holdout["items"]
        for assertion in item["assertions"]
    }
    by_canonical: dict[tuple[str, str], list[dict[str, str]]] = {}
    for organizer_map, label_document in zip(organizer_maps, labels, strict=True):
        if organizer_map["packet_id"] != label_document["packet_id"]:
            raise HoldoutReferenceError("map and label packet identity mismatch")
        if organizer_map["holdout_set_id"] != label_document["calibration_set_id"]:
            raise HoldoutReferenceError("map and label holdout identity mismatch")
        if organizer_map["grader_execution_id"] != label_document["grader_execution_id"]:
            raise HoldoutReferenceError("map and label grader identity mismatch")
        map_by_opaque = {
            row["rating_item_id"]: row for row in organizer_map["mappings"]
        }
        expected = {
            (row["rating_item_id"], assertion_id)
            for row in organizer_map["mappings"]
            for assertion_id in row["assertion_ids"]
        }
        observed: set[tuple[str, str]] = set()
        for label in label_document["labels"]:
            opaque_key = (label["rating_item_id"], label["assertion_id"])
            if opaque_key in observed or opaque_key not in expected:
                raise HoldoutReferenceError("reference label rows differ from map")
            observed.add(opaque_key)
            mapping = map_by_opaque[label["rating_item_id"]]
            canonical_key = (mapping["holdout_item_id"], label["assertion_id"])
            by_canonical.setdefault(canonical_key, []).append(
                {
                    "grader_execution_id": label_document["grader_execution_id"],
                    "label": label["label"],
                }
            )
        if observed != expected:
            raise HoldoutReferenceError("reference labels are incomplete")
    if set(by_canonical) != set(severity_by_key):
        raise HoldoutReferenceError("reference panel coverage differs from holdout")
    if any(len(rows) != 3 for rows in by_canonical.values()):
        raise HoldoutReferenceError("reference panel coverage is incomplete")

    consensus_labels: list[dict[str, str]] = []
    disagreements: list[dict[str, Any]] = []
    for key, rows in sorted(by_canonical.items()):
        holdout_item_id, assertion_id = key
        values = {row["label"] for row in rows}
        base = {
            "holdout_item_id": holdout_item_id,
            "assertion_id": assertion_id,
            "severity": severity_by_key[key],
        }
        if len(values) == 1:
            consensus_labels.append({**base, "label": next(iter(values))})
        else:
            disagreements.append({**base, "ratings": rows})
    report = {
        "schema_version": "general-chat-holdout-reference-panel-report/v1",
        "holdout_set_id": holdout["holdout_set_id"],
        "evaluation_role": "holdout_reference_formation",
        "ai_grader_count": 3,
        "assertion_count": len(severity_by_key),
        "consensus_labels": consensus_labels,
        "disagreements": disagreements,
        "reference_state": (
            "multi_grader_consensus_reference"
            if not disagreements
            else "ai_adjudication_required"
        ),
        "human_alignment_state": "unmeasured",
        "qualification_effect": "none",
    }
    jsonschema.Draft202012Validator(load_object(REFERENCE_REPORT_SCHEMA_PATH)).validate(
        report
    )
    return report


run_slot = panel_runtime.run_slot


def execute(preflight_path: Path) -> dict[str, Any]:
    """Issue the three fixed reference slots once and aggregate valid labels."""
    receipt = validate_preflight(preflight_path)
    run_root = Path(receipt["storage"]["run_root"])
    dispatch_path = run_root / "issued.json"
    result_path = run_root / "run-result.json"
    if dispatch_path.exists() or result_path.exists() or (run_root / "output").exists():
        raise HoldoutReferenceError("reference slots were already issued or partially issued")
    host_codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve()
    host_auth = host_codex_home / "auth.json"
    if not host_auth.is_file():
        raise HoldoutReferenceError("host Codex auth identity is unavailable")
    dispatch = {
        "schema_version": "general-chat-holdout-reference-panel-dispatch/v1",
        "dispatch_id": DISPATCH_ID,
        "preflight_sha256": sha256_file(preflight_path),
        "slots": [slot["slot_id"] for slot in receipt["slots"]],
        "issued_slot_count": len(receipt["slots"]),
        "state": "issued_once",
    }
    dispatch["dispatch_sha256"] = content_identity(dispatch, "dispatch_sha256")
    jsonschema.Draft202012Validator(load_object(DISPATCH_SCHEMA_PATH)).validate(dispatch)
    write_once(dispatch_path, dispatch)

    rows: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(run_slot, receipt, slot, host_auth): slot
            for slot in receipt["slots"]
        }
        for future in as_completed(futures):
            rows.append(future.result())
    rows.sort(key=lambda row: row["slot_id"])
    valid = [row for row in rows if row["status"] == "valid"]
    report_reference: dict[str, str] | None = None
    if len(valid) == 3:
        holdout = load_object(HOLDOUT_PATH)
        maps = [
            load_object(Path(slot["organizer_map"]["path"]))
            for slot in receipt["slots"]
        ]
        labels = [load_object(Path(row["label"]["path"])) for row in valid]
        report = analyze_reference_panel(holdout, maps, labels)
        report_path = run_root / "reference-panel-report.json"
        write_once(report_path, report)
        report_reference = external_reference(report_path)
    result = {
        "schema_version": "general-chat-holdout-reference-panel-run-result/v1",
        "run_id": RUN_ID,
        "plan_id": receipt["plan_id"],
        "preflight": external_reference(preflight_path),
        "dispatch": external_reference(dispatch_path),
        "slots": rows,
        "reference_report": report_reference,
        "summary": {
            "authorized_slots": 3,
            "valid_results": len(valid),
            "external_failures": sum(row["status"] == "external_failure" for row in rows),
            "unrateable_results": sum(row["status"] == "unrateable" for row in rows),
            "measurement_state": (
                "reference_measurement_established"
                if len(valid) == 3
                else "reference_measurement_not_established"
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
    validate = commands.add_parser("validate")
    validate.add_argument("--preflight", type=Path, required=True)
    run = commands.add_parser("run")
    run.add_argument("--preflight", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            receipt = make_preflight(args.run_root)
        elif args.command == "validate":
            receipt = validate_preflight(args.preflight)
        else:
            result = execute(args.preflight)
            print(json.dumps(result["summary"], ensure_ascii=False, sort_keys=True))
            return 0
    except (HoldoutReferenceError, jsonschema.ValidationError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "receipt_id": receipt["receipt_id"],
                "authorized_slot_count": len(receipt["slots"]),
                "issued_slot_count": receipt["issued_slot_count"],
                "state": receipt["state"],
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
