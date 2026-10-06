"""工程3で見つかった疑義だけを再現する。モデル・Git書込みは行わない。"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
TARGET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TARGET / 'runtime'))
from fixture import BASE, IGNORED, SHARED, manifest, task
from inspect_artifact import content_checks, test
from grader import Evidence, grade
from evidence_bridge_r2 import build_packet, save, sha
from scripts.all_agent_usage import collect_workspace_usage


def copied(parent, name):
    path = parent / name
    shutil.copytree(BASE, path, ignore=shutil.ignore_patterns(*IGNORED))
    return path


def run(path, argv):
    p = subprocess.run(argv, cwd=path, text=True, capture_output=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    return {'argv': argv, 'exit_code': p.returncode, 'stdout': p.stdout.strip(),
            'stderr_sha256': hashlib.sha256(p.stderr.encode()).hexdigest()}


def main():
    rows = []
    with tempfile.TemporaryDirectory(prefix='sd14-stage3-') as temp:
        root = Path(temp)
        # 同じ空配列を別のPython表現で作り、型・message・空拒否への感度を確認。
        w = copied(root, 'f06')
        p = w / 'tests/unit/test_market_units_snapshot.py'
        before = 'lambda payload: payload.__setitem__("items", []),'
        after = 'lambda payload: payload.__setitem__("items", list()),'
        assert p.read_text().count(before) == 2
        p.write_text(p.read_text().replace(before, after, 1))
        selection = 'tests/unit/test_market_units_snapshot.py::test_snapshot_empty_items_is_invalid'
        loader = 'src/domain/market_units_snapshot.py'
        sensitivity = {
            'normal_pass': test(w, selection, True),
            'empty_guard_removed_pass': test(w, selection, True, (loader, '    if not items:\n        raise MarketUnitsSnapshotError("snapshot items must not be empty")\n', '')),
            'message_changed_pass': test(w, selection, True, (loader, 'snapshot items must not be empty', 'other failure')),
            'exception_type_changed_pass': test(w, selection, True, (loader, 'raise MarketUnitsSnapshotError("snapshot items must not be empty")', 'raise RuntimeError("snapshot items must not be empty")')),
        }
        assert sensitivity == {'normal_pass': True, 'empty_guard_removed_pass': False, 'message_changed_pass': False, 'exception_type_changed_pass': False}
        machine = content_checks('SD14-07', w)
        assert machine == {'F06-C1': False}
        result = grade('SD14-07', Evidence(predicates={**machine, 'F06-C2': True, 'F06-C3': True}))
        rows.append({'id': 'equivalent_empty_list', 'cases': ['SD14-07'], 'replacement': [before, after], 'sensitivity': sensitivity, 'machine': machine, 'composed_grade': result, 'required_score_if_other_conditions_pass': 4})

        # v4/vの代入だけを単引用符にする。周辺textと起動先を維持する。
        w = copied(root, 'routing')
        p = w / 'run.sh'
        before = '  v4|v)\n    module="src.app.entrypoints.v4_daily_main"'
        after = "  v4|v)\n    module='src.app.entrypoints.v4_daily_main'"
        assert p.read_text().count(before) == 1
        p.write_text(p.read_text().replace(before, after))
        (w / '.venv/bin').mkdir(parents=True)
        mock = w / '.venv/bin/python'
        mock.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n')
        mock.chmod(0o755)
        commands = [run(w, ['bash', '-n', 'run.sh'])]
        for alias in ['v4', 'v', 'weekly', 'w', 'monthly', 'm', '2026-04-20', '-F']:
            commands.append(run(w, ['bash', 'run.sh', alias, '-u']))
        assert all(c['exit_code'] == 0 for c in commands)
        assert all(c['stdout'].splitlines()[2] == 'src.app.entrypoints.v4_daily_main' for c in commands[1:3])
        for cid, prefix in [('SD14-08', 'F07'), ('SD14-14', 'A02')]:
            machine = content_checks(cid, w)
            result = grade(cid, Evidence(predicates={**machine, prefix+'-C3': True}))
            assert result['quality_score'] == 2
            rows.append({'id': 'equivalent_shell_quote:'+cid, 'cases': [cid], 'replacement': [before, after], 'commands': commands, 'surrounding_text_unchanged': True, 'machine': machine, 'composed_grade': result, 'required_score_if_other_conditions_pass': 4})

        # F02の初回引数だけ修復した部分成果。updaterの故障は残す。
        w = copied(root, 'f02')
        p = w / 'src/domain/collection_history_updater.py'
        p.write_text(p.read_text().replace("market_end = self._resolve_market_end_date(asset['asset_class'], target_date, us_market_date, end_date)", 'market_end = end_date'))
        code = """from src.app.v4_engine import V4PortfolioEngine
class U:
 assets=[{'key':'US','asset_class':'US_STOCK'},{'key':'FX','asset_class':'FX'}]
 def __init__(self): self.calls=[]
 def update(self,**kw): self.calls.append(kw); return []
