"""試験データを一括圧縮し、復元照合後に指定した作業データだけを削除する。"""
from __future__ import annotations

import base64
import ctypes
from functools import cache
import os
import re
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
from typing import Any

from layer2.extensions.long_run_storage.long_run_storage import (
    GIB, LongRunStorageError, capacity_guard, completed_executions, load_object,
    resolve_cycle, sha256_file, utc_now, write_json_once,
)

SCHEMA = "the-caption-prompt.registered-batch-archive/v1"
# 内容の同一性に不要なOS属性だけを除外する。その他の属性は照合する。
IGNORED_XATTR = "com.apple.provenance"


def require_usage(cycle: Path, run_id: str) -> None:
    """CodexとClaudeの正式な使用量記録を、元の形式のまま確認する。"""
    usage = load_object(cycle / "layer2/extensions" / run_id / "all-agent-usage/usage.json")
    if usage.get("schema_version") not in {
        "the-caption-prompt.all-agent-usage/v1",
        "the-caption-prompt.claude-all-agent-usage/v1",
    }:
        raise LongRunStorageError(f"未対応の使用量記録です: {run_id}")
    total = usage.get("all_agent_total_tokens")
    if not isinstance(total, int) or isinstance(total, bool) or total < 0:
        raise LongRunStorageError(f"使用量の合計が不正です: {run_id}")
    if not isinstance(usage.get("sessions"), list) or not usage["sessions"]:
        raise LongRunStorageError(f"使用量のセッション記録が不足しています: {run_id}")


@cache
def mac_library():
    lib = ctypes.CDLL(None, use_errno=True)
    lib.listxattr.argtypes = [ctypes.c_char_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int]
    lib.listxattr.restype = ctypes.c_ssize_t
    lib.getxattr.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p,
                             ctypes.c_size_t, ctypes.c_uint32, ctypes.c_int]
    lib.getxattr.restype = ctypes.c_ssize_t
    lib.acl_get_link_np.argtypes = [ctypes.c_char_p, ctypes.c_int]
    lib.acl_get_link_np.restype = ctypes.c_void_p
    lib.acl_to_text.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ssize_t)]
    lib.acl_to_text.restype = ctypes.c_void_p
    lib.acl_free.argtypes = [ctypes.c_void_p]
    return lib


def mac_metadata(path: Path) -> tuple[dict[str, str], str | None]:
    lib = mac_library()
    name = os.fsencode(path)
    size = lib.listxattr(name, None, 0, 1)
    if size < 0:
        raise OSError(ctypes.get_errno(), str(path))
    buffer = ctypes.create_string_buffer(size)
    if lib.listxattr(name, buffer, size, 1) != size:
        raise LongRunStorageError(f"属性の取得中に変更されました: {path}")
    attributes = {}
    for key in sorted(filter(None, buffer.raw.split(b"\0"))):
        if os.fsdecode(key) == IGNORED_XATTR:
            continue
        size = lib.getxattr(name, key, None, 0, 0, 1)
        if size < 0:
            raise OSError(ctypes.get_errno(), str(path))
        value = ctypes.create_string_buffer(size)
        if lib.getxattr(name, key, value, size, 0, 1) != size:
            raise LongRunStorageError(f"属性の取得中に変更されました: {path}")
        attributes[os.fsdecode(key)] = base64.b64encode(value.raw).decode()
    acl = lib.acl_get_link_np(name, 0x100)  # ACL_TYPE_EXTENDED
    if not acl:
        if ctypes.get_errno() == 2:
            return attributes, None
        raise OSError(ctypes.get_errno(), str(path))
    try:
        length = ctypes.c_ssize_t()
        text = lib.acl_to_text(acl, ctypes.byref(length))
        if not text:
            raise OSError(ctypes.get_errno(), str(path))
        try:
            return attributes, ctypes.string_at(text, length.value).decode()
        finally:
            lib.acl_free(text)
    finally:
        lib.acl_free(acl)


