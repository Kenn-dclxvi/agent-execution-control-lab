"""旧STD14を、専用測定と条件対応させる非登録の追加測定。"""
import concurrent.futures,copy,importlib.util,json,os,shutil,subprocess,sys,time
from pathlib import Path
from types import SimpleNamespace
from fixture import TARGET,SHARED,manifest,sha,commit
from evidence_bridge_r6 import save,load
from execution_binding_r6 import load_bound_executor,bind_sources,MATERIALIZER
from node_environment_r3 import environment
import stage4_campaign_r2 as prior
REPO=TARGET.parents[2];sys.path.insert(0,str(REPO))
from scripts.prepare_case_fixture import prepare_fixture
ROOT=prior.ROOT.parent/'standard14-old-new-paired-n2-20261004-r2'
SOURCE=Path(load(REPO/'docs/standard14-dedicated-evidence-r1.json')['old_source_repository'])
MAP={c['case_id']:c for c in load(TARGET/'registrations/stage3-verdict-r4.json')['cases']}

def prepare_old():
 assert not ROOT.exists();ROOT.mkdir();rows={};pre=load(prior.ROOT/'preflight-r4.json')
 for p,h in pre['fixed_sources'].items():assert sha(Path(p))==h,p
 for sd,c in MAP.items():
  case=REPO/'evaluations/cases'/c['source_case']/c['source_revision'];w=ROOT/'fixed-fixtures'/sd
  receipt=prepare_fixture(case,SOURCE,w)
  (w/'AGENTS.md').write_bytes(b'');free=commit(w,'repository authority')
  assert not subprocess.check_output(['git','status','--porcelain'],cwd=w,text=True)
  for name in ['src/AGENTS.md','tests/AGENTS.md','docs/AGENTS.md']:assert sha(w/name)==sha(TARGET/'fixture/base'/name)
  raw=(case/'trial-prompt-input.json').read_bytes()
  if sd!='SD14-12':assert raw==(prior.ROOT/'cases'/sd/'task.txt').read_bytes()
  rows[sd]={'source_case':c['source_case'],'source_revision':c['source_revision'],'fixture_receipt':receipt,'free_commit':free,'manifest':manifest(w),'task_sha256':__import__('hashlib').sha256(raw).hexdigest(),'contract_sha256':sha(case/'private/case-data.json')}
  dest=ROOT/'cases'/sd;dest.mkdir(parents=True);(dest/'task.txt').write_bytes(raw)
  print(sd,'fixed',flush=True)
 save(ROOT/'fixed-inputs-r1.json',rows)
 save(TARGET/'registrations/old-new-fixed-inputs-r1.json',{'source_path':str(ROOT/'fixed-inputs-r1.json'),'source_sha256':sha(ROOT/'fixed-inputs-r1.json'),'case_ids':list(MAP),'declared_material_delta':True,'old_source_commit':'3ce91a403f9e0c83f29d56bbe9e7b449b713445d','frozen_once_reused_all_reasoning':True})

def prepare_setting(reason):
 rows=load(ROOT/'fixed-inputs-r1.json');oldpre=load(prior.ROOT/'preflight-r4.json');settings=ROOT/reason;settings.mkdir()
 profile=copy.deepcopy(load(TARGET/f'profiles/free-astra-{reason}-n2-r1.json'));profile['profile_id']=f'standard14-old-free-astra-{reason}-n2-r1'
 cli=Path(profile['runtime']['executable_binding']['executable']);assert sha(cli)==profile['runtime']['executable_binding']['entrypoint_sha256'];assert prior.command([str(cli),'--version'])['stdout']=='codex-cli 0.159.0'
 assert sha(prior.CATALOG)==prior.EXPECTED_CATALOG
 assert sha(SHARED/'requirements.freeze.txt')==oldpre['conditions']['agent_environment']['python_dependency_sha256']
 env=environment(settings/'environment-check');checks=[prior.command([str(SHARED/'bin/python'),'--version']),prior.command(['node','--version'],env=env),prior.command(['npm','--version'],env=env)]
 assert [c['stdout'] for c in checks]==['Python 3.14.5','v26.0.0','11.12.1']
 pair=TARGET/f'results/standard14-dedicated-free-astra-{reason}-n2_2026-10-04-r1.json';assert load(pair)['valid_runs']==28
 pp=load(TARGET/('registrations/stage4-preflight-r4.json' if reason=='low' else f'registrations/stage5-{reason}-preflight-r1.json'))
 assert profile['runtime']==pp['conditions']['agent_environment']['runtime'] and profile['permission']==pp['conditions']['permission']
 for p,h in pp['fixed_sources'].items():assert sha(Path(p))==h,p
 for sd in MAP:
  dest=settings/'cases'/sd;dest.mkdir(parents=True);shutil.copy2(ROOT/'cases'/sd/'task.txt',dest/'task.txt');auth=dest/'authentication-source';auth.mkdir(mode=0o700);shutil.copy2(prior.CATALOG,auth/'models_cache.json')
  assert manifest(ROOT/'fixed-fixtures'/sd)==rows[sd]['manifest']
 slots=[{'case_id':sd,'iteration':i,'label':f'{reason}-{i:02}'} for sd in MAP for i in [1,2]]
 save(settings/'profile.json',profile)
 receipt={'schema_version':'standard14-old-new-correspondence-preflight/r1','ready':True,'reasoning_effort':reason,'planned_slots':28,'max_workers':24,'batches':[slots[:24],slots[24:]],'paired_result':str(pair),'paired_result_sha256':sha(pair),'paired_preflight_sha256':sha(TARGET/('registrations/stage4-preflight-r4.json' if reason=='low' else f'registrations/stage5-{reason}-preflight-r1.json')),'profile_sha256':sha(settings/'profile.json'),'fixed_inputs_sha256':sha(ROOT/'fixed-inputs-r1.json'),'controller_sha256':sha(Path(__file__)),'fixed_sources':pp['fixed_sources'],'fixed_executor':bind_sources(),'fixed_conditions':pp['conditions'],'declared_delta':['instance and material fixture','original monthly seed SHA','instance-specific rating implementation mapped to original 42 criteria'],'environment_checks':checks,'effective_runtime_identical':True,'task_authority_rating_semantics_correspondence':'stage3-verdict-r4; original TaskSpec bytes; original Rating14 criteria','elapsed_boundary':'cli_subprocess_start_to_return_monotonic','token_accounting':{'scope':'all_agents','revision':'v1'},'automatic_retry':False,'generic_layer4_registered':False,'comparison_plan_sha256':sha(REPO/'docs/standard14-dedicated-old-new-comparison-plan-r1.md'),'repair_plan_sha256':sha(REPO/'docs/standard14-dedicated-old-new-comparison-repair-r2.md'),'start_receipt_keys_match_dedicated':True,'model_visible_receipt_delta_removed':True}
 save(settings/'preflight.json',receipt);save(TARGET/f'registrations/old-new-{reason}-preflight-r2.json',receipt);print(reason,'ready',flush=True)