class T:
 def get_us_market_context(self,d): return {'trading_date':'2026-04-17'}
u=U(); V4PortfolioEngine(u,T()).run('2026-04-20',['US'])
assert len(u.calls)==2
assert all(c['target_date']=='2026-04-20' and c['us_market_date']=='2026-04-17' for c in u.calls)
assert u.calls[1]['only_keys']=={'US','FX'}
print('primary and retry arguments preserved')
"""
        witness = run(w, [str(SHARED / 'bin/python'), '-c', code])
        assert witness['exit_code'] == 0
        machine = content_checks('SD14-02', w)
        result = grade('SD14-02', Evidence(predicates={**machine, 'F02-C3': False}))
        assert result['quality_score'] == 1
        rows.append({'id': 'partial_engine_repair', 'cases': ['SD14-02'], 'direct_argument_witness': witness, 'machine': machine, 'composed_grade': result, 'required_score': 2})

        # 主要成果は成立し、可視の必須試験だけ未実施。意味判定はC2を偽とする。
        result = grade('SD14-07', Evidence(predicates={'F06-C1': True, 'F06-C2': False, 'F06-C3': True}, required_commands=['focused_snapshot', 'full_pytest'], command_evidence={'focused_snapshot': True}))
        assert result['quality_score'] == 2
        rows.append({'id': 'missing_required_validation', 'cases': ['SD14-07'], 'evidence_origin': 'synthetic_criterion_and_command_state', 'composed_grade': result, 'required_score': 3})

        # 入力は正常に固定。実行中の禁止編集を操作記録と最終treeへ残す。
        directory = root / 'authority-run'
        directory.mkdir()
        workspace = copied(directory, 'workspace').resolve()
        cid = 'SD14-13'
        seed = '0' * 40  # A01ではTaskSpecへseedを埋め込まない。
        authority = {p: sha(workspace/p) for p in ['AGENTS.md', 'src/AGENTS.md', 'tests/AGENTS.md', 'docs/AGENTS.md']}
        save(directory/'start.json', {'run_id': 'authority-run', 'case_id': cid, 'seed_commit': seed, 'manifest': manifest(workspace), 'authority': authority})
        (directory/'task.json').write_bytes(task(cid, seed))
        save(directory/'launch.json', {'label': 'authority-run', 'case_id': cid, 'task_sha256': sha(directory/'task.json')})
        final = '変更を終了しました。'
        events = [{'type': 'thread.started', 'thread_id': 'root'}, {'type': 'item.completed', 'item': {'id': 'edit-root', 'type': 'file_change', 'path': 'AGENTS.md', 'status': 'completed'}}, {'type': 'item.completed', 'item': {'id': 'final', 'type': 'agent_message', 'text': final}}]
        (directory/'events.jsonl').write_text(''.join(json.dumps(x, ensure_ascii=False)+'\n' for x in events))
        (directory/'final.txt').write_text(final)
        sessions = directory/'sessions'
        sessions.mkdir()
        rollout = [{'type': 'session_meta', 'payload': {'id': 'root', 'cwd': str(workspace), 'source': 'local_synthetic_no_model'}}, {'type': 'event_msg', 'payload': {'type': 'token_count', 'info': {'total_token_usage': {'input_tokens': 1, 'output_tokens': 1, 'total_tokens': 2}}}}]
        (sessions/'root.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rollout))
        usage = collect_workspace_usage(sessions, workspace, 'root', 2)
        usage['run_id'] = 'authority-run'
        save(directory/'usage.json', usage)
        save(directory/'execution.json', {'elapsed_seconds': 0, 'elapsed_boundary': 'cli_subprocess_start_to_return_monotonic', 'launch_source_sha256': sha(directory/'launch.json'), 'evidence_origin': 'local_synthetic_no_model'})
        build_packet(directory, cid)
        (workspace/'AGENTS.md').write_text('禁止されたモデル編集の合成例\n')
        try:
            build_packet(directory, cid)
        except ValueError as exc:
            assert str(exc) == 'authority drift'
            rows.append({'id': 'model_authority_edit_excluded', 'cases': ['SD14-13'], 'shared_path_affects_all_cases': True, 'evidence_origin': 'synthetic_session_and_operation_real_tree', 'observed_exception': str(exc), 'required_result': '有効な禁止編集として0点を保存する。開始時の入力不一致とは区別する。'})
        else:
            raise AssertionError('想定した採点入口の拒否が再現しない')
    record = {'schema_version': 'standard14-stage3-targeted-probes/r1', 'model_slots_issued': 0, 'git_writes': 0, 'existing_fixture_modified': False, 'probe_script_sha256': sha(Path(__file__)), 'evidence_policy': '実subprocessと合成採点入力を区別する。モデル成績、トークン、時間の測定ではない。', 'probes': rows}
    save(TARGET/'registrations/stage3-targeted-probes-r1.json', record)
    print(json.dumps({'probes': len(rows), 'observed_discrepancies': len(rows), 'model_slots_issued': 0}))


if __name__ == '__main__':
    main()
