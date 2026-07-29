#!/usr/bin/env python3
"""Fail-closed storage controls and evidence sealing for long evaluation runs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.storage_copy import COPY_MODE_ENV, StorageCopyError, materialize_tree

from layer2.extensions.long_run_storage.codex_config_cleanup import (
    CodexConfigCleanupError,
    maintain_codex_config_for_batch,
)


GIB = 1024**3
DEFAULT_DISPATCH_STOP_GIB = 25.0
DEFAULT_HARD_FLOOR_GIB = 20.0
ZSTD_LONG_WINDOW_LOG = 27


def default_codex_config() -> Path:
    codex_root = os.environ.get("CODEX_HOME")
    if codex_root:
        return Path(codex_root).expanduser() / "config.toml"
    return Path.home() / ".codex" / "config.toml"


class LongRunStorageError(Exception):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise LongRunStorageError(f"invalid JSON object: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise LongRunStorageError(f"JSON root must be an object: {path}")
    return value


def write_json_once(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError as exc:
        raise LongRunStorageError(f"refusing to overwrite: {path}") from exc


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(serialized + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def allocated_bytes(path: Path) -> int:
    total = 0
    for directory, names, files in os.walk(path, followlinks=False):
        for name in (*names, *files):
            candidate = Path(directory) / name
            try:
                metadata = candidate.lstat()
            except FileNotFoundError:
                continue
            total += metadata.st_blocks * 512
    return total


def evaluate_capacity(
    free_bytes: int,
    dispatch_stop_bytes: int,
    hard_floor_bytes: int,
    estimated_next_batch_bytes: int = 0,
) -> dict[str, Any]:
    if hard_floor_bytes <= 0 or dispatch_stop_bytes < hard_floor_bytes:
        raise LongRunStorageError("capacity limits must satisfy 0 < hard floor <= dispatch stop")
    if estimated_next_batch_bytes < 0:
        raise LongRunStorageError("estimated next batch bytes must not be negative")
    projected_free = free_bytes - estimated_next_batch_bytes
    if free_bytes < hard_floor_bytes:
        status = "hard_floor_breached"
        dispatch_allowed = False
    elif projected_free < dispatch_stop_bytes:
        status = "dispatch_stopped"
        dispatch_allowed = False
    else:
        status = "dispatch_allowed"
        dispatch_allowed = True
    return {
        "schema_version": "the-caption-prompt.long-run-capacity/v1",
        "sampled_at": utc_now(),
        "status": status,
        "dispatch_allowed": dispatch_allowed,
        "free_bytes": free_bytes,
        "estimated_next_batch_bytes": estimated_next_batch_bytes,
        "projected_free_bytes": projected_free,
        "dispatch_stop_bytes": dispatch_stop_bytes,
        "hard_floor_bytes": hard_floor_bytes,
    }


def capacity_guard(
    path: Path,
    sample_log: Path | None,
    dispatch_stop_gib: float = DEFAULT_DISPATCH_STOP_GIB,
    hard_floor_gib: float = DEFAULT_HARD_FLOOR_GIB,
    estimated_next_batch_gib: float = 0.0,
) -> dict[str, Any]:
    path = path.resolve()
    if not path.exists():
        raise LongRunStorageError(f"capacity path does not exist: {path}")
    if dispatch_stop_gib <= 0 or hard_floor_gib <= 0 or estimated_next_batch_gib < 0:
        raise LongRunStorageError("GiB values must be positive (estimate may be zero)")
    usage = shutil.disk_usage(path)
    result = evaluate_capacity(
        usage.free,
        round(dispatch_stop_gib * GIB),
        round(hard_floor_gib * GIB),
        round(estimated_next_batch_gib * GIB),
    )
    result["path"] = str(path)
    result["total_bytes"] = usage.total
    result["used_bytes"] = usage.used
    if sample_log is not None:
        append_jsonl(sample_log.resolve(), result)
    return result


def materialize_layer1(
    source: Path,
    destination: Path,
    receipt: Path,
    allow_copy_fallback: bool = False,
) -> dict[str, Any]:
    source = source.resolve()
    destination = destination.resolve()
    receipt = receipt.resolve()
    old_mode = os.environ.get(COPY_MODE_ENV)
    os.environ[COPY_MODE_ENV] = "auto" if allow_copy_fallback else "clonefile"
    try:
        method = materialize_tree(source, destination)
    except StorageCopyError as exc:
        raise LongRunStorageError(f"Layer 1 materialization failed: {exc}") from exc
    finally:
        if old_mode is None:
            os.environ.pop(COPY_MODE_ENV, None)
        else:
            os.environ[COPY_MODE_ENV] = old_mode
    if method != "clonefile" and not allow_copy_fallback:
        shutil.rmtree(destination)
        raise LongRunStorageError("Layer 1 materialization did not use clonefile")
    document = {
        "schema_version": "the-caption-prompt.layer1-materialization/v1",
        "created_at": utc_now(),
        "source": str(source),
        "destination": str(destination),
        "method": method,
        "copy_fallback_allowed": allow_copy_fallback,
    }
    write_json_once(receipt, document)
    return document


def run_git(workspace: Path, arguments: list[str], env: dict[str, str] | None = None) -> bytes:
    completed = subprocess.run(
        ["git", *arguments], cwd=workspace, env=env, capture_output=True, check=False
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise LongRunStorageError(f"git {' '.join(arguments)} failed: {detail}")
    return completed.stdout


def bundle_targets(capsule: dict[str, Any]) -> set[str]:
    parameters = capsule.get("parameters")
    if not isinstance(parameters, dict):
        raise LongRunStorageError("capsule.parameters must be an object")
    bundle_value = parameters.get("prompt_bundle")
    if not isinstance(bundle_value, str) or not bundle_value:
        raise LongRunStorageError("capsule.parameters.prompt_bundle is required")
    manifest = load_object(Path(bundle_value).resolve() / "manifest.json")
    files = manifest.get("files")
    if not isinstance(files, list):
        raise LongRunStorageError("bundle manifest files must be an array")
    targets: set[str] = set()
    for index, item in enumerate(files):
        target = item.get("target") if isinstance(item, dict) else None
        if not isinstance(target, str) or not target:
            raise LongRunStorageError(f"bundle manifest files[{index}].target is invalid")
        targets.add(target)
    return targets


def result_diff(workspace: Path, base_commit: str, paths: list[str]) -> bytes:
    if not paths:
        return b""
    with tempfile.TemporaryDirectory(prefix="rating-view-index-") as temporary:
        index = Path(temporary) / "index"
        env = os.environ.copy()
        env["GIT_INDEX_FILE"] = str(index)
        run_git(workspace, ["read-tree", base_commit], env)
        run_git(workspace, ["add", "-A", "--", *paths], env)
        return run_git(
            workspace,
            ["diff", "--cached", "--binary", "--full-index", base_commit, "--", *paths],
            env,
        )


def valid_all_agent_usage(cycle: Path, run_id: str) -> dict[str, Any]:
    path = cycle / "layer2" / "extensions" / run_id / "all-agent-usage" / "usage.json"
    try:
        usage = load_object(path)
    except LongRunStorageError as exc:
        raise LongRunStorageError(f"run lacks all-agent usage v1: {run_id}") from exc
    if usage.get("schema_version") != "the-caption-prompt.all-agent-usage/v1":
        raise LongRunStorageError(f"run lacks all-agent usage v1: {run_id}")
    total = usage.get("all_agent_total_tokens")
    sessions = usage.get("sessions")
    if not isinstance(total, int) or isinstance(total, bool) or total < 0:
        raise LongRunStorageError(f"run has invalid all-agent total: {run_id}")
    if not isinstance(sessions, list) or not sessions:
        raise LongRunStorageError(f"run has incomplete all-agent sessions: {run_id}")
    return usage


def create_rating_view(cycle: Path, run_id: str) -> dict[str, Any]:
    evidence = cycle / "layer2" / "evidence" / run_id
    workspace = evidence / "workspace"
    extension = cycle / "layer2" / "extensions" / run_id / "codex-adapter"
    capsule_path = cycle / "layer2" / "capsules" / f"{run_id}.json"
    adapter = load_object(extension / "execution.json")
    capsule = load_object(capsule_path)
    final_paths = adapter.get("final_changed_paths")
    if not isinstance(final_paths, list) or not all(
        isinstance(item, str) and item for item in final_paths
    ):
        raise LongRunStorageError(f"adapter final_changed_paths is invalid: {run_id}")
    prompt_targets = bundle_targets(capsule)
    visible_paths = sorted(set(final_paths) - prompt_targets)
    base_commit = adapter.get("prompt_overlay_commit")
    if not isinstance(base_commit, str) or not base_commit:
        raise LongRunStorageError(f"adapter prompt_overlay_commit is missing: {run_id}")
    if not (workspace / ".git").exists():
        raise LongRunStorageError(f"workspace is not an intact Git checkout: {run_id}")

    rating_view = evidence / "rating-view"
    if rating_view.exists() or rating_view.is_symlink():
        raise LongRunStorageError(f"refusing to overwrite rating view: {rating_view}")
    rating_view.mkdir()
    diff = result_diff(workspace, base_commit, visible_paths)
    (rating_view / "result.diff").write_bytes(diff)
    final_response = extension / "final-response.txt"
    if not final_response.is_file():
        raise LongRunStorageError(f"adapter final response is missing: {run_id}")
    shutil.copyfile(final_response, rating_view / "final-response.txt")
    unexpected = adapter.get("unexpected_changed_paths")
    validation = {
        "schema_version": "the-caption-prompt.rating-view-validation/v1",
        "generated_at": utc_now(),
        "run_id": run_id,
        "adapter_exit_code": adapter.get("codex_exit_code"),
        "final_changed_paths": sorted(final_paths),
        "bundle_targets_excluded": sorted(set(final_paths).intersection(prompt_targets)),
        "result_paths": visible_paths,
        "unexpected_changed_paths": unexpected if isinstance(unexpected, list) else [],
        "test_claim_source": "final-response.txt; no machine pass/fail inferred",
    }
    write_json_once(rating_view / "validation.json", validation)
    return {
        "run_id": run_id,
        "result_paths": visible_paths,
        "result_diff_sha256": sha256_bytes(diff),
        "final_response_sha256": sha256_file(rating_view / "final-response.txt"),
        "validation_sha256": sha256_file(rating_view / "validation.json"),
    }


def archive_entries(batch: Path, excluded_prefixes: tuple[str, ...]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for directory, names, files in os.walk(batch, followlinks=False):
        base = Path(directory)
        names[:] = [
            name
            for name in names
            if not any(
                (base / name).relative_to(batch).as_posix() == prefix
                or (base / name).relative_to(batch).as_posix().startswith(prefix + "/")
                for prefix in excluded_prefixes
            )
        ]
        for name in sorted((*names, *files)):
            path = base / name
            relative = path.relative_to(batch).as_posix()
            if any(
                relative == prefix or relative.startswith(prefix + "/")
                for prefix in excluded_prefixes
            ):
                continue
            if path.is_symlink():
                target = os.readlink(path)
                entries.append(
                    {
                        "path": relative,
                        "type": "symlink",
                        "link_target": target,
                        "sha256": sha256_bytes(target.encode("utf-8")),
                        "size": len(target.encode("utf-8")),
                        "mode": stat.S_IMODE(path.lstat().st_mode),
                    }
                )
            elif path.is_file():
                entries.append(
                    {
                        "path": relative,
                        "type": "file",
                        "sha256": sha256_file(path),
                        "size": path.stat().st_size,
                        "mode": stat.S_IMODE(path.stat().st_mode),
                    }
                )
            elif path.is_dir():
                entries.append(
                    {
                        "path": relative,
                        "type": "directory",
                        "size": 0,
                        "mode": stat.S_IMODE(path.stat().st_mode),
                    }
                )
    entries.sort(key=lambda item: item["path"])
    return entries


def create_verified_archive(
    batch: Path, archive: Path, entries: list[dict[str, Any]], zstd_level: int
) -> dict[str, Any]:
    if archive.exists() or archive.is_symlink():
        raise LongRunStorageError(f"refusing to overwrite archive: {archive}")
    zstd = shutil.which("zstd")
    if zstd is None:
        raise LongRunStorageError("zstd executable is required")
    archive.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="long-run-archive-", dir=archive.parent) as temporary:
        compressed = Path(temporary) / "evidence.tar.zst"
        with compressed.open("wb") as output:
            compressor = subprocess.Popen(
                [
                    zstd,
                    "-q",
                    f"-{zstd_level}",
                    f"--long={ZSTD_LONG_WINDOW_LOG}",
                    "-c",
                ],
                stdin=subprocess.PIPE,
                stdout=output,
                stderr=subprocess.PIPE,
            )
            if compressor.stdin is None or compressor.stderr is None:
                compressor.kill()
                raise LongRunStorageError("failed to open zstd compression stream")
            try:
                with tarfile.open(
                    fileobj=compressor.stdin, mode="w|", format=tarfile.PAX_FORMAT
                ) as handle:
                    for entry in entries:
                        handle.add(
                            batch / entry["path"],
                            arcname=entry["path"],
                            recursive=False,
                        )
                compressor.stdin.close()
                stderr = compressor.stderr.read().decode("utf-8", errors="replace").strip()
                compressor.stderr.close()
                returncode = compressor.wait()
            except Exception:
                compressor.kill()
                compressor.wait()
                raise
        if returncode != 0:
            raise LongRunStorageError(f"zstd compression failed: {stderr}")
        tested = subprocess.run([zstd, "-q", "-t", str(compressed)], check=False)
        if tested.returncode != 0:
            raise LongRunStorageError("zstd integrity test failed")
        expected = {entry["path"]: entry for entry in entries}
        decompressor = subprocess.Popen(
            [zstd, "-q", "-dc", str(compressed)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if decompressor.stdout is None or decompressor.stderr is None:
            decompressor.kill()
            raise LongRunStorageError("failed to open zstd verification stream")
        seen: set[str] = set()
        try:
            with tarfile.open(fileobj=decompressor.stdout, mode="r|") as handle:
                for member in handle:
                    name = member.name
                    entry = expected.get(name)
                    if entry is None or name in seen:
                        raise LongRunStorageError(f"unexpected archive member: {name}")
                    seen.add(name)
                    if member.mode != entry["mode"]:
                        raise LongRunStorageError(f"archive member mode mismatch: {name}")
                    if entry["type"] == "directory":
                        if not member.isdir():
                            raise LongRunStorageError(f"archive member type mismatch: {name}")
                        continue
                    if entry["type"] == "symlink":
                        if not member.issym():
                            raise LongRunStorageError(f"archive member type mismatch: {name}")
                        actual = sha256_bytes(member.linkname.encode("utf-8"))
                    else:
                        if not member.isfile():
                            raise LongRunStorageError(f"archive member type mismatch: {name}")
                        extracted = handle.extractfile(member)
                        if extracted is None:
                            raise LongRunStorageError(f"archive member is unreadable: {name}")
                        digest = hashlib.sha256()
                        for block in iter(lambda: extracted.read(1024 * 1024), b""):
                            digest.update(block)
                        actual = digest.hexdigest()
                    if actual != entry["sha256"]:
                        raise LongRunStorageError(f"archive member hash mismatch: {name}")
            decompressor.stdout.close()
            stderr = decompressor.stderr.read().decode("utf-8", errors="replace").strip()
            decompressor.stderr.close()
            returncode = decompressor.wait()
        except Exception:
            decompressor.kill()
            decompressor.wait()
            raise
        if returncode != 0:
            raise LongRunStorageError(f"zstd verification failed: {stderr}")
        if seen != set(expected):
            missing = sorted(set(expected) - seen)
            raise LongRunStorageError(f"archive members are missing: {missing}")
        os.replace(compressed, archive)
    return {
        "archive": str(archive),
        "archive_sha256": sha256_file(archive),
        "archive_bytes": archive.stat().st_size,
        "entry_count": len(entries),
        "source_bytes": sum(entry["size"] for entry in entries),
        "zstd_level": zstd_level,
    }


def completed_executions(cycle: Path) -> tuple[list[str], list[str]]:
    valid: list[str] = []
    excluded: list[str] = []
    executions = sorted((cycle / "layer2" / "evidence").glob("*/execution.json"))
    if not executions:
        raise LongRunStorageError("batch has no Layer 2 executions")
    for path in executions:
        execution = load_object(path)
        run_id = path.parent.name
        status = execution.get("status")
        if status == "valid":
            valid.append(run_id)
        elif status == "excluded":
            excluded.append(run_id)
        else:
            raise LongRunStorageError(f"run is not terminal: {run_id}")
    return valid, excluded


def seal_batch(batch: Path, zstd_level: int = 6) -> dict[str, Any]:
    batch = batch.resolve()
    cycle = batch / "cycle"
    if not (cycle / "layer1" / "set.json").is_file():
        raise LongRunStorageError(f"batch is not a frozen cycle: {batch}")
    compact = batch / "compact"
    archive = compact / "execution-evidence.tar.zst"
    manifest_path = compact / "execution-seal.json"
    receipt_path = compact / "execution-prune-receipt.json"
    for output in (archive, manifest_path, receipt_path):
        if output.exists() or output.is_symlink():
            raise LongRunStorageError(f"refusing to overwrite sealed output: {output}")

    valid, excluded = completed_executions(cycle)
    ratings: list[dict[str, Any]] = []
    for run_id in valid:
        valid_all_agent_usage(cycle, run_id)
        ratings.append(create_rating_view(cycle, run_id))

    archived_then_pruned = [
        f"cycle/layer2/evidence/{run_id}/workspace" for run_id in (*valid, *excluded)
    ]
    excluded_prefixes = ("compact",)
    entries = archive_entries(batch, excluded_prefixes)
    archive_result = create_verified_archive(batch, archive, entries, zstd_level)
    manifest = {
        "schema_version": "the-caption-prompt.execution-evidence-seal/v1",
        "created_at": utc_now(),
        "batch": str(batch),
        "valid_run_ids": valid,
        "excluded_run_ids": excluded,
        "rating_views": ratings,
        "archived_then_pruned_paths": archived_then_pruned,
        "entries": entries,
        **archive_result,
    }
    write_json_once(manifest_path, manifest)

    before = allocated_bytes(batch)
    pruned: list[str] = []
    for run_id in (*valid, *excluded):
        workspace = cycle / "layer2" / "evidence" / run_id / "workspace"
        if workspace.is_dir() and not workspace.is_symlink():
            shutil.rmtree(workspace)
            pruned.append(workspace.relative_to(batch).as_posix())
    after = allocated_bytes(batch)
    receipt = {
        "schema_version": "the-caption-prompt.execution-prune-receipt/v1",
        "created_at": utc_now(),
        "batch": str(batch),
        "seal_sha256": sha256_file(manifest_path),
        "archive_sha256": archive_result["archive_sha256"],
        "pruned_paths": pruned,
        "allocated_bytes_before_prune": before,
        "allocated_bytes_after_prune": after,
        "allocated_bytes_reclaimed": max(0, before - after),
    }
    write_json_once(receipt_path, receipt)
    return receipt


def compact_batch(batch: Path, zstd_level: int = 9) -> dict[str, Any]:
    batch = batch.resolve()
    cycle = batch / "cycle"
    registration = cycle / "layer4" / "result-registration.json"
    if not registration.is_file():
        raise LongRunStorageError("final compact requires layer4/result-registration.json")
    execution_receipt = batch / "compact" / "execution-prune-receipt.json"
    if not execution_receipt.is_file():
        raise LongRunStorageError("final compact requires a completed execution seal")
    compact = batch / "compact"
    archive = compact / "final-evidence.tar.zst"
    manifest_path = compact / "final-compact-manifest.json"
    receipt_path = compact / "final-compact-receipt.json"
    for output in (archive, manifest_path, receipt_path):
        if output.exists() or output.is_symlink():
            raise LongRunStorageError(f"refusing to overwrite compact output: {output}")
    entries = archive_entries(batch, ("compact", "cycle/layer1"))
    archive_result = create_verified_archive(batch, archive, entries, zstd_level)
    manifest = {
        "schema_version": "the-caption-prompt.final-evidence-seal/v1",
        "created_at": utc_now(),
        "batch": str(batch),
        "result_registration_sha256": sha256_file(registration),
        "entries": entries,
        **archive_result,
    }
    write_json_once(manifest_path, manifest)
    before = allocated_bytes(batch)
    pruned: list[str] = []
    for name in ("runner-evidence",):
        path = batch / name
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
            pruned.append(name)
    for name in ("layer2", "layer3"):
        path = cycle / name
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
            pruned.append(f"cycle/{name}")
    for path in (cycle / "layer4").iterdir():
        if path != registration:
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()
            pruned.append(path.relative_to(batch).as_posix())
    after = allocated_bytes(batch)
    receipt = {
        "schema_version": "the-caption-prompt.final-compact-receipt/v1",
        "created_at": utc_now(),
        "batch": str(batch),
        "manifest_sha256": sha256_file(manifest_path),
        "archive_sha256": archive_result["archive_sha256"],
        "retained_uncompressed": [
            path
            for path in (
                "summary.json",
                "plan.json",
                "cycle/layer1",
                "cycle/layer4/result-registration.json",
            )
            if (batch / path).exists()
        ],
        "pruned_paths": pruned,
        "allocated_bytes_before_prune": before,
        "allocated_bytes_after_prune": after,
        "allocated_bytes_reclaimed": max(0, before - after),
    }
    write_json_once(receipt_path, receipt)
    return receipt


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


def non_negative_float(value: str) -> float:
    parsed = float(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must not be negative")
    return parsed


def zstd_level(value: str) -> int:
    parsed = int(value)
    if parsed < 1 or parsed > 19:
        raise argparse.ArgumentTypeError("zstd level must be 1..19")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    guard = subparsers.add_parser("guard", help="stop dispatch before free space is exhausted")
    guard.add_argument("--path", type=Path, required=True)
    guard.add_argument("--sample-log", type=Path)
    guard.add_argument(
        "--dispatch-stop-gib", type=positive_float, default=DEFAULT_DISPATCH_STOP_GIB
    )
    guard.add_argument("--hard-floor-gib", type=positive_float, default=DEFAULT_HARD_FLOOR_GIB)
    guard.add_argument("--estimated-next-batch-gib", type=non_negative_float, default=0.0)

    materialize = subparsers.add_parser("materialize-layer1", help="clone a frozen Layer 1")
    materialize.add_argument("--source", type=Path, required=True)
    materialize.add_argument("--destination", type=Path, required=True)
    materialize.add_argument("--receipt", type=Path, required=True)
    materialize.add_argument("--allow-copy-fallback", action="store_true")

    seal = subparsers.add_parser("seal-batch", help="seal rating evidence and prune workspaces")
    seal.add_argument("--batch", type=Path, required=True)
    seal.add_argument("--zstd-level", type=zstd_level, default=6)
    seal.add_argument("--codex-config", type=Path, default=default_codex_config())
    seal.add_argument("--skip-codex-config-cleanup", action="store_true")

    compact = subparsers.add_parser("compact-batch", help="compress a registered batch")
    compact.add_argument("--batch", type=Path, required=True)
    compact.add_argument("--zstd-level", type=zstd_level, default=9)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "guard":
            result = capacity_guard(
                args.path,
                args.sample_log,
                args.dispatch_stop_gib,
                args.hard_floor_gib,
                args.estimated_next_batch_gib,
            )
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0 if result["dispatch_allowed"] else 3
        if args.command == "materialize-layer1":
            result = materialize_layer1(
                args.source, args.destination, args.receipt, args.allow_copy_fallback
            )
        elif args.command == "seal-batch":
            result = seal_batch(args.batch, args.zstd_level)
            if not args.skip_codex_config_cleanup:
                try:
                    result["codex_project_config_cleanup"] = maintain_codex_config_for_batch(
                        args.batch, args.codex_config
                    )
                except (CodexConfigCleanupError, OSError) as exc:
                    result["codex_project_config_cleanup"] = {
                        "status": "warning",
                        "error": str(exc),
                    }
        else:
            result = compact_batch(args.batch, args.zstd_level)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (LongRunStorageError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
