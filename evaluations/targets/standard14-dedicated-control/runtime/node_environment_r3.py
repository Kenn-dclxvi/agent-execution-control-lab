"""Node/npmとlock指定cacheを固定し、各実行に同じ初期環境を接続する。"""
import base64, hashlib, json, os, shutil, subprocess, tempfile, time
from pathlib import Path
from fixture import TARGET, BASE, IGNORED, sha
from evidence_bridge_r2 import save
ROOT=TARGET.parents[3]/'standard14-stage2-node-environment-r1'
REG=TARGET/'registrations/node-environment-binding-r3.json'
def inventory(root):
    result={}
    for p in sorted(root.rglob('*')):
        if p.is_symlink(): result[str(p.relative_to(root))]={'symlink':os.readlink(p)}
        elif p.is_file(): result[str(p.relative_to(root))]={'sha256':sha(p),'bytes':p.stat().st_size}
    return result
def environment(run_root):
    record=json.loads(REG.read_text()); frozen=Path(record['frozen_root'])
    if inventory(frozen)!=record['frozen_manifest']: raise ValueError('固定Node環境が変更された')
    closure=json.loads((TARGET/'registrations/node-dynamic-closure-r4.json').read_text())
    if sha(REG)!=closure['binding_sha256']: raise ValueError('Node環境参照が変更された')
    for name,value in closure['dynamic_dependencies'].items():
        if sha(Path(name))!=value: raise ValueError('Node共有ライブラリが変更された')
    run_root=Path(run_root); run_root.mkdir(parents=True,exist_ok=False)
    shutil.copytree(frozen/'cache',run_root/'cache')
    bins=run_root/'bin'; bins.mkdir()
    (bins/'node').symlink_to(frozen/'bin/node')
    # npmのshebangの解決をPATH任せにせず、同じ固定Nodeへ結ぶ。
    npm=bins/'npm'; npm.write_text('#!/bin/sh\nexec "'+str(frozen/'bin/node')+'" "'+str(frozen/'npm/bin/npm-cli.js')+'" "$@"\n'); npm.chmod(0o755)
    return dict(os.environ,PATH=str(bins)+os.pathsep+os.environ['PATH'],npm_config_cache=str(run_root/'cache'),npm_config_offline='true')
def main():
    if ROOT.exists() or REG.exists(): raise ValueError('固定環境・証拠は上書きしない')
    audit=json.loads((TARGET/'registrations/node-environment-audit-r2.json').read_text()); current=audit['current']
    ROOT.mkdir(); (ROOT/'bin').mkdir(); shutil.copy2(current['node_path'],ROOT/'bin/node'); shutil.copytree(Path(current['node_path']).parents[1]/'lib',ROOT/'lib',symlinks=True); shutil.copytree(Path(current['npm_path']).parents[1],ROOT/'npm',symlinks=True)
    cache=ROOT/'cache/_cacache/content-v2/sha512'; cache.mkdir(parents=True)
    for row in audit['cache']['present']:
        h=base64.b64decode(row['integrity'].split('-')[1]).hex(); rel=Path(h[:2])/h[2:4]/h[4:]
        dest=cache/rel; dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists(): shutil.copy2(Path(audit['cache']['root'])/rel,dest)
        if hashlib.sha512(dest.read_bytes()).hexdigest()!=h: raise ValueError('cache integrity mismatch')
    dependencies={}
    for line in subprocess.check_output(['otool','-L',str(Path(current['node_path']).parents[1]/'lib/libnode.147.dylib')],text=True).splitlines()[1:]:
        p=Path(line.strip().split(' (')[0])
        if p.is_file(): dependencies[str(p)]=sha(p)
    lock=json.loads((BASE/'src/web/market_units_editor/package-lock.json').read_text())
    absent=audit['cache']['absent']; applicable=[]
    for row in absent:
        compatible=lambda values,actual: not values or (actual not in [v[1:] for v in values if v.startswith('!')] and (not [v for v in values if not v.startswith('!')] or actual in values))
        if not row['optional'] or (compatible(row['platform'],'darwin') and compatible(row['cpu'],'arm64')): applicable.append(row)
    if applicable: raise ValueError('適用対象依存cacheが不足')
    record={'schema_version':'standard14-node-environment-binding/r3','frozen_root':str(ROOT),'frozen_manifest':inventory(ROOT),'dynamic_dependencies':dependencies,'source_audit_sha256':sha(TARGET/'registrations/node-environment-audit-r2.json'),'source_versions_match_old_receipt':audit['versions_match'],'package_and_lock_match':audit['package_and_lock_match'],'same_binding_for_reasoning':['low','medium','high'],'missing_applicable_dependencies':0,'missing_optional_nonapplicable':len(absent),'historical_execution_identity_proven':False,'model_slots_issued':0,'commands':[]}
    # environment()は固定証拠を読むため、検証開始用に一時記録を使わず同じ照合を直接行う。
    with tempfile.TemporaryDirectory(prefix='sd14-fixed-node-') as tmp:
        tmp=Path(tmp); shutil.copytree(BASE/'src/web/market_units_editor',tmp/'web',ignore=shutil.ignore_patterns(*IGNORED)); shutil.copytree(ROOT/'cache',tmp/'cache'); (tmp/'bin').mkdir(); (tmp/'bin/node').symlink_to(ROOT/'bin/node'); npm=tmp/'bin/npm'; npm.write_text('#!/bin/sh\nexec "'+str(ROOT/'bin/node')+'" "'+str(ROOT/'npm/bin/npm-cli.js')+'" "$@"\n'); npm.chmod(0o755)
        env=dict(os.environ,PATH=str(tmp/'bin')+os.pathsep+os.environ['PATH'],npm_config_cache=str(tmp/'cache'),npm_config_offline='true')
        for args in [['node','--version'],['npm','--version'],['npm','ci','--ignore-scripts','--no-audit','--no-fund','--include=dev'],['npm','run','lint'],['npm','run','build']]:
            begin=time.monotonic(); p=subprocess.run(args,cwd=tmp/'web',env=env,capture_output=True,text=True); record['commands'].append({'argv':args,'exit_code':p.returncode,'elapsed_seconds':time.monotonic()-begin,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()})
            if p.returncode: raise ValueError(p.stderr[-2000:])
    assert inventory(ROOT)==record['frozen_manifest']
    record['all_pass']=True; record['logical_bytes']=sum(v.get('bytes',0) for v in record['frozen_manifest'].values()); save(REG,record)
    print(json.dumps({'frozen_files':len(record['frozen_manifest']),'logical_bytes':record['logical_bytes'],'commands_passed':len(record['commands']),'same_binding_for_reasoning':record['same_binding_for_reasoning'],'model_slots_issued':0}))
if __name__=='__main__': main()
