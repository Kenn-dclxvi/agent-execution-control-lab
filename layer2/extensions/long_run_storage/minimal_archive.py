"""内容と属性を分離し、固定内容を共有する試験保存。元データは検証後だけ削除可能。"""
from __future__ import annotations

import base64
from contextlib import contextmanager
import ctypes
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile

from .batch_archive import tree_snapshot, require_same, require_usage
from .long_run_storage import (LongRunStorageError, completed_executions, resolve_cycle,
                               sha256_file, load_object)

SCHEMA = 'the-caption-prompt.minimal-archive/v1'


def sync_directory(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_json_once(path, value):
    with tempfile.NamedTemporaryFile(dir=path.parent) as temporary:
        temporary.write(json.dumps(value, ensure_ascii=False, sort_keys=True).encode())
        temporary.flush()
        os.fsync(temporary.fileno())
        os.link(temporary.name, path)
        sync_directory(path.parent)


def digest_json(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def real_directory(path, create=False):
    path = Path(path).absolute()
    if path.resolve() != path:
        raise LongRunStorageError(f'リンクを経由する保存先は使えません: {path}')
    if create:
        path.mkdir(parents=True, exist_ok=True)
    if not path.is_dir():
        raise LongRunStorageError(f'ディレクトリがありません: {path}')
    return path


@contextmanager
def locked(store):
    store = real_directory(store, create=True)
    lock = store / '.lock'
    fd = os.open(lock, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'r+') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield store


def compressed_json(path, data):
    with tempfile.NamedTemporaryFile(dir=path.parent) as temporary:
        subprocess.run(['zstd', '-q', '-3', '-c'],
                       input=json.dumps(data, sort_keys=True, separators=(',', ':')).encode(),
                       stdout=temporary, check=True)
        temporary.flush()
        os.fsync(temporary.fileno())
        os.link(temporary.name, path)
        sync_directory(path.parent)


def read_manifest(archive):
    archive = real_directory(archive)
    if (archive / 'manifest.json.zst').is_symlink():
        raise LongRunStorageError('マニフェストがリンクです')
    raw = subprocess.run(['zstd', '-q', '-dc', str(archive / 'manifest.json.zst')],
                         capture_output=True, check=True).stdout
    manifest = json.loads(raw)
    content = dict(manifest)
    stored = content.pop('content_sha256', None)
    if manifest.get('schema_version') != SCHEMA or digest_json(content) != stored:
        raise LongRunStorageError('マニフェストが改変されています')
    entries = manifest['entries']
    if '.' not in entries or entries['.']['type'] != stat.S_IFDIR:
        raise LongRunStorageError('ルートの定義が不正です')
    for name, entry in entries.items():
        path = PurePosixPath(name)
        if name != '.' and (path.is_absolute() or '..' in path.parts or path.as_posix() != name):
            raise LongRunStorageError('復元パスが不正です')
        if name != '.' and entries.get(path.parent.as_posix(), {}).get('type') != stat.S_IFDIR:
            raise LongRunStorageError('リンクまたは未定義の親へ復元できません')
        if entry['type'] not in (stat.S_IFDIR, stat.S_IFREG, stat.S_IFLNK):
            raise LongRunStorageError('未対応のファイル種別です')
        if 'sha256' in entry and (len(entry['sha256']) != 64 or
                                 any(c not in '0123456789abcdef' for c in entry['sha256'])):
            raise LongRunStorageError('内容識別値が不正です')
    for prefix in manifest['workspaces']:
        if not prefix.startswith(manifest['cycle_path'] + '/layer2/evidence/') or not prefix.endswith('/workspace'):
            raise LongRunStorageError('削除対象の定義が不正です')
        if entries.get(prefix, {}).get('type') != stat.S_IFDIR:
            raise LongRunStorageError('作業コピーの定義が不正です')
    for pack in ('base', 'delta'):
        h = manifest['packs'][pack]['sha256']
        if len(h) != 64 or any(c not in '0123456789abcdef' for c in h):
            raise LongRunStorageError('圧縮識別値が不正です')
    return manifest


def publish_pack(batch, entries, hashes, target):
    representatives = {}
    for name, entry in entries.items():
        if entry.get('sha256') in hashes:
            representatives.setdefault(entry['sha256'], name)
    with tempfile.NamedTemporaryFile(dir=target.parent) as output:
        with tempfile.TemporaryFile() as errors:
            proc = subprocess.Popen(['zstd', '-q', '-3', '--long=27', '-c'], stdin=subprocess.PIPE,
                                    stdout=output, stderr=errors)
            try:
                with tarfile.open(fileobj=proc.stdin, mode='w|', format=tarfile.PAX_FORMAT) as archive:
                    for digest, name in sorted(representatives.items()):
                        source = batch / name
                        if source.resolve() != source or sha256_file(source) != digest:
                            raise LongRunStorageError(f'保存中に内容が変化しました: {name}')
                        info = tarfile.TarInfo(digest)
                        info.size = entries[name]['size']
                        info.mode = 0o600
                        with source.open('rb') as data:
                            archive.addfile(info, data)
                proc.stdin.close()
                if proc.wait():
                    raise LongRunStorageError('内容の圧縮に失敗しました')
            except BaseException:
                proc.kill()
                proc.wait()
                raise
        output.flush()
        os.fsync(output.fileno())
        digest = sha256_file(Path(output.name))
        final = target / (digest + '.tar.zst')
        if final.exists():
            if final.is_symlink() or sha256_file(final) != digest:
                raise LongRunStorageError('共有内容が改変されています')
        else:
            os.link(output.name, final)
            sync_directory(target)
        return {'sha256': digest, 'bytes': final.stat().st_size}


def clone_file(source, destination):
    if sys.platform != 'darwin':
        shutil.copyfile(source, destination)
        return
    lib = ctypes.CDLL(None, use_errno=True)
    lib.clonefile.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    if lib.clonefile(os.fsencode(source), os.fsencode(destination), 0):
        raise OSError(ctypes.get_errno(), f'clonefile: {destination}')


def apply_metadata(path, entry):
    link = entry['type'] == stat.S_IFLNK
    current = path.lstat()
    if (current.st_uid, current.st_gid) != (entry['uid'], entry['gid']):
        os.chown(path, entry['uid'], entry['gid'], follow_symlinks=False)
    if link:
        if hasattr(os, 'lchmod'):
            os.lchmod(path, entry['mode'])
        elif stat.S_IMODE(current.st_mode) != entry['mode']:
            raise LongRunStorageError('リンク権限を復元できません')
    else:
        os.chmod(path, entry['mode'])
    if sys.platform == 'darwin':
        lib = ctypes.CDLL(None, use_errno=True)
        lib.setxattr.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p,
                                ctypes.c_size_t, ctypes.c_uint32, ctypes.c_int]
        for key, encoded in entry['xattrs'].items():
            value = base64.b64decode(encoded)
            if lib.setxattr(os.fsencode(path), os.fsencode(key), value, len(value), 0, 1):
                raise OSError(ctypes.get_errno(), f'xattr: {path}')
        if entry['acl']:
            lib.acl_from_text.argtypes = [ctypes.c_char_p]
            lib.acl_from_text.restype = ctypes.c_void_p
            lib.acl_set_link_np.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_void_p]
            lib.acl_free.argtypes = [ctypes.c_void_p]
            acl = lib.acl_from_text(entry['acl'].encode())
            if not acl:
                raise OSError(ctypes.get_errno(), 'acl_from_text')
            try:
                if lib.acl_set_link_np(os.fsencode(path), 0x100, acl):
                    raise OSError(ctypes.get_errno(), f'ACL: {path}')
            finally:
                lib.acl_free(acl)
    else:
        if entry['acl']:
            raise LongRunStorageError('このOSではACLを復元できません')
        for key, encoded in entry['xattrs'].items():
            os.setxattr(path, key, base64.b64decode(encoded), follow_symlinks=False)
    if 'mtime_ns' in entry:
        os.utime(path, ns=(entry['mtime_ns'], entry['mtime_ns']), follow_symlinks=False)
    if entry['flags']:
        if not hasattr(os, 'chflags'):
            raise LongRunStorageError('ファイルフラグを復元できません')
        os.chflags(path, entry['flags'], follow_symlinks=False)


