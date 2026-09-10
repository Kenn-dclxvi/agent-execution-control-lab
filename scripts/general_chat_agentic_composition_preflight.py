#!/usr/bin/env python3
"""Compose exact runtime and synthetic adapter evidence without issuing a probe."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from pathlib import Path
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "docs/general-chat-agentic-composition-preflight-r1.json"
DEFAULT_SCHEMA = ROOT / "docs/general-chat-agentic-composition-preflight-input.schema.json"
RECEIPT_SCHEMA_VERSION = "general-chat-agentic-composition-preflight/v1"


class CompositionError(Exception):
    """A composition boundary or expected state did not match."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def load_object(path: Path, code: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CompositionError(code) from error
    if not isinstance(value, dict):
        raise CompositionError(code)
    return value


def canonical_sha256(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def validate_input(value: dict[str, Any], schema: dict[str, Any]) -> None:
    try:
        jsonschema.Draft202012Validator.check_schema(schema)
        jsonschema.Draft202012Validator(schema).validate(value)
    except (jsonschema.SchemaError, jsonschema.ValidationError) as error:
        raise CompositionError("COMPOSITION_INPUT_SCHEMA_INVALID") from error


def resolve_identity(repository_root: Path, identity: dict[str, Any]) -> Path:
    root = repository_root.resolve()
    path = (root / identity["path"]).resolve()
    try:
        path.relative_to(root)
    except ValueError as error:
        raise CompositionError("COMPOSITION_PATH_OUTSIDE_REPOSITORY") from error
    if not path.is_file():
        raise CompositionError("COMPOSITION_FILE_UNAVAILABLE")
    try:
        data = path.read_bytes()
    except OSError as error:
        raise CompositionError("COMPOSITION_FILE_UNAVAILABLE") from error
    if len(data) != identity["bytes"]:
        raise CompositionError("COMPOSITION_FILE_BYTES_MISMATCH")
    if hashlib.sha256(data).hexdigest() != identity["sha256"]:
        raise CompositionError("COMPOSITION_FILE_HASH_MISMATCH")
    return path


def bound_paths(value: dict[str, Any], repository_root: Path) -> dict[str, Path]:
    identities = {
        "output_schema": value["output_schema"],
        "runtime_ticket": value["runtime"]["ticket"],
        "runtime_schema": value["runtime"]["schema"],
        "runtime_validator": value["runtime"]["validator"],
        "adapter_packet": value["adapter"]["packet"],
        "adapter_packet_schema": value["adapter"]["packet_schema"],
        "adapter_validator": value["adapter"]["validator"],
        "adapter_normalizer": value["adapter"]["normalizer"],
        "adapter_normalized_schema": value["adapter"]["normalized_schema"],
        "binding_evaluator": value["binding"]["evaluator"],
        "binding_fixture": value["binding"]["fixture"],
    }
    return {name: resolve_identity(repository_root, identity) for name, identity in identities.items()}


def dependency_modules() -> tuple[Any, Any, Any]:
    try:
        runtime = importlib.import_module("scripts.general_chat_agentic_exact_runtime_preflight")
        adapter = importlib.import_module("scripts.general_chat_agentic_real_trace_adapter")
        binding = importlib.import_module("scripts.general_chat_agentic_binding_extractor")
    except ModuleNotFoundError:
        runtime = importlib.import_module("general_chat_agentic_exact_runtime_preflight")
        adapter = importlib.import_module("general_chat_agentic_real_trace_adapter")
        binding = importlib.import_module("general_chat_agentic_binding_extractor")
    return runtime, adapter, binding


def compose(value: dict[str, Any], repository_root: Path = ROOT) -> dict[str, Any]:
    paths = bound_paths(value, repository_root)
    runtime_module, adapter_module, binding_module = dependency_modules()

    ticket = load_object(paths["runtime_ticket"], "RUNTIME_TICKET_INVALID")
    packet = load_object(paths["adapter_packet"], "ADAPTER_PACKET_INVALID")
    if (
        ticket.get("probe_id") != value["probe_id"]
        or packet.get("probe_id") != value["probe_id"]
        or packet.get("runtime_id") != (ticket.get("runtime_ref") or {}).get("runtime_id")
        or packet.get("normalized_output_schema") != value["adapter"]["normalized_schema"]
    ):
        raise CompositionError("COMPOSITION_IDENTITY_RELATION_MISMATCH")

    runtime_receipt = runtime_module.validate_ticket(
        paths["runtime_ticket"], paths["runtime_schema"], repository_root
    )
    packet_schema = load_object(paths["adapter_packet_schema"], "ADAPTER_PACKET_SCHEMA_INVALID")
    adapter_module.validate_packet(packet, packet_schema)
    normalized = adapter_module.adapt_packet(packet, repository_root)
    fixture = load_object(paths["binding_fixture"], "BINDING_FIXTURE_INVALID")
    binding_result = binding_module.extract(normalized, fixture)

    receipt = {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "composition_id": value["composition_id"],
        "probe_id": value["probe_id"],
        "runtime_identity_state": runtime_receipt["runtime_identity_state"],
        "runtime_id": runtime_receipt["runtime_id"],
        "adapter_state": "synthetic_verified",
        "adapter_input_mode": packet["input_mode"],
        "normalized_output_sha256": canonical_sha256(normalized),
        "binding_criteria": binding_result["criteria"],
        "binding_admission": binding_result["admission"],
        "ticket_real_trace_adapter_ready": ticket["real_trace_adapter_ready"],
        "issuance_authority": ticket["issuance_authority"],
        "dispatch_state": runtime_receipt["dispatch_state"],
        "reasons": runtime_receipt["reasons"],
        "model_invocations": runtime_receipt["model_invocations"],
        "real_trace_reads": 0,
        "probe_issues": 0,
    }
    expected = value["expected"]
    observed = {
        "runtime_identity_state": receipt["runtime_identity_state"],
        "adapter_state": receipt["adapter_state"],
        "normalized_output_sha256": receipt["normalized_output_sha256"],
        "binding_criteria": receipt["binding_criteria"],
        "binding_admission": receipt["binding_admission"],
        "dispatch_state": receipt["dispatch_state"],
        "reasons": receipt["reasons"],
        "model_invocations": receipt["model_invocations"],
        "real_trace_reads": receipt["real_trace_reads"],
        "probe_issues": receipt["probe_issues"],
    }
    if observed != expected:
        raise CompositionError("COMPOSITION_EXPECTED_STATE_MISMATCH")
    if receipt["ticket_real_trace_adapter_ready"] is not False:
        raise CompositionError("REAL_TRACE_ADAPTER_GATE_CHANGED")
    if receipt["issuance_authority"] != "not_authorized":
        raise CompositionError("ISSUANCE_AUTHORITY_CHANGED")
    output_schema = load_object(paths["output_schema"], "COMPOSITION_OUTPUT_SCHEMA_INVALID")
    try:
        jsonschema.Draft202012Validator.check_schema(output_schema)
        jsonschema.Draft202012Validator(output_schema).validate(receipt)
    except (jsonschema.SchemaError, jsonschema.ValidationError) as error:
        raise CompositionError("COMPOSITION_OUTPUT_SCHEMA_INVALID") from error
    return receipt


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    value.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    value.add_argument("--repo-root", type=Path, default=ROOT)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        value = load_object(args.input.resolve(), "COMPOSITION_INPUT_UNAVAILABLE")
        schema = load_object(args.schema.resolve(), "COMPOSITION_SCHEMA_UNAVAILABLE")
        validate_input(value, schema)
        receipt = compose(value, args.repo_root.resolve())
    except CompositionError as error:
        print(
            json.dumps(
                {
                    "schema_version": RECEIPT_SCHEMA_VERSION,
                    "status": "composition_error",
                    "reason": error.code,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 2
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
