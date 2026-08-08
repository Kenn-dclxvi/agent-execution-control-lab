#!/usr/bin/env python3
"""Materialize model-visible authority content from a fixed selection receipt."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pr_review_authority_collector as collector


class AuthorityPacketError(ValueError):
    pass


INSTANCE_ROOT = Path(__file__).resolve().parents[1]


def _load_json(path: Path) -> Any:
    try:
        with path.open(encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise AuthorityPacketError(f"unable to read JSON {path}: {exc}") from exc


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def materialize_authority_packet(
    repository: Path, receipt_path: Path
) -> dict[str, Any]:
    receipt = _load_json(receipt_path)
    if receipt.get("schema_version") != (
        "agent-execution-control-lab.pr-review-authority-selection/v1"
    ):
        raise AuthorityPacketError("authority selection schema is invalid")
    target = receipt.get("target_repository_ref")
    if not isinstance(target, dict):
        raise AuthorityPacketError("target_repository_ref is invalid")
    commit = target.get("commit")
    tree = target.get("tree")
    observed_tree = collector._git(
        repository, "rev-parse", f"{commit}^{{tree}}"
    ).decode().strip()
    if observed_tree != tree:
        raise AuthorityPacketError("target tree mismatch")

    packet_authorities = []
    for index, expected in enumerate(receipt.get("authorities", [])):
        if not isinstance(expected, dict):
            raise AuthorityPacketError(f"authorities[{index}] is invalid")
        observed = collector._resolve_authority(
            repository, commit, expected["source_path"]
        )
        for key in (
            "source_path",
            "source_mode",
            "source_blob_sha1",
            "symlink_target",
            "resolved_path",
            "resolved_mode",
            "resolved_blob_sha1",
            "content_sha256",
            "content_bytes",
        ):
            if observed[key] != expected[key]:
                raise AuthorityPacketError(
                    f"authorities[{index}].{key} does not match fixed tree"
                )
        content = collector._blob(repository, commit, observed["resolved_path"])
        try:
            content_text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise AuthorityPacketError(
                f"authority is not UTF-8: {observed['resolved_path']}"
            ) from exc
        packet_authorities.append(
            {
                "source_path": observed["source_path"],
                "resolved_path": observed["resolved_path"],
                "authority_role": expected["authority_role"],
                "applies_to": expected["applies_to"],
                "content_sha256": observed["content_sha256"],
                "content": content_text,
            }
        )

    if not packet_authorities:
        raise AuthorityPacketError("authority selection is empty")
    try:
        receipt_identity = receipt_path.resolve().relative_to(
            INSTANCE_ROOT.resolve()
        ).as_posix()
    except ValueError:
        receipt_identity = receipt_path.name
    return {
        "schema_version": "agent-execution-control-lab.pr-review-authority-packet/v1",
        "target_repository_ref": {"commit": commit, "tree": tree},
        "selection_receipt": {
            "path": receipt_identity,
            "sha256": _sha256(receipt_path),
        },
        "path_bindings": receipt["path_bindings"],
        "authorities": packet_authorities,
    }


def _write_once(path: Path, value: Any) -> None:
    if path.exists():
        raise AuthorityPacketError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--selection-receipt", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        packet = materialize_authority_packet(
            args.repository, args.selection_receipt
        )
        if args.output is not None:
            _write_once(args.output, packet)
        print(json.dumps(packet, ensure_ascii=False, indent=2, sort_keys=True))
    except (AuthorityPacketError, collector.AuthorityCollectionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
