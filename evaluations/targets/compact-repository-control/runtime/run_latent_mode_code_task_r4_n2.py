#!/usr/bin/env python3
"""現状確認と変更結果検証の関係だけを変えたTASKの診断。"""
from pathlib import Path
import importlib.util,os,sys
from types import SimpleNamespace
BASE=Path(__file__).resolve().parents[1]
REPO=BASE.parents[2]
s=importlib.util.spec_from_file_location('task_r4_base',BASE/'runtime/run_latent_mode_code_r2.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);r=m.runner

def main():
 c=Path(sys.argv[1]).resolve();p=r.load(c/'comparison-preflight.json')
 if not p['ready'] or p['slots']!=6:raise ValueError('実行前照合未成立')
 if sys.executable!=p['python_executable'] or sys.version!=p['python_version'] or os.environ['PATH']!=p['inherited_path']:raise ValueError('環境差')
 for rel,h in p['module_sha256'].items():
  if r.sha(REPO/rel)!=h:raise ValueError('実行器差')
 if r.sha(Path(p['baseline_result']))!=p['baseline_sha256']:raise ValueError('基準差')
 if r.sha(Path(p['runtime_binding']['executable']))!=p['runtime_binding']['entrypoint_sha256']:raise ValueError('CLI差')
 case=BASE/'cases/latent-mode-code/r4'
 actual={str(x.relative_to(case/'visible')) for x in (case/'visible').rglob('*') if x.is_file()}
 if actual!=set(p['fixture']):raise ValueError('fixture集合差')
 for rel,v in p['fixture'].items():
  f=case/'visible'/rel
  if r.sha(f)!=v['sha256'] or oct(f.stat().st_mode&0o777)!=v['mode']:raise ValueError('fixture差')
 profiles={}
 for level,v in p['profiles'].items():
  f=Path(v['path'])
  if r.sha(f)!=v['sha256']:raise ValueError('profile差')
  profiles[level]=r.load(f)
  for k in ['evaluation_set_ref','rating_ref','prompt_ref']:
   ref=profiles[level][k]
   if r.sha(REPO/ref['path'])!=ref['sha256']:raise ValueError('参照差')
 r.write(c/'controller-preflight.json',{'ready':True,'comparison_preflight_sha256':r.sha(c/'comparison-preflight.json'),'controller_sha256':r.sha(Path(__file__).resolve()),'new_slots':6,'max_workers':24,'actual_concurrency':1})
 m.old.CASE=case;r.fixture=SimpleNamespace(prepare=m.old.prepare,grade=m.old.grade)
 try:
  for level in ['low','medium','high']:
   for n in [1,2]:
    out=r.execute(c,profiles[level],'CRC-A01-CODE',f'{level}-{n:02}')
    if not out['valid']:raise ValueError('無効runで追加発行停止')
 finally:(c/'authentication-source/auth.json').unlink(missing_ok=True)
if __name__=='__main__':main()
