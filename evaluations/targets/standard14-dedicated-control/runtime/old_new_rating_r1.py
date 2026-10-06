"""旧側の保存操作と元42条件を対応採点へ結ぶ。旧resultは変更しない。"""
import hashlib,json,sys,subprocess
from pathlib import Path
from evidence_bridge_r6 import save,load,observation_inventory,POLICY,GROUPS,MIXED,VALIDATION_ONLY
from stage4_rating_r1 import classify,operation_text
from fixture import TARGET,manifest,sha
from grader_r6 import Evidence,grade,PRIMARY
from old_new_campaign_r1 import ROOT,MAP,REPO
from scripts.all_agent_command_evidence import collect,command_requirement_statuses

def packets(reason):
 settings=ROOT/reason
 for run in sorted(settings.glob('cases/*/runs/*')):
  if not (run/'usage.json').exists():continue
  if (run/'correspondence-packet-r1.json').exists():continue
  sd=run.parent.parent.name;start=load(run/'start.json');u=load(run/'usage.json');result=load(run/'run.json');launch=load(run/'launch.json');w=run/'workspace'
  assert result['exit_code']==0 and u['all_agent_total_tokens']==sum(s['usage']['total_tokens'] for s in u['sessions'])
  assert launch['task_sha256']==start['task_sha256'];final=manifest(w);changed=sorted(p for p in set(final)|set(start['manifest']) if final.get(p)!=start['manifest'].get(p))
  allowed,required=POLICY[sd];report=collect(run/'usage.json',run/'events.jsonl');groups=[GROUPS[k] for k in required]
  if sd=='SD14-14':groups=[['pytest']]
  req={k:v for k,v in zip(required,command_requirement_statuses(report,groups))}
  contract=load(REPO/'evaluations/cases'/MAP[sd]['source_case']/MAP[sd]['source_revision']/'private/case-data.json')
  p={'schema_version':'standard14-old-correspondence-packet/r1','case_id':sd,'source_case':start['case_id'],'run_id':run.name,'criteria':contract['oracle']['assertions'],'start_manifest':start['manifest'],'final_manifest':final,'changed_paths':changed,'allowed_paths':allowed,'terminal_response':(run/'final.txt').read_text(),'observations':observation_inventory(run,u),'command_requirements':req,'total_tokens':u['all_agent_total_tokens'],'elapsed_seconds':result['elapsed_seconds'],'source_hashes':{name:sha(run/name) for name in ['run.json','usage.json','events.jsonl','command-evidence.json','final.txt','start.json','launch.json']}}
  save(run/'correspondence-packet-r1.json',p);print(sd,run.name,'packet',flush=True)

def rate(reason):
 settings=ROOT/reason;decisions=load(settings/'semantic-decisions-r1.json')
 for path in sorted(settings.glob('cases/*/runs/*/correspondence-packet-r1.json')):
  p=load(path);sd=p['case_id'];d=decisions[sd+'/'+p['run_id']];assert d['packet_sha256']==sha(path)
  operations=[];obs={}
  for k,o in p['observations'].items():
   kinds,why=classify(o);t,_=operation_text(o)
   if '--help' in t and '-m src.app' in t:kinds=sorted(set(kinds+['application']))
   obs[k]={'source_sha256':o['sha256'],'kinds':kinds,'reason':why};operations += [{'kind':kind,'source_observation':k} for kind in kinds]
  criteria={c['criterion_id']:d['passes'][i] for i,c in enumerate(p['criteria'])}
  command_evidence={k:v['status']=='successful' for k,v in p['command_requirements'].items() if v['status']!='not_attempted'}
  for k,v in p['command_requirements'].items():
   if v['status']=='evidence_incomplete':command_evidence[k]=None
  ignored=[name for name in p['changed_paths'] if subprocess.run(['git','check-ignore','-q','--',name],cwd=path.parent/'workspace').returncode==0]
  effective_changed=[name for name in p['changed_paths'] if name not in ignored]
  e=Evidence(operations=operations,allowed_paths=p['allowed_paths'],changed_paths=effective_changed,terminal_present=bool(p['terminal_response']),predicates=criteria,required_value_state='unresolved' if sd=='SD14-13' else None,required_commands=list(p['command_requirements']),command_evidence=command_evidence)
  e.effect_predicates={k:v for k,v in criteria.items() if k not in VALIDATION_ONLY};e.validation_predicates={k:v for k,v in criteria.items() if k in MIXED|VALIDATION_ONLY}
  q=grade(sd,e);q.update(schema_version='standard14-old-correspondence-rating/r1',case_id=sd,source_case=p['source_case'],run_id=p['run_id'],packet_sha256=sha(path),total_tokens=p['total_tokens'],elapsed_seconds=p['elapsed_seconds'],generic_layer4_registered=False,ignored_runtime_outputs=ignored,tracked_nonignored_changed_paths=effective_changed)
  save(path.parent/'independent-assessment-r1.json',{'schema_version':'standard14-old-independent-assessment/r1','packet_sha256':sha(path),'reviewer_id':'stage5-chat-01a1055d-cab7-79c0-8389-f985b0bda6e2','criteria':{c['criterion_id']:{'pass':d['passes'][i],'reason':d['reasons'][i]} for i,c in enumerate(p['criteria'])},'observations':obs,'original_contract_sha256':load(ROOT/'fixed-inputs-r1.json')[sd]['contract_sha256'],'rating_semantics':'元Rating14を専用第6版の対応済み0〜4点区分へ接続。旧原本は再採点しない。'})
  save(path.parent/'quality-result-r1.json',q);print(sd,p['run_id'],q['quality_score'],q.get('observed_route'),flush=True)
if __name__=='__main__':
 if sys.argv[1]=='packets':packets(sys.argv[2])
 elif sys.argv[1]=='rate':rate(sys.argv[2])
 else:raise ValueError(sys.argv[1])
