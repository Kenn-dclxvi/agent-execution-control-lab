#!/usr/bin/env python3
"""Run a deterministic command wave without exposing intermediate output."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLAN_SCHEMA = "the-caption-prompt.sealed-execution-wave-plan/v1"
RECEIPT_SCHEMA = "the-caption-prompt.sealed-execution-wave-receipt/v1"
FAILURE_TAIL_BYTES = 4096
OPERATION_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")


class SealedWaveError(Exception):
    pass


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def path_within(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def load_plan(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SealedWaveError(f"missing plan: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SealedWaveError(f"invalid plan JSON: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise SealedWaveError("plan root must be an object")
    return value


def validate_plan(plan: dict[str, Any]) -> list[dict[str, Any]]:
    if plan.get("schema_version") != PLAN_SCHEMA:
        raise SealedWaveError(f"schema_version must be {PLAN_SCHEMA}")
    wave_id = plan.get("wave_id")
    if not isinstance(wave_id, str) or not OPERATION_ID.fullmatch(wave_id):
        raise SealedWaveError("wave_id must be a safe non-empty identifier")
    operations = plan.get("operations")
    if not isinstance(operations, list) or not operations:
        raise SealedWaveError("operations must be a non-empty array")

    seen: set[str] = set()
    validated: list[dict[str, Any]] = []
    allowed_keys = {"id", "argv", "expected_exit_codes", "timeout_seconds"}
    for index, operation in enumerate(operations):
        if not isinstance(operation, dict):
            raise SealedWaveError(f"operation {index} must be an object")
        unknown_keys = set(operation) - allowed_keys
        if unknown_keys:
            raise SealedWaveError(
                f"operation {index} has unsupported keys: {sorted(unknown_keys)}"
            )
        operation_id = operation.get("id")
        if not isinstance(operation_id, str) or not OPERATION_ID.fullmatch(operation_id):
            raise SealedWaveError(f"operation {index} has an unsafe id")
        if operation_id in seen:
            raise SealedWaveError(f"duplicate operation id: {operation_id}")
        seen.add(operation_id)

        argv = operation.get("argv")
        if (
            not isinstance(argv, list)
            or not argv
            or any(not isinstance(item, str) or not item for item in argv)
        ):
            raise SealedWaveError(f"operation {operation_id} argv must be string array")

        expected = operation.get("expected_exit_codes", [0])
        if (
            not isinstance(expected, list)
            or not expected
            or any(not isinstance(code, int) or isinstance(code, bool) for code in expected)
        ):
            raise SealedWaveError(
                f"operation {operation_id} expected_exit_codes must be an integer array"
            )

        timeout = operation.get("timeout_seconds")
        if timeout is not None and (
            not isinstance(timeout, (int, float))
            or isinstance(timeout, bool)
            or timeout <= 0
        ):
            raise SealedWaveError(
                f"operation {operation_id} timeout_seconds must be positive"
            )
        validated.append(
            {
                "id": operation_id,
                "argv": argv,
                "expected_exit_codes": sorted(set(expected)),
                "timeout_seconds": timeout,
            }
        )
    return validated


def write_bytes_once(path: Path, value: bytes) -> None:
    try:
        with path.open("xb") as handle:
            handle.write(value)
    except FileExistsError as exc:
        raise SealedWaveError(f"refusing to overwrite: {path}") from exc


def write_json_once(path: Path, value: dict[str, Any]) -> None:
    write_bytes_once(path, json.dumps(
        value, ensure_ascii=False, indent=2, sort_keys=True
    ).encode("utf-8") + b"\n")


def evidence_reference(path: Path, value: bytes) -> dict[str, Any]:
    return {
        "path": str(path),
        "sha256": sha256_bytes(value),
        "bytes": len(value),
    }


def failure_excerpt(stdout: bytes, stderr: bytes) -> dict[str, Any]:
    stream = "stderr" if stderr else "stdout"
    value = stderr if stderr else stdout
    tail = value[-FAILURE_TAIL_BYTES:]
    return {
        "stream": stream,
        "text": tail.decode("utf-8", errors="replace"),
        "byte_limit": FAILURE_TAIL_BYTES,
        "truncated": len(value) > len(tail),
    }


def terminate_process(process: subprocess.Popen[bytes]) -> None:
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    else:
        process.kill()


def run_operation(
    operation: dict[str, Any], workspace: Path
) -> tuple[str, int | None, bytes, bytes, float, str | None]:
    started = time.monotonic()
    try:
        process = subprocess.Popen(
            operation["argv"],
            cwd=workspace,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except OSError as exc:
        return "unknown", None, b"", str(exc).encode("utf-8"), time.monotonic() - started, "launch_error"

    try:
        stdout, stderr = process.communicate(timeout=operation["timeout_seconds"])
    except subprocess.TimeoutExpired:
        terminate_process(process)
        stdout, stderr = process.communicate()
        return "unknown", None, stdout, stderr, time.monotonic() - started, "timeout"

    status = (
        "success"
        if process.returncode in operation["expected_exit_codes"]
        else "predicate_false"
    )
    return status, process.returncode, stdout, stderr, time.monotonic() - started, None


def execute_wave(
    plan: dict[str, Any], workspace: Path, evidence_directory: Path
) -> tuple[dict[str, Any], int]:
    operations = validate_plan(plan)
    workspace = workspace.resolve()
    evidence_directory = evidence_directory.resolve()
    if not workspace.is_dir():
        raise SealedWaveError(f"workspace must be an existing directory: {workspace}")
    if path_within(evidence_directory, workspace):
        raise SealedWaveError("evidence directory must be outside the workspace")
    try:
        evidence_directory.mkdir(parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise SealedWaveError(
            f"evidence directory already exists: {evidence_directory}"
        ) from exc

    plan_bytes = canonical_json(plan)
    write_bytes_once(evidence_directory / "plan.json", plan_bytes + b"\n")
    started_at = utc_now()
    wave_started = time.monotonic()
    operation_receipts: list[dict[str, Any]] = []
    wave_status = "terminal"
    reentry_reason: str | None = None

    for index, operation in enumerate(operations, start=1):
        status, exit_code, stdout, stderr, duration, detail = run_operation(
            operation, workspace
        )
        stem = f"{index:02d}-{operation['id']}"
        stdout_path = evidence_directory / f"{stem}.stdout"
        stderr_path = evidence_directory / f"{stem}.stderr"
        write_bytes_once(stdout_path, stdout)
        write_bytes_once(stderr_path, stderr)
        operation_receipt: dict[str, Any] = {
            "id": operation["id"],
            "argv_sha256": sha256_bytes(canonical_json(operation["argv"])),
            "status": status,
            "exit_code": exit_code,
            "duration_seconds": round(duration, 6),
            "stdout": evidence_reference(stdout_path, stdout),
            "stderr": evidence_reference(stderr_path, stderr),
        }
        if detail is not None:
            operation_receipt["unknown_detail"] = detail
        if status != "success":
            operation_receipt["failure_excerpt"] = failure_excerpt(stdout, stderr)
        operation_receipts.append(operation_receipt)
        if status != "success":
            wave_status = status
            reentry_reason = f"operation_{status}"
            break

    completed_ids = {item["id"] for item in operation_receipts}
    receipt = {
        "schema_version": RECEIPT_SCHEMA,
        "plan_schema_version": PLAN_SCHEMA,
        "plan_sha256": sha256_bytes(plan_bytes),
        "wave_id": plan["wave_id"],
        "workspace": str(workspace),
        "evidence_directory": str(evidence_directory),
        "started_at": started_at,
        "finished_at": utc_now(),
        "duration_seconds": round(time.monotonic() - wave_started, 6),
        "wave_status": wave_status,
        "reentry_reason": reentry_reason,
        "operations": operation_receipts,
        "not_run_operation_ids": [
            item["id"] for item in operations if item["id"] not in completed_ids
        ],
        "model_visibility": {
            "delivery": "terminal_receipt_only",
            "intermediate_success_output": "buffered_external_to_workspace",
            "visible_receipt_count": 1,
        },
    }
    write_json_once(evidence_directory / "receipt.json", receipt)
    exit_code = {"terminal": 0, "predicate_false": 2, "unknown": 3}[wave_status]
    return receipt, exit_code


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--plan", required=True)
    value.add_argument("--workspace", required=True)
    value.add_argument("--evidence-directory", required=True)
    return value


def invalid_receipt(message: str) -> dict[str, Any]:
    return {
        "schema_version": RECEIPT_SCHEMA,
        "wave_status": "invalid_plan",
        "reentry_reason": "invalid_plan",
        "error": message,
        "model_visibility": {
            "delivery": "terminal_receipt_only",
            "visible_receipt_count": 1,
        },
    }


def main() -> int:
    args = parser().parse_args()
    try:
        plan = load_plan(Path(args.plan).resolve())
        receipt, exit_code = execute_wave(
            plan,
            Path(args.workspace),
            Path(args.evidence_directory),
        )
    except SealedWaveError as exc:
        receipt = invalid_receipt(str(exc))
        exit_code = 4
    print(json.dumps(receipt, ensure_ascii=False, separators=(",", ":"), sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
