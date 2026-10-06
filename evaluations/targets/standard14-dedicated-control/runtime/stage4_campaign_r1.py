"""工程4の初回準備と固定実行器の発行。既存の実行・採点コードは変更しない。"""
import argparse, concurrent.futures, hashlib, importlib.util, json, os, shutil, subprocess, sys, time
from pathlib import Path
from types import SimpleNamespace
from fixture import TARGET, SHARED, materialize, task, sha, manifest
from evidence_bridge_r6 import save, load
from execution_binding_r6 import prepare, load_bound_executor, capture_completed_execution, bind_sources
from node_environment_r3 import environment
REPO=TARGET.parents[2]
sys.path.insert(0,str(REPO))
from scripts.evaluation_loop import layer1_freeze, identity_sha256, utc_now
from scripts.atomic_run_registry import RUN_POOL_SCHEMA, plan_missing, split_conditions
from layer2.extensions.parallel_execution.prepare_atomic_plan import prepare_atomic_plan
ROOT=Path('/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/standard14-dedicated-low-n2-20261004-r1')
CATALOG=Path('/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/astra-old-a01-isolated-n20-20261003-r1/authentication-source/models_cache.json')
PROFILE=TARGET/'profiles/free-astra-low-n2-r1.json'
EXPECTED_CATALOG='e7f386c6adaac4f7754464150107ada16c1dea09e9bca3fcd365aa32a5dd3b1e'

