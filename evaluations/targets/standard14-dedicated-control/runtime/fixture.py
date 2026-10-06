"""専用素材の展開と固定。実行器は発行しない。"""
import hashlib, json, os, shutil, subprocess
from pathlib import Path
TARGET=Path(__file__).resolve().parents[1]
BASE=TARGET/'fixture/base'
SHARED=Path('/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/environment/.venv')
IGNORED={'.git','__pycache__','.pytest_cache','node_modules','dist','.venv'}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(root):
    rows={}
    for p in sorted(root.rglob('*')):
        r=p.relative_to(root)
        if any(x in IGNORED for x in r.parts): continue
        if p.is_symlink(): rows[str(r)]={'type':'symlink','target':os.readlink(p),'mode':oct(p.lstat().st_mode&0o777)}
        elif p.is_file(): rows[str(r)]={'type':'file','sha256':sha(p),'bytes':p.stat().st_size,'mode':oct(p.stat().st_mode&0o777)}
    return rows
def git(w,*args): return subprocess.check_output(['git','-C',str(w),*args],text=True).strip()
def commit(w,message):
    git(w,'add','--all')
    env=dict(os.environ,GIT_AUTHOR_DATE='2000-01-01T00:00:00Z',GIT_COMMITTER_DATE='2000-01-01T00:00:00Z',GIT_AUTHOR_NAME='Evaluation',GIT_COMMITTER_NAME='Evaluation',GIT_AUTHOR_EMAIL='evaluation@example.invalid',GIT_COMMITTER_EMAIL='evaluation@example.invalid')
    subprocess.run(['git','-C',str(w),'commit','--allow-empty','-qm',message],check=True,env=env)
    return git(w,'rev-parse','HEAD')
def materialize(case_id, output, reference=False):
    output=Path(output)
    if output.exists(): raise ValueError('既存workspaceへ重ねない')
    shutil.copytree(BASE,output,ignore=shutil.ignore_patterns(*IGNORED))
    git(output,'init','-q'); git(output,'config','core.autocrlf','false')
    base=commit(output,'repository base')
    data=json.loads((TARGET/'cases'/case_id/'r1/private/case-data.json').read_text())
    for path,before,after in data['seed_operations']:
        p=output/path; t=p.read_text(); assert t.count(before)==1; p.write_text(t.replace(before,after))
    seed=commit(output,'repository change')
    # Free配置を独立commitにする。固定月次diffとHEAD^の取り違えを検出可能にする。
    commit(output,'repository authority')
    free=commit(output,'repository start')
    if reference:
        for path,_,_ in data['seed_operations']:
            shutil.copyfile(BASE/path,output/path)
    (output/'.venv').symlink_to(SHARED,target_is_directory=True)
    return {'base_commit':base,'seed_commit':seed,'free_commit':free,'manifest':manifest(output),'git_objects_logical_bytes':sum(p.stat().st_size for p in (output/'.git/objects').rglob('*') if p.is_file()),'git_objects_allocated_bytes':sum(p.stat().st_blocks*512 for p in (output/'.git/objects').rglob('*') if p.is_file())}
def task(case_id,seed_commit):
    raw=(TARGET/'cases'/case_id/'r1/trial-prompt-input.json').read_bytes()
    if case_id=='SD14-12':
        old=b'a53601614b41f52633f1d75e77c72861a0f0f1c8'
        assert old in raw; raw=raw.replace(old,seed_commit.encode())
    return raw
