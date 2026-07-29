#!/usr/bin/env python3
"""Run one allowlisted validator and suppress only its successful raw output."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any


POLICY_SCHEMA_VERSION = "the-caption-prompt.success-command-runtime/v1"
RECEIPT_SCHEMA_VERSION = "the-caption-prompt.success-command-receipt/v1"
POLICY_REJECTION_EXIT_CODE = 64


class SuccessSilentCommandError(Exception):
    pass


def load_policy(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise SuccessSilentCommandError(f"invalid policy file: {path}") from exc
    if not isinstance(value, dict) or value.get("schema_version") != POLICY_SCHEMA_VERSION:
        raise SuccessSilentCommandError("unsupported success command policy")
    if not isinstance(value.get("workspace"), str):
        raise SuccessSilentCommandError("success command policy has no workspace")
    commands = value.get("commands")
    if not isinstance(commands, list):
        raise SuccessSilentCommandError("success command policy has no commands")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def matching_entry(policy: dict[str, Any], argv: list[str]) -> dict[str, Any] | None:
    for raw_entry in policy["commands"]:
        if not isinstance(raw_entry, dict) or raw_entry.get("argv") != argv:
            continue
        return raw_entry
    return None


def validate_entry(entry: dict[str, Any], workspace: Path) -> None:
    script_path = entry.get("script_path")
    expected_sha256 = entry.get("script_sha256")
    if script_path is None and expected_sha256 is None:
        return
    if not isinstance(script_path, str) or not isinstance(expected_sha256, str):
        raise SuccessSilentCommandError("pinned wrapper identity is incomplete")
    path = workspace / script_path
    try:
        actual_sha256 = sha256_bytes(path.read_bytes())
    except FileNotFoundError as exc:
        raise SuccessSilentCommandError(f"pinned wrapper missing: {script_path}") from exc
    if actual_sha256 != expected_sha256:
        raise SuccessSilentCommandError(f"pinned wrapper identity mismatch: {script_path}")


def write_evidence(
    evidence_dir: Path,
    argv: list[str],
    completed: subprocess.CompletedProcess[bytes],
) -> dict[str, Any]:
    evidence_dir.mkdir(parents=True, exist_ok=True)
    evidence_id = uuid.uuid4().hex
    stdout_path = evidence_dir / f"{evidence_id}.stdout.bin"
    stderr_path = evidence_dir / f"{evidence_id}.stderr.bin"
    metadata_path = evidence_dir / f"{evidence_id}.json"
    stdout_path.write_bytes(completed.stdout)
    stderr_path.write_bytes(completed.stderr)
    metadata = {
        "schema_version": "the-caption-prompt.success-command-evidence/v1",
        "evidence_id": evidence_id,
        "argv": argv,
        "exit_code": completed.returncode,
        "stdout_bytes": len(completed.stdout),
        "stdout_sha256": sha256_bytes(completed.stdout),
        "stderr_bytes": len(completed.stderr),
        "stderr_sha256": sha256_bytes(completed.stderr),
    }
    with metadata_path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(metadata, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return metadata


def run(policy_path: Path, evidence_dir: Path, argv: list[str]) -> int:
    if not argv:
        raise SuccessSilentCommandError("command argv is empty")
    policy = load_policy(policy_path)
    workspace = Path(policy["workspace"]).resolve()
    if Path.cwd().resolve() != workspace:
        raise SuccessSilentCommandError("success command workspace mismatch")
    entry = matching_entry(policy, argv)
    if entry is None:
        raise SuccessSilentCommandError("command is not allowlisted")
    validate_entry(entry, workspace)

    completed = subprocess.run(argv, capture_output=True, check=False)
    metadata = write_evidence(evidence_dir, argv, completed)
    if completed.returncode == 0:
        receipt = {
            "schema_version": RECEIPT_SCHEMA_VERSION,
            "command": argv,
            "exit_code": 0,
            "evidence_id": metadata["evidence_id"],
        }
        sys.stdout.write(
            json.dumps(receipt, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
            + "\n"
        )
        return 0

    sys.stdout.buffer.write(completed.stdout)
    sys.stderr.buffer.write(completed.stderr)
    sys.stdout.buffer.flush()
    sys.stderr.buffer.flush()
    if completed.returncode < 0:
        signum = -completed.returncode
        signal.signal(signum, signal.SIG_DFL)
        os.kill(os.getpid(), signum)
        return 128 + signum
    return completed.returncode


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument(
        "--policy",
        default=os.environ.get("CODEX_SUCCESS_COMMAND_POLICY"),
    )
    value.add_argument(
        "--evidence-dir",
        default=os.environ.get("CODEX_SUCCESS_COMMAND_EVIDENCE_DIR"),
    )
    value.add_argument("command", nargs=argparse.REMAINDER)
    return value


def main() -> int:
    args = parser().parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    try:
        if not args.policy or not args.evidence_dir:
            raise SuccessSilentCommandError("policy and evidence directory are required")
        return run(Path(args.policy), Path(args.evidence_dir), command)
    except SuccessSilentCommandError as exc:
        print(f"success-command policy rejection: {exc}", file=sys.stderr)
        return POLICY_REJECTION_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
