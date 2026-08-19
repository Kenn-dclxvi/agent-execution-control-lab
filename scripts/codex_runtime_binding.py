#!/usr/bin/env python3
"""Resolve a Profile-pinned Codex CLI through the host-local immutable registry."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Mapping


class CodexRuntimeBindingError(RuntimeError):
    pass


VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
EXPECTED_TEAM_IDENTIFIER = "2DC432GLL2"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def version_from_conditions(conditions: Mapping[str, Any]) -> str | None:
    agent_environment = conditions.get("agent_environment")
    if not isinstance(agent_environment, dict):
        return None
    version = agent_environment.get("codex_cli")
    if version is None:
        return None
    if not isinstance(version, str) or VERSION_PATTERN.fullmatch(version) is None:
        raise CodexRuntimeBindingError("agent_environment.codex_cli must be an exact x.y.z version")
    return version


def find_runtime_manager(configured: str | None = None) -> Path:
    candidates: list[Path] = []
    if configured:
        candidates.append(Path(configured).expanduser())
    discovered = shutil.which("codex-runtime")
    if discovered:
        candidates.append(Path(discovered))
    candidates.append(
        Path(__file__).resolve().parents[2]
        / "codex-runtime-infrastructure"
        / "bin"
        / "codex-runtime"
    )
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.is_file() and os.access(resolved, os.X_OK):
            return resolved
    raise CodexRuntimeBindingError(
        "Codex runtime manager is unavailable; set CODEX_RUNTIME_MANAGER"
    )


def resolve_fixed_codex_runtime(
    version: str,
    *,
    manager_path: Path | None = None,
) -> dict[str, Any]:
    if VERSION_PATTERN.fullmatch(version) is None:
        raise CodexRuntimeBindingError("Codex CLI version must be an exact x.y.z value")
    alias = "codex-" + ".".join(version.split(".")[:2])
    manager = manager_path.resolve() if manager_path is not None else find_runtime_manager(
        os.environ.get("CODEX_RUNTIME_MANAGER")
    )
    completed = subprocess.run(
        [str(manager), "resolve", "--alias", alias, "--json"],
        capture_output=True,
        check=False,
        text=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or f"exit {completed.returncode}"
        raise CodexRuntimeBindingError(f"fixed Codex runtime resolution failed: {detail}")
    try:
        resolution = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise CodexRuntimeBindingError("fixed Codex runtime resolution returned invalid JSON") from error
    if not isinstance(resolution, dict):
        raise CodexRuntimeBindingError("fixed Codex runtime resolution must be an object")
    runtime_id = resolution.get("runtime_id")
    resolved_path_raw = resolution.get("resolved_path")
    entrypoint_sha256 = resolution.get("entrypoint_sha256")
    if (
        resolution.get("schema_version") != "codex-eval-runtime-resolution/v1"
        or resolution.get("alias") != alias
        or resolution.get("mutable") is not False
        or resolution.get("version_output") != f"codex-cli {version}"
        or resolution.get("codesign_team_identifier") != EXPECTED_TEAM_IDENTIFIER
        or not isinstance(runtime_id, str)
        or not runtime_id
        or not isinstance(resolved_path_raw, str)
        or not Path(resolved_path_raw).is_absolute()
        or not isinstance(entrypoint_sha256, str)
        or SHA256_PATTERN.fullmatch(entrypoint_sha256) is None
    ):
        raise CodexRuntimeBindingError("fixed Codex runtime resolution contract mismatch")
    executable = Path(resolved_path_raw).resolve()
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise CodexRuntimeBindingError("fixed Codex runtime executable is unavailable")
    if sha256_file(executable) != entrypoint_sha256:
        raise CodexRuntimeBindingError("fixed Codex runtime entrypoint hash mismatch")
    return {
        "schema_version": "the-caption-prompt.codex-runtime-binding/v1",
        "runtime_id": runtime_id,
        "alias": alias,
        "executable": str(executable),
        "version_output": f"codex-cli {version}",
        "entrypoint_sha256": entrypoint_sha256,
        "codesign_team_identifier": EXPECTED_TEAM_IDENTIFIER,
    }


def verify_codex_runtime_binding(binding: Mapping[str, Any]) -> None:
    if binding.get("schema_version") != "the-caption-prompt.codex-runtime-binding/v1":
        raise CodexRuntimeBindingError("Codex runtime binding schema mismatch")
    executable_raw = binding.get("executable")
    expected_hash = binding.get("entrypoint_sha256")
    expected_version = binding.get("version_output")
    if (
        not isinstance(executable_raw, str)
        or not Path(executable_raw).is_absolute()
        or not isinstance(expected_hash, str)
        or SHA256_PATTERN.fullmatch(expected_hash) is None
        or not isinstance(expected_version, str)
        or not expected_version.startswith("codex-cli ")
    ):
        raise CodexRuntimeBindingError("Codex runtime binding fields are invalid")
    executable = Path(executable_raw).resolve()
    if str(executable) != executable_raw or not executable.is_file() or not os.access(executable, os.X_OK):
        raise CodexRuntimeBindingError("bound Codex runtime executable is unavailable")
    if sha256_file(executable) != expected_hash:
        raise CodexRuntimeBindingError("bound Codex runtime entrypoint drifted")
    completed = subprocess.run(
        [str(executable), "--version"], capture_output=True, check=False, text=True
    )
    if completed.returncode != 0 or completed.stdout.strip() != expected_version:
        raise CodexRuntimeBindingError("bound Codex runtime version drifted")


def resolve_runtime_from_conditions(conditions: Mapping[str, Any]) -> dict[str, Any] | None:
    version = version_from_conditions(conditions)
    return None if version is None else resolve_fixed_codex_runtime(version)
