#!/usr/bin/env python3
"""Remove sealed evaluation workspaces from Codex's project configuration."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import tempfile
import tomllib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "the-caption-prompt.codex-project-config-prune-receipt/v1"
RECEIPT_NAME = "codex-project-config-prune-receipt.json"
MAX_WRITE_ATTEMPTS = 3


class CodexConfigCleanupError(Exception):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise CodexConfigCleanupError(f"invalid JSON object: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise CodexConfigCleanupError(f"JSON root must be an object: {path}")
    return value


def write_json_once(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError as exc:
        raise CodexConfigCleanupError(f"refusing to overwrite: {path}") from exc


def project_paths_from_prune_receipt(receipt_path: Path) -> tuple[Path, list[str]]:
    receipt = load_object(receipt_path)
    if receipt.get("schema_version") != "the-caption-prompt.execution-prune-receipt/v1":
        raise CodexConfigCleanupError("unsupported execution prune receipt schema")
    batch_value = receipt.get("batch")
    pruned_paths = receipt.get("pruned_paths")
    if not isinstance(batch_value, str) or not Path(batch_value).is_absolute():
        raise CodexConfigCleanupError("execution prune receipt batch must be absolute")
    if not isinstance(pruned_paths, list) or not all(
        isinstance(value, str) for value in pruned_paths
    ):
        raise CodexConfigCleanupError("execution prune receipt pruned_paths must be strings")

    batch = Path(batch_value)
    receipt_batch = receipt_path.resolve().parent.parent
    if batch.resolve() != receipt_batch:
        raise CodexConfigCleanupError(
            f"execution prune receipt batch does not match its location: {batch}"
        )
    targets: list[str] = []
    for value in pruned_paths:
        relative = Path(value)
        parts = relative.parts
        if (
            relative.is_absolute()
            or len(parts) != 5
            or parts[:3] != ("cycle", "layer2", "evidence")
            or parts[-1] != "workspace"
            or parts[3] in ("", ".", "..")
        ):
            raise CodexConfigCleanupError(f"unexpected pruned workspace path: {value}")
        targets.append(str(batch.joinpath(*parts)))
    return batch, sorted(set(targets))


def project_key_from_header(line: str) -> str | None:
    stripped = line.strip()
    if not stripped.startswith("[") or stripped.startswith("[["):
        return None
    try:
        document = tomllib.loads(f"{stripped}\n__codex_cleanup_marker__ = true\n")
    except tomllib.TOMLDecodeError:
        return None
    projects = document.get("projects")
    if not isinstance(projects, dict) or len(projects) != 1:
        return None
    project = next(iter(projects))
    return project if isinstance(projects[project], dict) else None


def remove_project_sections(source: bytes, targets: set[str]) -> tuple[bytes, list[str]]:
    try:
        text = source.decode("utf-8")
        tomllib.loads(text)
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise CodexConfigCleanupError(f"Codex config is not valid TOML: {exc}") from exc

    lines = text.splitlines(keepends=True)
    headers = [index for index, line in enumerate(lines) if line.lstrip().startswith("[")]
    headers.append(len(lines))
    remove_indexes: set[int] = set()
    removed: set[str] = set()
    for position, start in enumerate(headers[:-1]):
        project = project_key_from_header(lines[start])
        if project not in targets:
            continue
        remove_indexes.update(range(start, headers[position + 1]))
        removed.add(project)

    rewritten = "".join(
        line for index, line in enumerate(lines) if index not in remove_indexes
    ).encode("utf-8")
    try:
        tomllib.loads(rewritten.decode("utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise CodexConfigCleanupError(
            f"rewritten Codex config is not valid TOML: {exc}"
        ) from exc
    return rewritten, sorted(removed)


def atomic_replace_if_unchanged(path: Path, expected: bytes, replacement: bytes) -> bool:
    if path.read_bytes() != expected:
        return False
    metadata = path.stat()
    temporary_name: str | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.", dir=path.parent
        )
        with os.fdopen(descriptor, "wb") as handle:
            os.fchmod(handle.fileno(), stat.S_IMODE(metadata.st_mode))
            handle.write(replacement)
            handle.flush()
            os.fsync(handle.fileno())
        if path.read_bytes() != expected:
            return False
        os.replace(temporary_name, path)
        temporary_name = None
        directory_descriptor = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_descriptor)
        finally:
            os.close(directory_descriptor)
        return True
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)


def prune_codex_project_config(
    receipt_path: Path,
    config_path: Path,
    max_attempts: int = MAX_WRITE_ATTEMPTS,
) -> dict[str, Any]:
    batch, targets = project_paths_from_prune_receipt(receipt_path)
    if max_attempts < 1:
        raise CodexConfigCleanupError("max_attempts must be positive")

    if not config_path.is_file():
        return {
            "schema_version": SCHEMA_VERSION,
            "created_at": utc_now(),
            "status": "config_missing",
            "batch": str(batch),
            "config_path": str(config_path),
            "target_paths": targets,
            "removed_paths": [],
            "missing_paths": targets,
        }

    for attempt in range(1, max_attempts + 1):
        before = config_path.read_bytes()
        after, removed = remove_project_sections(before, set(targets))
        if after == before or atomic_replace_if_unchanged(config_path, before, after):
            return {
                "schema_version": SCHEMA_VERSION,
                "created_at": utc_now(),
                "status": "updated" if after != before else "unchanged",
                "batch": str(batch),
                "config_path": str(config_path),
                "attempts": attempt,
                "target_paths": targets,
                "removed_paths": removed,
                "missing_paths": sorted(set(targets) - set(removed)),
                "bytes_before": len(before),
                "bytes_after": len(after),
                "sha256_before": sha256_bytes(before),
                "sha256_after": sha256_bytes(after),
            }
    raise CodexConfigCleanupError(
        f"Codex config changed during {max_attempts} cleanup attempts: {config_path}"
    )


def maintain_codex_config_for_batch(batch: Path, config_path: Path) -> dict[str, Any]:
    batch = batch.resolve()
    maintenance_receipt = batch / "compact" / RECEIPT_NAME
    if maintenance_receipt.is_file():
        return load_object(maintenance_receipt)
    result = prune_codex_project_config(
        batch / "compact" / "execution-prune-receipt.json", config_path
    )
    write_json_once(maintenance_receipt, result)
    return result
