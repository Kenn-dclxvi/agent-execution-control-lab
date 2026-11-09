from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from layer2.extensions.long_run_storage import minimal_archive as storage
from layer2.extensions.long_run_storage.batch_archive import tree_snapshot
from layer2.extensions.long_run_storage.long_run_storage import LongRunStorageError


@unittest.skipUnless(shutil.which('zstd'), 'zstdが必要です')
class MinimalArchiveTest(unittest.TestCase):
    def source(self, root, name='trial'):
        batch = root / name
        fixture = batch / 'cycle/layer1/fixtures/case'
        fixture.mkdir(parents=True)
        (fixture / 'data').write_bytes(b'common content\n' * 100)
        (batch / 'cycle/layer1/set.json').write_text('{}')
        registration = batch / 'cycle/layer4/result-registration.json'
        registration.parent.mkdir()
        registration.write_text('{"result_id":"kept"}')
        common = root / 'common'
        common.mkdir(exist_ok=True)
        (common / 'keep').write_text('unchanged')
        for run in ['a', 'b']:
            work = batch / 'cycle/layer2/evidence' / run / 'workspace'
            work.mkdir(parents=True)
            shutil.copyfile(fixture / 'data', work / 'data')
            (work / 'data').chmod(0o755)
            (work / 'changed').write_text(run)
            (work / 'compact').mkdir()
            (work / 'compact/keep').write_text('nested compact must be kept')
            (work / 'environment').symlink_to(common, target_is_directory=True)
        return batch

    def archive(self, root, batch, output='archive', prune=False):
        return storage.archive_minimal(batch, root / 'store', root / output,
                                       preserve_existing=True, prune_workspaces=prune)

    def test_roundtrip_attributes_sharing_and_clone_isolation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            batch = self.source(root)
            changed = batch / 'cycle/layer2/evidence/a/workspace/changed'
            if sys.platform == 'darwin':
                subprocess.run(['xattr', '-w', 'com.example.test', 'attribute', str(changed)], check=True)
                subprocess.run(['chmod', '+a', 'everyone allow read', str(changed)], check=True)
                os.chflags(changed, 0x8000)  # UF_HIDDEN
            before = tree_snapshot(batch)
            self.archive(root, batch)
            storage.restore_minimal(root / 'archive', root / 'store', root / 'restored')
            self.assertEqual(tree_snapshot(root / 'restored'), before)
            self.assertEqual(tree_snapshot(batch), before)
            (root / 'restored/cycle/layer2/evidence/a/workspace/data').write_text('independent')
            self.assertEqual(tree_snapshot(batch), before)
            second = self.source(root, 'second')
            self.archive(root, second, 'archive2')
            one = storage.read_manifest(root / 'archive')
            two = storage.read_manifest(root / 'archive2')
            self.assertEqual(one['packs']['base'], two['packs']['base'])
            self.assertEqual(len(list((root / 'store').glob('*.tar.zst'))), 1)

    def test_corrupt_pack_never_prunes_and_missing_pack_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            batch = self.source(root)
            self.archive(root, batch)
            before = tree_snapshot(batch)
            manifest = storage.read_manifest(root / 'archive')
            pack = root / 'store' / (manifest['packs']['base']['sha256'] + '.tar.zst')
            pack.write_bytes(b'corrupt')
            with self.assertRaises(LongRunStorageError):
                self.archive(root, batch, prune=True)
            self.assertEqual(tree_snapshot(batch), before)
            pack.unlink()
            with self.assertRaises(OSError):
                self.archive(root, batch, prune=True)
            self.assertEqual(tree_snapshot(batch), before)

    def test_resume_partial_pruning_preserves_fixed_inputs_and_registration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            batch = self.source(root)
            fixed = tree_snapshot(batch / 'cycle/layer1')
            registration = (batch / 'cycle/layer4/result-registration.json').read_bytes()
            self.archive(root, batch)
            original = shutil.rmtree
            blocked = batch / 'cycle/layer2/evidence/b/workspace'
            def interrupted(path, *args, **kwargs):
                if Path(path) == blocked:
                    raise OSError('interrupted')
                return original(path, *args, **kwargs)
            with mock.patch.object(storage.shutil, 'rmtree', side_effect=interrupted):
                with self.assertRaises(OSError):
                    self.archive(root, batch, prune=True)
            self.assertFalse((batch / 'cycle/layer2/evidence/a/workspace').exists())
            self.assertTrue(blocked.exists())
            self.archive(root, batch, prune=True)
            self.assertFalse(blocked.exists())
            self.assertEqual(tree_snapshot(batch / 'cycle/layer1'), fixed)
            self.assertEqual((batch / 'cycle/layer4/result-registration.json').read_bytes(), registration)
            self.assertEqual((root / 'common/keep').read_text(), 'unchanged')
            self.archive(root, batch, prune=True)

    def test_changed_source_rejects_resume_and_normal_gate_requires_registration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            batch = self.source(root)
            with self.assertRaises(LongRunStorageError):
                storage.archive_minimal(batch, root / 'store', root / 'normal')
            self.archive(root, batch)
            (batch / 'cycle/layer2/evidence/a/workspace/changed').write_text('new')
            with self.assertRaises(LongRunStorageError):
                self.archive(root, batch, prune=True)
            self.assertTrue((batch / 'cycle/layer2/evidence/a/workspace').exists())

    def test_interrupted_save_can_resume_and_invalid_destination_does_not_change_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            batch = self.source(root)
            before = tree_snapshot(batch)
            with self.assertRaises(LongRunStorageError):
                storage.archive_minimal(batch, root / 'store', batch / 'bad-output', preserve_existing=True)
            self.assertEqual(tree_snapshot(batch), before)
            with mock.patch.object(storage, 'compressed_json', side_effect=OSError('interrupted')):
                with self.assertRaises(OSError):
                    self.archive(root, batch)
            self.assertEqual(tree_snapshot(batch), before)
            result = self.archive(root, batch)
            self.assertEqual(result['status'], 'verified')
            self.assertEqual(tree_snapshot(batch), before)

    def test_registered_trial_uses_normal_cli_and_keeps_registration(self):
        from tests.test_batch_archive import BatchArchiveTest
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            batch, run_id = BatchArchiveTest().make_registered(root)
            registration = batch / 'cycle/layer4/result-registration.json'
            original = registration.read_bytes()
            cli = [sys.executable, 'layer2/extensions/long_run_storage/long_run_storage.py',
                   'archive-minimal', '--batch', str(batch), '--store', str(root / 'store'),
                   '--output', str(root / 'archive'), '--prune-workspaces']
            result = subprocess.run(cli, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((batch / 'cycle/layer2/evidence' / run_id / 'workspace').exists())
            self.assertEqual(registration.read_bytes(), original)
            self.assertTrue((batch / 'cycle/layer1/set.json').exists())

    def test_cli_restore_single_workspace_and_reject_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            batch = self.source(root)
            self.archive(root, batch)
            prefix = 'cycle/layer2/evidence/a/workspace'
            cli = [sys.executable, 'layer2/extensions/long_run_storage/long_run_storage.py',
                   'restore-minimal', '--archive', str(root / 'archive'), '--store', str(root / 'store'),
                   '--output', str(root / 'work'), '--workspace', prefix]
            result = subprocess.run(cli, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(tree_snapshot(root / 'work', False), tree_snapshot(batch / prefix, False))
            self.assertNotEqual(subprocess.run(cli, capture_output=True).returncode, 0)
