#!/usr/bin/env python3
"""Materialize a fixed read-only repository snapshot for fixture schema v2 or v3."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

import pr_review_authority_collector as collector
import pr_review_repository_snapshot as r1


SnapshotError = r1.SnapshotError


def materialize_snapshot(
    repository: Path, commit: str, fixture_input_path: Path, output_dir: Path
) -> dict[str, Any]:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise SnapshotError(f"output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    snapshot_root = output_dir / "repository"
    snapshot_root.mkdir()

    observed_commit = collector._git(
        repository, "rev-parse", f"{commit}^{{commit}}"
    ).decode().strip()
    if observed_commit != commit:
        raise SnapshotError("commit identity mismatch")
    tree = collector._git(repository, "rev-parse", f"{commit}^{{tree}}").decode().strip()
    entries = r1._extract_tree(repository, commit, snapshot_root)

    fixture = r1._load_json(fixture_input_path)
    schema_version = fixture.get("schema_version")
    if schema_version not in {2, 3}:
        raise SnapshotError("snapshot r2 requires fixture input schema version 2 or 3")
    if not isinstance(fixture.get("case_id"), str) or not fixture["case_id"]:
        raise SnapshotError("fixture case_id must be a non-empty string")
    if not isinstance(fixture.get("fixture_revision"), str) or not fixture[
        "fixture_revision"
    ]:
        raise SnapshotError("fixture revision must be a non-empty string")
    if fixture["fixture_revision"] != f"r{schema_version}":
        raise SnapshotError("fixture revision must match fixture schema version")
    changes = fixture.get("changes")
    if not isinstance(changes, list) or not changes:
        raise SnapshotError("fixture changes must be a non-empty array")
    changed_paths = fixture.get("changed_paths")
    if changed_paths != [change.get("path") for change in changes]:
        raise SnapshotError("changed_paths must match changes in order")

    overlay_paths = []
    for change in changes:
        path = r1._normalized_path(change["path"], "fixture change path")
        if not isinstance(change.get("content_after"), str):
            raise SnapshotError(f"fixture content_after must be text: {path}")
        content = change["content_after"].encode("utf-8")
        destination = r1._safe_destination(snapshot_root, path)
        r1._write_regular(destination, content, executable=False)
        entries[path] = {
            "path": path,
            "type": "file",
            "mode": "100644",
            "sha256": r1._sha256_bytes(content),
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
        "snapshot_revision": "pr-review-repository-snapshot-r2",
        "target_repository_ref": {"commit": commit, "tree": tree},
        "fixture": {
            "case_id": fixture["case_id"],
            "revision": fixture["fixture_revision"],
            "input_sha256": r1._sha256_file(fixture_input_path),
        },
        "overlay_paths": overlay_paths,
        "file_count": len(entries),
        "regular_file_bytes": sum(
            entry.get("bytes", 0) for entry in canonical_entries
        ),
        "available_paths_sha256": r1._sha256_bytes(available_paths),
        "snapshot_sha256": r1._sha256_bytes(canonical),
        "workspace_boundary": {"git_directory_present": False, "write_allowed": False},
    }
    r1._make_read_only(snapshot_root)
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
            with tempfile.TemporaryDirectory(
                prefix="pr-review-snapshot-r2-"
            ) as directory:
                temporary_root = Path(directory)
                try:
                    receipt = materialize_snapshot(
                        args.repository,
                        args.commit,
                        args.fixture_input,
                        temporary_root,
                    )
                finally:
                    r1._make_cleanup_writable(temporary_root / "repository")
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
    except (SnapshotError, collector.AuthorityCollectionError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
