#!/usr/bin/env python3
"""旧A01の判断入力を保持したPNGだけの疎な投影を確認する。"""
from pathlib import Path
import sys,os,json,importlib.util,subprocess
REPO=Path(__file__).resolve().parents[4]
def load(p):return json.loads(p.read_text())
def main():
 c=Path(sys.argv[1]).resolve();r=load(c/'comparison-preflight.json')
 s=importlib.util.spec_from_file_location('fixed_original_executor',REPO/'evaluations/targets/the-caption/runtime/run_old_a01_current_environment_n2_r1.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.receipt=r
 assert r['ready'] and r['slots']==2 and sys.executable==r['python_executable'] and sys.version==r['python_version']
 os.environ['PATH']=r['inherited_path']
 for path,h in r['source_sha256'].items():assert m.sha(Path(path))==h,path
 manifest=load(c/'fixture-manifest.json');w=c/'fixed-fixture'
 for path,v in manifest['preserved_files'].items():
  f=w/path;assert m.sha(f)==v['sha256'] and oct(f.lstat().st_mode&0o777)==v['mode'] and f.is_symlink()==(v['type']=='symlink')
 for path in manifest['removed_files']:assert not (w/path).exists()
 def git(*args):return subprocess.check_output(['git',*args],cwd=w,text=True).strip()
 assert git('rev-parse','HEAD')==manifest['git_start']['head']
 assert git('rev-parse','HEAD^{tree}')==manifest['git_start']['tree']
 assert git('ls-files','--stage')==manifest['git_start']['stage']
 assert git('show-ref')==manifest['git_start']['refs']
 assert not git('status','--porcelain')
 m.write(c/'controller-preflight.json',{'ready':True,'comparison_preflight_sha256':m.sha(c/'comparison-preflight.json'),'preserved_file_count':len(manifest['preserved_files']),'removed_file_count':len(manifest['removed_files']),'slots':2,'actual_concurrency':1})
 p=load(Path(r['profile_path']))
 try:
  for n in [1,2]:
   x=m.execute(c,p,'TC-A01-LATENT-MODE-POLICY',f'low-{n:02}')
   if not x['valid']:raise ValueError('無効runで停止。再試行なし。')
 finally:(c/'authentication-source/auth.json').unlink(missing_ok=True)
if __name__=='__main__':main()
