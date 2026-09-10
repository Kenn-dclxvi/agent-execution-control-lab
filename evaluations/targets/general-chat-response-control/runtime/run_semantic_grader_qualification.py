#!/usr/bin/env python3
"""Prepare and execute the fixed semantic grader qualification once."""

from __future__ import annotations

import argparse
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
REFERENCE_PATH = CALIBRATION / "qualification-reference-r1.json"
REFERENCE_SCHEMA_PATH = CALIBRATION / "qualification-reference-r1.schema.json"
THRESHOLD_PATH = CALIBRATION / "qualification-threshold-r1.json"
METRIC_PATH = CALIBRATION / "qualification-metric-contract-r1.json"
METRIC_SCHEMA_PATH = CALIBRATION / "qualification-metric-contract-r1.schema.json"
MEMBER_PROMPT_PATH = TARGET / "rating-contracts/general-chat-semantic-panel-member-r1.txt"
PACKET_SCHEMA_PATH = CALIBRATION / "rater-packet-r1.schema.json"
ORGANIZER_MAP_SCHEMA_PATH = CALIBRATION / "holdout-organizer-map-r1.schema.json"
LABEL_TEMPLATE_SCHEMA_PATH = CALIBRATION / "ai-grader-label-template-r1.schema.json"
CANONICAL_LABEL_SCHEMA_PATH = CALIBRATION / "ai-grader-label-r1.schema.json"
QUALIFICATION_REPORT_SCHEMA_PATH = CALIBRATION / "grader-qualification-report-r1.schema.json"
PREFLIGHT_SCHEMA_PATH = CALIBRATION / "qualification-grader-preflight-r1.schema.json"
DISPATCH_SCHEMA_PATH = CALIBRATION / "qualification-grader-dispatch-r1.schema.json"
RUN_RESULT_SCHEMA_PATH = CALIBRATION / "qualification-grader-run-result-r1.schema.json"
RUNNER_PATH = Path(__file__).resolve()
RUNTIME_VERSION = "0.148.0"
RECEIPT_ID = "general-chat-semantic-qualification-grader-r1-preflight-r1"
DISPATCH_ID = "general-chat-semantic-qualification-grader-r1-dispatch-r1"
RUN_ID = "general-chat-semantic-qualification-grader-r1-run-r1"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


panel_runtime = _load_module(
    "general_chat_qualification_panel_runtime",
    Path(__file__).with_name("run_ai_grader_panel.py"),
)
holdout_runtime = _load_module(
    "general_chat_qualification_holdout_runtime",
    Path(__file__).with_name("run_holdout_reference_panel.py"),
)
calibration_runtime = _load_module(
    "general_chat_qualification_calibration_runtime",
    Path(__file__).with_name("prepare_semantic_calibration.py"),
)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.codex_runtime_binding import (  # noqa: E402
    CodexRuntimeBindingError,
    resolve_fixed_codex_runtime,
    verify_codex_runtime_binding,
)