def tree_snapshot(root: Path, exclude_compact: bool = True) -> dict[str, dict[str, Any]]:
    """共通環境へのリンクをたどらず、復元に必要な内容と属性を記録する。"""
    paths = [root]
    for directory, dirs, files in os.walk(root, followlinks=False):
        if exclude_compact and Path(directory) == root:
            dirs[:] = [name for name in dirs if name != "compact"]
            files = [name for name in files if name != "compact"]
        paths.extend(Path(directory) / name for name in sorted(dirs + files))
    result = {}
    for path in sorted(paths):
        relative = path.relative_to(root).as_posix()
        metadata = path.lstat()
        if sys.platform == "darwin":
            attributes, acl = mac_metadata(path)
        else:
            attributes = {
                name: base64.b64encode(os.getxattr(path, name, follow_symlinks=False)).decode()
                for name in os.listxattr(path, follow_symlinks=False)
                if name != IGNORED_XATTR
            }
            acl = None  # POSIX ACLはsystem.posix_acl_*属性として照合する。
        entry = {"type": stat.S_IFMT(metadata.st_mode), "mode": stat.S_IMODE(metadata.st_mode),
                 "uid": metadata.st_uid, "gid": metadata.st_gid,
                 "flags": getattr(metadata, "st_flags", 0), "xattrs": attributes, "acl": acl}
        if relative != ".":
            entry["mtime_ns"] = metadata.st_mtime_ns
        if stat.S_ISLNK(metadata.st_mode):
            entry["target"] = os.readlink(path)
        elif stat.S_ISREG(metadata.st_mode):
            entry.update(size=metadata.st_size, sha256=sha256_file(path))
        elif not stat.S_ISDIR(metadata.st_mode):
            raise LongRunStorageError(f"未対応のファイル種別です: {path}")
        result[relative] = entry
    return result


def require_same(expected: dict, actual: dict, stage: str) -> None:
    if expected != actual:
        changed = sorted(name for name in expected.keys() | actual.keys()
                         if expected.get(name) != actual.get(name))
        raise LongRunStorageError(f"{stage}の照合が不一致です: {changed[:5]}")


def native_archive(batch: Path, target: Path, restored: Path, level: int,
                   exclude_compact: bool = True) -> None:
    zstd = shutil.which("zstd")
    tar = shutil.which("tar")
    if not zstd or not tar:
        raise LongRunStorageError("tarとzstdが必要です")
    env = dict(os.environ)
    for name in ("COPYFILE_DISABLE", "COPY_EXTENDED_ATTRIBUTES_DISABLE", "TAR_OPTIONS", "ZSTD_CLEVEL"):
        env.pop(name, None)
    # stderrはファイルへ流し、パイプの満杯による停止を避ける。
    with tempfile.TemporaryFile() as errors, target.open("xb") as output:
        producer = subprocess.Popen([tar, "--format=pax", "--acls", "--xattrs", *(["--exclude=./compact"] if exclude_compact else []),
                                     "-cf", "-", "-C", str(batch), "."],
                                    stdout=subprocess.PIPE, stderr=errors, env=env)
        try:
            compressed = subprocess.run([zstd, "-q", f"-{level}", "--long=27", "-c"],
                                        stdin=producer.stdout, stdout=output, stderr=errors, env=env)
        finally:
            producer.stdout.close()
        if compressed.returncode:
            producer.kill()
        code = producer.wait()
        if code or compressed.returncode:
            raise LongRunStorageError("一括圧縮に失敗しました。作業コピーは保持します")
    tested = subprocess.run([zstd, "-q", "-t", str(target)], capture_output=True)
    if tested.returncode:
        raise LongRunStorageError("圧縮ファイルの健全性確認に失敗しました")
    restored.mkdir()
    with tempfile.TemporaryFile() as errors:
        producer = subprocess.Popen([zstd, "-q", "-dc", str(target)], stdout=subprocess.PIPE, stderr=errors)
        try:
            extracted = subprocess.run([tar, "--acls", "--xattrs", "-xpf", "-", "-C", str(restored)],
                                       stdin=producer.stdout, stderr=errors, env=env)
        finally:
            producer.stdout.close()
        if extracted.returncode:
            producer.kill()
        code = producer.wait()
        if code or extracted.returncode:
            raise LongRunStorageError("復元に失敗しました。作業コピーは保持します")


