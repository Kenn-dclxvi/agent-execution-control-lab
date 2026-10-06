"""固定hash・双方向対応・環境照合を保存する。未確認があれば発行不可。"""
import hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
from fixture import TARGET,BASE,SHARED,manifest,sha
REPO=TARGET.parents[2]
REG=TARGET/'registrations'
def write(path,data): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def command(args):
    p=subprocess.run(args,text=True,capture_output=True); return {'exit_code':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
def main():
    evidence=json.loads((REPO/'docs/standard14-dedicated-evidence-r1.json').read_text())
    local=json.loads((REG/'local-qualification-r1.json').read_text())
    profile=json.loads((REPO/'evaluations/profiles/control-free-astra-low-old-a01-isolated-n20-20261003-r1.json').read_text())
    # Session payloadから必要な設定だけ保存し、非公開の生ログは複製しない。
    session=Path('/Users/kenn/.codex/sessions/2026/10/04/rollout-2026-10-04T00-47-00-01a10272-8060-7d92-8e98-df630cf13d77.jsonl')
    turns=[json.loads(l)['payload'] for l in session.open() if json.loads(l).get('type')=='turn_context']
    actual={'model':turns[-1]['model'],'reasoning_effort':turns[-1]['effort'],'session_id':'01a10272-8060-7d92-8e98-df630cf13d77','source':'session turn_context','requested_model':'gpt-6.1-sol','requested_reasoning':'medium'}
    cli=Path(profile['runtime']['executable_binding']['executable']); binding=profile['runtime']['executable_binding']
    node=Path(shutil.which('node')).resolve(); npm=Path(shutil.which('npm')).resolve()
    env={'stage2_actual':actual,'shared_python':{'path':str(SHARED),'requirements_freeze_sha256':sha(SHARED/'requirements.freeze.txt'),'expected_sha256':'61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73','version':command([str(SHARED/'bin/python'),'--version']),'python3':command([str(SHARED/'bin/python3'),'--version']),'pytest':command([str(SHARED/'bin/python'),'-m','pytest','--version'])},'cli':{'binding':binding,'actual_sha256':sha(cli),'version':command([str(cli),'--version']),'codesign':command(['codesign','-dv','--verbose=4',str(cli)])},'node':{'path':str(node),'sha256':sha(node),'version':command([str(node),'--version']),'npm_path':str(npm),'npm_sha256':sha(npm),'npm_version':command(['npm','--version']),'old_environment_match':'unverified','cache':str(Path.home()/'.npm')},'execution':{'max_workers':24,'all_agent_usage':'scripts/all_agent_usage.py','command_evidence':'scripts/all_agent_command_evidence.py','token_accounting':'all-agent/v1','elapsed':'execution-time-recording/r1','interval':'CLI subprocess start to return; question wait included','permissions':profile['runtime']['permission'],'network_access':False,'memories':False,'per_run_home':'empty_auth_only','retry':False,'slots_per_reasoning':28,'authorized_now':0}}
    env['shared_python']['identity_matches']=env['shared_python']['requirements_freeze_sha256']==env['shared_python']['expected_sha256']
    env['cli']['identity_matches']=env['cli']['actual_sha256']==binding['entrypoint_sha256'] and env['cli']['version']['stdout']==binding['version_output']
    frozen_executor=Path('/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/astra-a01-old-and-compact-n20-20261001-r1/frozen-lab/scripts/run_codex_evaluation.py')
    env['execution']['fixed_executor']={'path':str(frozen_executor),'sha256':sha(frozen_executor),'expected_sha256':'28728c2284550f227a5c24f40f4751e2654bc7598b8d9cf68ddef9eae162d80c'}
    env['execution']['fixed_executor']['identity_matches']=env['execution']['fixed_executor']['sha256']==env['execution']['fixed_executor']['expected_sha256']
    write(REG/'environment-r1.json',env)
    # 対応表は全旧criterionを列挙し、検査はそのcriterionからしか品質条件を導かない。
    rows=[]
    for i,c in enumerate(evidence['case_contracts'],1):
        cid=f'SD14-{i:02}'; old=REPO/'evaluations/cases'/c['case_id']/c['revision']/'private/case-data.json'; d=json.loads(old.read_text())
        for a in d['oracle']['assertions']:
            rows.append({'new_case':cid,'old_case':c['case_id'],'old_revision':c['revision'],'old_criterion':a['criterion_id'],'new_criterion':a['criterion_id'],'source':str(old.relative_to(REPO))+'#/oracle/assertions/'+a['criterion_id'],'expected':a['expected'],'checks':['runtime/inspect_artifact.py::content_checks','runtime/grader.py::grade','registrations/local-qualification-r1.json#'+cid+':'+a['criterion_id']],'evidence_sources':next(x['evidence_sources'] for x in d['grader']['criteria'] if x['criterion_id']==a['criterion_id'])})
    assert len(rows)==42; write(REG/'criterion-map-r1.json',{'forward':rows,'reverse':{r['new_case']+':'+r['new_criterion']:r['source'] for r in rows},'orphan_quality_conditions':[],'notes':'数値行と生成者情報は診断のみ。A01本文語句は採点に使わない。抽象検証条件を特定コマンドへ変換しない。'})
    source=manifest(BASE); fixed={}
    for p in sorted(TARGET.rglob('*')):
        if p.is_file() and not any(x in {'.git','__pycache__','node_modules','dist','.pytest_cache'} for x in p.relative_to(TARGET).parts) and p.name not in {'source-freeze-r1.json','handoff-r1.json','storage-r1.json'}:
            fixed[str(p.relative_to(TARGET))]={'sha256':sha(p),'bytes':p.stat().st_size,'mode':oct(p.stat().st_mode&0o777)}
    leakage={'case_count':14,'root_bytes':(BASE/'AGENTS.md').stat().st_size,'tasks_byte_preserved':True,'declared_replacement':{'case':'SD14-12','old_sha':'a53601614b41f52633f1d75e77c72861a0f0f1c8','new_sha':local['identities']['SD14-12']['seed_commit'],'replacement_only':True},'authority_match':all(sha(BASE/p)==hashlib.sha256(subprocess.check_output(['git','-C',evidence['old_source_repository'],'show',evidence['old_source_commit']+':'+p])).hexdigest() for p in ['src/AGENTS.md','tests/AGENTS.md','docs/AGENTS.md']),'model_input_contains_design_or_oracle':False,'checks':[]}
    for i,c in enumerate(evidence['case_contracts'],1):
        cid=f'SD14-{i:02}'; old=REPO/'evaluations/cases'/c['case_id']/c['revision']/'trial-prompt-input.json'; new=TARGET/'cases'/cid/'r1/trial-prompt-input.json'
        assert old.read_bytes()==new.read_bytes()
        leakage['checks'].append({'case_id':cid,'source_task_sha256':sha(old),'stored_task_sha256':sha(new),'delivered_task_sha256':local['identities'][cid]['task_sha256'],'fixture_manifest_sha256':hashlib.sha256(json.dumps(local['identities'][cid]['manifest'],sort_keys=True).encode()).hexdigest()})
    for path,v in source.items():
        assert v['type']=='file',path
        text=(BASE/path).read_text(errors='replace')
        assert not any(s in text for s in ['standard14-dedicated-case-spec','standard14-dedicated-evidence','private/case-data.json','SD14-','CRC-','candidate214']),path
    assert leakage['root_bytes']==0 and leakage['authority_match']; write(REG/'delivery-audit-r1.json',leakage)
    # 発行前の未確認条件を明示。局所合格とモデル測定成立を分離する。
    missing=['工程3の全14対応最終確認','旧F04保存環境のNode/npm実体とcacheの同一性','固定モデル一覧の実配送照合','CLI basic/developer/skills/toolと質問方式の一致','空home・認証だけ・network禁止の各実行照合','all-agent usageと時間区間の新系列実測成立','新集合Layer 1とatomic planの実行前照合','F05/F10とtest差分の独立意味判定の運用接続']
    write(REG/'admission-r1.json',{'ready':False,'model_slots_issued':0,'authorized_slots_now':0,'planned':{'low':28,'medium':28,'high':28},'max_workers':24,'automatic_retry':False,'retain_valid_low_quality':True,'unverified':missing})
    write(REG/'source-freeze-r1.json',{'schema_version':'standard14-dedicated-source-freeze/v1','fixture':source,'artifacts':fixed,'base_commit':local['identities']['SD14-01']['base_commit'],'cases':{k:{x:v[x] for x in ['base_commit','seed_commit','free_commit','task_sha256']} for k,v in local['identities'].items()},'ready_for_model_dispatch':False,'model_slots_issued':0})
    storage={'fixture_files':len(source),'fixture_logical_bytes':sum(x['bytes'] for x in source.values()),'fixture_lines':sum(len((BASE/p).read_bytes().splitlines()) for p in source),'fixture_python_lines':sum(len((BASE/p).read_bytes().splitlines()) for p in source if p.endswith('.py')),'fixture_allocated_bytes':sum((BASE/p).stat().st_blocks*512 for p in source),'target_artifact_logical_bytes':sum(v['bytes'] for v in fixed.values()),'dependencies':{'node_modules_logical_bytes':sum(p.stat().st_size for p in (BASE/'src/web/market_units_editor/node_modules').rglob('*') if p.is_file()),'shared_python':'既存共有環境をsymlinkする。専用素材の論理量へ合算しない'},'git_objects':'局所検証の一時Gitは各workspace独立。完了後削除。固定commit/treeを検証記録へ保存。モデル試験のピークと保持量は未測定。','cost_claim':'未認定。素材の短さからトークン削減・モデル差保持を認定しない。'}
    storage['per_case_git_objects']={k:{n:v[n] for n in ['git_objects_logical_bytes','git_objects_allocated_bytes']} for k,v in local['identities'].items()}
    write(REG/'storage-r1.json',storage)
    fixed={}
    for p in sorted(TARGET.rglob('*')):
        if p.is_file() and not any(x in {'.git','__pycache__','node_modules','dist','.pytest_cache'} for x in p.relative_to(TARGET).parts) and p.name not in {'source-freeze-r1.json','handoff-r1.json'}:
            fixed[str(p.relative_to(TARGET))]={'sha256':sha(p),'bytes':p.stat().st_size,'mode':oct(p.stat().st_mode&0o777)}
    frozen=json.loads((REG/'source-freeze-r1.json').read_text()); frozen['artifacts']=fixed
    frozen['reused_kernel_sources']={str(p.relative_to(REPO)):sha(p) for p in [REPO/'scripts/all_agent_usage.py',REPO/'scripts/all_agent_command_evidence.py',REPO/'layer2/extensions/parallel_execution/prepare_atomic_plan.py',REPO/'scripts/execution_time_recording.py'] if p.exists()}
    frozen['stage1_inputs']={str(p.relative_to(REPO)):sha(p) for p in (REPO/'docs').glob('standard14-dedicated-*-r1.*') if 'stage2' not in p.name}
    write(REG/'source-freeze-r1.json',frozen)
    print(json.dumps({'source_files':len(source),'criteria':len(rows),'fixture_bytes':storage['fixture_logical_bytes'],'ready':False},ensure_ascii=False))
if __name__=='__main__':main()
