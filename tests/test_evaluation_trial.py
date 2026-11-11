"""外部モデルを呼ばず、標準経路の終了条件と保護境界を検証する。"""
import argparse
import json
from pathlib import Path
import shutil
import sys
import tempfile
from unittest import mock

import pytest

from scripts import evaluation_trial as trial
from tests import test_evaluation_loop as fixtures
from layer2.extensions.long_run_storage import minimal_archive, batch_archive


pytestmark = pytest.mark.skipif(sys.platform != "darwin", reason="clonefileによる標準経路はmacOSが必要です")


def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def setup_trial(root, iterations=1):
    helper = fixtures.EvaluationLoopTest()
    conditions = helper.conditions(iterations)
    identity = {"name": "test", "revision": "r1"}
    profile = helper.install(root, helper.make_set(root), root / 'seed-cycle', identity, conditions)
    document = trial.load(profile)
    document['execution']['duration_hints_seconds'] = {'TEST-CASE': 0.01}
    document['execution']['monitor_interval_seconds'] = 1
    document['execution']['max_attempts'] = 1
    put(profile, document)
    template = helper.write_capsule(root / 'capsule.json', identity, 1, conditions,
                                   'import os,json,pathlib;' + helper.usage_code(10))
    common = root / 'common'
    common.mkdir()
    (common / 'data').write_text('保護')
    resource = root / 'resource.json'
    put(resource, {'agent': 'test'})
    args = argparse.Namespace(profile=profile, store=root / 'store', registry=root / 'registry',
                              price_table=helper.price_table(root), resource_class=resource,
                              archive_store=root / 'archive-store', archive_root=root / 'archives',
                              template=[template], protect=[common], homes=[])
    return root / 'trial', args


def finalize_usage_and_rate(cycle):
    for path in (cycle / 'layer2/bindings').glob('*.json'):
        binding = trial.load(path)
        if binding['status'] != 'valid':
            continue
        run_id = binding['run_id']
        put(cycle / 'layer2/extensions' / run_id / 'all-agent-usage/usage.json', {
            'schema_version': 'the-caption-prompt.all-agent-usage/v1',
            'all_agent_total_tokens': 10, 'sessions': [{'tokens': 10}]})
        put(cycle / 'layer3/ratings' / f'{run_id}.json', {'run_id': run_id, 'score': 4})
        view = cycle / 'layer2/evidence' / run_id / 'rating-view'
        view.mkdir()
        for name in ('result.diff', 'validation.json', 'final-response.txt'):
            (view / name).write_text('{}')


@pytest.fixture
def space():
    with tempfile.TemporaryDirectory() as name, mock.patch.object(trial, 'capacity_guard', return_value={'dispatch_allowed': True}), mock.patch.object(batch_archive, 'capacity_guard', return_value={'dispatch_allowed': True}):
        yield Path(name).resolve()


@pytest.mark.skipif(not shutil.which('zstd'), reason='zstdが必要です')
def test_prepare_run_finish_and_reuse_without_model(space):
    directory, args = setup_trial(space)
    args.homes = [directory / 'codex-homes']
    home = args.homes[0] / ('a' * 32)
    home.mkdir(parents=True)
    (home / 'sessions').write_text('非公開実行記録')
    protected = trial.snapshot(space / 'store'), trial.snapshot(space / 'common')
    assert trial.prepare(directory, args)['missing_slots'] == 1
    prepared = trial.load(directory / 'receipts/0001-prepared.json')
    assert prepared['authorized_slot_count'] == 1
    result = trial.run(directory)
    assert result['runner_return_code'] == 0
    cycle = Path(result['cycle'])
    with pytest.raises((trial.TrialError, trial.LongRunStorageError)):
        trial.finish(directory)
    assert not (directory / 'complete.json').exists()
    finalize_usage_and_rate(cycle)
    with mock.patch.object(trial, 'archive_minimal', side_effect=OSError('保存中断')):
        with pytest.raises(OSError):
            trial.finish(directory)
    assert not (directory / 'complete.json').exists()
    assert list((cycle / 'layer2/evidence').glob('*/workspace'))
    result = trial.finish(directory)
    assert result['status'] == 'complete'
    assert not list((cycle / 'layer2/evidence').glob('*/workspace'))
    restored = space / 'restored'
    minimal_archive.restore_minimal(space / 'archives/0001', space / 'archive-store', restored)
    # 登録の追記だけを含めて実際の保存元と照合する。
    manifest = minimal_archive.read_manifest(space / 'archives/0001')
    assert trial.snapshot(restored) == manifest['entries']
    assert (restored / 'lifecycle/selection.json').is_file()
    assert (restored / 'lifecycle/inputs/profile.json').read_bytes() == (directory / 'inputs/profile.json').read_bytes()
    assert trial.finish(directory) == result
    assert protected == (trial.snapshot(space / 'store'), trial.snapshot(space / 'common'))
    assert not args.homes[0].exists()
    assert result['home_receipts']
    args.homes = []
    old_registry = trial.snapshot(space / 'registry')
    second = space / 'reuse'
    args.archive_root = space / 'reuse-archives'
    assert trial.prepare(second, args)['missing_slots'] == 0
    assert trial.run(second)['runner_return_code'] == 0
    assert trial.finish(second)['status'] == 'complete'
    config = trial.load(second / 'trial.json')
    trial.check_protected(config)
    assert all(value == trial.snapshot(space / 'registry')[name] for name, value in old_registry.items() if value['type'] != 16384)