def archive_batch(batch: Path, zstd_level: int = 3, cycle_path: Path = Path("cycle"),
                  preserve_existing: bool = False) -> dict[str, Any]:
    """通常の試験完了処理、または停止済み履歴の現状保存。"""
    original = batch.absolute()
    batch = batch.resolve()
    if original != batch or not batch.is_dir():
        raise LongRunStorageError("試験rootはリンクを経由しない実ディレクトリが必要です")
    cycle, prefix = resolve_cycle(batch, cycle_path)
    if not (cycle / "layer1/set.json").is_file():
        raise LongRunStorageError("固定済みLayer 1がありません")
    registration = cycle / "layer4/result-registration.json"
    if preserve_existing:
        # 証拠の欠落や中断状態を補完せず、そのまま保存する。
        workspaces = sorted((cycle / "layer2/evidence").glob("*/workspace"))
        if not workspaces:
            raise LongRunStorageError("保存対象の作業コピーがありません")
    else:
        record = load_object(registration)
        if not record.get("result_id") or not record.get("result_content_sha256"):
            raise LongRunStorageError("結果の登録記録が不完全です")
        valid, excluded = completed_executions(cycle)
        for binding in (cycle / "layer2/bindings").glob("*.json"):
            if load_object(binding).get("run_id") not in valid + excluded:
                raise LongRunStorageError("終了記録のない実行が残っています")
        for run_id in valid:
            require_usage(cycle, run_id)
            rating = load_object(cycle / "layer3/ratings" / f"{run_id}.json")
            if rating.get("run_id") != run_id or rating.get("score") not in range(5):
                raise LongRunStorageError(f"採点が完了していません: {run_id}")
            for name in ("result.diff", "validation.json", "final-response.txt"):
                if not (cycle / "layer2/evidence" / run_id / "rating-view" / name).is_file():
                    raise LongRunStorageError(f"採点証拠が不足しています: {run_id}/{name}")
        workspaces = [cycle / "layer2/evidence" / run_id / "workspace" for run_id in valid + excluded]
    for path in workspaces:
        if path.resolve() != path or not path.is_dir():
            raise LongRunStorageError(f"作業コピーが欠落またはリンクです: {path}")
    compact = batch / "compact"
    if compact.is_symlink() or (compact.exists() and any(compact.iterdir())):
        raise LongRunStorageError("既存の圧縮記録は上書きしません")
    compact.mkdir(exist_ok=True)
    before = tree_snapshot(batch)
    source_bytes = sum(entry.get("size", 0) for entry in before.values())
    guard = capacity_guard(batch, None, estimated_next_batch_gib=2 * source_bytes / GIB)
    if not guard["dispatch_allowed"]:
        raise LongRunStorageError("圧縮と復元照合の一時容量が不足しています")
    archive = compact / "batch-evidence.tar.zst"
    manifest_path = compact / "batch-archive-manifest.json"
    with tempfile.TemporaryDirectory(prefix="verify-", dir=compact) as temporary:
        target = Path(temporary) / "batch.tar.zst"
        restored = Path(temporary) / "restored"
        native_archive(batch, target, restored, zstd_level)
        require_same(before, tree_snapshot(restored), "復元内容")
        require_same(before, tree_snapshot(batch), "圧縮中の元データ")
        os.link(target, archive)  # 排他的に公開し、既存アーカイブは上書きしない。
    manifest = {"schema_version": "the-caption-prompt.preserved-batch-archive/v1" if preserve_existing else SCHEMA,
                "preserve_existing": preserve_existing, "created_at": utc_now(), "batch": str(batch),
                "cycle_path": prefix, "archive": str(archive), "archive_sha256": sha256_file(archive),
                "archive_bytes": archive.stat().st_size, "source_bytes": source_bytes,
                "zstd_level": zstd_level, "entries": before,
                "ignored_fields": ["xattr:com.apple.provenance", "root_directory_mtime"],
                "prune_paths": [str(p.relative_to(batch)) for p in workspaces],
                "result_registration_sha256": sha256_file(registration) if registration.is_file() else None}
    write_json_once(manifest_path, manifest)
    require_same(before, tree_snapshot(batch), "削除直前の元データ")
    if sha256_file(archive) != manifest["archive_sha256"]:
        raise LongRunStorageError("削除前にアーカイブが変化しました")
    free_before = shutil.disk_usage(batch).free
    pruned = []
    for workspace in workspaces:
        if workspace.resolve() != workspace or workspace.is_symlink():
            raise LongRunStorageError("作業コピーのパスが変化しました")
        shutil.rmtree(workspace)
        pruned.append(str(workspace.relative_to(batch)))
    retained = [str((cycle / "layer1").relative_to(batch))]
    if registration.exists():
        retained.append(str(registration.relative_to(batch)))
    receipt = {"schema_version": "the-caption-prompt.preserved-batch-prune/v1" if preserve_existing else "the-caption-prompt.registered-batch-prune/v1", "created_at": utc_now(),
               "archive_sha256": manifest["archive_sha256"], "manifest_sha256": sha256_file(manifest_path),
               "pruned_paths": pruned, "retained": retained,
               "free_bytes_before_prune": free_before, "free_bytes_after_prune": shutil.disk_usage(batch).free,
               "status": "complete"}
    write_json_once(compact / "batch-prune-receipt.json", receipt)
    return receipt


