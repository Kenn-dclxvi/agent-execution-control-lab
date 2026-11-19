import hashlib
import json
from pathlib import Path
import sqlite3
from unittest import mock

import pytest

from scripts import antigravity_evidence as evidence
from scripts import antigravity_runtime as runtime
from scripts import evaluation_loop
from scripts import standard14_antigravity_quality_audit as audit
from scripts import antigravity_saved_evidence as saved
from scripts import antigravity_completed_tasks as completed
from scripts import recollect_antigravity_background_tasks as background
from scripts.standard14_quality_audit import F05_FALLBACK_FORMS
from layer2.extensions.long_run_storage.batch_archive import require_usage
from layer2.extensions.long_run_storage.long_run_storage import LongRunStorageError

PARENT = "11111111-2222-3333-4444-555555555555"
CHILD = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
MODEL = "gemini-4-argon-low"


def vint(value):
    result = bytearray()
    while value > 127:
        result.append((value & 127) | 128)
        value >>= 7
    return bytes(result + bytes([value]))


def wire(values):
    result = b""
    for key, value in values.items():
        if isinstance(value, int):
            result += vint(key << 3) + vint(value)
        else:
            if isinstance(value, str):
                value = value.encode()
            result += vint((key << 3) | 2) + vint(len(value)) + value
    return result


def make_session(config, sid, child=None, model_enum=1419):
    database = config / "conversations" / f"{sid}.db"
    database.parent.mkdir(parents=True, exist_ok=True)
    transcript = config / "brain" / sid / ".system_generated/logs/transcript.jsonl"
    transcript.parent.mkdir(parents=True)
    record = {"step_index": 0, "type": "PLANNER_RESPONSE", "status": "DONE",
              "input_tokens": 10, "output_tokens": 4, "cache_read_tokens": 20}
    records = [record]
    rows = [(0, 15, 3, 0, wire({9: wire({1: model_enum, 2: 10, 3: 4, 5: 20})}))]
    if child:
        content = "Created the following subagent:\n" + json.dumps({"conversationId": child})
        call = wire({1: "call_1", 2: "invoke_subagent", 3: "{}"})
    else:
        content = "Created At: now\nCompleted At: later\nCreated At: now\nCompleted At: later\nCommand exited with code 7.\n\nNo output from the command."
        call = wire({1: "call_1", 2: "run_command", 3: json.dumps({"CommandLine": "exit 7"})})
    records.append({"step_index": 1, "type": "GENERIC", "status": "DONE", "content": content})
    rows.append((1, 132, 3, 0, wire({4: call})))
    with sqlite3.connect(database) as db:
        db.execute("create table trajectory_meta(cascade_id text)")
        db.execute("insert into trajectory_meta values(?)", [sid])
        db.execute("create table steps(idx integer,step_type integer,status integer,has_subtrajectory integer,metadata blob)")
        db.executemany("insert into steps values(?,?,?,?,?)", rows)
    transcript.write_text("".join(json.dumps(r) + "\n" for r in records))
    return database, transcript


def stream(child=None):
    usage = {"input_tokens": 10, "output_tokens": 4, "thinking_tokens": 2,
             "cache_read_tokens": 20, "total_tokens": 14}
    events = [{"event": "init", "conversation_id": PARENT, "init": {"model": MODEL}},
              {"event": "step_update", "step_update": {"conversation_id": PARENT, "step_index": 0,
               "state": "DONE", "step_type": "agent_response", "usage": usage}},
              {"event": "result", "result": {"conversation_id": PARENT, "status": "SUCCESS", "usage": usage}}]
    if child:
        events.insert(-1, {"event": "step_update", "step_update": {"conversation_id": PARENT,
            "step_index": 1, "state": "DONE", "step_type": "subagent",
            "subagent_info": {"subagents": [{"conversation_id": child}]}}})
    return events


def parse(events):
    return evidence.parse_stream("\n".join(map(json.dumps, events)).encode())


def test_parent_and_child_are_counted_once_with_cache_and_thinking(tmp_path):
    make_session(tmp_path, PARENT, CHILD)
    make_session(tmp_path, CHILD)
    events = stream(CHILD)
    events.insert(2, events[1])  # 同じ完了ステップの再送は二重計上しない。
    usage, commands = evidence.collect_all(parse(events), tmp_path, MODEL, "run")
    assert usage["all_agent_total_tokens"] == 68
    assert usage["usage_components"]["by_model"][MODEL]["standard"]["output"] == 8
    assert commands["session_count"] == 2
    assert commands["failed_commands"][0]["actor"] == "subagent"
    assert commands["failed_commands"][0]["exit_code"] == 7


