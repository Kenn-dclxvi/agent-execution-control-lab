#!/usr/bin/env python3
"""Materialize one model-visible semantic protocol case and a private receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
from typing import Any


class MaterializationError(Exception):
    pass


TASK_INSTRUCTION = (
    "Return exactly one JSON object that satisfies response_schema for the supplied case. "
    "Do not add explanations or fields."
)


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise MaterializationError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise MaterializationError(f"expected JSON object: {path}")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_once(path: Path, value: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as stream:
            stream.write(value)
    except FileExistsError as error:
        raise MaterializationError(f"refusing to overwrite: {path}") from error


def select_case(cases: dict[str, Any], case_id: str) -> dict[str, Any]:
    entries = cases.get("cases")
    if not isinstance(entries, list):
        raise MaterializationError("cases must be an array")
    selected = [entry for entry in entries if isinstance(entry, dict) and entry.get("case_id") == case_id]
    if len(selected) != 1:
        raise MaterializationError(f"case_id must resolve exactly once: {case_id}")
    return selected[0]


def target_subject_ref(descriptor: dict[str, Any], response_schema_path: Path) -> dict[str, Any]:
    if descriptor.get("schema_version") != "the-caption-prompt.evaluation-target/v2":
        raise MaterializationError("descriptor is not evaluation target v2")
    if descriptor.get("target_kind") != "semantic_protocol":
        raise MaterializationError("descriptor is not a semantic protocol target")
    subject = descriptor.get("target_subject")
    if not isinstance(subject, dict) or subject.get("kind") != "semantic_protocol":
        raise MaterializationError("semantic protocol subject is invalid")
    if subject.get("response_schema_sha256") != sha256_file(response_schema_path):
        raise MaterializationError("response schema hash does not match target subject")
    return {
        "kind": subject["kind"],
        "protocol_id": subject["protocol_id"],
        "protocol_revision": subject["protocol_revision"],
        "interaction_mode": subject["interaction_mode"],
        "response_schema_sha256": subject["response_schema_sha256"],
    }


def materialize(
    descriptor_path: Path,
    cases_path: Path,
    response_schema_path: Path,
    case_id: str,
    output: Path,
) -> dict[str, Any]:
    descriptor_path = descriptor_path.resolve()
    cases_path = cases_path.resolve()
    response_schema_path = response_schema_path.resolve()
    output = output.resolve()
    if output.exists():
        raise MaterializationError(f"refusing to overwrite output: {output}")

    descriptor = load_object(descriptor_path)
    cases = load_object(cases_path)
    response_schema = load_object(response_schema_path)
    subject = target_subject_ref(descriptor, response_schema_path)
    selected = select_case(cases, case_id)
    if selected.get("required_response_schema") != "portable-instruction-control-response/r2":
        raise MaterializationError("case response schema identity mismatch")

    packet = {
        "schema_version": "portable-instruction-semantic-model-packet/v1",
        "task_spec": {"instruction": TASK_INSTRUCTION, "response_schema": response_schema},
        "case": selected,
    }
    packet_bytes = canonical_json_bytes(packet)
    receipt = {
        "schema_version": "portable-instruction-semantic-materialization-receipt/v1",
        "case_id": case_id,
        "case_revision": selected.get("case_revision"),
        "target_subject_ref": subject,
        "sources": {
            "descriptor": {"path": str(descriptor_path), "sha256": sha256_file(descriptor_path)},
            "cases": {"path": str(cases_path), "sha256": sha256_file(cases_path)},
            "response_schema": {"path": str(response_schema_path), "sha256": sha256_file(response_schema_path)},
        },
        "model_visible": {"path": "model-visible/input.json", "sha256": sha256_bytes(packet_bytes)},
        "private": {"path": "private/materialization-receipt.json"},
        "excluded_from_model_visible": ["oracle", "rating_contract", "freeze", "other_cases", "materialization_receipt"],
    }
    try:
        write_once(output / "model-visible/input.json", packet_bytes)
        write_once(output / "private/materialization-receipt.json", canonical_json_bytes(receipt))
    except Exception:
        if output.exists():
            shutil.rmtree(output)
        raise
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--descriptor", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--response-schema", type=Path, required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        receipt = materialize(
            args.descriptor,
            args.cases,
            args.response_schema,
            args.case_id,
            args.output,
        )
    except MaterializationError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