def archive_homes(source: Path, zstd_level: int = 3) -> dict[str, Any]:
    """停止済み試験の実行別ホームを丸ごと保存し、検証後にだけ削除する。"""
    source = source.absolute()
    if source.name != "codex-homes" or source.resolve() != source or not source.is_dir():
        raise LongRunStorageError("実ディレクトリのcodex-homesを指定してください")
    children = list(source.iterdir())
    if not children or any(not re.fullmatch(r"[0-9a-f]{32}", p.name)
                           or p.is_symlink() or not p.is_dir() for p in children):
        raise LongRunStorageError("実行ID別ホーム以外を含むため削除できません")
    # 出力は対象外に置く。全ホームを収録し、cacheやsessionも省略しない。
    output = source.with_name("codex-homes.archive")
    if output.exists() or output.is_symlink():
        raise LongRunStorageError("既存のホーム圧縮記録は上書きしません")
    before = tree_snapshot(source)
    source_bytes = sum(e.get("size", 0) for e in before.values())
    if not capacity_guard(source, None, estimated_next_batch_gib=2 * source_bytes / GIB)["dispatch_allowed"]:
        raise LongRunStorageError("圧縮と復元照合の一時容量が不足しています")
    output.mkdir()
    archive = output / "homes.tar.zst"
    with tempfile.TemporaryDirectory(prefix="verify-", dir=output) as temporary:
        target = Path(temporary) / "homes.tar.zst"
        restored = Path(temporary) / "restored"
        native_archive(source, target, restored, zstd_level, exclude_compact=False)
        require_same(before, tree_snapshot(restored), "ホーム復元内容")
        os.link(target, archive)
    manifest_path = output / "manifest.json"
    manifest = {"schema_version": "the-caption-prompt.codex-homes-archive/v1",
                "created_at": utc_now(), "source": str(source), "archive": str(archive),
                "archive_sha256": sha256_file(archive), "archive_bytes": archive.stat().st_size,
                "source_bytes": source_bytes, "run_ids": sorted(p.name for p in children),
                "entries": before, "zstd_level": zstd_level,
                "ignored_fields": ["xattr:com.apple.provenance", "root_directory_mtime"]}
    write_json_once(manifest_path, manifest)
    if source.resolve() != source or source.is_symlink():
        raise LongRunStorageError("ホームのパスが変化しました")
    require_same(before, tree_snapshot(source), "削除直前のホーム")
    if sha256_file(archive) != manifest["archive_sha256"]:
        raise LongRunStorageError("削除前にアーカイブが変化しました")
    free_before = shutil.disk_usage(source).free
    shutil.rmtree(source)
    receipt = {"schema_version": "the-caption-prompt.codex-homes-prune/v1",
               "created_at": utc_now(), "status": "complete", "source": str(source),
               "archive_sha256": manifest["archive_sha256"],
               "manifest_sha256": sha256_file(manifest_path), "home_count": len(children),
               "free_bytes_before_prune": free_before,
               "free_bytes_after_prune": shutil.disk_usage(output).free}
    write_json_once(output / "prune-receipt.json", receipt)
    return receipt
