#!/usr/bin/env python3
"""依存関係を戻したfixtureを同じLayer 1から推論設定別に診断する。"""
from pathlib import Path
import importlib.util, sys, shutil, subprocess
from types import SimpleNamespace
BASE=Path(__file__).resolve().parents[1]
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
old=module('latent_r1',BASE/'runtime/run_latent_mode_code_r1.py')
runner=module('latent_dependency_executor',BASE/'runtime/run_free_latent_dependency_r2.py')
old.CASE=BASE/'cases/latent-mode-code/r2'
runner.fixture=SimpleNamespace(prepare=old.prepare,grade=old.grade)
if __name__=='__main__':
    campaign=Path(sys.argv[1]).resolve()
    freeze=runner.load(BASE/'registrations/latent-mode-code-source-freeze-r2.json')
    for path,digest in freeze['sha256'].items():
        if runner.sha(old.REPO/path)!=digest:raise ValueError('固定内容不一致: '+path)
    profiles=[runner.load(BASE/f'profiles/free-astra6-{l}-latent-mode-code-n2-r2.json') for l in ['low','medium','high']]
    for p in profiles:
        q=dict(p['runtime']);q.pop('reasoning_effort')
        ref=dict(profiles[0]['runtime']);ref.pop('reasoning_effort')
        if q!=ref:raise ValueError('推論設定以外のruntime差')
        for k in ['evaluation_set_ref','rating_ref','prompt_ref','repetition','budget']:
            if p[k]!=profiles[0][k]:raise ValueError('比較条件差: '+k)
    binding=profiles[0]['runtime']['executable_binding']
    if runner.sha(Path(binding['executable']))!=binding['entrypoint_sha256']:raise ValueError('CLI hash差')
    if subprocess.check_output([binding['executable'],'--version'],text=True).strip()!=binding['version_output']:raise ValueError('CLI版差')
    runner.write(campaign/'execution-preflight.json',{'series':'fixture-r2-reasoning-axis','reference':'same_frozen_layer1','source_freeze_sha256':runner.sha(BASE/'registrations/latent-mode-code-source-freeze-r2.json'),'declared_axis':'runtime.reasoning_effort','non_axis_conditions_equal':True,'historical_comparison':False,'layer4_registration':False,'slots':6,'max_workers':24,'actual_concurrency':1,'python_executable':sys.executable,'python_version':sys.version,'model_catalog_sha256':runner.sha(campaign/'authentication-source/models_cache.json'),'local_qualification':freeze['local_qualification']})
    try:
        for p in profiles:
            for n in [1,2]:
                result=runner.execute(campaign,p,'CRC-A01-CODE',p['runtime']['reasoning_effort']+f'-{n:02}')
                if not result['valid']:raise ValueError('実行不成立のため続行停止')
    finally:(campaign/'authentication-source/auth.json').unlink(missing_ok=True)