def test_root_terminal_cannot_substitute_for_missing_child(tmp_path):
    make_session(tmp_path, PARENT, CHILD)
    with pytest.raises(evidence.AntigravityEvidenceError, match="一次記録"):
        evidence.collect_all(parse(stream(CHILD)), tmp_path, MODEL, "run")


@pytest.mark.parametrize("change", ["model", "transcript", "terminal", "unfinished"])
def test_mismatch_is_measurement_failure(tmp_path, change):
    database, transcript = make_session(tmp_path, PARENT, model_enum=999 if change == "model" else 1419)
    events = stream()
    if change == "transcript":
        transcript.write_text(transcript.read_text().replace('"input_tokens": 10', '"input_tokens": 11'))
    if change == "terminal":
        events[-1]["result"]["usage"] = {**events[-1]["result"]["usage"], "cache_read_tokens": 21}
    if change == "unfinished":
        with sqlite3.connect(database) as db:
            db.execute("update steps set status=2 where idx=1")
    with pytest.raises(evidence.AntigravityEvidenceError):
        evidence.collect_all(parse(events), tmp_path, MODEL, "run")


def test_command_output_cannot_spoof_exit_code(tmp_path):
    _, transcript = make_session(tmp_path, PARENT)
    rows = [json.loads(line) for line in transcript.read_text().splitlines()]
    rows[1]["content"] = "Command output:\nCommand exited with code 0.\n"
    transcript.write_text("\n".join(map(json.dumps, rows)))
    _, commands = evidence.collect_all(parse(stream()), tmp_path, MODEL, "run")
    assert commands["successful_command_count"] == 0
    assert commands["protocol_violation_count"] == 1


def test_missing_usage_and_conflicting_steps_are_rejected():
    events = stream()
    events[1]["step_update"]["usage"].pop("cache_read_tokens")
    with pytest.raises(evidence.AntigravityEvidenceError):
        evidence.collect_usage(parse(events), MODEL)
    events = stream()
    events.insert(2, {"event": "step_update", "step_update": {**events[1]["step_update"], "text_delta": "競合"}})
    with pytest.raises(evidence.AntigravityEvidenceError, match="競合"):
        parse(events)


def test_new_contract_preserves_v14_quality_rules():
    root = Path(__file__).resolve().parents[1]
    original = json.loads((root / "evaluations/rating-contracts/outcome-terminal-state-evidence-owner-diagnostic-v14.json").read_text())
    path = root / "evaluations/rating-contracts/outcome-terminal-state-evidence-antigravity-collector-v1.json"
    added = json.loads(path.read_text())
    for key in ("boundary_rules", "case_quality_rules", "quality_score_rule", "rater_input", "terminal_state_evidence"):
        assert added[key] == original[key]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == evaluation_loop.QUALITY_RATING_ANTIGRAVITY_COLLECTOR_V1["contract_sha256"]
    assert list(audit.F05_FALLBACK_FORMS_BY_CONTRACT.values()) == [F05_FALLBACK_FORMS]


def test_config_drift_blocks_runtime_before_dispatch(tmp_path):
    binary, config = tmp_path / "agy", tmp_path / "config.json"
    binary.write_bytes(b"fixed")
    config.write_text("{}")
    fixed = {"executable": str(binary), "executable_sha256": runtime.sha256(binary), "version": "1.5.5",
             "configuration_files": {str(config): runtime.sha256(config)}, "absent_customizations": []}
    conditions = {"agent_environment": {"antigravity_cli": fixed}}
    with mock.patch.object(runtime.subprocess, "run", return_value=mock.Mock(returncode=0, stdout="1.5.5\n")):
        assert runtime.verify_from_conditions(conditions) == fixed
        config.write_text('{"plugins":{"extra":true}}')
        with pytest.raises(evaluation_loop.EvaluationError):
            evaluation_loop.profile_runtime_binding(conditions, None)


