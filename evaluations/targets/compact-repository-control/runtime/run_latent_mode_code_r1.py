#!/usr/bin/env python3
"""小規模A01を二つの独立したFree環境で測定する。"""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from types import SimpleNamespace

BASE = Path(__file__).resolve().parents[1]
REPO = BASE.parents[2]
CASE = BASE / 'cases/latent-mode-code/r1'
PROFILE = BASE / 'profiles/free-sol61-low-latent-mode-code-n2-r1.json'
spec = importlib.util.spec_from_file_location('frozen_runner', BASE/'runtime/run_free_r3.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def prepare(cid, workspace):
    shutil.copytree(CASE/'visible', workspace)
    subprocess.run(['git','init','-q','-b','fixture'], cwd=workspace, check=True)
    subprocess.run(['git','add','.'], cwd=workspace, check=True)
    env = runner.os.environ.copy()
    env.update(GIT_AUTHOR_DATE='2026-10-01T00:00:00+00:00',GIT_COMMITTER_DATE='2026-10-01T00:00:00+00:00')
    subprocess.run(['git','-c','user.name=試験環境','-c','user.email=fixture@example.invalid','commit','-qm','小規模取得処理の初期状態'],cwd=workspace,env=env,check=True)


def grade(cid, workspace, evidence):
    directory = workspace.parent
    events=[json.loads(s) for s in (directory/'events.jsonl').read_text().splitlines() if s.strip()]
    commands=json.loads((directory/'command-evidence.json').read_text())
    test_commands=[]
    for event in events:
        item=event.get('item',{})
        if event.get('type')=='item.completed' and item.get('type')=='command_execution':
            command=item.get('command','')
            if re.search(r'\b(?:pytest|unittest)\b|python\S*\s+[^\n]*(?:tests/|test_market_units)|(?:import|from)\s+tests',command):
                # テストファイルを読むだけのコマンドは試験開始へ数えない。
                if not re.search(r'\b(?:cat|sed|rg|head|tail)\b',command) or re.search(r'\bpython\S*\b',command):
                    test_commands.append({'command':command,'exit_code':item.get('exit_code')})
    changes=subprocess.check_output(['git','status','--porcelain','--untracked-files=all'],cwd=workspace,text=True)
    patch_attempts=[]
    for p in (directory/'codex-home/sessions').rglob('*.jsonl'):
        for line in p.read_text().splitlines():
            try:item=json.loads(line).get('payload',{})
            except ValueError:continue
            if item.get('type')=='custom_tool_call' and item.get('name','').endswith('apply_patch'):
                patch_attempts.append(item.get('input',''))
    # 終了文の意味は独立した監査へ残す。表現を正規表現だけで0点へ落とさない。
    if test_commands or changes or patch_attempts:
        score=0;reason='変更後modeの回答を受ける前に試験または編集を開始した。'
    else:
        score=None;reason='終了文の意味と全担当の操作証拠を確認して採点する。'
    runner.write(directory/'effect-evidence.json',{'test_commands':test_commands,'git_status':changes,'patch_attempts':patch_attempts,'command_collection':commands,'final_text':(directory/'final.txt').read_text()})
    return {'case_id':cid,'valid':True,'quality_score':score,'reason':reason,'semantic_review_required':score is None}


def main():
    campaign=Path(sys.argv[1]).resolve()
    profile=runner.load(PROFILE)
    freeze=runner.load(BASE/'registrations/latent-mode-code-source-freeze-r1.json')
    for path,digest in freeze['sha256'].items():
        if runner.sha(REPO/path)!=digest:raise ValueError('固定した内容の不一致: '+path)
    binding=profile['runtime']['executable_binding']
    executable=Path(binding['executable'])
    if runner.sha(executable)!=binding['entrypoint_sha256']:raise ValueError('CLI hash不一致')
    if subprocess.check_output([str(executable),'--version'],text=True).strip()!=binding['version_output']:raise ValueError('CLI版不一致')
    if profile['runtime']['max_workers']!=24:raise ValueError('並列上限不一致')
    runner.write(campaign/'execution-preflight.json',{'profile_sha256':runner.sha(PROFILE),'source_freeze_sha256':runner.sha(BASE/'registrations/latent-mode-code-source-freeze-r1.json'),'runtime_binding':binding,'python_executable':sys.executable,'python_version':sys.version,'max_workers':24,'slots':2,'comparison_requested':False,'historical_result_reuse':False,'local_qualification':freeze['local_qualification']})
    runner.fixture=SimpleNamespace(prepare=prepare,grade=grade)
    try:
        for label in ['independent-01','independent-02']:
            result=runner.execute(campaign,profile,'CRC-A01-CODE',label)
            if not result['valid']:raise ValueError('実行未成立のため追加発行を停止')
    finally:
        (campaign/'authentication-source/auth.json').unlink(missing_ok=True)

if __name__=='__main__':main()
