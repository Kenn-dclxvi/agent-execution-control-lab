#!/usr/bin/env python3
"""Materialize one model-visible full prompt bundle from a base and route delta."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

try:
    from .export_prompt_bundle import (
        BundleError,
        bundle_sha256,
        bundle_stored_path,
        canonical_json,
        storage_format_of,
        verify_bundle,
        write_manifest,
    )
except ImportError:
    from export_prompt_bundle import (  # type: ignore[no-redef]
        BundleError,
        bundle_sha256,
        bundle_stored_path,
        canonical_json,
        storage_format_of,
        verify_bundle,
        write_manifest,
    )


ROUTE_SCHEMA_VERSION = "the-caption-prompt.route-delta/v1"


class RouteMaterializationError(Exception):
    pass


def require_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RouteMaterializationError(f"{label} must be an object")
    return value


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise RouteMaterializationError(f"{label} must be a non-empty string")
    return value


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_blob_sha1(value: bytes) -> str:
    header = f"blob {len(value)}\0".encode("ascii")
    return hashlib.sha1(header + value).hexdigest()  # noqa: S324 - Git object identity


def load_route_delta(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_bytes()
        value = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RouteMaterializationError(f"invalid route delta: {path}") from exc
    delta = require_object(value, "route delta")
    if delta.get("schema_version") != ROUTE_SCHEMA_VERSION:
        raise RouteMaterializationError("unsupported route delta schema_version")
    delta["route_delta_sha256"] = sha256_bytes(canonical_json(value))
    return delta


def route_matches(delta: dict[str, Any], route_facts: dict[str, Any]) -> bool:
    applicability = require_object(delta.get("applicability"), "applicability")
    return route_facts == applicability


def select_prompt_identity(
    delta: dict[str, Any],
    route_facts: dict[str, Any],
    projected_prompt_identity: str,
) -> str:
    """Select the projected identity only for an exact route match."""
    base = require_object(delta.get("base"), "base")
    base_prompt_identity = require_string(
        base.get("prompt_identity"), "base.prompt_identity"
    )
    projected_prompt_identity = require_string(
        projected_prompt_identity, "projected_prompt_identity"
    )
    if route_matches(delta, route_facts):
        return projected_prompt_identity
    return base_prompt_identity


def insert_projection(source: bytes, projection: dict[str, Any]) -> bytes:
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RouteMaterializationError("projection target must be UTF-8") from exc
    prefix = require_string(
        projection.get("insert_after_line_prefix"),
        "projection.insert_after_line_prefix",
    )
    content = require_string(projection.get("content"), "projection.content")
    lines = text.splitlines()
    indexes = [index for index, line in enumerate(lines) if line.startswith(prefix)]
    if len(indexes) != 1:
        raise RouteMaterializationError(
            f"projection anchor must match exactly one line: {prefix!r}"
        )
    if content in lines:
        raise RouteMaterializationError("projection content is already present")
    lines.insert(indexes[0] + 1, content)
    return ("\n".join(lines) + "\n").encode("utf-8")


def materialize_route(
    base_bundle: Path,
    route_delta_path: Path,
    output: Path,
    prompt_identity: str,
    route_facts: dict[str, Any],
) -> dict[str, Any]:
    base_bundle = base_bundle.resolve()
    route_delta_path = route_delta_path.resolve()
    output = output.resolve()
    if output.exists():
        raise RouteMaterializationError(f"refusing to overwrite output: {output}")
    base = verify_bundle(base_bundle)
    delta = load_route_delta(route_delta_path)
    expected_base = require_object(delta.get("base"), "base")
    if base.get("prompt_identity") != expected_base.get("prompt_identity"):
        raise RouteMaterializationError("route delta base prompt_identity mismatch")
    if base.get("bundle_sha256") != expected_base.get("bundle_sha256"):
        raise RouteMaterializationError("route delta base bundle_sha256 mismatch")
    if not route_matches(delta, route_facts):
        raise RouteMaterializationError("route facts do not satisfy route applicability")

    projection = require_object(delta.get("projection"), "projection")
    target = require_string(projection.get("target"), "projection.target")
    route_identity = require_string(delta.get("route_identity"), "route_identity")
    route_delta_sha256 = require_string(
        delta.get("route_delta_sha256"), "route_delta_sha256"
    )
    try:
        shutil.copytree(base_bundle, output, symlinks=True)
        target_path = bundle_stored_path(output / "files", target, storage_format_of(base))
        projected = insert_projection(target_path.read_bytes(), projection)
        target_path.write_bytes(projected)

        manifest = copy.deepcopy(base)
        entries = manifest.get("files")
        if not isinstance(entries, list):
            raise RouteMaterializationError("base manifest files must be an array")
        matches = [entry for entry in entries if entry.get("target") == target]
        if len(matches) != 1 or matches[0].get("type") != "file":
            raise RouteMaterializationError("projection target must be one regular bundle file")
        matches[0]["git_blob_sha1"] = git_blob_sha1(projected)
        matches[0]["sha256"] = sha256_bytes(projected)

        manifest["artifact"] = {
            "artifact_role": "candidate",
            "baseline_identity": base["prompt_identity"],
            "change_reason": (
                "Candidate43を共通sourceとし、fixed-evidence-review routeでだけ"
                "固定evidence取得method差分を実行前合成する。"
            ),
            "evaluation_status": "not_evaluated",
            "non_goals": [
                "改善の主張",
                "採用判断",
                "release判断",
                "THE-CAPTION本体への反映",
                "非対象taskへのroute差分提示",
                "TaskSpec、Evaluation set、fixture、oracle、grader、rating contractの変更",
            ],
            "problem": (
                "固定read methodを常時可視promptへ置くと、非対象の変更taskや"
                "clarification taskへmethodが流入する。"
            ),
            "scope": (
                "Candidate43の19 path full bundleへ一つのroute差分を解決したfull bundle。"
                "変更targetはroot AGENTS.mdだけ。"
            ),
            "state": "draft",
        }
        manifest["content_relation"] = {
            "changed_targets": [target],
            "kind": "materialized_route_projection",
            "route_identity": route_identity,
            "source_prompt_identity": base["prompt_identity"],
        }
        manifest["prompt_identity"] = prompt_identity
        manifest["route_projection"] = {
            "base_bundle_sha256": base["bundle_sha256"],
            "base_prompt_identity": base["prompt_identity"],
            "route_delta_sha256": route_delta_sha256,
            "route_identity": route_identity,
            "target": target,
        }
        manifest["bundle_sha256"] = bundle_sha256(entries)
        manifest["provenance"] = {
            "construction_repository": (
                "https://github.com/Kenn-dclxvi/agent-execution-control-lab.git"
            ),
            "construction_state": "uncommitted_working_tree",
            "design_inputs": [
                "docs/candidate63-fixed-evidence-route-projection-design.md",
                "docs/prompt-control-design-principles.md",
                "docs/prompt-file-bundle.md",
                "evaluations/results/candidate43-candidate56-candidate62-task-closed-read-route-catalog-fixed_2026-07-22.md",
            ],
            "design_status": "draft",
            "evaluation_status": "not_evaluated",
            "runtime_projection_status": "not_projected",
            "source_interpretation": (
                "source_prompt_identity is the one maintained common prompt source; "
                "the route delta is visible only in the resolved fixed-evidence-review bundle."
            ),
        }
        write_manifest(output, manifest)
        return verify_bundle(output)
    except Exception:
        if output.exists():
            shutil.rmtree(output)
        raise


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--base-bundle", required=True)
    result.add_argument("--route-delta", required=True)
    result.add_argument("--route-facts", required=True)
    result.add_argument("--output", required=True)
    result.add_argument("--prompt-identity", required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        route_facts = require_object(
            json.loads(Path(args.route_facts).read_text(encoding="utf-8")),
            "route facts",
        )
        manifest = materialize_route(
            Path(args.base_bundle),
            Path(args.route_delta),
            Path(args.output),
            args.prompt_identity,
            route_facts,
        )
    except (
        BundleError,
        OSError,
        json.JSONDecodeError,
        RouteMaterializationError,
    ) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
