#!/usr/bin/env python3
"""管理用componentから自己完結したpromptファイルを構成する。"""

from __future__ import annotations

import argparse
import hashlib
import json
import string
import sys
from pathlib import Path, PurePosixPath
from typing import Any

if __package__:
    from .export_prompt_bundle import (
        SCHEMA_VERSION as BUNDLE_SCHEMA_VERSION,
        BundleError,
        verify_bundle,
    )
else:
    from export_prompt_bundle import (
        SCHEMA_VERSION as BUNDLE_SCHEMA_VERSION,
        BundleError,
        verify_bundle,
    )

SCHEMA_VERSION = "agent-execution-control.prompt-composition/v1"
RECEIPT_SCHEMA_VERSION = "agent-execution-control.prompt-composition-receipt/v1"


class CompositionError(ValueError):
    """Composition manifestまたは構成結果がcontractを満たさない。"""


def _load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CompositionError(f"invalid composition manifest: {path}") from exc
    if not isinstance(value, dict):
        raise CompositionError("composition manifest root must be an object")
    if value.get("schema_version") != SCHEMA_VERSION:
        raise CompositionError("unsupported composition schema_version")
    return value


def composition_sha256(manifest: dict[str, Any]) -> str:
    """composition_sha256自身を除いた管理artifact identityを返す。"""

    identity = {key: value for key, value in manifest.items() if key != "composition_sha256"}
    canonical = json.dumps(
        identity,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _component_path(root: Path, raw_path: object) -> Path:
    if not isinstance(raw_path, str) or not raw_path:
        raise CompositionError("component path must be a non-empty string")
    relative = PurePosixPath(raw_path)
    if relative.is_absolute() or ".." in relative.parts or "." in relative.parts:
        raise CompositionError(f"unsafe component path: {raw_path}")
    resolved = root.joinpath(*relative.parts).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise CompositionError(f"component escapes composition root: {raw_path}") from exc
    if not resolved.is_file():
        raise CompositionError(f"component is not a file: {raw_path}")
    return resolved


def compose(manifest_path: Path) -> tuple[bytes, dict[str, Any]]:
    """Manifest順にcomponent bytesを連結し、検証済みreceiptを返す。"""

    manifest_path = manifest_path.resolve()
    manifest = _load_manifest(manifest_path)
    identity = manifest.get("composition_identity")
    artifact = manifest.get("artifact")
    declared_composition_sha256 = manifest.get("composition_sha256")
    source_prompt_identity = manifest.get("source_prompt_identity")
    output_prompt_identity = manifest.get("output_prompt_identity")
    output_target = manifest.get("output_target")
    expected_sha256 = manifest.get("expected_output_sha256")
    blocks = manifest.get("functional_blocks")
    components = manifest.get("components")
    if not isinstance(identity, str) or not identity:
        raise CompositionError("composition_identity must be a non-empty string")
    if artifact != {
        "artifact_role": "composition_source",
        "evaluation_eligible": False,
        "model_visible": False,
    }:
        raise CompositionError("composition artifact must be model-invisible and evaluation-ineligible")
    if not isinstance(source_prompt_identity, str) or not source_prompt_identity:
        raise CompositionError("source_prompt_identity must be a non-empty string")
    if not isinstance(output_prompt_identity, str) or not output_prompt_identity:
        raise CompositionError("output_prompt_identity must be a non-empty string")
    actual_composition_sha256 = composition_sha256(manifest)
    if declared_composition_sha256 != actual_composition_sha256:
        raise CompositionError(
            "composition SHA-256 mismatch: "
            f"expected {declared_composition_sha256}, got {actual_composition_sha256}"
        )
    if output_target != "AGENTS.md":
        raise CompositionError("output_target must be AGENTS.md")
    if (
        not isinstance(expected_sha256, str)
        or len(expected_sha256) != 64
        or any(character not in string.hexdigits for character in expected_sha256)
    ):
        raise CompositionError("expected_output_sha256 must be a SHA-256 hex string")
    if not isinstance(blocks, list) or not blocks or not all(isinstance(x, str) and x for x in blocks):
        raise CompositionError("functional_blocks must be a non-empty string array")
    if len(set(blocks)) != len(blocks):
        raise CompositionError("functional_blocks must be unique")
    if not isinstance(components, list) or not components:
        raise CompositionError("components must be a non-empty array")

    root = manifest_path.parent
    component_ids: set[str] = set()
    component_paths: set[str] = set()
    used_blocks: set[str] = set()
    payload = bytearray()
    receipt_components: list[dict[str, Any]] = []
    for entry in components:
        if not isinstance(entry, dict):
            raise CompositionError("component entry must be an object")
        component_id = entry.get("id")
        block = entry.get("functional_block")
        raw_path = entry.get("path")
        declared_component_sha256 = entry.get("sha256")
        if not isinstance(component_id, str) or not component_id:
            raise CompositionError("component id must be a non-empty string")
        if component_id in component_ids:
            raise CompositionError(f"duplicate component id: {component_id}")
        if block not in blocks:
            raise CompositionError(f"unknown functional_block for {component_id}: {block}")
        if not isinstance(raw_path, str) or not raw_path:
            raise CompositionError("component path must be a non-empty string")
        if raw_path in component_paths:
            raise CompositionError(f"duplicate component path: {raw_path}")
        path = _component_path(root, raw_path)
        content = path.read_bytes()
        actual_component_sha256 = hashlib.sha256(content).hexdigest()
        if declared_component_sha256 != actual_component_sha256:
            raise CompositionError(
                f"component SHA-256 mismatch for {component_id}: "
                f"expected {declared_component_sha256}, got {actual_component_sha256}"
            )
        component_ids.add(component_id)
        component_paths.add(raw_path)
        used_blocks.add(block)
        payload.extend(content)
        receipt_components.append(
            {
                "bytes": len(content),
                "functional_block": block,
                "id": component_id,
                "path": raw_path,
                "sha256": actual_component_sha256,
            }
        )
    if used_blocks != set(blocks):
        missing = sorted(set(blocks) - used_blocks)
        raise CompositionError(f"functional_blocks without components: {missing}")

    output = bytes(payload)
    actual_sha256 = hashlib.sha256(output).hexdigest()
    if actual_sha256 != expected_sha256:
        raise CompositionError(
            f"composed output SHA-256 mismatch: expected {expected_sha256}, got {actual_sha256}"
        )
    receipt = {
        "artifact_role": "composition_generation_receipt",
        "bytes": len(output),
        "components": receipt_components,
        "composition_identity": identity,
        "composition_sha256": actual_composition_sha256,
        "evaluation_eligible": False,
        "functional_blocks": blocks,
        "model_visible": False,
        "output_sha256": actual_sha256,
        "output_prompt_identity": output_prompt_identity,
        "output_target": output_target,
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "source_prompt_identity": source_prompt_identity,
    }
    return output, receipt


def verify_bundle_binding(manifest_path: Path, bundle_path: Path) -> dict[str, Any]:
    """構成結果が検証済みfull bundleの指定targetとprompt identityへ一致することを確認する。"""

    output, composition_receipt = compose(manifest_path)
    try:
        bundle = verify_bundle(bundle_path.resolve())
    except (BundleError, OSError) as exc:
        raise CompositionError(f"invalid prompt bundle: {bundle_path}") from exc
    if bundle.get("schema_version") != BUNDLE_SCHEMA_VERSION:
        raise CompositionError("bundle uses an unsupported schema_version")
    expected_prompt_identity = composition_receipt["output_prompt_identity"]
    if bundle.get("prompt_identity") != expected_prompt_identity:
        raise CompositionError(
            "bundle prompt identity mismatch: "
            f"expected {expected_prompt_identity}, got {bundle.get('prompt_identity')}"
        )
    output_target = composition_receipt["output_target"]
    entries = [entry for entry in bundle["files"] if entry.get("target") == output_target]
    if len(entries) != 1 or entries[0].get("type") != "file":
        raise CompositionError(f"bundle does not contain one regular {output_target} target")
    if entries[0].get("sha256") != composition_receipt["output_sha256"]:
        raise CompositionError(f"bundle {output_target} does not match composed output")
    return {
        **composition_receipt,
        "artifact_role": "composition_bundle_binding_receipt",
        "binding_status": "verified",
        "bundle_sha256": bundle["bundle_sha256"],
        "bundle_prompt_identity": bundle["prompt_identity"],
        "bundle_schema_version": bundle["schema_version"],
        "output_bytes_verified": len(output),
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    render = commands.add_parser("render")
    render.add_argument("--manifest", required=True)
    render.add_argument("--output", required=True)
    check = commands.add_parser("check")
    check.add_argument("--manifest", required=True)
    check.add_argument("--against", required=True)
    bind = commands.add_parser("verify-bundle")
    bind.add_argument("--manifest", required=True)
    bind.add_argument("--bundle", required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "verify-bundle":
            receipt = verify_bundle_binding(Path(args.manifest), Path(args.bundle))
            target = Path(args.bundle)
        else:
            output, receipt = compose(Path(args.manifest))
        if args.command == "render":
            target = Path(args.output)
            if target.exists():
                raise CompositionError(f"refusing to overwrite output: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(output)
        elif args.command == "check":
            target = Path(args.against)
            if not target.is_file():
                raise CompositionError(f"comparison target is not a file: {target}")
            if target.read_bytes() != output:
                raise CompositionError(f"composed output differs from comparison target: {target}")
        receipt["operation"] = args.command
        receipt["target"] = str(target)
    except (CompositionError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
