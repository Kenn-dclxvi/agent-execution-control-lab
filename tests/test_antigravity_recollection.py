import json
from pathlib import Path
import sys

import pytest

from scripts import recollect_antigravity_commands as repair
from scripts import run_antigravity_evaluation as adapter_v1
from scripts import run_antigravity_evaluation_v2 as adapter_v2

SID = '11111111-2222-3333-4444-555555555555'
HEADER = 'Created At: now\nCompleted At: later\n'


def put(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def saved_usage(tmp_path):
    config = tmp_path / 'runtime'
    full = config / 'brain' / SID / '.system_generated/steps/2/output.txt'
    full.parent.mkdir(parents=True)
    full.write_text(HEADER + 'Command exited with code 0.\n\nCommand output:\npassed\n')
    abbreviated = HEADER + "The tool's output was truncated due to being too long. You can find the full output in a file at " + full.as_uri() + '.\n\nHere is a preview with the middle of the output truncated:\n'
    return {
        'schema_version': 'the-caption-prompt.antigravity-usage/v1', 'run_id': 'old',
        'session_id': SID, 'token_accounting': repair.TOKEN_ACCOUNTING, 'all_agent_total_tokens': 34,
        'usage_components': {'unchanged': True},
        'sessions': [{'session_id': SID, 'database': str(config / 'conversations' / (SID + '.db')),
                      'commands': [{'name': 'run_command', 'step_index': 2, 'tool_use_id': 'call_1',
                                    'parameters': {'CommandLine': 'pytest'}, 'output': abbreviated}]}],
    }, full


def test_saved_full_output_restores_exit_without_reading_preview(tmp_path):
    usage, full = saved_usage(tmp_path)
    usage['sessions'][0]['commands'][0]['output'] += 'Command exited with code 7.\n'
    commands, sources = repair.recollect_commands(usage, 'new', tmp_path / 'outputs')
    assert commands['successful_command_count'] == 1
    assert commands['failed_command_count'] == 0
    assert commands['protocol_violation_count'] == 0
    assert sources[0]['sha256'] == repair.digest(full)
    assert (tmp_path / 'outputs' / SID / '2.txt').read_bytes() == full.read_bytes()


def test_collector_fix_does_not_change_model_visible_task():
    case = {'payload': {'trial_prompt_input': {'task': '指定された成果を作る'}}}
    protocol = {'required_commands': ['pytest']}
    assert adapter_v1.render_task(case, protocol) == adapter_v2.render_task(case, protocol)


@pytest.mark.parametrize('change', ['path', 'time', 'body'])
def test_unbound_output_is_not_accepted(tmp_path, change):
    usage, full = saved_usage(tmp_path)
    if change == 'path':
        usage['sessions'][0]['commands'][0]['output'] = usage['sessions'][0]['commands'][0]['output'].replace(full.as_uri(), (tmp_path / 'unrelated.txt').as_uri())
    elif change == 'time':
        full.write_text('Created At: different\nCompleted At: later\nCommand exited with code 0.\n')
    else:
        full.write_text(HEADER + 'Command output:\nCommand exited with code 0.\n')
    if change == 'body':
        commands, _ = repair.recollect_commands(usage, 'new', tmp_path / 'outputs')
        assert commands['successful_command_count'] == 0
        assert commands['protocol_violation_count'] == 1
    else:
        with pytest.raises(repair.RecollectionError):
            repair.recollect_commands(usage, 'new', tmp_path / 'outputs')


@pytest.mark.skipif(sys.platform != 'darwin', reason='clonefileの照合にはmacOSが必要です')
def test_recovery_appends_preserves_source_elapsed_and_sample_identity(tmp_path, monkeypatch):
    monkeypatch.setenv('THE_CAPTION_EVAL_COPY_MODE', 'clonefile')
    usage, _ = saved_usage(tmp_path)
    monkeypatch.setattr(repair, 'collect_saved_usage', lambda *args: usage)
    monkeypatch.setattr(repair, 'preserve_sessions', lambda *args: None)
    cycle = tmp_path / 'cycle'
    evidence = cycle / 'layer2/evidence/old'
    extension = cycle / 'layer2/extensions/old'
    workspace = evidence / 'workspace'
    workspace.mkdir(parents=True)
    (workspace / 'data').write_text('モデルの保存済み成果')
    execution = {'status': 'excluded', 'exit_code': 75, 'run_id': 'old', 'elapsed_seconds': 12.5,
                 'total_tokens': None, 'token_accounting': None}
    put(evidence / 'execution.json', execution)
    put(evidence / 'exclusion.json', {'reason_code': 'command_evidence_incomplete'})
    put(extension / 'antigravity-adapter/execution.json', {'antigravity_exit_code': 0, 'terminal': 'SUCCESS', 'external_failure': {}})
    (extension / 'antigravity-adapter/stream.jsonl').write_text('\n'.join(map(json.dumps, [
        {'event': 'init', 'conversation_id': SID, 'init': {}},
        {'event': 'result', 'result': {'conversation_id': SID, 'status': 'SUCCESS'}}])))
    put(extension / 'all-agent-usage/usage.json', usage)
    put(extension / 'all-agent-command-evidence/evidence.json', {'run_id': 'old'})
    put(extension / 'command-protocol-audit/audit.json', {'run_id': 'old'})
    protocol = {'schema_version': 'the-caption-prompt.command-evidence-protocol/v1',
                'mode': 'separate_required_commands_with_structured_exit',
                'required_command_groups_by_case': {'CASE': [['pytest']]}, 'omit_for_cases': []}
    binding = {'run_id': 'old', 'status': 'excluded', 'sample_id': 'planned:once', 'case_id': 'CASE',
               'comparison_conditions': {'model': 'gemini-4-argon-low',
                   'agent_environment': {'antigravity_cli': {'config_dir': str(tmp_path / 'runtime')}},
                   'executor_parameters': {'command_evidence_protocol': protocol}}}
    put(cycle / 'layer2/bindings/old.json', binding)
    put(cycle / 'layer2/capsules/old.json', {'fixed': True})
    before = repair.tree_snapshot(evidence), repair.tree_snapshot(extension), repair.digest(cycle / 'layer2/bindings/old.json')
    receipt = repair.recover(cycle, 'old')
    new_id = receipt['recovered_run_id']
    assert receipt['model_invocations'] == 0
    assert receipt['elapsed_seconds_preserved'] == 12.5
    assert before == (repair.tree_snapshot(evidence), repair.tree_snapshot(extension), repair.digest(cycle / 'layer2/bindings/old.json'))
    recovered = json.loads((cycle / 'layer2/bindings' / (new_id + '.json')).read_text())
    assert recovered['status'] == 'valid'
    assert recovered['sample_id'] == 'planned:once'
    assert json.loads((cycle / 'layer2/evidence' / new_id / 'execution.json').read_text())['elapsed_seconds'] == 12.5
    with pytest.raises(repair.RecollectionError, match='有効な記録'):
        repair.recover(cycle, 'old')