def restore_entries(entries, objects, destination):
    if destination.exists() or destination.is_symlink():
        raise LongRunStorageError('既存の復元先は上書きしません')
    destination.parent.mkdir(parents=True, exist_ok=True)
    for name, entry in sorted(entries.items(), key=lambda item: len(PurePosixPath(item[0]).parts)):
        path = destination if name == '.' else destination / name
        if entry['type'] == stat.S_IFDIR:
            path.mkdir()
        elif entry['type'] == stat.S_IFLNK:
            path.symlink_to(entry['target'])
        else:
            clone_file(objects / entry['sha256'], path)
    for name, entry in sorted(entries.items(), key=lambda item: len(PurePosixPath(item[0]).parts), reverse=True):
        apply_metadata(destination if name == '.' else destination / name, entry)
    expected = {name: dict(entry) for name, entry in entries.items()}
    expected['.'].pop('mtime_ns', None)
    require_same(expected, tree_snapshot(destination, exclude_compact=False), '復元内容と属性')
    if 'mtime_ns' in entries['.'] and destination.lstat().st_mtime_ns != entries['.']['mtime_ns']:
        raise LongRunStorageError('作業コピーの更新時刻が一致しません')


def remove_restored(root):
    """復元した一時領域だけでフラグ・権限を解除して片付ける。"""
    if not root.exists():
        return
    for directory, dirs, files in os.walk(root, topdown=True, followlinks=False):
        for path in [Path(directory)] + [Path(directory) / n for n in dirs + files]:
            if hasattr(os, 'chflags'):
                os.chflags(path, 0, follow_symlinks=False)
            if not path.is_symlink() and path.is_dir():
                os.chmod(path, 0o700)
    shutil.rmtree(root)


