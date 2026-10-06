"""固定Low Layer 1を再利用した推論設定別の発行。採点判断は含めない。"""
import copy, json, os, shutil, subprocess, sys, time
from pathlib import Path
from types import SimpleNamespace
import stage4_campaign_r2 as prior
from stage4_campaign_r2 import load, save, sha, TARGET, SHARED, REPO, environment, bind_sources, identity_sha256, split_conditions, RUN_POOL_SCHEMA, plan_missing, prepare_atomic_plan, utc_now
LOW=prior.ROOT
REASON=sys.argv[2]
assert REASON in ['medium','high']
ROOT=LOW.parent/f'standard14-dedicated-{REASON}-n2-20261004-r1'
PROFILE=TARGET/f'profiles/free-astra-{REASON}-n2-r1.json'
def prepare_campaign():
    assert not ROOT.exists(); ROOT.mkdir()
    pre=load(LOW/'preflight-r4.json'); baseline=TARGET/'results/standard14-dedicated-free-astra-low-n2_2026-10-04-r1.json'
    assert load(baseline)['measurement_gate_pass']
    for p,h in pre['fixed_sources'].items(): assert sha(Path(p))==h,p
    profile=load(PROFILE); oldprofile=load(prior.PROFILE)
    a=copy.deepcopy(profile);b=copy.deepcopy(oldprofile)
    for v in [a,b]:v.pop('profile_id');v['runtime'].pop('reasoning_effort')
    assert a==b
    cli=Path(profile['runtime']['executable_binding']['executable']);assert sha(cli)==profile['runtime']['executable_binding']['entrypoint_sha256']
    assert prior.command([str(cli),'--version'])['stdout']=='codex-cli 0.159.0'
    assert sha(prior.CATALOG)==prior.EXPECTED_CATALOG
    assert sha(SHARED/'requirements.freeze.txt')==pre['conditions']['agent_environment']['python_dependency_sha256']
    env=environment(ROOT/'controller-node-environment')
    checks=[prior.command([str(SHARED/'bin/python'),'--version']),prior.command(['node','--version'],env=env),prior.command(['npm','--version'],env=env)]
    assert [v['stdout'] for v in checks]==['Python 3.14.5','v26.0.0','11.12.1']
    # 固定Layer 1の実物をコピーし、再freezeしない。
    cycle=ROOT/'cycle';shutil.copytree(LOW/'cycle/layer1',cycle/'layer1',symlinks=True)
    assert sha(cycle/'layer1/set.json')==pre['layer1_sha256']
    frozen=load(cycle/'layer1/set.json');cases=[c['id'] for c in frozen['cases']]
    for cid in cases:
        src=LOW/'cases'/cid;dest=ROOT/'cases'/cid;dest.mkdir(parents=True)
        shutil.copy2(src/'task.txt',dest/'task.txt');assert sha(dest/'task.txt')==pre['identities'][cid]['task_sha256']
        auth=dest/'authentication-source';auth.mkdir(mode=0o700);shutil.copy2(prior.CATALOG,auth/'models_cache.json')
    conditions=copy.deepcopy(pre['conditions']);conditions['reasoning_effort']=REASON;conditions['agent_environment']['runtime']=profile['runtime']
    expected=copy.deepcopy(pre['conditions']);expected['reasoning_effort']=REASON;expected['agent_environment']['runtime']['reasoning_effort']=REASON
    assert conditions==expected
    prompt=load(LOW/'atomic-registry/pools'/f"{pre['atomic_pool_key']}.json")['prompt_set_identity']
    common,_=split_conditions({'evaluation_set':{k:frozen[k] for k in ['set_id','revision','identity_sha256']},**conditions})
    bycase={c['id']:{**common,'case_id':c['id'],'fixture':c['fixture_identity']} for c in frozen['cases']}
    blocks={c:identity_sha256(v) for c,v in bycase.items()};key=identity_sha256({'prompt_set_identity':prompt,'comparison_block_keys':blocks})
    pool={'schema_version':RUN_POOL_SCHEMA,'pool_key':key,'prompt_set_identity':prompt,'prompt_set_identity_sha256':identity_sha256(prompt),'case_ids':cases,'comparison_block_keys':blocks,'comparison_key':identity_sha256(bycase),'effective_conditions_by_case':bycase,'created_at':utc_now()};pool['pool_content_sha256']=identity_sha256(pool)
    registry=ROOT/'atomic-registry';save(registry/'pools'/f'{key}.json',pool)
    dispatch=ROOT/'atomic-dispatch.json';plan_missing(SimpleNamespace(registry=str(registry),pool_key=key,desired_count=2,output=str(dispatch)))
    templates=[]
    for cid in cases:
        p=ROOT/'templates'/f'{cid}.json';save(p,{'schema_version':'the-caption-prompt.execution-capsule/v2','binding':{'case_id':cid,'iteration':1,'prompt_set_identity':prompt},'comparison_conditions':conditions});templates.append(p)
    hints=ROOT/'duration-hints.json';shutil.copy2(LOW/'duration-hints.json',hints)
    plan=prepare_atomic_plan(templates=templates,dispatch_plan_path=dispatch,registry=registry,cycle=cycle,evaluator=REPO/'scripts/evaluation_loop.py',duration_hints_path=hints,resource_class={'host':'local','fixed_max_workers':24},output=ROOT/'atomic-plan',max_workers=24,max_attempts=1)
    slots=load(dispatch)['missing_slots'];assert len(slots)==28
    batch=[{'case_id':cid,'iteration':i,'label':f'{REASON}-{i:02}','sample_id':next(s['sample_id'] for s in slots if s['case_id']==cid and s['dispatch_iteration']==i)} for cid in cases for i in [1,2]]
    receipt=copy.deepcopy(pre);receipt.update(schema_version='standard14-dedicated-stage5-preflight/r1',reasoning_effort=REASON,batches=[batch[:24],batch[24:]],conditions=conditions,profile_sha256=sha(PROFILE),layer1=str(cycle/'layer1/set.json'),atomic_pool_key=key,dispatch_plan_sha256=sha(dispatch),atomic_plan_sha256=sha(Path(plan['plan'])),baseline_result_path=str(baseline),baseline_result_sha256=sha(baseline),declared_axis=['reasoning_effort'],all_other_effective_conditions_identical=True,environment_checks=checks,actual_work_model={'source':'current chat; no model setting inferred'},controller_revision='stage5_campaign_r1')
    receipt['fixed_sources'][str(Path(__file__).resolve())]=sha(Path(__file__))
    save(ROOT/'preflight-r4.json',receipt);save(TARGET/f'registrations/stage5-{REASON}-preflight-r1.json',receipt)
    print(json.dumps({'ready':True,'reasoning':REASON,'slots':28,'layer1_reused':True}))
def setup():
    prior.ROOT=ROOT;prior.PROFILE=PROFILE
if __name__=='__main__':
    op=sys.argv[1]
    if op=='prepare':prepare_campaign()
    elif op=='worker':setup();prior.worker(sys.argv[3],sys.argv[4])
    elif op=='batch':
        # 元制御と同じworker呼出しへ、この固定済み入口を接続する。
        setup(); prior.__file__=__file__
        original=subprocess.run
        def run(args,**kwargs):
            if isinstance(args,list) and len(args)>2 and args[2]=='worker':args=args[:3]+[REASON]+args[3:]
            return original(args,**kwargs)
        prior.subprocess.run=run
        prior.dispatch_batch(int(sys.argv[3]))
    else:raise ValueError(op)
