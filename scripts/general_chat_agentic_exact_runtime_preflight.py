#!/usr/bin/env python3
"""Verify the exact Codex CLI 0.146.0 runtime without issuing a probe."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TICKET = ROOT / "docs/general-chat-agentic-capability-preflight-ticket-r2.json"
DEFAULT_SCHEMA = ROOT / "docs/general-chat-agentic-capability-preflight-ticket-r2.schema.json"
RECEIPT_SCHEMA_VERSION = "general-chat-agentic-exact-runtime-preflight/v1"


class ExactRuntimeError(Exception):
    """The exact runtime preflight input could not be loaded."""


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ExactRuntimeError(f"cannot load JSON object: {path}") from error
    if not isinstance(value, dict):
        raise ExactRuntimeError(f"JSON value must be an object: {path}")
    return value


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def repository_identity_rejection(ticket: dict[str, Any], repo_root: Path) -> str | None:
    root = repo_root.resolve()
    identities = {
        "LINEAGE": ticket.get("lineage"),
        "TASK": (ticket.get("artifacts") or {}).get("task"),
        "FIXTURE": (ticket.get("artifacts") or {}).get("fixture"),
    }
    for label, identity in identities.items():
        if not isinstance(identity, dict) or not isinstance(identity.get("path"), str):
            return f"{label}_IDENTITY_INVALID"
        path = (root / identity["path"]).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            return f"{label}_PATH_INVALID"
        try:
            content = path.read_bytes()
        except OSError:
            return f"{label}_UNREADABLE"
        if label != "LINEAGE" and len(content) != identity.get("bytes"):
            return f"{label}_BYTES_MISMATCH"
        if hashlib.sha256(content).hexdigest() != identity.get("sha256"):
            return f"{label}_SHA256_MISMATCH"
    return None


def file_identity_rejection(identity: dict[str, Any], label: str) -> tuple[str | None, Path | None]:
    path = Path(identity.get("path", "")).resolve()
    if not path.is_file():
        return f"{label}_PATH_INVALID", None
    try:
        observed = sha256_file(path)
    except OSError:
        return f"{label}_UNREADABLE", None
    if observed != identity.get("sha256"):
        return f"{label}_SHA256_MISMATCH", None
    return None, path


def runtime_files_rejection(runtime: dict[str, Any]) -> tuple[str | None, Path | None]:
    rejection, alias_path = file_identity_rejection(runtime["alias"], "ALIAS")
    if rejection is not None:
        return rejection, None
    alias = load_object(alias_path)
    if alias != {
        "schema_version": "codex-eval-runtime-alias/v1",
        "alias": "codex-0.146",
        "runtime_id": runtime["runtime_id"],
        "mutable": False,
    }:
        return "ALIAS_CONTRACT_MISMATCH", None

    rejection, manifest_path = file_identity_rejection(runtime["manifest"], "MANIFEST")
    if rejection is not None:
        return rejection, None
    manifest = load_object(manifest_path)
    expected_manifest = {
        "schema_version": "codex-eval-runtime-manifest/v1",
        "runtime_id": runtime["runtime_id"],
        "product": runtime["product"],
        "version_output": runtime["version_output"],
        "target": runtime["target"],
        "bundle_path": runtime["bundle_path"],
        "entrypoint": runtime["entrypoint"],
        "bundle_sha256": runtime["bundle_sha256"],
        "entrypoint_sha256": runtime["entrypoint_sha256"],
        "codesign_team_identifier": runtime["codesign_team_identifier"],
        "registration_status": "registered",
    }
    if any(manifest.get(key) != value for key, value in expected_manifest.items()):
        return "MANIFEST_CONTRACT_MISMATCH", None

    bundle = Path(runtime["bundle_path"]).resolve()
    if not bundle.is_dir() or manifest_path.parent / "bundle" != bundle:
        return "BUNDLE_PATH_INVALID", None
    if bundle.stat().st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH):
        return "BUNDLE_WRITABLE", None

    expected_files = {item["path"]: item for item in runtime["file_inventory"]}
    actual_files = {
        path.relative_to(bundle).as_posix(): path
        for path in bundle.rglob("*")
        if path.is_file() and not path.is_symlink()
    }
    if set(actual_files) != set(expected_files):
        return "BUNDLE_FILE_INVENTORY_MISMATCH", None
    for relative, identity in expected_files.items():
        path = actual_files[relative]
        if path.stat().st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH):
            return "BUNDLE_FILE_WRITABLE", None
        if path.stat().st_size != identity["bytes"]:
            return "BUNDLE_FILE_BYTES_MISMATCH", None
        if sha256_file(path) != identity["sha256"]:
            return "BUNDLE_FILE_SHA256_MISMATCH", None

    expected_links = {item["path"]: item["target"] for item in runtime["symlink_inventory"]}
    actual_links = {
        path.relative_to(bundle).as_posix(): os.readlink(path)
        for path in bundle.rglob("*")
        if path.is_symlink()
    }
    if actual_links != expected_links:
        return "BUNDLE_SYMLINK_MISMATCH", None
    for relative in actual_links:
        if not (bundle / relative).resolve().is_relative_to(bundle):
            return "BUNDLE_SYMLINK_ESCAPES", None

    entrypoint = (bundle / runtime["entrypoint"]).resolve()
    if not entrypoint.is_file() or not entrypoint.is_relative_to(bundle):
        return "ENTRYPOINT_PATH_INVALID", None
    if sha256_file(entrypoint) != runtime["entrypoint_sha256"]:
        return "ENTRYPOINT_SHA256_MISMATCH", None
    return None, entrypoint


def process_identity_rejection(runtime: dict[str, Any], entrypoint: Path) -> str | None:
    try:
        version = subprocess.run(
            [str(entrypoint), "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return "ENTRYPOINT_VERSION_UNAVAILABLE"
    if version.returncode != 0 or version.stdout.strip() != runtime["version_output"]:
        return "ENTRYPOINT_VERSION_MISMATCH"
    try:
        signed = subprocess.run(
            ["codesign", "-dv", "--verbose=4", str(entrypoint)],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return "CODESIGN_UNAVAILABLE"
    evidence = signed.stdout + signed.stderr
    if signed.returncode != 0 or f"TeamIdentifier={runtime['codesign_team_identifier']}" not in evidence:
        return "CODESIGN_TEAM_MISMATCH"
    return None


def verify_ticket(ticket: dict[str, Any], schema: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    schema_error = next(jsonschema.Draft202012Validator(schema).iter_errors(ticket), None)
    rejection = "TICKET_SCHEMA_INVALID" if schema_error is not None else None
    if rejection is None:
        rejection = repository_identity_rejection(ticket, repo_root)
    entrypoint = None
    if rejection is None:
        rejection, entrypoint = runtime_files_rejection(ticket["runtime_ref"])
    if rejection is None and entrypoint is not None:
        rejection = process_identity_rejection(ticket["runtime_ref"], entrypoint)
    runtime_verified = rejection is None
    dispatch_reasons = []
    if rejection is not None:
        dispatch_reasons.append(rejection)
    else:
        if ticket["real_trace_adapter_ready"] is not True:
            dispatch_reasons.append("REAL_TRACE_ADAPTER_NOT_READY")
        if ticket["issuance_authority"] != "authorized_not_issued":
            dispatch_reasons.append("ISSUANCE_NOT_AUTHORIZED")
    return {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "probe_id": ticket.get("probe_id"),
        "model_invocations": 0,
        "runtime_identity_state": "verified" if runtime_verified else "unavailable",
        "runtime_id": ticket.get("runtime_ref", {}).get("runtime_id"),
        "entrypoint": str(entrypoint) if runtime_verified and entrypoint is not None else None,
        "dispatch_state": "allowed" if runtime_verified and not dispatch_reasons else "denied",
        "reasons": dispatch_reasons,
    }


def validate_ticket(ticket_path: Path, schema_path: Path, repo_root: Path) -> dict[str, Any]:
    ticket = load_object(ticket_path)
    schema = load_object(schema_path)
    jsonschema.Draft202012Validator.check_schema(schema)
    result = verify_ticket(ticket, schema, repo_root)
    result["ticket_sha256"] = sha256_file(ticket_path)
    return result


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--ticket", type=Path, default=DEFAULT_TICKET)
    value.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    value.add_argument("--repo-root", type=Path, default=ROOT)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        result = validate_ticket(args.ticket.resolve(), args.schema.resolve(), args.repo_root.resolve())
    except (ExactRuntimeError, jsonschema.SchemaError) as error:
        print(json.dumps({"schema_version": RECEIPT_SCHEMA_VERSION, "status": "validator_error", "error": str(error)}, ensure_ascii=False, sort_keys=True))
        return 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