def workspace_entries(manifest, prefix):
    if prefix not in manifest['workspaces']:
        raise LongRunStorageError('指定の作業コピーは保存記録にありません')
    return {('.' if name == prefix else name[len(prefix) + 1:]): entry
            for name, entry in manifest['entries'].items()
            if name == prefix or name.startswith(prefix + '/')}


def fixed_entries(manifest):
    return {name: entry for name, entry in manifest['entries'].items()
            if not any(name == prefix or name.startswith(prefix + '/') for prefix in manifest['workspaces'])}


@contextmanager
def open_archive(archive, store, temporary_parent):
    """ロック中に圧縮内容を検証し、内容だけを一時展開する。"""
    archive = real_directory(archive)
    with locked(store) as store:
        manifest = read_manifest(archive)
        with tempfile.TemporaryDirectory(prefix='minimal-objects-', dir=temporary_parent) as tmp:
            objects = Path(tmp)
            expected = {entry['sha256']: entry['size'] for entry in manifest['entries'].values() if 'sha256' in entry}
            seen = set()
            for kind in ('base', 'delta'):
                digest = manifest['packs'][kind]['sha256']
                pack = (store if kind == 'base' else archive) / (digest + '.tar.zst')
                if pack.is_symlink() or sha256_file(pack) != digest:
                    raise LongRunStorageError('圧縮内容が欠落または改変されています')
                proc = subprocess.Popen(['zstd', '-q', '-dc', str(pack)], stdout=subprocess.PIPE)
                try:
                    with tarfile.open(fileobj=proc.stdout, mode='r|') as stream:
                        for member in stream:
                            if (not member.isfile() or member.name not in expected or member.name in seen
                                    or member.size != expected[member.name]):
                                raise LongRunStorageError('圧縮内容のパス・種別・サイズが不正です')
                            with (objects / member.name).open('xb') as output:
                                shutil.copyfileobj(stream.extractfile(member), output)
                            if sha256_file(objects / member.name) != member.name:
                                raise LongRunStorageError('内容ハッシュが一致しません')
                            seen.add(member.name)
                    proc.stdout.close()
                    if proc.wait():
                        raise LongRunStorageError('内容の展開に失敗しました')
                except BaseException:
                    proc.kill()
                    proc.wait()
                    raise
            if seen != set(expected):
                raise LongRunStorageError('内容が不足しています')
            yield manifest, objects