def worker(reason,sd,label):
 settings=ROOT/reason;pre=load(settings/'preflight.json');assert pre['ready'] and sha(settings/'profile.json')==pre['profile_sha256'] and sha(Path(__file__))==pre['controller_sha256']
 for p,h in pre['fixed_sources'].items():assert sha(Path(p))==h,p
 env=environment(settings/'run-node-environments'/f'{sd}-{label}');os.environ.update(env);os.environ['PATH']=str(SHARED/'bin')+os.pathsep+os.environ['PATH']
 rows=load(ROOT/'fixed-inputs-r1.json');module=load_bound_executor()
 def prepare(cid,w):
  subprocess.run(['cp','-cRp',str(ROOT/'fixed-fixtures'/sd),str(w)],check=True)
  assert manifest(w)==rows[sd]['manifest'];assert not subprocess.check_output(['git','status','--porcelain'],cwd=w,text=True)
  spec=importlib.util.spec_from_file_location('old_shared_materializer',MATERIALIZER);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.materialize_shared_venv(SHARED,w/'.venv',w)
  save(w.parent/'start.json',{'case_id':cid,'run_id':label,'base_commit':'3ce91a403f9e0c83f29d56bbe9e7b449b713445d','seed_commit':rows[sd]['fixture_receipt']['fixture_head_commit'],'free_commit':rows[sd]['free_commit'],'manifest':rows[sd]['manifest'],'authority':{p:sha(w/p) for p in ['AGENTS.md','src/AGENTS.md','tests/AGENTS.md','docs/AGENTS.md']},'task_sha256':rows[sd]['task_sha256'],'executor_binding':bind_sources()})
 module.fixture=SimpleNamespace(prepare=prepare,grade=lambda cid,w,e:{'case_id':cid,'valid':False,'execution_valid':True,'quality_score':None,'reason':'independent_rating_pending'})
 result=module.execute(settings/'cases'/sd,load(settings/'profile.json'),MAP[sd]['source_case'],label)
 assert result.get('exit_code')==0,result

def batch(reason,index):
 settings=ROOT/reason;pre=load(settings/'preflight.json');slots=pre['batches'][index];start=time.time()
 if index:assert load(settings/'batch-0-complete.json')['all_execution_valid']
 for sd in {s['case_id'] for s in slots}:shutil.copy2('/Users/kenn/.codex/auth.json',settings/'cases'/sd/'authentication-source/auth.json');(settings/'cases'/sd/'authentication-source/auth.json').chmod(0o600)
 records=[]
 try:
  with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
   def launch(s):
    p=subprocess.run([sys.executable,str(Path(__file__).resolve()),'worker',reason,s['case_id'],s['label']],capture_output=True,text=True)
    r={**s,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr};save(settings/'controller-output'/f"{s['case_id']}-{s['label']}.json",r);print(s['case_id'],s['iteration'],p.returncode,flush=True);return r
   for f in concurrent.futures.as_completed([executor.submit(launch,s) for s in slots]):records.append(f.result())
 finally:
  for sd in {s['case_id'] for s in slots}:(settings/'cases'/sd/'authentication-source/auth.json').unlink(missing_ok=True)
 save(settings/f'batch-{index}-complete.json',{'slots_issued':len(slots),'all_execution_valid':all(r['exit_code']==0 for r in records),'records':records,'started_epoch':start,'ended_epoch':time.time(),'max_workers':24})

if __name__=='__main__':
 op=sys.argv[1]
 if op=='freeze':prepare_old()
 elif op=='prepare':prepare_setting(sys.argv[2])
 elif op=='worker':worker(*sys.argv[2:])
 elif op=='batch':batch(sys.argv[2],int(sys.argv[3]))
 else:raise ValueError(op)
