#!/usr/bin/env python3
"""Export a prompt file bundle from Git and duplicate it as a candidate."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any


SCHEMA_VERSION = "the-caption-prompt.bundle/v1"
BUNDLE_HASH_ALGORITHM = "sha256(canonical-json({schema_version,files}))"

# At-rest storage layout. bundle_sha256 は {schema_version, files} だけを hash する
# ため storage_format は identity に含まれず、格納形式を変えても bundle_sha256 は不変。
# - tree/v1: files/<target> をそのまま格納（従来）。
# - instruction-suffixed/v1: 命令ファイル名を suffix 付きで格納し、リポジトリ内に
#   AGENTS.md / CLAUDE.md という自動読込対象名を残さない。実体名は展開時に復元する。
STORAGE_FORMAT_LEGACY = "tree/v1"
STORAGE_FORMAT_SUFFIXED = "instruction-suffixed/v1"
DEFAULT_STORAGE_FORMAT = STORAGE_FORMAT_SUFFIXED
SUPPORTED_STORAGE_FORMATS = (STORAGE_FORMAT_LEGACY, STORAGE_FORMAT_SUFFIXED)
# 自動読込対象になる basename と、格納時に付与する suffix。
INSTRUCTION_BASENAMES = ("AGENTS.md", "CLAUDE.md")
STORE_SUFFIX = ".txt"


class BundleError(Exception):
    pass


def is_instruction_path(posix_path: str) -> bool:
    return PurePosixPath(posix_path).name in INSTRUCTION_BASENAMES


def storage_format_of(manifest: dict[str, Any]) -> str:
    value = manifest.get("storage_format", STORAGE_FORMAT_LEGACY)
    if value not in SUPPORTED_STORAGE_FORMATS:
        raise BundleError(f"unsupported storage_format: {value!r}")
    return value


def stored_relpath(target: str, storage_format: str) -> str:
    """manifest target -> at-rest 相対 path。"""
    if storage_format == STORAGE_FORMAT_SUFFIXED and is_instruction_path(target):
        return target + STORE_SUFFIX
    return target


def target_from_stored(stored: str, storage_format: str) -> str:
    """at-rest 相対 path -> manifest target。"""
    if (
        storage_format == STORAGE_FORMAT_SUFFIXED
        and stored.endswith(STORE_SUFFIX)
        and is_instruction_path(stored[: -len(STORE_SUFFIX)])
    ):
        return stored[: -len(STORE_SUFFIX)]
    return stored


def stored_link_target(link_target: str, storage_format: str) -> str:
    """symlink の manifest link_target -> at-rest link target。"""
    if storage_format == STORAGE_FORMAT_SUFFIXED and is_instruction_path(link_target):
        return link_target + STORE_SUFFIX
    return link_target


def bundle_stored_path(files_root: Path, target: str, storage_format: str) -> Path:
    relative = stored_relpath(target, storage_format)
    return files_root.joinpath(*PurePosixPath(relative).parts)


def ensure_representable(target: str, storage_format: str) -> None:
    """target が storage_format 上で一意・可逆に格納できることを保証する。

    stored_relpath は instruction basename へ suffix を付けるだけなので、
    ``<dir>/AGENTS.md.txt`` のような「instruction 名 + suffix」の target は
    ``<dir>/AGENTS.md`` の格納形と衝突し、逆写像で別 target へ潰れる。
    round-trip が成立しない target は表現不能として拒否する。
    """
    if target_from_stored(stored_relpath(target, storage_format), storage_format) != target:
        raise BundleError(
            f"target is not uniquely representable under {storage_format!r}: {target!r}"
        )


def run_git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", errors="replace").strip()
        raise BundleError(f"git {' '.join(args)} failed: {detail}")
    if binary:
        return completed.stdout
    return completed.stdout.decode("utf-8", errors="strict").strip()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def safe_target(raw: str) -> str:
    path = PurePosixPath(raw)
    if not raw or path.is_absolute() or raw != path.as_posix() or ".." in path.parts:
        raise BundleError(f"unsafe bundle target: {raw!r}")
    return raw


def git_entry(repo: Path, revision: str, target: str) -> tuple[str, str, bytes]:
    output = run_git(repo, "ls-tree", "-z", revision, "--", target, binary=True)
    assert isinstance(output, bytes)
    records = [record for record in output.split(b"\0") if record]
    if len(records) != 1:
        raise BundleError(f"expected one tracked path at {revision}: {target}")
    try:
        metadata, listed = records[0].split(b"\t", 1)
        mode, object_type, object_id = metadata.decode("ascii").split(" ")
        listed_target = listed.decode("utf-8")
    except (UnicodeDecodeError, ValueError) as exc:
        raise BundleError(f"unexpected ls-tree output for {target}") from exc
    if listed_target != target or object_type != "blob":
        raise BundleError(f"unsupported Git entry for {target}")
    content = run_git(repo, "cat-file", "blob", object_id, binary=True)
    assert isinstance(content, bytes)
    return mode, object_id, content


def entry_and_write(
    files_root: Path,
    target: str,
    mode: str,
    object_id: str,
    content: bytes,
    storage_format: str = DEFAULT_STORAGE_FORMAT,
) -> dict[str, str]:
    destination = bundle_stored_path(files_root, target, storage_format)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if mode == "120000":
        try:
            link_target = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise BundleError(f"non-UTF-8 symlink target: {target}") from exc
        os.symlink(stored_link_target(link_target, storage_format), destination)
        return {
            "git_blob_sha1": object_id,
            "link_target": link_target,
            "mode": mode,
            "target": target,
            "type": "symlink",
        }
    if mode not in {"100644", "100755"}:
        raise BundleError(f"unsupported Git mode for {target}: {mode}")
    destination.write_bytes(content)
    destination.chmod(0o755 if mode == "100755" else 0o644)
    return {
        "git_blob_sha1": object_id,
        "mode": mode,
        "sha256": sha256_bytes(content),
        "target": target,
        "type": "file",
    }


def bundle_sha256(entries: list[dict[str, str]]) -> str:
    identity = {"files": entries, "schema_version": SCHEMA_VERSION}
    return sha256_bytes(canonical_json(identity))


def write_manifest(output: Path, manifest: dict[str, Any]) -> None:
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_manifest(bundle: Path) -> dict[str, Any]:
    try:
        value = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        raise BundleError(f"invalid bundle manifest: {bundle}") from exc
    if not isinstance(value, dict):
        raise BundleError("bundle manifest root must be an object")
    return value


def verify_bundle(bundle: Path) -> dict[str, Any]:
    manifest = load_manifest(bundle)
    storage_format = storage_format_of(manifest)
    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise BundleError("manifest files must be an array")
    files_root = bundle / "files"
    expected_targets: set[str] = set()
    normalized: list[dict[str, str]] = []
    for raw_entry in entries:
        if not isinstance(raw_entry, dict):
            raise BundleError("manifest file entry must be an object")
        entry = {key: value for key, value in raw_entry.items() if isinstance(value, str)}
        target = safe_target(entry.get("target", ""))
        ensure_representable(target, storage_format)
        if target in expected_targets:
            raise BundleError(f"duplicate bundle target: {target}")
        expected_targets.add(target)
        path = bundle_stored_path(files_root, target, storage_format)
        if entry.get("type") == "symlink":
            expected_link = stored_link_target(entry.get("link_target", ""), storage_format)
            if not path.is_symlink() or os.readlink(path) != expected_link:
                raise BundleError(f"symlink mismatch: {target}")
        elif entry.get("type") == "file":
            if not path.is_file() or path.is_symlink():
                raise BundleError(f"missing regular file: {target}")
            actual_mode = "100755" if path.stat().st_mode & stat.S_IXUSR else "100644"
            if actual_mode != entry.get("mode") or sha256_bytes(path.read_bytes()) != entry.get("sha256"):
                raise BundleError(f"file identity mismatch: {target}")
        else:
            raise BundleError(f"unsupported manifest entry type: {target}")
        normalized.append(entry)
    if normalized != sorted(normalized, key=lambda item: item["target"]):
        raise BundleError("manifest files must be sorted by target")
    # target -> 正規stored path の forward 写像で照合する。逆写像 + set 化では、
    # 正規 "AGENTS.md.txt" と非正規 "AGENTS.md" が同一 target へ潰れて重複が消え、
    # manifest 未列挙の自動読込対象ファイルを見逃す(alias 問題)。forward なら
    # 非正規 alias は expected に無い stored path として必ず検出される。
    expected_stored = {stored_relpath(target, storage_format) for target in expected_targets}
    actual_stored = {
        path.relative_to(files_root).as_posix()
        for path in files_root.rglob("*")
        if path.is_file() or path.is_symlink()
    }
    if actual_stored != expected_stored:
        raise BundleError("bundle contains an unlisted or missing target")
    expected_hash = manifest.get("bundle_sha256")
    if bundle_sha256(normalized) != expected_hash:
        raise BundleError("bundle SHA-256 mismatch")
    return manifest


def export_baseline(
    source_repo: Path,
    source_ref: str,
    source_origin: str,
    output: Path,
    prompt_identity: str,
    targets: list[str],
) -> dict[str, Any]:
    source_repo = source_repo.resolve()
    output = output.resolve()
    if output.exists():
        raise BundleError(f"refusing to overwrite output: {output}")
    normalized_targets = sorted({safe_target(target) for target in targets})
    if len(normalized_targets) != len(targets):
        raise BundleError("bundle targets must be unique")
    for target in normalized_targets:
        ensure_representable(target, DEFAULT_STORAGE_FORMAT)
    commit = run_git(source_repo, "rev-parse", f"{source_ref}^{{commit}}")
    tree = run_git(source_repo, "rev-parse", f"{source_ref}^{{tree}}")
    assert isinstance(commit, str) and isinstance(tree, str)
    try:
        files_root = output / "files"
        files_root.mkdir(parents=True)
        entries = []
        for target in normalized_targets:
            mode, object_id, content = git_entry(source_repo, commit, target)
            entries.append(
                entry_and_write(files_root, target, mode, object_id, content, DEFAULT_STORAGE_FORMAT)
            )
        manifest: dict[str, Any] = {
            "artifact": {
                "artifact_role": "baseline",
                "description": "固定commit上の現行prompt setをそのまま格納した比較元。",
                "evaluation_status": "not_evaluated",
                "state": "draft",
            },
            "bundle_hash_algorithm": BUNDLE_HASH_ALGORITHM,
            "bundle_sha256": bundle_sha256(entries),
            "files": entries,
            "prompt_identity": prompt_identity,
            "schema_version": SCHEMA_VERSION,
            "storage_format": DEFAULT_STORAGE_FORMAT,
            "source": {
                "commit": commit,
                "repository": source_origin,
                "tree": tree,
            },
        }
        write_manifest(output, manifest)
        return verify_bundle(output)
    except Exception:
        if output.exists():
            shutil.rmtree(output)
        raise


def duplicate_candidate(source_bundle: Path, output: Path, prompt_identity: str) -> dict[str, Any]:
    source_bundle = source_bundle.resolve()
    output = output.resolve()
    if output.exists():
        raise BundleError(f"refusing to overwrite output: {output}")
    baseline = verify_bundle(source_bundle)
    baseline_identity = baseline.get("prompt_identity")
    if not isinstance(baseline_identity, str) or not baseline_identity:
        raise BundleError("baseline prompt identity is missing")
    try:
        shutil.copytree(source_bundle, output, symlinks=True)
        candidate = dict(baseline)
        candidate["artifact"] = {
            "artifact_role": "candidate",
            "baseline_identity": baseline_identity,
            "change_reason": "candidate格納形を先に固定するための初期複製。prompt変更はない。",
            "evaluation_status": "not_evaluated",
            "non_goals": ["改善の主張", "採用判断", "release判断", "THE-CAPTION本体への反映"],
            "problem": "未設定。baselineのbit-identicalな初期複製として保持する。",
            "scope": "baseline manifestに列挙されたprompt file一式。",
            "state": "draft",
        }
        candidate["content_relation"] = {
            "kind": "bit_identical_copy",
            "source_prompt_identity": baseline_identity,
        }
        candidate["prompt_identity"] = prompt_identity
        write_manifest(output, candidate)
        return verify_bundle(output)
    except Exception:
        if output.exists():
            shutil.rmtree(output)
        raise


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    commands = result.add_subparsers(dest="command", required=True)
    export = commands.add_parser("export-baseline")
    export.add_argument("--source-repo", required=True)
    export.add_argument("--source-ref", required=True)
    export.add_argument("--source-origin", required=True)
    export.add_argument("--output", required=True)
    export.add_argument("--prompt-identity", required=True)
    export.add_argument("--path", action="append", default=[], dest="targets")
    duplicate = commands.add_parser("duplicate-candidate")
    duplicate.add_argument("--source-bundle", required=True)
    duplicate.add_argument("--output", required=True)
    duplicate.add_argument("--prompt-identity", required=True)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "export-baseline":
            manifest = export_baseline(
                Path(args.source_repo),
                args.source_ref,
                args.source_origin,
                Path(args.output),
                args.prompt_identity,
                args.targets,
            )
        else:
            manifest = duplicate_candidate(
                Path(args.source_bundle),
                Path(args.output),
                args.prompt_identity,
            )
    except (BundleError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(manifest, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
