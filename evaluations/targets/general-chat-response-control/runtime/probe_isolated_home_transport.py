#!/usr/bin/env python3
"""Run the single, non-evaluation isolated-CODEX_HOME transport probe."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
from typing import Any

import jsonschema


ROOT = Path(__file__).resolve().parents[4]
PROBE_INPUT = "Return exactly one JSON object matching the supplied schema. Set status to ok.\n"
PROBE_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "required": ["status"],
    "properties": {"status": {"const": "ok"}},
}


class ProbeError(RuntimeError):
    """The probe could not be prepared without issuing a model request."""


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def parse_jsonl(stdout: bytes) -> dict[str, Any]:
    event_types: list[str] = []
    thread_ids: list[str] = []
    terminal_usage: list[dict[str, int]] = []
    error_messages: list[str] = []
    invalid_json_lines = 0
    for raw_line in stdout.splitlines():
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError:
            invalid_json_lines += 1
            continue
        if not isinstance(event, dict):
            invalid_json_lines += 1
            continue
        event_type = event.get("type")
        if isinstance(event_type, str):
            event_types.append(event_type)
        thread_id = event.get("thread_id")
        if isinstance(thread_id, str) and thread_id not in thread_ids:
            thread_ids.append(thread_id)
        usage = event.get("usage")
        if event_type == "turn.completed" and isinstance(usage, dict):
            accepted = {
                key: value
                for key, value in usage.items()
                if key in {"input_tokens", "cached_input_tokens", "output_tokens", "total_tokens"}
                and isinstance(value, int)
            }
            terminal_usage.append(accepted)
        if event_type in {"error", "turn.failed"}:
            message = event.get("message")
            if not isinstance(message, str):
                error = event.get("error")
                if isinstance(error, dict) and isinstance(error.get("message"), str):
                    message = error["message"]
            if isinstance(message, str):
                error_messages.append(message[-2000:])
    return {
        "event_types": event_types,
        "thread_ids": thread_ids,
        "terminal_usage": terminal_usage,
        "error_messages": error_messages,
        "invalid_json_lines": invalid_json_lines,
    }


def write_once(path: Path, value: dict[str, Any]) -> None:
    if path.exists():
        raise ProbeError(f"refusing to overwrite probe result: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_probe(output_path: Path) -> dict[str, Any]:
    if output_path.exists():
        raise ProbeError(f"refusing to reissue completed probe: {output_path}")
    host_codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).resolve()
    host_auth = host_codex_home / "auth.json"
    if not host_auth.is_file():
        raise ProbeError("host Codex auth identity is unavailable")

    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="general-chat-probe-workspace-") as raw_workspace, tempfile.TemporaryDirectory(
        prefix="general-chat-probe-home-"
    ) as raw_codex_home:
        workspace = Path(raw_workspace)
        codex_home = Path(raw_codex_home)
        os.symlink(host_auth, codex_home / "auth.json")
        (workspace / "AGENTS.md").write_bytes(b"")
        schema_path = workspace / "response-schema.json"
        schema_path.write_text(json.dumps(PROBE_SCHEMA, ensure_ascii=False), encoding="utf-8")
        final_path = workspace / "final.json"
        command = [
            "codex", "exec", "--skip-git-repo-check", "--cd", str(workspace),
            "--ignore-user-config", "--ignore-rules", "--strict-config", "--ephemeral",
            "--disable", "multi_agent", "--disable", "memories", "--disable", "apps",
            "--disable", "plugins", "--disable", "plugin_sharing",
            "-c", 'approval_policy="never"', "--model", "gpt-5.6-sol",
            "-c", 'model_reasoning_effort="medium"', "--sandbox", "read-only",
            "--output-schema", str(schema_path), "--json", "--output-last-message", str(final_path), "-",
        ]
        environment = dict(os.environ)
        environment["CODEX_HOME"] = str(codex_home)
        completed = subprocess.run(
            command,
            input=PROBE_INPUT.encode(),
            capture_output=True,
            check=False,
            env=environment,
        )
        elapsed_seconds = round(time.monotonic() - started, 6)
        summary = parse_jsonl(completed.stdout)
        final_exists = final_path.is_file()
        final_sha256 = sha256_file(final_path) if final_exists else None
        final_schema_valid = False
        final_error: str | None = None
        if final_exists:
            try:
                final_value = json.loads(final_path.read_text(encoding="utf-8"))
                jsonschema.Draft202012Validator(PROBE_SCHEMA).validate(final_value)
                final_schema_valid = True
            except (json.JSONDecodeError, jsonschema.ValidationError) as error:
                final_error = str(error)[-2000:]

    total_tokens = [item.get("total_tokens") for item in summary["terminal_usage"]]
    admission_passed = (
        completed.returncode == 0
        and final_schema_valid
        and len(summary["thread_ids"]) == 1
        and len(summary["terminal_usage"]) == 1
        and len(total_tokens) == 1
        and isinstance(total_tokens[0], int)
        and not summary["error_messages"]
    )
    result = {
        "schema_version": "general-chat-transport-probe/v1",
        "probe_id": "general-chat-isolated-home-transport-probe-r1",
        "purpose": "non_evaluation_transport_diagnostic",
        "issued_once": True,
        "fixed_input_sha256": sha256_bytes(PROBE_INPUT.encode()),
        "fixed_schema_sha256": sha256_bytes(
            json.dumps(PROBE_SCHEMA, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        ),
        "runtime": {
            "codex_cli": "0.146.0",
            "model": "gpt-5.6-sol",
            "reasoning_effort": "medium",
            "codex_home": "per_probe_temporary",
            "auth_transport": "host_auth_symlink_not_persisted",
            "runtime_adapter_path": str(Path(__file__).resolve().relative_to(ROOT)),
            "runtime_adapter_sha256": sha256_file(Path(__file__)),
        },
        "observation": {
            "process_exit_code": completed.returncode,
            "elapsed_seconds": elapsed_seconds,
            "stdout_sha256": sha256_bytes(completed.stdout),
            "stderr_sha256": sha256_bytes(completed.stderr),
            "stderr_tail": completed.stderr.decode(errors="replace")[-1000:],
            **summary,
            "final_exists": final_exists,
            "final_sha256": final_sha256,
            "final_schema_valid": final_schema_valid,
            "final_error": final_error,
        },
        "admission": {
            "state": "available" if admission_passed else "unavailable",
            "passed": admission_passed,
        },
        "evaluation_effect": {
            "evaluation_slot_issued": False,
            "qualification_result_changed": False,
            "candidate_created": False,
        },
    }
    result["result_sha256"] = sha256_bytes(
        json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    )
    write_once(output_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = run_probe(args.output.resolve())
    except ProbeError as error:
        print(str(error), file=__import__("sys").stderr)
        return 1
    print(json.dumps(result["admission"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