def validate_source(batch, cycle_path, preserve_existing):
    cycle, prefix = resolve_cycle(batch, cycle_path)
    if not (cycle / 'layer1/set.json').is_file():
        raise LongRunStorageError('固定済みLayer 1がありません')
    if preserve_existing:
        paths = sorted((cycle / 'layer2/evidence').glob('*/workspace'))
    else:
        registration = load_object(cycle / 'layer4/result-registration.json')
        if not registration.get('result_id') or not registration.get('result_content_sha256'):
            raise LongRunStorageError('結果の登録記録が不完全です')
        # 既存atomic runだけを選択した試験には、新規の実行・作業コピーがない。
        # 結果登録の確認後に限り、この空の実行集合を保存できる。
        valid, excluded = (completed_executions(cycle)
                           if list((cycle / 'layer2/evidence').glob('*/execution.json')) else ([], []))
        for binding in (cycle / 'layer2/bindings').glob('*.json'):
            if load_object(binding).get('run_id') not in valid + excluded:
                raise LongRunStorageError('終了記録のない実行があります')
        for run_id in valid:
            require_usage(cycle, run_id)
            rating = load_object(cycle / 'layer3/ratings' / (run_id + '.json'))
            if rating.get('run_id') != run_id or rating.get('score') not in range(5):
                raise LongRunStorageError('採点が完了していません')
            for name in ('result.diff', 'validation.json', 'final-response.txt'):
                if not (cycle / 'layer2/evidence' / run_id / 'rating-view' / name).is_file():
                    raise LongRunStorageError('採点証拠が不足しています')
        paths = [cycle / 'layer2/evidence' / run_id / 'workspace' for run_id in valid + excluded]
    for path in paths:
        real_directory(path)
    return prefix, [p.relative_to(batch).as_posix() for p in paths]


def check_remaining(batch, manifest, pruning=False):
    actual = tree_snapshot(batch)
    expected = manifest['entries']
    if not pruning:
        require_same(expected, actual, '元データの不変')
        return
    # 中断した削除で欠けてよいのは作業コピー内だけ。残存内容の変更は拒否する。
    workspaces = manifest['workspaces']
    ancestors = {PurePosixPath(p).parent.as_posix() for p in workspaces}
    for name in actual.keys() | expected.keys():
        a, e = actual.get(name), expected.get(name)
        inside = any(name == p or name.startswith(p + '/') for p in workspaces)
        if a is None and inside:
            continue
        if a is None or e is None:
            raise LongRunStorageError('削除再開時の元データが一致しません')
        a, e = dict(a), dict(e)
        if name in ancestors or (inside and e['type'] == stat.S_IFDIR):
            a.pop('mtime_ns', None)
            e.pop('mtime_ns', None)
        require_same(e, a, '削除再開時の内容')