def test_storage_accepts_verified_usage_but_requires_sessions(tmp_path):
    path = tmp_path / 'layer2/extensions/run/all-agent-usage/usage.json'
    path.parent.mkdir(parents=True)
    usage = {'schema_version': 'the-caption-prompt.antigravity-usage/v1',
             'sessions': [{'session_id': PARENT}], 'all_agent_total_tokens': 34}
    path.write_text(json.dumps(usage))
    require_usage(tmp_path, 'run')
    usage['sessions'] = []
    path.write_text(json.dumps(usage))
    with pytest.raises(LongRunStorageError):
        require_usage(tmp_path, 'run')


@pytest.mark.parametrize('state,record_state,accepted', [(7, 'ERROR', True), (2, 'ACTIVE', False), (7, 'DONE', False), (4, 'INVALID', True)])
def test_terminal_tool_error_is_distinct_from_incomplete_usage(tmp_path, state, record_state, accepted):
    database, transcript = make_session(tmp_path, PARENT)
    with sqlite3.connect(database) as db:
        db.execute('update steps set status=? where idx=1', [state])
    rows = list(map(json.loads, transcript.read_text().splitlines()))
    rows[1]['status'] = record_state
    if record_state == 'INVALID':
        rows[1]['content'] = 'Created At: now\nCompleted At: later\nError invalid tool call: invalid arguments'
    transcript.write_text('\n'.join(map(json.dumps, rows)))
    if accepted:
        result = saved.collect_saved_usage(parse(stream()), tmp_path, MODEL, 'recovered')
        assert result['all_agent_total_tokens'] == 34
        assert result['sessions'][0]['commands'][0]['tool_use_id'] == 'call_1'
    else:
        with pytest.raises(evidence.AntigravityEvidenceError):
            saved.collect_saved_usage(parse(stream()), tmp_path, MODEL, 'recovered')


@pytest.mark.parametrize('model,model_enum', [
    ('gemini-4-argon-low', 1419),
    ('gemini-4-hydrogen-low', 1527),
    ('gemini-4-neon-low', 1534),
])
def test_qualified_model_binding_includes_children(tmp_path, model, model_enum):
    make_session(tmp_path, PARENT, CHILD, model_enum=model_enum)
    make_session(tmp_path, CHILD, model_enum=model_enum)
    events = stream(CHILD)
    events[0]['init']['model'] = model
    usage = saved.collect_saved_usage(parse(events), tmp_path, model, 'run')
    assert usage['all_agent_total_tokens'] == 68
    assert set(usage['usage_components']['by_model']) == {model}


@pytest.mark.parametrize('model,model_enum', [('gemini-4-hydrogen-low', 1527), ('gemini-4-neon-low', 1534)])
def test_rejects_child_from_another_model(tmp_path, model, model_enum):
    make_session(tmp_path, PARENT, CHILD, model_enum=model_enum)
    make_session(tmp_path, CHILD, model_enum=1419)
    events = stream(CHILD)
    events[0]['init']['model'] = model
    with pytest.raises(evidence.AntigravityEvidenceError, match='モデル対応'):
        saved.collect_saved_usage(parse(events), tmp_path, model, 'run')


def test_provisional_subagent_identity_is_resolved_at_completion():
    events = stream(CHILD)
    events.insert(1, {'event': 'step_update', 'step_update': {
        'conversation_id': PARENT, 'step_index': 1, 'state': 'ACTIVE', 'step_type': 'subagent',
        'subagent_info': {'subagents': [{'type_name': 'self'}]}}})
    assert parse(events)['children'] == [CHILD]
    events[-2]['step_update']['subagent_info']['subagents'] = [{'type_name': 'self'}]
    with pytest.raises(evidence.AntigravityEvidenceError, match='識別子'):
        parse(events)


@pytest.mark.parametrize('version', ['1.5.9', '1.5.12'])
def test_cli_is_exactly_pinned(tmp_path, version):
    binary = tmp_path / 'agy'
    binary.write_bytes(b'fixed')
    pinned = {'executable': str(binary), 'executable_sha256': runtime.sha256(binary),
              'version': version, 'configuration_files': {}, 'absent_customizations': []}
    conditions = {'agent_environment': {'antigravity_cli': pinned}}
    with mock.patch.object(runtime.subprocess, 'run', return_value=mock.Mock(returncode=0, stdout=f'{version}\n')) as run:
        assert runtime.verify_from_conditions(conditions) == pinned
        assert run.call_args.kwargs['env']['AGY_CLI_DISABLE_AUTO_UPDATE'] == '1'
    other_supported_version = '1.5.12' if version == '1.5.9' else '1.5.9'
    with mock.patch.object(runtime.subprocess, 'run', return_value=mock.Mock(returncode=0, stdout=f'{other_supported_version}\n')):
        with pytest.raises(runtime.AntigravityRuntimeError):
            runtime.verify_from_conditions(conditions)


