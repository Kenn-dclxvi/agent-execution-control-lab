import json,tempfile,subprocess,hashlib,shutil
from pathlib import Path
from fixture import TARGET,BASE,materialize,sha,SHARED
from qualification import run,RESULTS
REG=TARGET/'registrations'
def main():
    p=REG/'local-qualification-r1.json'; local=json.loads(p.read_text())
    with tempfile.TemporaryDirectory(prefix='sd14-storage-') as temp:
        for cid,old in local['identities'].items():
            new=materialize(cid,Path(temp)/cid)
            for key in ['base_commit','seed_commit','free_commit','manifest']: assert old[key]==new[key],(cid,key)
            old.update({k:new[k] for k in ['git_objects_logical_bytes','git_objects_allocated_bytes']})
    p.write_text(json.dumps(local,ensure_ascii=False,indent=2)+'\n')
    # F04の実toolchainの終了証拠を同じ固定素材へ保存する。
    web=BASE/'src/web/market_units_editor'
    for args in [['npm','ci','--ignore-scripts','--no-audit','--no-fund','--include=dev'],['npm','run','lint'],['npm','run','build']]: run(web,args)
    (REG/'node-qualification-r1.json').write_text(json.dumps({'package_sha256':sha(web/'package.json'),'lock_sha256':sha(web/'package-lock.json'),'commands':RESULTS,'actual_node':shutil.which('node'),'actual_npm':shutil.which('npm'),'legacy_environment_match':'unverified','model_slots_issued':0},ensure_ascii=False,indent=2)+'\n')
    print('固定Git配置とNode終了証拠を保存')
if __name__=='__main__':main()