def test_protected_and_preflight_drift_block_dispatch(space):
    directory, args = setup_trial(space)
    trial.prepare(directory, args)
    (space / 'common/data').write_text('変更')
    with pytest.raises(trial.TrialError, match='保護対象'):
        trial.run(directory)
    assert not (directory / 'receipts/0001-executed.json').exists()


def test_plan_drift_and_duplicate_dispatch_rejected(space):
    directory, args = setup_trial(space)
    trial.prepare(directory, args)
    prepared = trial.load(directory / 'receipts/0001-prepared.json')
    Path(prepared['plan']).write_text('{}')
    with pytest.raises(trial.TrialError, match='発行計画'):
        trial.run(directory)


def test_storage_shortage_blocks_prepare(space):
    directory, args = setup_trial(space)
    with mock.patch.object(trial, 'capacity_guard', return_value={'dispatch_allowed': False}):
        with pytest.raises(trial.TrialError, match='空き容量'):
            trial.prepare(directory, args)
    assert not (directory / 'rounds').exists()


@pytest.mark.skipif(not shutil.which('zstd'), reason='zstdが必要です')
def test_partial_round_saved_then_only_missing_run_dispatched(space):
    directory, args = setup_trial(space, iterations=2)
    assert trial.prepare(directory, args)['missing_slots'] == 2
    cycle = Path(trial.run(directory)['cycle'])
    finalize_usage_and_rate(cycle)
    binding_path = sorted((cycle / 'layer2/bindings').glob('*.json'))[0]
    binding = trial.load(binding_path)
    binding['status'] = 'excluded'
    put(binding_path, binding)
    execution_path = cycle / 'layer2/evidence' / binding['run_id'] / 'execution.json'
    execution = trial.load(execution_path)
    execution['status'] = 'excluded'
    put(execution_path, execution)
    result = trial.finish(directory)
    assert result['status'] == 'incomplete_saved'
    assert result['missing_slots'] == 1
    assert not (directory / 'complete.json').exists()
    assert not list((cycle / 'layer2/evidence').glob('*/workspace'))
    assert trial.prepare(directory, args)['missing_slots'] == 1
    second = Path(trial.run(directory)['cycle'])
    finalize_usage_and_rate(second)
    assert trial.finish(directory)['status'] == 'complete'
    assert len(trial.rounds(directory)) == 2
    with pytest.raises(trial.TrialError, match='発行済み'):
        trial.run(directory)


def test_prepare_failure_resumes_without_changing_fixed_inputs(space):
    directory, args = setup_trial(space)
    real = trial.call
    def fail(script, *arguments):
        if 'preflight-execution' in arguments:
            raise trial.TrialError('preflight中断')
        return real(script, *arguments)
    with mock.patch.object(trial, 'call', side_effect=fail):
        with pytest.raises(trial.TrialError, match='preflight中断'):
            trial.prepare(directory, args)
    assert not (directory / 'receipts/0001-prepared.json').exists()
    assert trial.prepare(directory, args)['missing_slots'] == 1
    assert len(trial.rounds(directory)) == 1


def test_append_only_guard_rejects_old_result_mutation(space):
    directory, args = setup_trial(space)
    old = space / 'registry/results/old.json'
    put(old, {'preserve': True})
    trial.prepare(directory, args)
    put(old, {'preserve': False})
    with pytest.raises(trial.TrialError, match='保護対象'):
        trial.run(directory)


@pytest.mark.skipif(not shutil.which('zstd'), reason='zstdが必要です')
def test_interruption_before_first_execution_is_saved_but_incomplete(space):
    directory, args = setup_trial(space)
    trial.prepare(directory, args)
    (directory / 'rounds/0001/runner.log').write_text('発行前に親プロセスが終了')
    result = trial.finish(directory)
    assert result['status'] == 'incomplete_saved'
    assert result['missing_slots'] == 1
    assert not (directory / 'complete.json').exists()
    manifest = minimal_archive.read_manifest(space / 'archives/0001')
    assert manifest['workspaces'] == []
    assert trial.prepare(directory, args)['missing_slots'] == 1


def test_layer1_drift_blocks_dispatch(space):
    directory, args = setup_trial(space)
    trial.prepare(directory, args)
    (directory / 'rounds/0001/cycle/layer1/fixtures/TEST-CASE/input.txt').write_text('改変')
    with pytest.raises(trial.TrialError, match='Layer 1'):
        trial.run(directory)


def test_group_uses_one_queue_and_records_both_trials(space):
    directories = []
    for name in ('a', 'b'):
        root = space / name
        root.mkdir()
        directory, args = setup_trial(root)
        trial.prepare(directory, args)
        directories.append(directory)
    result = trial.run_group(directories)
    assert result['runner_return_code'] == 0
    assert len(result['cycles']) == 2
    receipts = [trial.load(p / 'receipts/0001-executed.json') for p in directories]
    assert receipts[0]['campaign'] == receipts[1]['campaign']
    with pytest.raises(trial.TrialError, match='発行済み'):
        trial.run_group(directories)


def test_group_checks_every_trial_before_starting_runner(space):
    directories = []
    for name in ('a', 'b'):
        root = space / name
        root.mkdir()
        directory, args = setup_trial(root)
        trial.prepare(directory, args)
        directories.append(directory)
    (directories[-1] / 'rounds/0001/cycle/layer1/fixtures/TEST-CASE/input.txt').write_text('改変')
    with mock.patch.object(trial, 'call', return_value={}), mock.patch.object(trial.subprocess, 'Popen') as start:
        with pytest.raises(trial.TrialError, match='Layer 1'):
            trial.run_group(directories)
        start.assert_not_called()
