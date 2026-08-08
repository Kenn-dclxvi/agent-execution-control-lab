#!/usr/bin/env python3
"""Collect applicable PR-review authority identities from a fixed Git tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any


class AuthorityCollectionError(ValueError):
    pass


def _git(repository: Path, *args: str) -> bytes:
    completed = subprocess.run(
        ["git", "-C", str(repository), *args], check=False, capture_output=True
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise AuthorityCollectionError(f"git {' '.join(args)} failed: {detail}")
    return completed.stdout


def _normalized_path(value: str, label: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise AuthorityCollectionError(f"{label} must be a normalized repository-relative path")
    return value


def _tree_entry(repository: Path, commit: str, path: str) -> dict[str, str] | None:
    output = _git(repository, "ls-tree", commit, "--", path).decode("utf-8")
    if not output:
        return None
    lines = output.rstrip("\n").splitlines()
    if len(lines) != 1:
        raise AuthorityCollectionError(f"tree path is ambiguous: {path}")
    metadata, observed_path = lines[0].split("\t", 1)
    mode, object_type, object_id = metadata.split(" ", 2)
    if observed_path != path:
        raise AuthorityCollectionError(f"tree path mismatch: expected={path} actual={observed_path}")
    return {"mode": mode, "type": object_type, "object_id": object_id, "path": path}


def _blob(repository: Path, commit: str, path: str) -> bytes:
    return _git(repository, "show", f"{commit}:{path}")


def _resolve_authority(repository: Path, commit: str, source_path: str) -> dict[str, Any]:
    source = _tree_entry(repository, commit, source_path)
    if source is None:
        raise AuthorityCollectionError(f"authority source is missing: {source_path}")
    if source["type"] != "blob":
        raise AuthorityCollectionError(f"authority source is not a blob: {source_path}")

    resolved_path = source_path
    symlink_target = None
    if source["mode"] == "120000":
        symlink_target = _blob(repository, commit, source_path).decode("utf-8")
        resolved_path = _normalized_path(
            (PurePosixPath(source_path).parent / symlink_target).as_posix(),
            "resolved symlink target",
        )

    resolved = _tree_entry(repository, commit, resolved_path)
    if resolved is None or resolved["mode"] != "100644" or resolved["type"] != "blob":
        raise AuthorityCollectionError(
            f"resolved authority must be a regular file: {resolved_path}"
        )
    content = _blob(repository, commit, resolved_path)
    return {
        "source_path": source_path,
        "source_mode": source["mode"],
        "source_blob_sha1": source["object_id"],
        "symlink_target": symlink_target,
        "resolved_path": resolved_path,
        "resolved_mode": resolved["mode"],
        "resolved_blob_sha1": resolved["object_id"],
        "content_sha256": hashlib.sha256(content).hexdigest(),
        "content_bytes": len(content),
    }


def _ancestor_directories(changed_path: str) -> list[PurePosixPath]:
    parent = PurePosixPath(changed_path).parent
    if parent == PurePosixPath("."):
        return []
    return [PurePosixPath(*parent.parts[:index]) for index in range(1, len(parent.parts) + 1)]


def collect_authorities(
    repository: Path, commit: str, changed_paths: list[str]
) -> dict[str, Any]:
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise AuthorityCollectionError("commit must be a 40-character lowercase SHA")
    normalized_paths = [_normalized_path(path, "changed path") for path in changed_paths]
    if not normalized_paths or len(normalized_paths) != len(set(normalized_paths)):
        raise AuthorityCollectionError("changed paths must be a non-empty unique list")

    observed_commit = _git(repository, "rev-parse", f"{commit}^{{commit}}").decode().strip()
    if observed_commit != commit:
        raise AuthorityCollectionError("commit identity mismatch")
    tree = _git(repository, "rev-parse", f"{commit}^{{tree}}").decode().strip()

    selected: dict[str, dict[str, Any]] = {}
    root = _resolve_authority(repository, commit, "CLAUDE.md")
    root["authority_role"] = "root"
    root["applies_to"] = list(normalized_paths)
    selected[root["source_path"]] = root

    path_bindings: list[dict[str, Any]] = []
    for changed_path in normalized_paths:
        applicable = ["CLAUDE.md"]
        for directory in _ancestor_directories(changed_path):
            candidate = f"{directory.as_posix()}/AGENTS.md"
            if _tree_entry(repository, commit, candidate) is None:
                continue
            applicable.append(candidate)
            if candidate not in selected:
                authority = _resolve_authority(repository, commit, candidate)
                authority["authority_role"] = "local"
                authority["applies_to"] = []
                selected[candidate] = authority
            selected[candidate]["applies_to"].append(changed_path)
        path_bindings.append(
            {"changed_path": changed_path, "applicable_authorities": applicable}
        )

    return {
        "schema_version": "agent-execution-control-lab.pr-review-authority-selection/v1",
        "collector_revision": "pr-review-authority-collector-r1",
        "target_repository_ref": {"commit": commit, "tree": tree},
        "selection_rule": {
            "root": "resolve root CLAUDE.md and apply it first",
            "local": "for each changed path, apply ancestor AGENTS.md files from shallow to deep",
        },
        "changed_paths": normalized_paths,
        "path_bindings": path_bindings,
        "authorities": list(selected.values()),
    }


def _write_once(path: Path, value: Any) -> None:
    if path.exists():
        raise AuthorityCollectionError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--changed-path", action="append", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        receipt = collect_authorities(args.repository, args.commit, args.changed_path)
        if args.output is not None:
            _write_once(args.output, receipt)
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    except AuthorityCollectionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
