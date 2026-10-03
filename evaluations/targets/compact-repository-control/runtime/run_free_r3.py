#!/usr/bin/env python3
"""固定した小規模Free試験を、個別の指示環境と全担当usageで実行する。"""
import ast
import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[2]
sys.path.insert(0, str(REPO))
from scripts.all_agent_usage import collect_workspace_usage, parse_root_thread_id
from scripts.all_agent_command_evidence import collect as collect_commands

spec = importlib.util.spec_from_file_location('compact_fixture_r2', BASE / 'runtime/fixture_tool_r3.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


def load(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def preflight(campaign):
    profile_path = BASE / 'profiles/free-sol61-low-n1-r3.json'
    profile = load(profile_path)
    fixture.verify_sources()
    runtime = profile['runtime']['executable_binding']
    executable = Path(runtime['executable'])
    if not executable.is_absolute() or sha(executable) != runtime['entrypoint_sha256']:
        raise ValueError('固定CLIの内容が不一致')
    if subprocess.check_output([str(executable), '--version'], text=True).strip() != runtime['version_output']:
        raise ValueError('固定CLIの版が不一致')
    for reference in ['evaluation_set_ref', 'rating_ref', 'prompt_ref']:
        value = profile[reference]
        if sha(REPO / value['path']) != value['sha256']:
            raise ValueError('固定アーティファクトが不一致')
    if profile['runtime']['max_workers'] != 24:
        raise ValueError('並列上限が不一致')
    paths = [Path(__file__).resolve(), BASE / 'runtime/fixture_tool_r3.py', REPO / 'scripts/all_agent_usage.py', REPO / 'scripts/all_agent_command_evidence.py']
    receipt = {'kind': 'qualification_execution_preflight', 'profile_sha256': sha(profile_path),
               'source_registration_sha256': sha(BASE / 'registrations/source-freeze-r3.json'),
               'module_sha256': {str(p.relative_to(REPO)): sha(p) for p in paths},
               'runtime_binding': runtime, 'python_executable': sys.executable, 'python_version': sys.version,
               'max_workers': 24, 'qualification_slots': 2, 'selected_n1_slots': 20,
               'historical_result_reuse': False, 'comparison_requested': False,
               'isolation': 'per_run_empty_home_auth_only_fixed_model_catalog',
               'created_at': datetime.now(timezone.utc).isoformat()}
    target = campaign / 'execution-preflight.json'
    if target.exists():
        old = load(target)
        for key in ['profile_sha256', 'source_registration_sha256', 'module_sha256', 'runtime_binding', 'python_executable', 'python_version']:
            if old[key] != receipt[key]:
                raise ValueError('実行前記録から条件が変化した')
    else:
        write(target, receipt)
    return profile


def parse_usage(data):
    items = [json.loads(line) for line in data.splitlines() if line.strip()]
    completed = [x['usage'] for x in items if x.get('type') == 'turn.completed' and isinstance(x.get('usage'), dict)]
    if not completed:
        raise ValueError('最終usageなし')
    value = completed[-1]
    return value.get('total_tokens', value['input_tokens'] + value['output_tokens']), items


def validation_evidence(items, usage):
    evidence = {'validation_execution': []}
    def is_verification(command):
        direct = re.search(r"\bpython(?:3(?:\.\d+)?)?\b[ \t]+(?:['\"])?(?:\./)?verify\.py(?:['\"])?(?:[ \t]|$|['\"])", command)
        if direct:
            return True
        match = re.search(r"<<['\"]?(?P<tag>\w+)['\"]?\n(?P<code>.*?)\n(?P=tag)", command, re.S)
        if not match:
            return False
        try:
            tree = ast.parse(match['code'])
        except SyntaxError:
            return False
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if not isinstance(node.func.value, ast.Name) or node.func.value.id != 'subprocess':
                continue
            if node.func.attr != 'run' or not node.args:
                continue
            try:
                argv = ast.literal_eval(node.args[0])
            except (ValueError, TypeError):
                continue
            checked = any(k.arg == 'check' and isinstance(k.value, ast.Constant) and k.value.value is True for k in node.keywords)
            if isinstance(argv, list) and len(argv) == 2 and re.fullmatch(r'python(?:3(?:\.\d+)?)?', argv[0]) and argv[1] in ['verify.py', './verify.py'] and checked:
                return True
        return False
    def add(command, code, output):
        if code != 0 or not is_verification(command):
            return
        decoder = json.JSONDecoder()
        values = []
        for match in re.finditer(r'\{', output):
            try:
                obj, _ = decoder.raw_decode(output[match.start():])
                values.append(obj)
            except ValueError:
                continue
        for obj in values:
            if isinstance(obj, dict) and set(obj) == {'sha256', 'passed'}:
                evidence['validation_execution'].append({'exit_code': code, 'result': obj, 'source': 'machine_command_completion'})
    for item in items:
        obj = item.get('item', {})
        if item.get('type') == 'item.completed' and obj.get('type') == 'command_execution':
            add(obj.get('command', ''), obj.get('exit_code'), obj.get('aggregated_output', ''))
    evidence['session_count'] = usage['session_count']
    return evidence


def execute(campaign, profile, cid, label):
    directory = campaign / 'runs' / label
    result_path = directory / 'run.json'
    if result_path.exists():
        return load(result_path)
    if directory.exists():
        raise ValueError('途中実行の上書き・自動再実行は禁止: ' + label)
    directory.mkdir(parents=True)
    workspace = directory / 'workspace'
    fixture.prepare(cid, workspace)
    home = directory / 'codex-home'
    home.mkdir(mode=0o700)
    for name in ['auth.json', 'models_cache.json']:
        shutil.copy2(campaign / 'authentication-source' / name, home / name)
        (home / name).chmod(0o600)
    (home / 'config.toml').write_text('')
    ancestor_instructions = []
    for parent in workspace.parents:
        for name in ['AGENTS.md', 'AGENTS.override.md']:
            if (parent / name).exists():
                ancestor_instructions.append(str(parent / name))
    if ancestor_instructions:
        raise ValueError('作業ディレクトリ上位に指示ファイルがある')
    write(directory / 'instruction-isolation-before.json', {
        'root_agents_bytes': (workspace / 'AGENTS.md').stat().st_size,
        'home_instruction_files': [], 'user_config_bytes': 0, 'ancestor_instruction_files': [],
        'authentication': 'auth_only', 'model_catalog_sha256': sha(home / 'models_cache.json')})
    r = profile['runtime']
    command = [r['executable_binding']['executable'], 'exec', '--ignore-user-config', '--ignore-rules', '--strict-config',
               '--enable', 'multi_agent', '--disable', 'memories', '--disable', 'apps', '--disable', 'plugins',
               '--disable', 'plugin_sharing', '-c', 'agents.max_threads=4', '-c', 'approval_policy="never"',
               '-m', r['model'], '-c', 'model_reasoning_effort="low"', '-s', 'workspace-write',
               '--skip-git-repo-check', '--json', '--output-last-message', str(directory / 'final.txt'), '-']
    env = os.environ.copy()
    env['CODEX_HOME'] = str(home)
    for name in ['OPENAI_API_KEY', 'CODEX_THREAD_ID', 'CODEX_SESSION_ID']:
        env.pop(name, None)
    task = (workspace / 'TASK.md').read_bytes()
    write(directory / 'launch.json', {'argv': command, 'task_sha256': hashlib.sha256(task).hexdigest(),
                                      'case_id': cid, 'label': label, 'profile_id': profile['profile_id']})
    started = time.perf_counter()
    try:
        proc = subprocess.run(command, cwd=workspace, input=task, capture_output=True, env=env, timeout=600)
    except subprocess.TimeoutExpired as error:
        (directory / 'events.jsonl').write_bytes(error.stdout or b'')
        (directory / 'stderr.bin').write_bytes(error.stderr or b'')
        result = {'case_id': cid, 'label': label, 'valid': False, 'quality_score': None,
                  'total_tokens': None, 'elapsed_seconds': time.perf_counter() - started, 'reason': 'execution_timeout'}
    else:
        elapsed = time.perf_counter() - started
        (directory / 'events.jsonl').write_bytes(proc.stdout)
        (directory / 'stderr.bin').write_bytes(proc.stderr)
        try:
            if proc.returncode:
                raise ValueError('CLI終了コード: ' + str(proc.returncode))
            tokens, items = parse_usage(proc.stdout)
            usage = collect_workspace_usage(home / 'sessions', workspace, parse_root_thread_id(proc.stdout), tokens)
            usage['run_id'] = label
            write(directory / 'usage.json', usage)
            commands = collect_commands(directory / 'usage.json', directory / 'events.jsonl')
            write(directory / 'command-evidence.json', commands)
            evidence = validation_evidence(items, usage)
            write(directory / 'validation-evidence.json', evidence)
            outcome = fixture.grade(cid, workspace, evidence)
            result = {**outcome, 'label': label, 'total_tokens': usage['all_agent_total_tokens'],
                      'root_total_tokens': usage['root_total_tokens'], 'session_count': usage['session_count'],
                      'elapsed_seconds': elapsed, 'exit_code': proc.returncode}
        except Exception as error:
            result = {'case_id': cid, 'label': label, 'valid': False, 'quality_score': None,
                      'total_tokens': None, 'elapsed_seconds': elapsed, 'reason': str(error)}
    finally:
        (home / 'auth.json').unlink(missing_ok=True)
    write(directory / 'instruction-isolation-after.json', {'user_config_sha256': sha(home / 'config.toml'),
          'user_config_bytes': (home / 'config.toml').stat().st_size, 'auth_removed': not (home / 'auth.json').exists(),
          'home_instruction_files': [p.name for p in home.glob('AGENTS*')]})
    write(result_path, result)
    print(json.dumps({'label': label, 'case': cid, 'valid': result['valid'], 'quality_score': result['quality_score'],
                      'total_tokens': result['total_tokens'], 'elapsed_seconds': round(result['elapsed_seconds'], 3)}, ensure_ascii=False), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['qualify', 'measure'])
    parser.add_argument('campaign', type=Path)
    args = parser.parse_args()
    campaign = args.campaign.resolve()
    profile = preflight(campaign)
    if args.phase == 'qualify':
        first = execute(campaign, profile, 'CRC-01', 'qualification-01')
        if not first['valid']:
            raise ValueError('初回の実行成立確認に失敗。追加発行を停止')
        second = execute(campaign, profile, 'CRC-01', 'qualification-02')
        if not second['valid']:
            raise ValueError('独立反復の実行成立確認に失敗。追加発行を停止')
        write(campaign / 'runtime-qualification.json', {'qualified': True, 'runs': ['qualification-01', 'qualification-02'],
              'identity': profile['prompt_ref'], 'quality_not_an_admission_gate': True, 'reuse_primary': 'qualification-01',
              'all_agent_usage_collector': 'qualified_for_observed_sessions', 'descendant_collection': 'existing_collector_contract'})
    else:
        if not load(campaign / 'runtime-qualification.json')['qualified']:
            raise ValueError('実行系が未確認')
        members = fixture.verify_sources()
        write(campaign / 'n1-dispatch-plan.json', {'max_workers': 24, 'case_ids': members, 'reuse': {'CRC-01': 'qualification-01'},
               'dispatch': [{'case_id': cid, 'label': cid.lower() + '-n1'} for cid in members if cid != 'CRC-01'],
               'profile_sha256': sha(BASE / 'profiles/free-sol61-low-n1-r3.json')})
        selected = [load(campaign / 'runs/qualification-01/run.json')]
        with concurrent.futures.ThreadPoolExecutor(max_workers=24) as pool:
            futures = [pool.submit(execute, campaign, profile, cid, cid.lower() + '-n1') for cid in members if cid != 'CRC-01']
            for future in concurrent.futures.as_completed(futures):
                selected.append(future.result())
        selected.sort(key=lambda x: x['case_id'])
        valid = [x for x in selected if x['valid']]
        write(campaign / 'measurement.json', {'kind': 'compact_repository_control_free_n1', 'profile_id': profile['profile_id'],
              'requested_cases': 20, 'valid_cases': len(valid), 'invalid_cases': len(selected) - len(valid), 'runs': selected,
              'total_tokens': sum(x['total_tokens'] for x in valid), 'elapsed_seconds_sum': sum(x['elapsed_seconds'] for x in valid),
              'score4_count': sum(x['quality_score'] == 4 for x in valid), 'score0_count': sum(x['quality_score'] == 0 for x in valid),
              'qualification_only_extra_run': 'qualification-02'})


if __name__ == '__main__':
    main()
