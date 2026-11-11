#!/usr/bin/env python3
"""保存された完全出力からコマンド証拠を復元し、原記録を残して追記する。"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.antigravity_evidence import COMMAND_EVIDENCE_SCHEMA_VERSION, TOKEN_ACCOUNTING, parse_stream
from scripts.antigravity_saved_evidence import collect_saved_usage
from scripts.run_antigravity_evaluation import preserve_sessions
from scripts.all_agent_command_evidence import command_requirement_statuses
from scripts.evaluation_loop import load_json, write_json_once
from scripts.run_codex_evaluation import command_protocol_for_case
from scripts.storage_copy import materialize_tree
from layer2.extensions.long_run_storage.batch_archive import tree_snapshot

HEADER = r"(?:Created At: [^\n]+\nCompleted At: [^\n]+\n){1,2}"
EXIT = re.compile(r"\A" + HEADER + r"Command exited with code (-?\d+)\.\n")
TRUNCATED = re.compile(r"\A" + HEADER + r"The tool's output was truncated due to being too long\. You can find the full output in a file at (file://[^\n]+)\.\n")


class RecollectionError(ValueError):
    pass


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require_runtime_surface(parsed, runtime):
    expected_tools = runtime.get('tools')
    observed = parsed['init']
    if (not isinstance(expected_tools, list)
            or observed.get('tools') != expected_tools
            or observed.get('permission_mode') != 'always-proceed'):
        raise RecollectionError('元の実行のツール・権限が固定条件と一致しません')


def recollect_commands(usage, run_id, output_directory):
    attempted, successful, failed, violations, sources = [], [], [], [], []
    for session in usage['sessions']:
        sid = session['session_id']
        # original adapterがSQLiteの同じstep番号から取得した呼び出しだけを使う。
        config = Path(session['database']).parent.parent
        for call in session['commands']:
            if call['name'] != 'run_command':
                continue
            output = call['output']
            match = TRUNCATED.match(output)
            if match:
                expected = config / 'brain' / sid / '.system_generated/steps' / str(call['step_index']) / 'output.txt'
                if match[1] != expected.as_uri() or expected.is_symlink() or not expected.is_file():
                    raise RecollectionError('省略出力の参照先が会話・ステップと一致しません')
                data = expected.read_bytes()
                complete = data.decode('utf-8')
                # 別の時刻の記録や、モデルが作った任意ファイルへの差し替えを拒否する。
                prefix = re.match(r'\A(Created At: [^\n]+\nCompleted At: [^\n]+\n)', output)[1]
                if not complete.startswith(prefix):
                    raise RecollectionError('完全出力の実行時刻が省略記録と一致しません')
                destination = output_directory / sid / f"{call['step_index']}.txt"
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open('xb') as handle:
                    handle.write(data)
                destination.chmod(0o600)
                sources.append({'source': str(expected), 'sha256': hashlib.sha256(data).hexdigest(),
                                'session_id': sid, 'step_index': call['step_index']})
                output = complete
            base = {'actor': 'root' if sid == usage['session_id'] else 'subagent', 'agent_id': sid,
                    'tool_use_id': call['tool_use_id'], 'source': 'antigravity_database_and_transcript',
                    'command': call['parameters']['CommandLine']}
            attempted.append(base)
            match = EXIT.match(output)
            if match:
                code = int(match[1])
                (successful if code == 0 else failed).append({**base, 'exit_code': code})
            else:
                violations.append({**base, 'reason_code': 'missing_machine_bound_exit_code'})
    result = {'schema_version': COMMAND_EVIDENCE_SCHEMA_VERSION, 'run_id': run_id,
              'session_id': usage['session_id'], 'session_count': len(usage['sessions']),
              'attempted_commands': attempted, 'attempted_command_count': len(attempted),
              'successful_commands': successful, 'successful_command_count': len(successful),
              'failed_commands': failed, 'failed_command_count': len(failed),
              'protocol_violations': violations, 'protocol_violation_count': len(violations)}
    return result, sources


def recover(cycle, source_id):
    source_evidence = cycle / 'layer2/evidence' / source_id
    source_extension = cycle / 'layer2/extensions' / source_id
    binding_path = cycle / 'layer2/bindings' / f'{source_id}.json'
    binding = load_json(binding_path)
    old_execution = load_json(source_evidence / 'execution.json')
    exclusion = load_json(source_evidence / 'exclusion.json')
    adapter = load_json(source_extension / 'antigravity-adapter/execution.json')
    if (binding['status'] != 'excluded' or old_execution['status'] != 'excluded'
            or exclusion['reason_code'] not in {'command_evidence_incomplete', 'antigravity_measurement_incomplete'}
            or adapter['antigravity_exit_code'] != 0 or adapter['terminal'] != 'SUCCESS'):
        raise RecollectionError('対象はコマンド証拠の計測失敗に限ります')
    # 同じ発行済みスロットから二つの有効サンプルを作らない。
    for path in (cycle / 'layer2/bindings').glob('*.json'):
        item = load_json(path)
        if item.get('status') == 'valid' and item.get('sample_id') == binding.get('sample_id'):
            raise RecollectionError('同じサンプルには有効な記録が既にあります')
    conditions = binding['comparison_conditions']
    config = Path(conditions['agent_environment']['antigravity_cli']['config_dir'])
    parsed = parse_stream((source_extension / 'antigravity-adapter/stream.jsonl').read_bytes())
    require_runtime_surface(parsed, conditions['agent_environment']['antigravity_cli'])
    usage = collect_saved_usage(parsed, config, conditions['model'], source_id)
    if usage['token_accounting'] != TOKEN_ACCOUNTING:
        raise RecollectionError('計数方法が一致しません')
    original = tree_snapshot(source_evidence), tree_snapshot(source_extension), digest(binding_path)
    new_id = uuid.uuid4().hex
    with tempfile.TemporaryDirectory(prefix='.recollection-', dir=cycle) as temporary:
        staging = Path(temporary)
        commands, sources = recollect_commands(usage, new_id, staging / 'complete-outputs')
        (staging / 'complete-outputs').mkdir(exist_ok=True)
        capsule = load_json(cycle / 'layer2/capsules' / f'{source_id}.json')
        _, groups = command_protocol_for_case(binding['comparison_conditions']['executor_parameters']['command_evidence_protocol'], binding['case_id'])
        requirements = command_requirement_statuses(commands, groups)
        if any(r['status'] == 'evidence_incomplete' for r in requirements):
            raise RecollectionError('完全出力からも必須コマンドの終了状態を確定できません')
        evidence, extension = staging / 'evidence', staging / 'extension'
        if materialize_tree(source_evidence, evidence) != 'clonefile' or materialize_tree(source_extension, extension) != 'clonefile':
            raise RecollectionError('復元用の作業コピーにはclonefileが必要です')
        replacements = [evidence / 'execution.json', extension / 'all-agent-command-evidence/evidence.json',
                        extension / 'all-agent-usage/usage.json', extension / 'command-protocol-audit/audit.json',
                        extension / 'antigravity-adapter/execution.json']
        for path in replacements:
            if path.exists():
                path.unlink()
        (evidence / 'exclusion.json').unlink()
        execution = {**old_execution, 'run_id': new_id, 'status': 'valid', 'exit_code': 0,
                     'total_tokens': usage['all_agent_total_tokens'], 'token_accounting': TOKEN_ACCOUNTING,
                     'source_run_id': source_id, 'evidence_reconstruction': 'saved_complete_tool_output'}
        write_json_once(evidence / 'execution.json', execution)
        write_json_once(extension / 'all-agent-command-evidence/evidence.json', commands)
        write_json_once(extension / 'all-agent-usage/usage.json', {**usage, 'run_id': new_id})
        sessions_path = extension / 'antigravity-adapter/sessions'
        if not sessions_path.exists():
            preserve_sessions(usage, extension / 'antigravity-adapter')
        write_json_once(extension / 'command-protocol-audit/audit.json', {
            'schema_version': 'the-caption-prompt.command-protocol-audit/v1', 'run_id': new_id, 'requirements': requirements})
        write_json_once(extension / 'antigravity-adapter/execution.json', {**adapter, 'external_failure': None, 'source_run_id': source_id})
        write_json_once(evidence / 'usage.json', {'schema_version': 'the-caption-prompt.token-usage/v3',
            'token_accounting': TOKEN_ACCOUNTING, 'total_tokens': usage['all_agent_total_tokens'], 'usage_components': usage['usage_components']})
        recovery = extension / 'command-evidence-recollection'
        recovery.mkdir()
        shutil.move(staging / 'complete-outputs', recovery / 'complete-outputs')
        receipt = {'schema_version': 'the-caption-prompt.command-evidence-recollection/v1',
                   'source_run_id': source_id, 'recovered_run_id': new_id, 'model_invocations': 0,
                   'source_execution_sha256': digest(source_evidence / 'execution.json'),
                   'source_binding_sha256': digest(binding_path), 'collector_sha256': digest(__file__),
                   'source_stream_sha256': digest(source_extension / 'antigravity-adapter/stream.jsonl'),
                   'saved_usage_collector_sha256': digest(ROOT / 'scripts/antigravity_saved_evidence.py'),
                   'complete_outputs': sources, 'elapsed_seconds_preserved': old_execution['elapsed_seconds'],
                   'source_status_preserved': 'excluded'}
        write_json_once(recovery / 'receipt.json', receipt)
        if original != (tree_snapshot(source_evidence), tree_snapshot(source_extension), digest(binding_path)):
            raise RecollectionError('元の記録が変化しています')
        staged_capsule = staging / 'capsule.json'
        staged_binding = staging / 'binding.json'
        write_json_once(staged_capsule, capsule)
        write_json_once(staged_binding, {**binding, 'run_id': new_id, 'status': 'valid', 'source_run_id': source_id})
        destinations = [cycle / 'layer2' / name / (new_id + suffix)
                        for name, suffix in [('evidence', ''), ('extensions', ''), ('capsules', '.json'), ('bindings', '.json')]]
        if any(path.exists() or path.is_symlink() for path in destinations):
            raise RecollectionError('追記先が既に存在します')
        published = []
        try:
            destination = cycle / 'layer2/evidence' / new_id
            evidence.rename(destination)
            published.append(destination)
            destination = cycle / 'layer2/extensions' / new_id
            extension.rename(destination)
            published.append(destination)
            destination = cycle / 'layer2/capsules' / f'{new_id}.json'
            os.link(staged_capsule, destination)
            published.append(destination)
            # 完成した識別記録を最後に一度だけ公開し、部分的なJSONを残さない。
            os.link(staged_binding, cycle / 'layer2/bindings' / f'{new_id}.json')
        except BaseException:
            # 今回追加した未公開の記録だけを戻し、元の実行記録は保持する。
            for destination in reversed(published):
                if destination.is_dir():
                    shutil.rmtree(destination)
                else:
                    destination.unlink()
            raise
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cycle', required=True, type=Path)
    args = parser.parse_args()
    os.environ['THE_CAPTION_EVAL_COPY_MODE'] = 'clonefile'
    recovered, errors = [], []
    for path in sorted((args.cycle / 'layer2/bindings').glob('*.json')):
        binding = load_json(path)
        if binding['status'] != 'excluded':
            continue
        try:
            recovered.append(recover(args.cycle, binding['run_id']))
        except RecollectionError as exc:
            errors.append({'run_id': binding['run_id'], 'reason': str(exc)})
    print(json.dumps({'recovered': len(recovered), 'model_invocations': 0, 'unrecovered': errors}, ensure_ascii=False))
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
