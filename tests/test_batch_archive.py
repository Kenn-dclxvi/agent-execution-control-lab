from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from layer2.extensions.long_run_storage import batch_archive as storage
from layer2.extensions.long_run_storage.long_run_storage import create_rating_view, LongRunStorageError
from tests import test_long_run_storage as fixtures


@unittest.skipUnless(shutil.which('zstd') and shutil.which('tar'), 'tarとzstdが必要です')
class BatchArchiveTest(unittest.TestCase):
    def setUp(self):
        patch = mock.patch.object(storage, 'capacity_guard', return_value={'dispatch_allowed': True})
        patch.start()
        self.addCleanup(patch.stop)

    def make_registered(self, root):
        batch, run_id = fixtures.LongRunStorageTest().make_batch(root)
        cycle = batch / 'cycle'
        create_rating_view(cycle, run_id)
        ratings = cycle / 'layer3/ratings'
        ratings.mkdir(parents=True)
        (ratings / f'{run_id}.json').write_text(json.dumps({'run_id': run_id, 'score': 4}))
        layer4 = cycle / 'layer4'
        layer4.mkdir()
        (layer4 / 'result-registration.json').write_text(json.dumps({'result_id': 'result-1', 'result_content_sha256': 'a'*64}))
        return batch, run_id

    def test_homes_roundtrip_keeps_all_content_and_protected_siblings(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve(); source = root / 'codex-homes'
            home = source / ('a' * 32); home.mkdir(parents=True)
            for name in ('cache', 'sessions', 'compact'):
                (home / name).mkdir(); (home / name / 'data').write_text(name)
            (home / 'config.toml').write_text('設定'); (home / 'config.toml').chmod(0o600)
            for name in ('environment', 'layer1', 'result-registration.json'):
                (root / name).write_text('保持')
            (home / 'shared').symlink_to(root / 'environment')
            before = storage.tree_snapshot(source)
            receipt = storage.archive_homes(source)
            self.assertEqual(receipt['home_count'], 1)
            self.assertFalse(source.exists())
            for name in ('environment', 'layer1', 'result-registration.json'):
                self.assertEqual((root / name).read_text(), '保持')
            restored = root / 'restored'; restored.mkdir()
            z = subprocess.Popen(['zstd', '-dc', str(root / 'codex-homes.archive/homes.tar.zst')], stdout=subprocess.PIPE)
            t = subprocess.run(['tar', '--acls', '--xattrs', '-xpf', '-', '-C', str(restored)], stdin=z.stdout, capture_output=True)
            z.stdout.close(); self.assertEqual(z.wait(), 0); self.assertEqual(t.returncode, 0, t.stderr)
            self.assertEqual(storage.tree_snapshot(restored), before)

    def test_homes_mismatch_mutation_and_existing_output_keep_source(self):
        for failure in ('restored', 'source', 'existing'):
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as temp:
                root = Path(temp).resolve(); source = root / 'codex-homes'
                home = source / ('a' * 32); home.mkdir(parents=True); (home / 'data').write_text('保存')
                if failure == 'existing': (root / 'codex-homes.archive').mkdir()
                real = storage.native_archive
                def changed(batch, target, restored, level, **kwargs):
                    real(batch, target, restored, level, **kwargs)
                    ((batch if failure == 'source' else restored) / ('a' * 32) / 'data').write_text('変更')
                with mock.patch.object(storage, 'native_archive', side_effect=changed):
                    with self.assertRaises(LongRunStorageError): storage.archive_homes(source)
                self.assertTrue(source.is_dir())
                self.assertFalse((root / 'codex-homes.archive/prune-receipt.json').exists())

    def test_homes_rejects_shared_directory_and_links(self):
        for kind in ('shared', 'link', 'unexpected_child'):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                root = Path(temp).resolve(); target = root / 'environment'; target.mkdir()
                (target / 'data').write_text('保持')
                source = root / 'codex-homes'
                if kind == 'link': source.symlink_to(target, target_is_directory=True)
                elif kind == 'unexpected_child': source.mkdir(); (source / 'layer1').mkdir()
                else: source = target
                with self.assertRaises(LongRunStorageError): storage.archive_homes(source)
                self.assertEqual((target / 'data').read_text(), '保持')

    def test_registered_batch_roundtrip_retains_shared_and_layer1_and_registration(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            batch, run_id = self.make_registered(root)
            shared = root / 'shared'
            shared.mkdir(); (shared / 'python-package').write_text('共通環境')
            workspace = batch / 'cycle/layer2/evidence' / run_id / 'workspace'
            (workspace / 'shared-link').symlink_to(shared, target_is_directory=True)
            (workspace / 'empty').mkdir()
            (workspace / 'new.txt').chmod(0o640)
            if sys.platform == 'darwin':
                subprocess.run(['xattr', '-w', 'com.example.archive-test', '保持する値',
                                str(workspace / 'new.txt')], check=True, capture_output=True)
            expected = storage.tree_snapshot(batch)
            registration = batch / 'cycle/layer4/result-registration.json'
            registered_bytes = registration.read_bytes()
            result = storage.archive_batch(batch)
            self.assertEqual(result['status'], 'complete')
            self.assertEqual(result['pruned_paths'], [str(workspace.relative_to(batch))])
            self.assertFalse(workspace.exists())
            self.assertEqual((shared / 'python-package').read_text(), '共通環境')
            self.assertEqual(registration.read_bytes(), registered_bytes)
            self.assertTrue((batch / 'cycle/layer1/fixtures/CASE-1/large-fixture.txt').exists())
            self.assertTrue((batch / 'cycle/layer3/ratings' / f'{run_id}.json').exists())
            restored = root / 'restored'; restored.mkdir()
            z = subprocess.Popen(['zstd', '-dc', str(batch / 'compact/batch-evidence.tar.zst')], stdout=subprocess.PIPE)
            t = subprocess.run(['tar', '--acls', '--xattrs', '-xpf', '-', '-C', str(restored)], stdin=z.stdout, capture_output=True)
            z.stdout.close()
            self.assertEqual(z.wait(), 0)
            self.assertEqual(t.returncode, 0, t.stderr)
            self.assertEqual(storage.tree_snapshot(restored), expected)
            with self.assertRaises(LongRunStorageError):
                storage.archive_batch(batch)

    def test_registration_and_rating_required_before_archive(self):
        for missing in ('registration', 'rating'):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory() as temp:
                batch, run_id = self.make_registered(Path(temp).resolve())
                target = batch / ('cycle/layer4/result-registration.json' if missing=='registration' else f'cycle/layer3/ratings/{run_id}.json')
                target.unlink()
                with self.assertRaises(LongRunStorageError): storage.archive_batch(batch)
                self.assertTrue((batch / 'cycle/layer2/evidence' / run_id / 'workspace').is_dir())
                self.assertFalse((batch / 'compact/batch-evidence.tar.zst').exists())

    def test_claude_usage_supported_without_weakening_completion_checks(self):
        for invalid in (None, 'sessions', 'all_agent_total_tokens'):
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as temp:
                batch, run_id = self.make_registered(Path(temp).resolve())
                usage_path = batch / 'cycle/layer2/extensions' / run_id / 'all-agent-usage/usage.json'
                usage = json.loads(usage_path.read_text())
                usage['schema_version'] = 'the-caption-prompt.claude-all-agent-usage/v1'
                if invalid:
                    usage[invalid] = [] if invalid == 'sessions' else -1
                usage_path.write_text(json.dumps(usage))
                workspace = batch / 'cycle/layer2/evidence' / run_id / 'workspace'
                if invalid:
                    with self.assertRaises(LongRunStorageError): storage.archive_batch(batch)
                    self.assertTrue(workspace.is_dir())
                    self.assertFalse((batch / 'compact/batch-evidence.tar.zst').exists())
                else:
                    self.assertEqual(storage.archive_batch(batch)['status'], 'complete')
                    self.assertFalse(workspace.exists())

    def test_restore_mismatch_prevents_deletion(self):
        with tempfile.TemporaryDirectory() as temp:
            batch, run_id = self.make_registered(Path(temp).resolve())
            real = storage.native_archive
            def broken(batch, target, restored, level):
                real(batch, target, restored, level)
                (restored / 'summary.json').write_text('破損')
            with mock.patch.object(storage, 'native_archive', side_effect=broken):
                with self.assertRaisesRegex(LongRunStorageError, '復元内容'): storage.archive_batch(batch)
            self.assertTrue((batch / 'cycle/layer2/evidence' / run_id / 'workspace').is_dir())
            self.assertFalse((batch / 'compact/batch-prune-receipt.json').exists())

    def test_preserve_existing_keeps_incomplete_history_and_restores_exactly(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            batch, run_id = self.make_registered(root)
            cycle = batch / 'cycle'
            (cycle / 'layer4/result-registration.json').unlink()
            (cycle / 'layer3/ratings' / f'{run_id}.json').unlink()
            evidence = cycle / 'layer2/evidence' / run_id
            (evidence / 'execution.json').unlink()
            shutil.rmtree(evidence / 'rating-view')
            before = storage.tree_snapshot(cycle)
            result = storage.archive_batch(cycle, cycle_path=Path('.'), preserve_existing=True)
            self.assertEqual(result['status'], 'complete')
            self.assertEqual(result['retained'], ['layer1'])
            self.assertFalse((evidence / 'workspace').exists())
            self.assertFalse((cycle / 'layer4/result-registration.json').exists())
            restored = root / 'restored'; restored.mkdir()
            z = subprocess.Popen(['zstd', '-dc', str(cycle / 'compact/batch-evidence.tar.zst')], stdout=subprocess.PIPE)
            t = subprocess.run(['tar', '--acls', '--xattrs', '-xpf', '-', '-C', str(restored)], stdin=z.stdout, capture_output=True)
            z.stdout.close()
            self.assertEqual(z.wait(), 0)
            self.assertEqual(t.returncode, 0, t.stderr)
            self.assertEqual(storage.tree_snapshot(restored), before)

    def test_preserve_existing_mismatch_or_mutation_never_prunes(self):
        for changed_source in (False, True):
            with self.subTest(changed_source=changed_source), tempfile.TemporaryDirectory() as temp:
                batch, run_id = self.make_registered(Path(temp).resolve())
                real = storage.native_archive
                def changed(batch, target, restored, level):
                    real(batch, target, restored, level)
                    ((batch if changed_source else restored) / 'summary.json').write_text('変更')
                with mock.patch.object(storage, 'native_archive', side_effect=changed):
                    with self.assertRaises(LongRunStorageError):
                        storage.archive_batch(batch, preserve_existing=True)
                self.assertTrue((batch / 'cycle/layer2/evidence' / run_id / 'workspace').is_dir())
                self.assertFalse((batch / 'compact/batch-prune-receipt.json').exists())

    def test_source_change_prevents_deletion(self):
        with tempfile.TemporaryDirectory() as temp:
            batch, run_id = self.make_registered(Path(temp).resolve())
            real = storage.native_archive
            def changed(batch, target, restored, level):
                real(batch, target, restored, level)
                (batch / 'summary.json').write_text('同時変更')
            with mock.patch.object(storage, 'native_archive', side_effect=changed):
                with self.assertRaisesRegex(LongRunStorageError, '元データ'): storage.archive_batch(batch)
            self.assertTrue((batch / 'cycle/layer2/evidence' / run_id / 'workspace').is_dir())

    def test_workspace_link_is_never_followed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve(); batch, run_id = self.make_registered(root)
            workspace = batch / 'cycle/layer2/evidence' / run_id / 'workspace'
            target = root / 'shared-workspace'; workspace.rename(target); workspace.symlink_to(target)
            with self.assertRaisesRegex(LongRunStorageError, 'リンク'): storage.archive_batch(batch)
            self.assertTrue((target / 'src.py').exists())

    def test_capacity_failure_keeps_workspace(self):
        with tempfile.TemporaryDirectory() as temp:
            batch, run_id = self.make_registered(Path(temp).resolve())
            with mock.patch.object(storage, 'capacity_guard', return_value={'dispatch_allowed': False}):
                with self.assertRaisesRegex(LongRunStorageError, '容量'): storage.archive_batch(batch)
            self.assertTrue((batch / 'cycle/layer2/evidence' / run_id / 'workspace').is_dir())

    def test_only_container_mtime_is_ignored(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve(); (root / 'file').write_text('内容')
            before = storage.tree_snapshot(root)
            os.utime(root, ns=(1000000000, 1000000000))
            self.assertEqual(before, storage.tree_snapshot(root))
            os.utime(root / 'file', ns=(1000000000, 1000000000))
            self.assertNotEqual(before, storage.tree_snapshot(root))

    def test_cli_has_registered_archive_command(self):
        from layer2.extensions.long_run_storage.long_run_storage import build_parser
        args = build_parser().parse_args(['archive-batch', '--batch', '/example'])
        self.assertEqual(args.zstd_level, 3)
        self.assertFalse(hasattr(args, 'codex_config'))

    def test_cli_failure_reports_nonzero_without_deletion(self):
        with tempfile.TemporaryDirectory() as temp:
            batch, run_id = self.make_registered(Path(temp).resolve())
            (batch / 'cycle/layer4/result-registration.json').unlink()
            script = Path(__file__).resolve().parents[1] / 'layer2/extensions/long_run_storage/long_run_storage.py'
            result = subprocess.run([sys.executable, str(script), 'archive-batch', '--batch', str(batch)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn('Traceback', result.stderr)
            self.assertTrue((batch / 'cycle/layer2/evidence' / run_id / 'workspace').is_dir())