def command(args,cwd=None,env=None):
    p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True,check=True)
    return {'argv':args,'stdout':p.stdout.strip(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest(),'exit_code':p.returncode}

def prepare_campaign():
    bind_sources(); assert sha(CATALOG)==EXPECTED_CATALOG
    profile=load(PROFILE); cases=load(TARGET/'sets/dedicated14-r1.json')['case_ids']
    freeze=load(TARGET/'registrations/source-freeze-r6.json')
    fixed_sources={}
    for group,base in [('artifacts',TARGET),('stage1_inputs',REPO),('reused_kernel_sources',REPO)]:
        for name,item in freeze[group].items():
            p=base/name; expected=item['sha256'] if isinstance(item,dict) else item
            assert sha(p)==expected,str(p); fixed_sources[str(p)]=expected
    cli=Path(profile['runtime']['executable_binding']['executable'])
    assert sha(cli)==profile['runtime']['executable_binding']['entrypoint_sha256']
    assert command([str(cli),'--version'])['stdout']=='codex-cli 0.159.0'
    signature=subprocess.run(['codesign','-dv','--verbose=4',str(cli)],capture_output=True,text=True,check=True)
    assert 'TeamIdentifier=2DC432GLL2' in signature.stderr
    assert sha(SHARED/'requirements.freeze.txt')=='61b26e617ae49be1858b6645d0280ba09c1211702cba6983e51475afec669a73'
    # 初回系列なので、保存resultを仮造せず固定入力から空のpoolを構築する。
    seeds=ROOT/'layer1-sources'; seeds.mkdir()
    local=load(TARGET/'registrations/local-qualification-r1.json')['identities']; identities={}; descriptors=[]
    for cid in cases:
        w=seeds/cid; ident=materialize(cid,w)
        for k in ['base_commit','seed_commit','free_commit','manifest']: assert ident[k]==local[cid][k],(cid,k)
        raw=task(cid,ident['seed_commit']); campaign=ROOT/'cases'/cid; campaign.mkdir(parents=True)
        (campaign/'task.txt').write_bytes(raw)
        auth=campaign/'authentication-source'; auth.mkdir(mode=0o700); shutil.copy2(CATALOG,auth/'models_cache.json')
        ident['task_sha256']=sha(campaign/'task.txt'); identities[cid]=ident
        descriptors.append({'id':cid,'revision':'r1','fixture':str(w),'payload':{'task_sha256':ident['task_sha256']}})
    source=ROOT/'set-source.json'; save(source,{'set_id':'dedicated14-r1','revision':'r1','cases':descriptors})
    cycle=ROOT/'cycle'; layer1_freeze(SimpleNamespace(set=str(source),cycle=str(cycle)))
    frozen=load(cycle/'layer1/set.json')
    # 配送されるモデルの定義と基本指示は原本と起動確認の全項目が一致する。
    selected=next(x for x in load(CATALOG)['models'] if x['slug']=='gpt-6-astra')
    startup=next(x for x in load(ROOT/'startup-home-r2/models_cache.json')['models'] if x['slug']=='gpt-6-astra')
    assert selected==startup
    oldhome=Path('/Volumes/SN7100/_verification/THE-CAPTION-prompt-ab-measurement/runs/astra-old-a01-current-env-low-n2-20261003-r1/runs/low-01/codex-home')
    skills={str(p.relative_to(ROOT/'startup-home-r2')):sha(p) for p in (ROOT/'startup-home-r2/skills').rglob('SKILL.md')}
    assert all(sha(oldhome/p)==h for p,h in skills.items())
    oldusage=load(oldhome.parent/'usage.json'); oldmeta=load_rollout_meta(Path(oldusage['sessions'][0]['rollout_file']))
    assert oldmeta['base_instructions']['text']==selected['model_messages']['instructions_template']
    effective=load(ROOT/'startup-thread-start-r2.json')[-1]['result']
    assert effective['model']=='gpt-6-astra' and effective['reasoningEffort']=='low'
    assert effective['approvalPolicy']=='never' and effective['sandbox']['networkAccess'] is False
    assert effective['instructionSources']==[] and effective['multiAgentMode']=='explicitRequestOnly'
    node_env=environment(ROOT/'controller-node-environment')
    env_checks=[command([str(SHARED/'bin/python'),'--version']),command([str(SHARED/'bin/python3'),'--version']),command([str(SHARED/'bin/python'),'-m','pytest','--version']),command(['node','--version'],env=node_env),command(['npm','--version'],env=node_env)]
    assert env_checks[0]['stdout']=='Python 3.14.5' and env_checks[3]['stdout']=='v26.0.0' and env_checks[4]['stdout']=='11.12.1'
    # 実行時のworkspace固有Python shimも、実行前に同じ接続処理で全ケース照合する。
    shim_checks={}
    for cid in cases:
        w=ROOT/'environment-checks'/cid/'workspace'; w.parent.mkdir(parents=True)
        ident=prepare(cid,w)
        assert ident['manifest']==identities[cid]['manifest'] and ident['task_sha256']==identities[cid]['task_sha256']
        shim_checks[cid]=command([str(w/'.venv/bin/python'),'-c','import sys,pytest; print(sys.version.split()[0]); print(pytest.__version__)'],cwd=w)
    conditions={'model':'gpt-6-astra','reasoning_effort':'low','case_revisions':{c:'r1' for c in cases},'tasks':{c:identities[c]['task_sha256'] for c in cases},'rating':{'path':str(TARGET/'rating-contracts/outcome-r1.json'),'sha256':sha(TARGET/'rating-contracts/outcome-r1.json'),'bridge_sha256':sha(TARGET/'runtime/evidence_bridge_r6.py')},'agent_environment':{'runtime':profile['runtime'],'model_catalog_source_sha256':EXPECTED_CATALOG,'selected_model_definition_sha256':identity_sha256(selected),'base_instructions_sha256':hashlib.sha256(selected['model_messages']['instructions_template'].encode()).hexdigest(),'skills':skills,'personal_instruction_isolation':'empty_home_auth_only','python_dependency_sha256':sha(SHARED/'requirements.freeze.txt'),'node_binding_sha256':sha(TARGET/'registrations/node-environment-binding-r3.json'),'question_interface':'fixed CLI default mode; no user answer supplied'},'permission':profile['permission'],'executor_parameters':{'max_workers':24,'max_attempts_per_slot':1,'fixed_executor_sha256':bind_sources()['executor']['sha256'],'source_bindings':fixed_sources},'token_accounting':{'scope':'all_agents','revision':'v1'}}
    prompt={'name':'standard14-dedicated-free-r1','revision':'r1','bundle_sha256':sha(TARGET/'prompts/baselines/free-r1/bundle.json')}
    common,_=split_conditions({'evaluation_set':{k:frozen[k] for k in ['set_id','revision','identity_sha256']},**conditions})
    bycase={c['id']:{**common,'case_id':c['id'],'fixture':c['fixture_identity']} for c in frozen['cases']}
    blocks={c:identity_sha256(v) for c,v in bycase.items()};key=identity_sha256({'prompt_set_identity':prompt,'comparison_block_keys':blocks})
    pool={'schema_version':RUN_POOL_SCHEMA,'pool_key':key,'prompt_set_identity':prompt,'prompt_set_identity_sha256':identity_sha256(prompt),'case_ids':cases,'comparison_block_keys':blocks,'comparison_key':identity_sha256(bycase),'effective_conditions_by_case':bycase,'created_at':utc_now()};pool['pool_content_sha256']=identity_sha256(pool)
    registry=ROOT/'atomic-registry';save(registry/'pools'/f'{key}.json',pool)
    dispatch=ROOT/'atomic-dispatch.json';plan_missing(SimpleNamespace(registry=str(registry),pool_key=key,desired_count=2,output=str(dispatch)))
    templates=[]
    for cid in cases:
        p=ROOT/'templates'/f'{cid}.json';save(p,{'schema_version':'the-caption-prompt.execution-capsule/v2','binding':{'case_id':cid,'iteration':1,'prompt_set_identity':prompt},'comparison_conditions':conditions});templates.append(p)
    hints=ROOT/'duration-hints.json';save(hints,{'duration_hints_seconds':{cid:float(15-i) for i,cid in enumerate(cases)}})
    plan_result=prepare_atomic_plan(templates=templates,dispatch_plan_path=dispatch,registry=registry,cycle=cycle,evaluator=REPO/'scripts/evaluation_loop.py',duration_hints_path=hints,resource_class={'host':'local','fixed_max_workers':24},output=ROOT/'atomic-plan',max_workers=24,max_attempts=1)
    generated=load(Path(plan_result['plan']));slots=load(dispatch)['missing_slots']; assert len(generated['jobs'])==28
    # 実際の発行は元の24件+4件。atomic計画の全枠と一対一に対応する。
    batch_plan=[{'case_id':cid,'iteration':i,'label':f'low-{i:02}','sample_id':next(s['sample_id'] for s in slots if s['case_id']==cid and s['dispatch_iteration']==i)} for cid in cases for i in [1,2]]
    worker_sources={str(Path(__file__).resolve()):sha(Path(__file__)),**fixed_sources}
    receipt={'schema_version':'standard14-dedicated-stage4-preflight/r3','ready':True,'model_slots_issued':0,'planned_slots':28,'max_workers':24,'batches':[batch_plan[:24],batch_plan[24:]],'automatic_retry':False,'retain_valid_low_quality':True,'initial_series_not_old_comparison':True,'stage3_verdict_sha256':sha(TARGET/'registrations/stage3-verdict-r4.json'),'fixed_sources':worker_sources,'identities':identities,'layer1':str(cycle/'layer1/set.json'),'layer1_sha256':sha(cycle/'layer1/set.json'),'dispatch_plan_sha256':sha(dispatch),'atomic_plan_sha256':sha(Path(plan_result['plan'])),'atomic_pool_key':key,'conditions':conditions,'profile_sha256':sha(PROFILE),'environment_checks':env_checks,'python_shim_checks':shim_checks,'model_catalog_delivery':{'source_sha256':sha(CATALOG),'copied_to_all_case_sources':True,'selected_definition_matches_no_inference_startup':True,'base_instructions_match_saved_fixed_cli':True,'catalog_refresh_diagnostic':'非対象GPT-5.5のupgradeと時刻の更新はAstraへの入力ではない。原本のSHAと選択モデル全定義の一致を別に記録する。'},'cli_startup_config_evidence_sha256':sha(ROOT/'startup-thread-start-r2.json'),'skills_match_saved_fixed_cli':True,'auth_retention':'発行直前に認証だけをcase sourceへコピー。各run完了後は固定実行器が削除。','runtime_isolation':'各run独立workspace/home/Node cache。空config、ancestor authorityなし、network false。','actual_work_model':actual_work_model(),'time_contract':'execution-time-recording/r1','elapsed_boundary':'cli_subprocess_start_to_return_monotonic','usage_connection':'固定全担当最終usage収集器。各runで実測成立を検証する。'}
    save(ROOT/'preflight-r3.json',receipt);save(TARGET/'registrations/stage4-preflight-r3.json',receipt)
    print(json.dumps({'ready':True,'slots':28,'atomic_plan':plan_result},ensure_ascii=False),flush=True)

def load_rollout_meta(path):
    for l in path.open():
        j=json.loads(l)
        if j['type']=='session_meta':return j['payload']
    raise ValueError('session meta unavailable')

def actual_work_model():
    # 生ログを複製せず、このチャットの設定だけを取り出す。
    for p in Path('/Users/kenn/.codex/sessions/2026/10/04').glob('*01a104e0-02e9-7470-9aef-08d91e723c14*'):
        found=None
        for n,l in enumerate(p.open(),1):
            j=json.loads(l)
            if j['type']=='turn_context':found={'model':j['payload']['model'],'reasoning_effort':j['payload'].get('effort'),'source_path':str(p),'line':n,'record_sha256':hashlib.sha256(l.encode()).hexdigest()}
        if found:return found
    raise ValueError('actual work model missing')

def worker(cid,label):
    receipt=load(ROOT/'preflight-r3.json');assert receipt['ready']; assert sha(PROFILE)==receipt['profile_sha256']
    for p,h in receipt['fixed_sources'].items():assert sha(p)==h,p
    campaign=ROOT/'cases'/cid
    env=environment(ROOT/'run-node-environments'/f'{cid}-{label}');os.environ.update(env)
    os.environ['PATH']=str(SHARED/'bin')+os.pathsep+os.environ['PATH']
    module=load_bound_executor(); before=time.time();result=module.execute(campaign,load(PROFILE),cid,label);after=time.time()
    run=campaign/'runs'/label
    save(run/'wall-clock.json',{'run_id':label,'cli_elapsed_seconds':result['elapsed_seconds'],'controller_started_epoch':before,'controller_returned_epoch':after,'includes_workspace_preparation':True,'elapsed_kpi_is_cli_only':True})
    if result.get('exit_code')==0:
        packet=capture_completed_execution(run)
        save(run/'stage4-execution-validity.json',{'execution_valid':True,'quality_pending':True,'packet_sha256':sha(run/'rating-packet.json')})
    else: raise ValueError(result)

def dispatch_batch(index):
    receipt=load(ROOT/'preflight-r3.json');slots=receipt['batches'][index]; started=time.time(); records=[]
    if index==1:assert load(ROOT/'batch-0-complete.json')['all_execution_valid']
    for cid in sorted({s['case_id'] for s in slots}):
        auth=ROOT/'cases'/cid/'authentication-source/auth.json';assert not auth.exists();shutil.copy2('/Users/kenn/.codex/auth.json',auth);auth.chmod(0o600)
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
            def launch(slot):
                p=subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker',slot['case_id'],slot['label']],capture_output=True,text=True)
                record={**slot,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
                save(ROOT/'controller-output'/f"{slot['case_id']}-{slot['label']}.json",record)
                print(json.dumps({k:record[k] for k in ['case_id','iteration','exit_code']},ensure_ascii=False),flush=True);return record
            futures=[executor.submit(launch,s) for s in slots]
            for f in concurrent.futures.as_completed(futures):records.append(f.result())
    finally:
        for cid in {s['case_id'] for s in slots}:(ROOT/'cases'/cid/'authentication-source/auth.json').unlink(missing_ok=True)
    save(ROOT/f'batch-{index}-complete.json',{'slots_issued':len(slots),'completed':records,'all_execution_valid':all(r['exit_code']==0 for r in records),'max_workers':24,'wall_elapsed_seconds':time.time()-started,'started_epoch':started,'ended_epoch':time.time()})

if __name__=='__main__':
    op=sys.argv[1]
    if op=='prepare':prepare_campaign()
    elif op=='worker':worker(sys.argv[2],sys.argv[3])
    elif op=='batch':dispatch_batch(int(sys.argv[2]))
    else:raise ValueError(op)
