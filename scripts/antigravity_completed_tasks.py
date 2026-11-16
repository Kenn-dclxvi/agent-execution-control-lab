"""完了DBと同一ステップの一次出力から、古い実行中表示を再照合する。"""

import hashlib
import json
from pathlib import Path
import re
import sqlite3
import tempfile

from scripts.antigravity_evidence import AntigravityEvidenceError, collect_usage, one, wire_fields
from scripts.antigravity_saved_evidence import MODEL_ENUMS, read_session
from scripts.usage_components import components_document, empty_buckets

RAW_EXIT = re.compile(r'\ACommand exited with code (-?\d+)\.\n')


def read_completed_session(config, sid, expected_model_enum):
    if re.fullmatch(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}", sid) is None:
        raise AntigravityEvidenceError("会話識別子が不正です")
    database = config / 'conversations' / f'{sid}.db'
    transcript = config / 'brain' / sid / '.system_generated/logs/transcript.jsonl'
    if database.is_symlink() or not database.is_file() or not transcript.is_file():
        raise AntigravityEvidenceError('一次記録がありません')
    records = [json.loads(line) for line in transcript.read_text().splitlines()]
    proof = {}
    with sqlite3.connect(database.as_uri() + '?mode=ro', uri=True) as db:
        rows = {row[0]: row[1:] for row in db.execute('select idx,step_type,status,has_subtrajectory,metadata from steps')}
        for record in records:
            if record.get('status') != 'RUNNING':
                continue
            index = record['step_index']
            kind, status, subtrajectory, metadata = rows[index]
            call = wire_fields(one(wire_fields(metadata), 4, b''))
            content = record.get('content', '')
            log = config / 'brain' / sid / '.system_generated/tasks' / f'task-{index}.log'
            output = config / 'brain' / sid / '.system_generated/steps' / str(index) / 'output.txt'
            if (kind != 132 or status != 3 or subtrajectory
                    or one(call, 2, b'').decode() != 'run_command'
                    or f'Tool is running as a background task with task id: {sid}/task-{index}\n' not in content
                    or f'Task logs are available at: {log.as_uri()}' not in content
                    or output.is_symlink() or not output.is_file()):
                raise AntigravityEvidenceError('実行中表示を完了記録へ対応づけられません')
            data = output.read_bytes()
            if RAW_EXIT.match(data.decode()) is None:
                raise AntigravityEvidenceError('同一ステップの完全出力に終了記録がありません')
            proof[index] = {'path': str(output), 'sha256': hashlib.sha256(data).hexdigest(),
                            'database_status': status, 'transcript_status': 'RUNNING', 'step_index': index}
            # 原本を変更せず、DBの終端状態を反映した照合用の投影だけを作る。
            record['status'] = 'DONE'
        with tempfile.TemporaryDirectory(prefix='antigravity-completed-task-') as name:
            view = Path(name)
            target_db = view / 'conversations' / f'{sid}.db'
            target_db.parent.mkdir()
            with sqlite3.connect(target_db) as target:
                db.backup(target)
            target_log = view / 'brain' / sid / '.system_generated/logs/transcript.jsonl'
            target_log.parent.mkdir(parents=True)
            target_log.write_text('\n'.join(json.dumps(row) for row in records))
            # モデル識別値は呼び出し側で必ず固定する。
            return view_session(view, sid, database, transcript, proof, expected_model_enum)


def view_session(view, sid, database, transcript, proof, expected_model_enum):
    session = read_session(view, sid, expected_model_enum)
    session['database'], session['transcript'] = str(database), str(transcript)
    for command in session['commands']:
        if command['step_index'] in proof:
            command['completed_task_evidence'] = proof[command['step_index']]
    return session


def collect_completed_usage(stream, config, model, run_id):
    if stream['init'].get('model') != model or model not in MODEL_ENUMS or stream['result'].get('status') != 'SUCCESS':
        raise AntigravityEvidenceError('固定モデルまたは終端状態が一致しません')
    pending, sessions = [stream['session_id']], {}
    while pending:
        sid = pending.pop()
        if sid in sessions:
            raise AntigravityEvidenceError('子の帰属が重複しています')
        session = read_completed_session(config, sid, MODEL_ENUMS[model])
        if any(item['model_enum'] != MODEL_ENUMS[model] for item in session['usage']):
            raise AntigravityEvidenceError('親子のモデルが固定条件と一致しません')
        sessions[sid] = session
        pending.extend(session['children'])
    root = sessions[stream['session_id']]
    if set(root['children']) != set(stream['children']):
        raise AntigravityEvidenceError('親子の対応が一致しません')
    reported = collect_usage({**stream, 'children': []}, model)['cli_reported_usage']
    for key in ['input_tokens', 'cache_read_tokens', 'output_tokens']:
        if sum(item[key] for item in root['usage']) != reported[key]:
            raise AntigravityEvidenceError('親の使用量が一次記録と一致しません')
    buckets = empty_buckets()
    for session in sessions.values():
        for item in session['usage']:
            for target, source in [('uncached_input', 'input_tokens'), ('cache_read', 'cache_read_tokens'), ('output', 'output_tokens')]:
                buckets[target] += item[source]
    components = components_document({model: {'standard': buckets}}, 'antigravity')
    from scripts.antigravity_evidence import TOKEN_ACCOUNTING
    return {'schema_version': 'the-caption-prompt.antigravity-usage/v1', 'run_id': run_id,
            'token_accounting': TOKEN_ACCOUNTING, 'session_id': stream['session_id'],
            'sessions': list(sessions.values()), 'all_agent_total_tokens': components['total_tokens'],
            'usage_components': components, 'root_terminal_usage_not_all_agent': stream['result']['usage']}