def archive_minimal(batch, store, output, cycle_path=Path('cycle'), preserve_existing=False,
                    prune_workspaces=False):
    batch = real_directory(batch)
    store, output = Path(store).absolute(), Path(output).absolute()
    if store.resolve() != store or output.resolve() != output:
        raise LongRunStorageError('リンクを経由する保存先は使えません')
    if output.is_relative_to(store) or store.is_relative_to(output) or output.is_relative_to(batch) or store.is_relative_to(batch) or batch.is_relative_to(output) or batch.is_relative_to(store):
        raise LongRunStorageError('保存先と共有内容は元データから分離してください')
    store = real_directory(store, create=True)
    output = real_directory(output, create=True)
    manifest_path = output / 'manifest.json.zst'
    with locked(store):
        if manifest_path.is_symlink():
            raise LongRunStorageError('マニフェストがリンクです')
        if manifest_path.exists():
            manifest = read_manifest(output)
            if manifest['source'] != str(batch) or manifest['preserve_existing'] != preserve_existing:
                raise LongRunStorageError('別の元データ・保存モードでは再開できません')
        else:
            prefix, workspaces = validate_source(batch, cycle_path, preserve_existing)
            entries = tree_snapshot(batch)
            hashes = {e['sha256'] for e in entries.values() if 'sha256' in e}
            base = {e['sha256'] for p, e in entries.items() if p.startswith(prefix + '/layer1/fixtures/') and 'sha256' in e}
            unique_sizes = {e['sha256']: e['size'] for e in entries.values() if 'sha256' in e}
            required = sum(unique_sizes.values()) * 2 + len(json.dumps(entries).encode())
            if sys.platform != 'darwin':
                required += sum(e.get('size', 0) for e in entries.values())
            if shutil.disk_usage(output).free < required:
                raise LongRunStorageError('保存・復元の一時容量が不足しています')
            packs = {'base': publish_pack(batch, entries, base, store),
                     'delta': publish_pack(batch, entries, hashes - base, output)}
            manifest = {'schema_version': SCHEMA, 'source': str(batch), 'cycle_path': prefix,
                        'preserve_existing': preserve_existing, 'entries': entries, 'packs': packs,
                        'workspaces': workspaces,
                        'ignored_fields': ['xattr:com.apple.provenance', 'root_directory_mtime']}
            manifest['content_sha256'] = digest_json(manifest)
            compressed_json(manifest_path, manifest)
        # 保管場所は追加専用。参照とpackを削除するAPIは提供しない。
        pin = store / (manifest['content_sha256'] + '.reference.json')
        if not pin.exists():
            write_json_once(pin, {'manifest': manifest['content_sha256'], 'archive': str(output),
                                  'base': manifest['packs']['base']['sha256']})
    intent = output / 'prune-intent.json'
    pruning = intent.exists()
    if pruning and load_object(intent).get('manifest') != manifest['content_sha256']:
        raise LongRunStorageError('削除再開記録が一致しません')
    check_remaining(batch, manifest, pruning)
    # 共有内容の読み取り検証と逐次復元。元の証拠・共通環境には書き込まない。
    with open_archive(output, store, output.parent) as (verified, objects):
        if verified['content_sha256'] != manifest['content_sha256']:
            raise LongRunStorageError('検証中にマニフェストが変化しました')
        with tempfile.TemporaryDirectory(prefix='minimal-verify-', dir=output.parent) as tmp:
            root = Path(tmp) / 'restored'
            try:
                restore_entries(fixed_entries(verified), objects, root)
            finally:
                remove_restored(root)
            for prefix in verified['workspaces']:
                try:
                    restore_entries(workspace_entries(verified, prefix), objects, root)
                finally:
                    remove_restored(root)
        check_remaining(batch, verified, pruning)
        verification = output / 'verification.json'
        if not verification.exists():
            write_json_once(verification, {'manifest': verified['content_sha256'], 'status': 'verified',
                                          'workspace_count': len(verified['workspaces']),
                                          'max_simultaneous_restored_workspaces': 1})
        if prune_workspaces:
            if not intent.exists():
                write_json_once(intent, {'manifest': verified['content_sha256']})
            before = shutil.disk_usage(batch).free
            for prefix in verified['workspaces']:
                path = batch / prefix
                if path.exists() or path.is_symlink():
                    if path.resolve() != path or path.is_symlink():
                        raise LongRunStorageError('削除対象がリンクへ変化しました')
                    remaining = tree_snapshot(path, exclude_compact=False)
                    expected = workspace_entries(verified, prefix)
                    for name, actual in remaining.items():
                        wanted = dict(expected.get(name, {}))
                        actual = dict(actual)
                        if wanted.get('type') == stat.S_IFDIR:
                            wanted.pop('mtime_ns', None)
                            actual.pop('mtime_ns', None)
                        require_same(wanted, actual, '削除直前の作業コピー')
                    shutil.rmtree(path)
            receipt = output / 'prune-receipt.json'
            if not receipt.exists():
                write_json_once(receipt, {'manifest': verified['content_sha256'], 'status': 'complete',
                                          'free_bytes_before_prune': before,
                                          'free_bytes_after_prune': shutil.disk_usage(batch).free})
    return {'status': 'complete' if prune_workspaces else 'verified', 'archive': str(output),
            'workspace_count': len(manifest['workspaces']),
            'archive_bytes': sum(p['bytes'] for p in manifest['packs'].values()) + manifest_path.stat().st_size}


def restore_minimal(archive, store, output, workspace=None, evidence_only=False):
    output = Path(output).absolute()
    if output.resolve() != output:
        raise LongRunStorageError('リンクを経由する復元先は使えません')
    output.parent.mkdir(parents=True, exist_ok=True)
    with open_archive(archive, store, output.parent) as (manifest, objects):
        entries = (workspace_entries(manifest, workspace) if workspace else
                   fixed_entries(manifest) if evidence_only else manifest['entries'])
        restore_entries(entries, objects, output)
    return {'status': 'restored', 'output': str(output)}
