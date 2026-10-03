#!/usr/bin/env python3
"""小規模版r4の固定Low条件で不足18件だけ追加する。"""
from pathlib import Path
import sys,os,json,importlib.util,concurrent.futures
from types import SimpleNamespace
BASE=Path(__file__).resolve().parents[1];REPO=BASE.parents[2]
def load(p):return json.loads(p.read_text())
def main():
 c=Path(sys.argv[1]).resolve();pf=load(c/'comparison-preflight.json')
 s=importlib.util.spec_from_file_location('r4_fixed_modules',BASE/'runtime/run_latent_mode_code_r2.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);r=m.runner
 assert pf['ready'] and pf['slots']==18
 assert sys.executable==pf['python_executable'] and sys.version==pf['python_version']
 os.environ['PATH']=pf['inherited_path']
 for path,h in pf['source_sha256'].items():assert r.sha(Path(path))==h,path
 for parent in (c/'fixed-case').parents:
  for name in ['AGENTS.md','AGENTS.override.md']:assert not (parent/name).exists()
 profile=load(Path(pf['profile_path']));assert profile['runtime']['reasoning_effort']=='low'
 m.old.CASE=c/'fixed-case';r.fixture=SimpleNamespace(prepare=m.old.prepare,grade=m.old.grade)
 r.write(c/'controller-preflight.json',{'ready':True,'receipt_sha256':r.sha(c/'comparison-preflight.json'),'max_workers':24,'new_slots':18})
 outcomes=[]
 try:
  with concurrent.futures.ThreadPoolExecutor(max_workers=24) as pool:
   fs=[pool.submit(r.execute,c,profile,'CRC-A01-CODE',label) for label in load(c/'dispatch-plan.json')['new_slots']]
   for f in concurrent.futures.as_completed(fs):outcomes.append(f.result())
  r.write(c/'execution-complete.json',{'count':len(outcomes),'outcomes':outcomes,'invalid':sum(not x['valid'] for x in outcomes)})
 finally:(c/'authentication-source/auth.json').unlink(missing_ok=True)
 if any(not x['valid'] for x in outcomes):raise SystemExit('無効runあり。追加発行しない。')
if __name__=='__main__':main()