class QualificationError(RuntimeError):
    """Qualification preparation or execution violated the fixed contract."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise QualificationError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise QualificationError(f"expected JSON object: {path}")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def content_identity(value: dict[str, Any], field: str) -> str:
    payload = {key: item for key, item in value.items() if key != field}
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def repository_reference(path: Path) -> dict[str, str]:
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(ROOT)
    except ValueError as error:
        raise QualificationError(f"repository source escapes root: {resolved}") from error
    if not resolved.is_file():
        raise QualificationError(f"repository source is unavailable: {resolved}")
    return {"path": str(relative), "sha256": sha256_file(resolved)}


def external_reference(path: Path) -> dict[str, str]:
    resolved = path.resolve()
    if not resolved.is_file():
        raise QualificationError(f"external material is unavailable: {resolved}")
    return {"path": str(resolved), "sha256": sha256_file(resolved)}


def ensure_external_run_root(path: Path) -> Path:
    resolved = path.resolve()
    try:
        resolved.relative_to(ROOT)
    except ValueError:
        return resolved
    raise QualificationError("run root must be outside the repository")


def write_once(path: Path, value: dict[str, Any]) -> None:
    if path.exists():
        raise QualificationError(f"refusing to overwrite artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_bytes_once(path: Path, value: bytes) -> None:
    if path.exists():
        raise QualificationError(f"refusing to overwrite artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value)


def _validate_fixed_sources() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    plan = load_object(PLAN_PATH)
    holdout = load_object(HOLDOUT_PATH)
    reference = load_object(REFERENCE_PATH)
    threshold = load_object(THRESHOLD_PATH)
    metric = load_object(METRIC_PATH)
    for schema_path, value in (
        (PLAN_SCHEMA_PATH, plan),
        (HOLDOUT_SCHEMA_PATH, holdout),
        (REFERENCE_SCHEMA_PATH, reference),
        (METRIC_SCHEMA_PATH, metric),
    ):
        jsonschema.Draft202012Validator(load_object(schema_path)).validate(value)
    if not calibration_runtime.threshold_is_bound(threshold):
        raise QualificationError("qualification threshold is not bound")
    if plan["threshold"]["sha256"] != sha256_file(THRESHOLD_PATH):
        raise QualificationError("threshold identity differs from plan")
    if plan["holdout"]["sha256"] != sha256_file(HOLDOUT_PATH):
        raise QualificationError("holdout identity differs from plan")
    if metric["threshold_sha256"] != sha256_file(THRESHOLD_PATH):
        raise QualificationError("metric threshold identity drifted")
    if metric["reference_sha256"] != sha256_file(REFERENCE_PATH):
        raise QualificationError("metric reference identity drifted")
    if reference["holdout_sha256"] != sha256_file(HOLDOUT_PATH):
        raise QualificationError("reference holdout identity drifted")
    if reference["status"] != "sealed" or reference["ambiguous_item_count"] != 0:
        raise QualificationError("qualification reference is not unambiguously sealed")
    qualifier = plan["qualification_grader"]
    if qualifier["issued"] is not False or qualifier["run_count"] != 1:
        raise QualificationError("qualification grader issuance plan drifted")
    if qualifier["runtime_identity"] != f"codex-cli {RUNTIME_VERSION}":
        raise QualificationError("qualification runtime identity mismatch")
    if qualifier["prompt_sha256"] != sha256_file(MEMBER_PROMPT_PATH):
        raise QualificationError("qualification prompt hash mismatch")
    if qualifier["output_schema_sha256"] != sha256_file(CANONICAL_LABEL_SCHEMA_PATH):
        raise QualificationError("qualification label schema hash mismatch")
    return plan, holdout, reference, threshold


def _fixed_sources() -> dict[str, dict[str, str]]:
    return {
        "plan": repository_reference(PLAN_PATH),
        "plan_schema": repository_reference(PLAN_SCHEMA_PATH),
        "holdout": repository_reference(HOLDOUT_PATH),
        "holdout_schema": repository_reference(HOLDOUT_SCHEMA_PATH),
        "reference": repository_reference(REFERENCE_PATH),
        "reference_schema": repository_reference(REFERENCE_SCHEMA_PATH),
        "threshold": repository_reference(THRESHOLD_PATH),
        "metric_contract": repository_reference(METRIC_PATH),
        "metric_contract_schema": repository_reference(METRIC_SCHEMA_PATH),
        "member_prompt": repository_reference(MEMBER_PROMPT_PATH),
        "packet_schema": repository_reference(PACKET_SCHEMA_PATH),
        "organizer_map_schema": repository_reference(ORGANIZER_MAP_SCHEMA_PATH),
        "label_template_schema": repository_reference(LABEL_TEMPLATE_SCHEMA_PATH),
        "canonical_label_schema": repository_reference(CANONICAL_LABEL_SCHEMA_PATH),
        "qualification_report_schema": repository_reference(QUALIFICATION_REPORT_SCHEMA_PATH),
        "dispatch_schema": repository_reference(DISPATCH_SCHEMA_PATH),
        "run_result_schema": repository_reference(RUN_RESULT_SCHEMA_PATH),
        "preflight_schema": repository_reference(PREFLIGHT_SCHEMA_PATH),
        "runner": repository_reference(RUNNER_PATH),
    }


def make_preflight(run_root: Path) -> dict[str, Any]:
    run_root = ensure_external_run_root(run_root)
    if run_root.exists() and any(run_root.iterdir()):
        raise QualificationError("preflight run root must be absent or empty")
    run_root.mkdir(parents=True, exist_ok=True)
    plan, holdout, _, _ = _validate_fixed_sources()
    qualifier = plan["qualification_grader"]
    canonical_schema = load_object(CANONICAL_LABEL_SCHEMA_PATH)
    transport_schema = panel_runtime.project_transport_schema(canonical_schema)
    panel_runtime.validate_transport_schema(transport_schema)
    packet, organizer_map, template = holdout_runtime.make_holdout_material(
        holdout,
        grader_execution_id=qualifier["execution_id"],
        source_sha256=sha256_file(HOLDOUT_PATH),
    )
    prompt = MEMBER_PROMPT_PATH.read_text(encoding="utf-8")
    stdin = panel_runtime.make_stdin(prompt, packet, template)
    for canonical_id in (item["holdout_item_id"] for item in holdout["items"]):
        if canonical_id.encode() in stdin:
            raise QualificationError("canonical holdout identity leaked into grader stdin")
    try:
        binding = resolve_fixed_codex_runtime(RUNTIME_VERSION)
        verify_codex_runtime_binding(binding)
    except CodexRuntimeBindingError as error:
        raise QualificationError(str(error)) from error
    material = run_root / "material" / qualifier["execution_id"]
    paths = {
        "packet": material / "packet.json",
        "organizer_map": material / "organizer-map.json",
        "label_template": material / "label-template.json",
        "transport_schema": material / "transport-schema.json",
    }
    for name, value in (
        ("packet", packet),
        ("organizer_map", organizer_map),
        ("label_template", template),
        ("transport_schema", transport_schema),
    ):
        write_once(paths[name], value)
    stdin_path = material / "stdin.txt"
    write_bytes_once(stdin_path, stdin)
    jsonschema.Draft202012Validator(load_object(PACKET_SCHEMA_PATH)).validate(packet)
    jsonschema.Draft202012Validator(load_object(ORGANIZER_MAP_SCHEMA_PATH)).validate(organizer_map)
    jsonschema.Draft202012Validator(load_object(LABEL_TEMPLATE_SCHEMA_PATH)).validate(template)
    receipt = {
        "schema_version": "general-chat-qualification-grader-preflight/v1",
        "receipt_id": RECEIPT_ID,
        "plan_id": plan["plan_id"],
        "state": "ready_not_issued",
        "issued_slot_count": 0,
        "runtime_binding": binding,
        "fixed_sources": _fixed_sources(),
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
        "reference_labels_in_model_input": False,
        "organizer_map_in_model_input": False,
        "slot": {
            "slot_id": "qualification-slot-01",
            "grader_identity": qualifier["grader_identity"],
            "grader_execution_id": qualifier["execution_id"],
            "model": qualifier["model"],
            "reasoning_effort": qualifier["reasoning_effort"],
            "run_count": 1,
            "packet": external_reference(paths["packet"]),
            "organizer_map": external_reference(paths["organizer_map"]),
            "label_template": external_reference(paths["label_template"]),
            "transport_schema": external_reference(paths["transport_schema"]),
            "stdin": external_reference(stdin_path),
        },
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
        raise QualificationError("preflight receipt hash mismatch")
    if Path(receipt["storage"]["run_root"]).resolve() != preflight_path.parent:
        raise QualificationError("preflight run root mismatch")
    ensure_external_run_root(preflight_path.parent)
    plan, holdout, _, _ = _validate_fixed_sources()
    if receipt["fixed_sources"] != _fixed_sources():
        raise QualificationError("preflight repository source drifted")
    qualifier = plan["qualification_grader"]
    if receipt["slot"]["grader_execution_id"] != qualifier["execution_id"]:
        raise QualificationError("qualification execution identity drifted")
    packet, organizer_map, template = holdout_runtime.make_holdout_material(
        holdout,
        grader_execution_id=qualifier["execution_id"],
        source_sha256=sha256_file(HOLDOUT_PATH),
    )
    transport = panel_runtime.project_transport_schema(load_object(CANONICAL_LABEL_SCHEMA_PATH))
    prompt = MEMBER_PROMPT_PATH.read_text(encoding="utf-8")
    expected = {
        "packet": packet,
        "organizer_map": organizer_map,
        "label_template": template,
        "transport_schema": transport,
    }
    for field, value in expected.items():
        ref = receipt["slot"][field]
        path = Path(ref["path"]).resolve()
        try:
            path.relative_to(preflight_path.parent)
        except ValueError as error:
            raise QualificationError("qualification material escapes run root") from error
        if external_reference(path) != ref or load_object(path) != value:
            raise QualificationError(f"qualification material drifted: {field}")
    stdin_ref = receipt["slot"]["stdin"]
    stdin_path = Path(stdin_ref["path"]).resolve()
    if external_reference(stdin_path) != stdin_ref:
        raise QualificationError("qualification stdin drifted")
    if stdin_path.read_bytes() != panel_runtime.make_stdin(prompt, packet, template):
        raise QualificationError("qualification stdin differs from fixed inputs")
    verify_codex_runtime_binding(receipt["runtime_binding"])
    if resolve_fixed_codex_runtime(RUNTIME_VERSION) != receipt["runtime_binding"]:
        raise QualificationError("qualification runtime binding drifted")
    return receipt


def calculate_qualification_report(
    receipt: dict[str, Any], label: dict[str, Any]
) -> dict[str, Any]:
    reference = load_object(REFERENCE_PATH)
    threshold = load_object(THRESHOLD_PATH)
    organizer_map = load_object(Path(receipt["slot"]["organizer_map"]["path"]))
    map_by_opaque = {row["rating_item_id"]: row for row in organizer_map["mappings"]}
    predicted: dict[tuple[str, str], str] = {}
    for row in label["labels"]:
        mapping = map_by_opaque.get(row["rating_item_id"])
        if mapping is None or row["assertion_id"] not in mapping["assertion_ids"]:
            raise QualificationError("qualification label cannot be mapped to holdout")
        key = (mapping["holdout_item_id"], row["assertion_id"])
        if key in predicted:
            raise QualificationError("duplicate qualification label")
        predicted[key] = row["label"]
    reference_by_key = {
        (row["holdout_item_id"], row["assertion_id"]): row
        for row in reference["labels"]
    }
    if set(predicted) != set(reference_by_key):
        raise QualificationError("qualification label coverage differs from reference")
    total = len(reference_by_key)
    reference_fail = sum(row["label"] == "fail" for row in reference_by_key.values())
    reference_pass = sum(row["label"] == "pass" for row in reference_by_key.values())
    exact = sum(predicted[key] == row["label"] for key, row in reference_by_key.items())
    false_pass = sum(row["label"] == "fail" and predicted[key] == "pass" for key, row in reference_by_key.items())
    false_fail = sum(row["label"] == "pass" and predicted[key] == "fail" for key, row in reference_by_key.items())
    unknown = sum(value == "unknown" for value in predicted.values())
    major_false_pass = sum(row["severity"] == "major" and row["label"] == "fail" and predicted[key] == "pass" for key, row in reference_by_key.items())
    metrics = {
        "reference_assertion_count": total,
        "exact_agreement_count": exact,
        "exact_agreement_rate": exact / total,
        "false_pass_count": false_pass,
        "false_pass_rate": false_pass / reference_fail if reference_fail else 0,
        "false_fail_count": false_fail,
        "false_fail_rate": false_fail / reference_pass if reference_pass else 0,
        "unknown_count": unknown,
        "unknown_rate": unknown / total,
        "major_false_pass_count": major_false_pass,
    }
    criteria = threshold["criteria"]
    passed = (
        metrics["exact_agreement_rate"] >= criteria["minimum_exact_agreement_rate"]
        and metrics["false_pass_rate"] <= criteria["maximum_false_pass_rate"]
        and metrics["false_fail_rate"] <= criteria["maximum_false_fail_rate"]
        and metrics["unknown_rate"] <= criteria["maximum_unknown_rate"]
        and metrics["major_false_pass_count"] <= criteria["maximum_major_false_pass_count"]
    )
    report = {
        "schema_version": "general-chat-grader-qualification-report/v1",
        "evaluation_role": "heldout_grader_qualification",
        "holdout_identity": {
            "set_id": load_object(HOLDOUT_PATH)["holdout_set_id"],
            "input_sha256": sha256_file(HOLDOUT_PATH),
            "reference_sha256": sha256_file(REFERENCE_PATH),
            "pilot_overlap_count": 0,
            "sealed_before_grader_run": True,
        },
        "reference_identity": {
            "type": reference["reference_type"],
            "ai_grader_count": reference["ai_grader_count"],
            "human_auditor_count": reference["human_auditor_count"],
            "human_alignment_state": reference["human_alignment_state"],
        },
        "grader_identity": receipt["slot"]["grader_identity"],
        "threshold_identity": {
            "threshold_contract_id": threshold["threshold_contract_id"],
            "sha256": sha256_file(THRESHOLD_PATH),
            "status": threshold["status"],
        },
        "metrics": metrics,
        "qualification_state": "passed" if passed else "failed",
        "run_count": 1,
        "formal_evaluation_effect": "grader_qualified" if passed else "grader_not_qualified",
    }
    jsonschema.Draft202012Validator(load_object(QUALIFICATION_REPORT_SCHEMA_PATH)).validate(report)
    return report


run_slot = panel_runtime.run_slot


def execute(preflight_path: Path) -> dict[str, Any]:
    receipt = validate_preflight(preflight_path)
    run_root = Path(receipt["storage"]["run_root"])
    dispatch_path = run_root / "issued.json"
    result_path = run_root / "run-result.json"
    if dispatch_path.exists() or result_path.exists() or (run_root / "output").exists():
        raise QualificationError("qualification slot was already issued or partially issued")
    host_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve()
    host_auth = host_home / "auth.json"
    if not host_auth.is_file():
        raise QualificationError("host Codex auth identity is unavailable")
    dispatch = {
        "schema_version": "general-chat-qualification-grader-dispatch/v1",
        "dispatch_id": DISPATCH_ID,
        "preflight_sha256": sha256_file(preflight_path),
        "slot_id": receipt["slot"]["slot_id"],
        "issued_slot_count": 1,
        "state": "issued_once",
    }
    dispatch["dispatch_sha256"] = content_identity(dispatch, "dispatch_sha256")
    jsonschema.Draft202012Validator(load_object(DISPATCH_SCHEMA_PATH)).validate(dispatch)
    write_once(dispatch_path, dispatch)
    row = run_slot(receipt, receipt["slot"], host_auth)
    report_ref = None
    if row["status"] == "valid":
        label = load_object(Path(row["label"]["path"]))
        report = calculate_qualification_report(receipt, label)
        report_path = run_root / "qualification-report.json"
        write_once(report_path, report)
        report_ref = external_reference(report_path)
    result = {
        "schema_version": "general-chat-qualification-grader-run-result/v1",
        "run_id": RUN_ID,
        "preflight": external_reference(preflight_path),
        "dispatch": external_reference(dispatch_path),
        "slot": row,
        "qualification_report": report_ref,
        "measurement_state": "qualification_measurement_established" if report_ref else "qualification_measurement_not_established",
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
            output = {"receipt_id": receipt["receipt_id"], "state": receipt["state"], "issued_slot_count": 0}
        elif args.command == "validate":
            receipt = validate_preflight(args.preflight)
            output = {"receipt_id": receipt["receipt_id"], "state": receipt["state"], "issued_slot_count": 0}
        else:
            result = execute(args.preflight)
            output = {"measurement_state": result["measurement_state"], "slot_status": result["slot"]["status"]}
    except (QualificationError, jsonschema.ValidationError, CodexRuntimeBindingError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