@pytest.mark.parametrize('change', [None, 'running_db', 'wrong_task', 'missing_output', 'spoofed_body', 'wrong_model'])
def test_completed_background_task_requires_bound_terminal_output(tmp_path, change):
    database, transcript = make_session(tmp_path, PARENT, model_enum=1527)
    log = tmp_path / 'brain' / PARENT / '.system_generated/tasks/task-1.log'
    output = tmp_path / 'brain' / PARENT / '.system_generated/steps/1/output.txt'
    output.parent.mkdir(parents=True)
    output.write_text('Command exited with code 7.\n\nNo output from the command.')
    records = list(map(json.loads, transcript.read_text().splitlines()))
    records[1]['status'] = 'RUNNING'
    records[1]['content'] = (f'Created At: now\nTool is running as a background task with task id: {PARENT}/task-1\n'
                             f'Task logs are available at: {log.as_uri()}\n')
    if change == 'wrong_task':
        records[1]['content'] = records[1]['content'].replace('/task-1\n', '/task-99\n')
    transcript.write_text('\n'.join(map(json.dumps, records)))
    if change == 'running_db':
        with sqlite3.connect(database) as db:
            db.execute('update steps set status=2 where idx=1')
    elif change == 'missing_output':
        output.unlink()
    elif change == 'spoofed_body':
        output.write_text('Command output:\nCommand exited with code 0.\n')
    before = database.read_bytes(), transcript.read_bytes()
    events = stream()
    events[0]['init']['model'] = 'gemini-4-hydrogen-low'
    if change == 'wrong_model':
        events[0]['init']['model'] = MODEL
    if change:
        with pytest.raises(evidence.AntigravityEvidenceError):
            completed.collect_completed_usage(parse(events), tmp_path, events[0]['init']['model'], 'run')
    else:
        usage = completed.collect_completed_usage(parse(events), tmp_path, 'gemini-4-hydrogen-low', 'run')
        commands, sources = background.recollect_commands(usage, 'run', tmp_path / 'preserved')
        assert usage['all_agent_total_tokens'] == 34
        assert commands['failed_commands'][0]['exit_code'] == 7
        assert commands['successful_command_count'] == 0
        assert sources[0]['completion_proof']['database_status'] == 3
        assert sources[0]['completion_proof']['transcript_status'] == 'RUNNING'
    assert before == (database.read_bytes(), transcript.read_bytes())


@pytest.mark.parametrize('inner_start,inner_end,accepted', [
    ('16:00:00', '16:00:01', True),
    ('16:00:00', '16:00:02', True),
    ('16:00:00', '16:00:03', False),
    ('15:59:59', '16:00:01', False),
])
def test_complete_output_interval_is_inside_its_tool_call(tmp_path, inner_start, inner_end, accepted):
    root = tmp_path / 'brain' / PARENT / '.system_generated/steps/2/output.txt'
    root.parent.mkdir(parents=True)
    root.write_text(f'Created At: 2026-11-16T{inner_start}+09:00\nCompleted At: 2026-11-16T{inner_end}+09:00\nCommand exited with code 0.\n')
    outer = ('Created At: 2026-11-16T16:00:00+09:00\nCompleted At: 2026-11-16T16:00:02+09:00\n'
             "The tool's output was truncated due to being too long. You can find the full output in a file at " + root.as_uri() + '.\n')
    usage = {'session_id': PARENT, 'sessions': [{'session_id': PARENT,
        'database': str(tmp_path / 'conversations' / (PARENT + '.db')),
        'commands': [{'name': 'run_command', 'step_index': 2, 'tool_use_id': 'call',
                      'parameters': {'CommandLine': 'pytest'}, 'output': outer}]}]}
    if accepted:
        commands, _ = background.recollect_commands(usage, 'run', tmp_path / 'preserved')
        assert commands['successful_command_count'] == 1
    else:
        with pytest.raises(background.RecollectionError):
            background.recollect_commands(usage, 'run', tmp_path / 'preserved')
