#!/usr/bin/env python3
"""Run one ticket-bound Claude Code measurement transport probe."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import time
from typing import Any


RECEIPT_SCHEMA = "claude-measurement-transport-receipt/v1"
SECRET_MARKERS = (
    b"sk-ant-",
    b"ANTHROPIC_API_KEY=",
    b"Authorization:",
    b"Bearer ",
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def file_mode(path: Path) -> str:
    return f"{stat.S_IMODE(path.stat().st_mode):04o}"


def write_private(path: Path, value: bytes) -> None:
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "wb") as stream:
        stream.write(value)


def secret_marker_names(*values: bytes) -> list[str]:
    matches = []
    for marker in SECRET_MARKERS:
        if any(marker in value for value in values):
            matches.append(marker.decode("ascii", errors="replace"))
    return matches


def terminal_projection(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "top_level_keys": sorted(value),
        "is_error": value.get("is_error"),
        "type": value.get("type"),
        "subtype": value.get("subtype"),
        "terminal_reason": value.get("terminal_reason"),
        "api_error_status": value.get("api_error_status"),
        "permission_denials": value.get("permission_denials"),
        "structured_output": value.get("structured_output"),
        "session_id": value.get("session_id"),
        "uuid": value.get("uuid"),
        "usage": value.get("usage"),
        "modelUsage": value.get("modelUsage"),
        "num_turns": value.get("num_turns"),
        "stop_reason": value.get("stop_reason"),
        "duration_ms": value.get("duration_ms"),
        "duration_api_ms": value.get("duration_api_ms"),
    }


def validate_ticket(ticket: dict[str, Any], ticket_path: Path) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "probe_id",
        "expected_cli_version",
        "executable",
        "arguments",
        "expected_structured_output",
        "harness_path",
        "harness_sha256",
        "attempts",
        "timeout_seconds",
    }
    if set(ticket) != required:
        errors.append(f"ticket_fields={sorted(ticket)}")
    if ticket.get("schema_version") != "claude-measurement-transport-ticket/v1":
        errors.append("ticket_schema_version")
    if ticket.get("probe_id") != "claude-measurement-transport-r2":
        errors.append("probe_id")
    if ticket.get("attempts") != 1:
        errors.append("attempts")
    if ticket.get("timeout_seconds") != 120:
        errors.append("timeout_seconds")
    harness_path = Path(ticket.get("harness_path", ""))
    if not harness_path.is_absolute() or not harness_path.is_file():
        errors.append("harness_path")
    elif sha256_file(harness_path) != ticket.get("harness_sha256"):
        errors.append("harness_sha256")
    if not ticket_path.is_absolute():
        errors.append("ticket_path_not_absolute")
    return errors


def run_probe(ticket_path: Path) -> dict[str, Any]:
    ticket = json.loads(ticket_path.read_text(encoding="utf-8"))
    errors = validate_ticket(ticket, ticket_path)
    if errors:
        return {
            "schema_version": RECEIPT_SCHEMA,
            "probe_id": ticket.get("probe_id"),
            "status": "not_started",
            "model_invocations": 0,
            "diagnostics": errors,
        }

    version_result = subprocess.run(
        [ticket["executable"], "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=10,
    )
    observed_version = version_result.stdout.decode("utf-8", errors="replace").strip()
    if version_result.returncode != 0 or observed_version != ticket["expected_cli_version"]:
        return {
            "schema_version": RECEIPT_SCHEMA,
            "probe_id": ticket["probe_id"],
            "status": "not_started",
            "model_invocations": 0,
            "cli_version": observed_version,
            "diagnostics": ["cli_version_mismatch"],
        }

    workdir = Path(tempfile.mkdtemp(prefix="portable-claude-transport-r2-work."))
    evidence_dir = Path(tempfile.mkdtemp(prefix="portable-claude-transport-r2-evidence."))
    os.chmod(workdir, 0o700)
    os.chmod(evidence_dir, 0o700)
    command = [ticket["executable"], *ticket["arguments"]]
    started_ns = time.monotonic_ns()
    try:
        result = subprocess.run(
            command,
            cwd=workdir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=ticket["timeout_seconds"],
        )
        timed_out = False
    except subprocess.TimeoutExpired as error:
        result = error
        timed_out = True
    ended_ns = time.monotonic_ns()

    stdout = result.stdout or b""
    stderr = result.stderr or b""
    stdout_path = evidence_dir / "stdout.raw"
    stderr_path = evidence_dir / "stderr.raw"
    write_private(stdout_path, stdout)
    write_private(stderr_path, stderr)
    stream_receipt = {
        "stdout": {"path": str(stdout_path), "bytes": len(stdout), "sha256": sha256_bytes(stdout), "mode": file_mode(stdout_path)},
        "stderr": {"path": str(stderr_path), "bytes": len(stderr), "sha256": sha256_bytes(stderr), "mode": file_mode(stderr_path)},
    }
    base = {
        "schema_version": RECEIPT_SCHEMA,
        "probe_id": ticket["probe_id"],
        "ticket_path": str(ticket_path),
        "ticket_sha256": sha256_file(ticket_path),
        "harness_sha256": ticket["harness_sha256"],
        "cli_version": observed_version,
        "model_invocations": 1,
        "workdir": str(workdir),
        "workdir_mode": file_mode(workdir),
        "evidence_dir": str(evidence_dir),
        "evidence_dir_mode": file_mode(evidence_dir),
        "streams": stream_receipt,
        "monotonic": {"started_ns": started_ns, "ended_ns": ended_ns, "elapsed_ns": ended_ns - started_ns},
        "timed_out": timed_out,
    }
    if timed_out:
        return {**base, "status": "external_failure", "process_exit": None, "secret_scan": {"passed": not secret_marker_names(stdout, stderr), "markers": secret_marker_names(stdout, stderr)}, "diagnostics": ["timeout"]}

    markers = secret_marker_names(stdout, stderr)
    process_exit = result.returncode
    try:
        terminal = json.loads(stdout)
        parsed_object = isinstance(terminal, dict)
    except (json.JSONDecodeError, UnicodeDecodeError):
        terminal = {}
        parsed_object = False
    required_terminal_fields = {"usage", "modelUsage", "session_id", "uuid", "terminal_reason", "structured_output"}
    checks = {
        "process_exit_zero": process_exit == 0,
        "stdout_is_single_json_object": parsed_object,
        "structured_output_exact": parsed_object and terminal.get("structured_output") == ticket["expected_structured_output"],
        "terminal_fields_present": parsed_object and required_terminal_fields <= set(terminal),
        "separate_stream_files": stdout_path.is_file() and stderr_path.is_file(),
        "private_modes": file_mode(stdout_path) == "0600" and file_mode(stderr_path) == "0600",
        "monotonic_elapsed_nonnegative": ended_ns >= started_ns,
        "secret_scan_passed": not markers,
    }
    if all(checks.values()):
        status = "transport_probe_observed"
    elif process_exit != 0 and parsed_object and (
        terminal.get("permission_denials") or terminal.get("api_error_status")
    ):
        status = "probe_unavailable"
    elif process_exit != 0:
        status = "external_failure"
    else:
        status = "probe_not_admitted"
    return {
        **base,
        "status": status,
        "process_exit": process_exit,
        "secret_scan": {"passed": not markers, "markers": markers},
        "admission_checks": checks,
        "terminal": terminal_projection(terminal) if parsed_object and not markers else None,
        "diagnostics": [name for name, passed in checks.items() if not passed],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticket", type=Path, required=True)
    args = parser.parse_args()
    receipt = run_probe(args.ticket.resolve())
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

