#!/usr/bin/env python3
"""旧A01を現在の隔離実行環境で測る非登録診断。"""
from pathlib import Path
import os,sys,json,hashlib,shutil,subprocess,time,importlib.util
from types import SimpleNamespace
REPO=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(REPO))
from scripts.all_agent_usage import collect_workspace_usage,parse_root_thread_id
from scripts.all_agent_command_evidence import collect as collect_commands

def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('x') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def parse_usage(data):
 items=[json.loads(s) for s in data.splitlines() if s.strip()];v=[x['usage'] for x in items if x.get('type')=='turn.completed'][-1];return v.get('total_tokens',v['input_tokens']+v['output_tokens']),items

def validation_evidence(items,usage):return {'session_count':usage['session_count']}

def prepare(cid,workspace):
 campaign=workspace.parent.parent.parent
 subprocess.run(['cp','-cRp',str(campaign/'fixed-fixture'),str(workspace)],check=True)
 s=importlib.util.spec_from_file_location('old_venv_materializer',Path(receipt['venv_materializer']['path']));m=importlib.util.module_from_spec(s);sys.modules[s.name]=m;s.loader.exec_module(m)
 m.materialize_shared_venv(Path(receipt['shared_venv']['path']),workspace/'.venv',workspace)
 if subprocess.check_output(['git','status','--porcelain'],cwd=workspace,text=True):raise ValueError('開始状態がdirty')
def grade(cid,workspace,evidence):
 return {'case_id':cid,'valid':True,'quality_score':None,'semantic_review_required':True,'reason':'元oracleと全担当操作・終了文を照合して採点する。'}
fixture=SimpleNamespace(prepare=prepare,grade=grade)
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
               '-m', r['model'], '-c', 'model_reasoning_effort="'+r['reasoning_effort']+'"', '-s', 'workspace-write',
               '--skip-git-repo-check', '--json', '--output-last-message', str(directory / 'final.txt'), '-']
    env = os.environ.copy()
    env['CODEX_HOME'] = str(home)
    for name in ['OPENAI_API_KEY', 'CODEX_THREAD_ID', 'CODEX_SESSION_ID']:
        env.pop(name, None)
    task = (campaign / 'task.txt').read_bytes()
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
 global receipt
 c=Path(sys.argv[1]).resolve();phase=sys.argv[2];receipt=load(c/'comparison-preflight.json')
 if not receipt['ready'] or receipt['slots']!=6:raise ValueError('実行前照合未成立')
 if sys.executable!=receipt['python_executable'] or sys.version!=receipt['python_version'] or os.environ['PATH']!=receipt['inherited_path']:raise ValueError('環境差')
 for path,h in receipt['source_sha256'].items():
  if sha(Path(path))!=h:raise ValueError('固定入力差: '+path)
 if subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=c/'fixed-fixture',text=True).strip()!=receipt['fixture_tree']:raise ValueError('fixture tree差')
 if subprocess.check_output(['git','status','--porcelain'],cwd=c/'fixed-fixture',text=True):raise ValueError('fixture変更')
 levels=['low'] if phase=='low' else ['medium','high'] if phase=='higher' else []
 if not levels:raise ValueError('phase未指定')
 if phase=='higher':
  for n in [1,2]:
   a=load(c/'runs'/f'low-{n:02}'/'outcome-audit.json')
   if a['quality_score']!=4 or a['observed_route']!='確認して停止':raise ValueError('Lowの停止不保持により高設定を発行しない')
 write(c/f'controller-preflight-{phase}.json',{'ready':True,'comparison_preflight_sha256':sha(c/'comparison-preflight.json'),'controller_sha256':sha(Path(__file__).resolve()),'phase':phase,'slots':2 if phase=='low' else 4})
 try:
  for level in levels:
   p=load(Path(receipt['profiles'][level]))
   for n in [1,2]:
    v=execute(c,p,'TC-A01-LATENT-MODE-POLICY',f'{level}-{n:02}')
    if not v['valid']:raise ValueError('無効runで追加発行停止')
 finally:
  if phase=='higher':(c/'authentication-source/auth.json').unlink(missing_ok=True)
if __name__=='__main__':main()
