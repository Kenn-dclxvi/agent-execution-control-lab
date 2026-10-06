"""旧F04の保存証拠と現環境を照合する。同一性未確認を版一致で補わない。"""
import hashlib,json,os,shutil,subprocess
from pathlib import Path
from fixture import TARGET,BASE,sha
from evidence_bridge_r2 import save
REPO=TARGET.parents[2]
def main():
    old=REPO/'evaluations/cases/TC-F04-WEB-AUDIT-COLUMN-VISIBILITY/r1/private/case-data.json'
    data=json.loads(old.read_text()); receipt=data['qualification']['receipt']
    node=Path(shutil.which('node')).resolve(); npm=Path(shutil.which('npm')).resolve()
    current_node=subprocess.check_output([str(node),'--version'],text=True).strip()
    current_npm=subprocess.check_output([str(node),str(npm),'--version'],text=True).strip()
    versions=f'node {current_node}; npm {current_npm}'
    stage1=json.loads((REPO/'docs/standard14-dedicated-evidence-r1.json').read_text())
    web=BASE/'src/web/market_units_editor'; source=stage1['old_source_repository']; ref=stage1['old_source_commit']
    package_match={name:sha(web/name)==hashlib.sha256(subprocess.check_output(['git','-C',source,'show',ref+':src/web/market_units_editor/'+name])).hexdigest() for name in ['package.json','package-lock.json']}
    cache=Path.home()/'.npm/_cacache/content-v2/sha512'; lock=json.loads((web/'package-lock.json').read_text())
    import base64
    present=[]; absent=[]
    for package,item in lock['packages'].items():
        integrity=item.get('integrity','')
        if not integrity.startswith('sha512-'): continue
        digest=base64.b64decode(integrity.split('-')[1]).hex(); path=cache/digest[:2]/digest[2:4]/digest[4:]
        row={'package':package,'integrity':integrity,'optional':bool(item.get('optional')),'platform':item.get('os',[]),'cpu':item.get('cpu',[])}
        if path.exists():
            if hashlib.sha512(path.read_bytes()).hexdigest()!=digest: raise ValueError('cache integrity mismatch')
            present.append(row)
        else: absent.append(row)
    # 旧receiptは版・gate成功の観測であり、実行ファイルhash/cache manifestを保存していない。
    report={'schema_version':'standard14-dedicated-node-environment-audit/r2','model_slots_issued':0,
            'old_receipt':{'path':str(old.relative_to(REPO)),'file_sha256':sha(old),'date':receipt['date'],'runtime':receipt['runtime'],'gates':receipt['seeded_gates'],'binary_sha256_recorded':False,'npm_binary_sha256_recorded':False,'cache_manifest_recorded':False},
            'current':{'node_path':str(node),'node_sha256':sha(node),'npm_path':str(npm),'npm_sha256':sha(npm),'node_version':current_node,'npm_version':current_npm},
            'versions_match':versions==receipt['runtime'],'package_and_lock_match':package_match,
            'cache':{'root':str(cache),'verified_present_count':len(present),'absent_count':len(absent),'present':present,'absent':absent},
            'historical_binary_identity_match':'unprovable_from_saved_receipt','historical_cache_identity_match':'unprovable_from_saved_receipt',
            'ready_for_model_dispatch':False,'specification_unfinished_condition':'工程1が要求する旧F04実体・cacheの完全同一性は、旧hash/manifestがないため証明できない。現在の版一致やoffline install成功で代用しない。','no_old_result_cost_comparison':True}
    save(TARGET/'registrations/node-environment-audit-r2.json',report)
    print(json.dumps({'versions_match':report['versions_match'],'package_match':all(package_match.values()),'historical_identity':'unproven','cache_present':len(present),'cache_absent':len(absent)}))
if __name__=='__main__':main()
