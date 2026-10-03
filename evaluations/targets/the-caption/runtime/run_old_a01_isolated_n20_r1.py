#!/usr/bin/env python3
"""個人指示を除外した旧A01の固定N20。"""
from pathlib import Path
import sys,os,json,importlib.util,concurrent.futures,hashlib,subprocess
REPO=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(REPO))


def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):
 with p.open('x') as f:f.write(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def main():
 c=Path(sys.argv[1]).resolve();r=load(c/'comparison-preflight.json')
 assert r['ready'] and r['slots']==58
 assert sys.executable==r['python_executable'] and sys.version==r['python_version']
 os.environ['PATH']=r['inherited_path']
 for path,h in r['source_sha256'].items():assert sha(Path(path))==h,path
 assert subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=c/'fixed-fixture',text=True).strip()==r['fixture_tree']
 assert not subprocess.check_output(['git','status','--porcelain'],cwd=c/'fixed-fixture',text=True)
 for parent in (c/'fixed-fixture').parents:
  for name in ['AGENTS.md','AGENTS.override.md']:assert not (parent/name).exists()
 spec=importlib.util.spec_from_file_location('fixed_old_a01_executor',r['executor_source']);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.receipt=r
 write(c/'controller-preflight.json',{'ready':True,'receipt_sha256':sha(c/'comparison-preflight.json'),'slots':58,'max_workers':24})
 plan=load(c/'dispatch-plan.json');profiles={e:load(Path(p)) for e,p in r['profiles'].items()}
 pending=iter(plan['slots']);invalid=False;completed=[]
 try:
  with concurrent.futures.ThreadPoolExecutor(max_workers=24) as pool:
   active={}
   def submit():
    try:s=next(pending)
    except StopIteration:return False
    f=pool.submit(m.execute,c,profiles[s['reasoning_effort']],'TC-A01-LATENT-MODE-POLICY',s['label']);active[f]=s;return True
   for _ in range(24):submit()
   while active:
    done,_=concurrent.futures.wait(active,return_when=concurrent.futures.FIRST_COMPLETED)
    for f in done:
     s=active.pop(f)
     try:v=f.result()
     except Exception as exc:v={'label':s['label'],'valid':False,'reason':str(exc)}
     completed.append(v)
     if not v['valid']:invalid=True
    if not invalid:
     while len(active)<24 and submit():pass
  write(c/'execution-complete.json',{'completed':completed,'invalid':invalid,'count':len(completed)})
 finally:(c/'authentication-source/auth.json').unlink(missing_ok=True)
 if invalid:raise SystemExit('無効runあり。追加発行停止。')
if __name__=='__main__':main()
