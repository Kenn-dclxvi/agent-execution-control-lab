#!/usr/bin/env python3
"""Materialize a .git-free fixed repository snapshot with fixture overlays."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import stat
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

import pr_review_authority_collector as collector


class SnapshotError(ValueError):
    pass


def _load_json(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise SnapshotError(f"unable to read JSON {path}: {exc}") from exc


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalized_path(value: str, label: str) -> str:
    path = PurePosixPath(value)
    if not value or path.is_absolute() or ".." in path.parts or path.as_posix() != value:
        raise SnapshotError(f"{label} must be a normalized repository-relative path")
    if path.parts[0] == ".git":
        raise SnapshotError(f"{label} must not enter .git")
    return value


def _safe_destination(root: Path, value: str) -> Path:
    normalized = _normalized_path(value, "snapshot path")
    destination = root.joinpath(*PurePosixPath(normalized).parts)
    current = root
    for part in PurePosixPath(normalized).parts[:-1]:
        current = current / part
        if current.is_symlink():
            raise SnapshotError(f"snapshot parent is a symlink: {current.relative_to(root)}")
    return destination


def _write_regular(path: Path, content: bytes, executable: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() or path.is_symlink():
        if path.is_dir() and not path.is_symlink():
            raise SnapshotError(f"regular file collides with directory: {path}")
        path.unlink()
    path.write_bytes(content)
    path.chmod(0o755 if executable else 0o644)


def _extract_tree(repository: Path, commit: str, root: Path) -> dict[str, dict[str, Any]]:
    completed = subprocess.run(
        ["git", "-C", str(repository), "archive", "--format=tar", commit],
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise SnapshotError(f"git archive failed: {detail}")
    entries: dict[str, dict[str, Any]] = {}
    with tarfile.open(fileobj=io.BytesIO(completed.stdout), mode="r:") as archive:
        for member in archive.getmembers():
            path = member.name.rstrip("/")
            if not path:
                continue
            _normalized_path(path, "archive path")
            destination = _safe_destination(root, path)
            if member.isdir():
                destination.mkdir(parents=True, exist_ok=True)
                continue
            if member.isfile():
                extracted = archive.extractfile(member)
                if extracted is None:
                    raise SnapshotError(f"archive file has no content: {path}")
                content = extracted.read()
                executable = bool(member.mode & stat.S_IXUSR)
                _write_regular(destination, content, executable)
                entries[path] = {
                    "path": path,
                    "type": "file",
                    "mode": "100755" if executable else "100644",
                    "sha256": _sha256_bytes(content),
                    "bytes": len(content),
                    "origin": "target_tree",
                }
                continue
            if member.issym():
                target = member.linkname
                resolved = PurePosixPath(path).parent / target
                _normalized_path(resolved.as_posix(), "archive symlink target")
                destination.parent.mkdir(parents=True, exist_ok=True)
                if destination.exists() or destination.is_symlink():
                    destination.unlink()
                destination.symlink_to(target)
                entries[path] = {
                    "path": path,
                    "type": "symlink",
                    "mode": "120000",
                    "target": target,
                    "origin": "target_tree",
                }
                continue
            raise SnapshotError(f"unsupported archive member type: {path}")
    return entries


def _make_read_only(root: Path) -> None:
    for directory, directories, files in os.walk(root, topdown=False, followlinks=False):
        current = Path(directory)
        for name in files:
            path = current / name
            if not path.is_symlink():
                path.chmod(0o555 if path.stat().st_mode & stat.S_IXUSR else 0o444)
        for name in directories:
            path = current / name
            if not path.is_symlink():
                path.chmod(0o555)
        current.chmod(0o555)


def _make_cleanup_writable(root: Path) -> None:
    if not root.exists():
        return
    for directory, directories, files in os.walk(root, topdown=True, followlinks=False):
        current = Path(directory)
        current.chmod(0o755)
        for name in files:
            path = current / name
            if not path.is_symlink():
                path.chmod(0o755 if path.stat().st_mode & stat.S_IXUSR else 0o644)


def materialize_snapshot(
    repository: Path, commit: str, fixture_input_path: Path, output_dir: Path
) -> dict[str, Any]:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise SnapshotError(f"output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    snapshot_root = output_dir / "repository"
    snapshot_root.mkdir()

    observed_commit = collector._git(repository, "rev-parse", f"{commit}^{{commit}}").decode().strip()
    if observed_commit != commit:
        raise SnapshotError("commit identity mismatch")
    tree = collector._git(repository, "rev-parse", f"{commit}^{{tree}}").decode().strip()
    entries = _extract_tree(repository, commit, snapshot_root)

    fixture = _load_json(fixture_input_path)
    if fixture.get("schema_version") != 2:
        raise SnapshotError("snapshot r1 requires fixture input schema version 2")
    if not isinstance(fixture.get("case_id"), str) or not fixture["case_id"]:
        raise SnapshotError("fixture case_id must be a non-empty string")
    if not isinstance(fixture.get("fixture_revision"), str) or not fixture["fixture_revision"]:
        raise SnapshotError("fixture revision must be a non-empty string")
    changes = fixture.get("changes")
    if not isinstance(changes, list) or not changes:
        raise SnapshotError("fixture changes must be a non-empty array")
    changed_paths = fixture.get("changed_paths")
    if changed_paths != [change.get("path") for change in changes]:
        raise SnapshotError("changed_paths must match changes in order")
    overlay_paths = []
    for change in changes:
        path = _normalized_path(change["path"], "fixture change path")
        if not isinstance(change.get("content_after"), str):
            raise SnapshotError(f"fixture content_after must be text: {path}")
        content = change["content_after"].encode("utf-8")
        destination = _safe_destination(snapshot_root, path)
        _write_regular(destination, content, executable=False)
        entries[path] = {
            "path": path,
            "type": "file",
            "mode": "100644",
            "sha256": _sha256_bytes(content),
            "bytes": len(content),
            "origin": "fixture_overlay",
        }
        overlay_paths.append(path)

    canonical_entries = [entries[path] for path in sorted(entries)]
    canonical = json.dumps(
        canonical_entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    available_paths = "".join(f"{path}\n" for path in sorted(entries)).encode("utf-8")
    receipt = {
        "schema_version": "agent-execution-control-lab.pr-review-repository-snapshot/v1",
        "snapshot_revision": "pr-review-repository-snapshot-r1",
        "target_repository_ref": {"commit": commit, "tree": tree},
        "fixture": {
            "case_id": fixture["case_id"],
            "revision": fixture["fixture_revision"],
            "input_sha256": _sha256_file(fixture_input_path),
        },
        "overlay_paths": overlay_paths,
        "file_count": len(entries),
        "regular_file_bytes": sum(
            entry.get("bytes", 0) for entry in canonical_entries
        ),
        "available_paths_sha256": _sha256_bytes(available_paths),
        "snapshot_sha256": _sha256_bytes(canonical),
        "workspace_boundary": {"git_directory_present": False, "write_allowed": False},
    }
    _make_read_only(snapshot_root)
    receipt_path = output_dir / "snapshot-receipt.json"
    receipt_path.write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--fixture-input", required=True, type=Path)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    try:
        if args.output_dir is not None:
            receipt = materialize_snapshot(
                args.repository, args.commit, args.fixture_input, args.output_dir
            )
        else:
            with tempfile.TemporaryDirectory(prefix="pr-review-snapshot-") as directory:
                temporary_root = Path(directory)
                try:
                    receipt = materialize_snapshot(
                        args.repository, args.commit, args.fixture_input, temporary_root
                    )
                finally:
                    _make_cleanup_writable(temporary_root / "repository")
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    except (SnapshotError, collector.AuthorityCollectionError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
