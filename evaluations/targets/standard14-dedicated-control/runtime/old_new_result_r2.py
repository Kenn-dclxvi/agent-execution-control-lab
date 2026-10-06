"""旧側の独立記録を非公開結果へ保存する。専用atomic poolへ混ぜない。"""
import collections,hashlib,json,statistics,sys,tomllib
from pathlib import Path
from evidence_bridge_r6 import load,save,sha
from fixture import manifest
from old_new_campaign_r2 import ROOT,TARGET
from correspondence_diagnostics_r1 import delivery,storage
from scripts.evaluation_loop import identity_sha256

def stats(v):return {'sum':sum(v),'mean':statistics.mean(v),'median':statistics.median(v),'maximum':max(v)}
def main(reason):
 settings=ROOT/reason;pre=load(settings/'preflight.json');rows=[]
 for slot in [s for b in pre['batches'] for s in b]:
  sd=slot['case_id'];run=settings/'cases'/sd/'runs'/slot['label'];q=load(run/'quality-result-r1.json');p=load(run/'correspondence-packet-r1.json');u=load(run/'usage.json');assert q['valid'] and p['final_manifest']==manifest(run/'workspace')
  assert q['total_tokens']==sum(s['usage']['total_tokens'] for s in u['sessions']);assert not (run/'codex-home/auth.json').exists()
  iso=load(run/'instruction-isolation-before.json');assert iso['model_catalog_sha256']==pre['fixed_conditions']['agent_environment']['model_catalog_source_sha256'];assert iso['root_agents_bytes']==0 and iso['user_config_bytes']==0 and not iso['ancestor_instruction_files']
  dev=[];turns=[]
  for session in u['sessions']:
   for l in Path(session['rollout_file']).open():
    j=json.loads(l);d=j['payload']
    if j['type']=='session_meta':assert hashlib.sha256(d['base_instructions']['text'].encode()).hexdigest()==pre['fixed_conditions']['agent_environment']['base_instructions_sha256']
    if j['type']=='turn_context':assert d['model']=='gpt-6-astra' and d['effort']==reason and d['approval_policy']=='never' and d['sandbox_policy']['network_access'] is False;turns.append(hashlib.sha256(l.encode()).hexdigest())
    if j['type']=='response_item' and d.get('type')=='message' and d.get('role')=='developer' and session['thread_id']==u['root_thread_id']:
     t=''.join(c.get('text','') for c in d.get('content',[])).replace(str(run/'codex-home'),'<RUN_HOME>').replace(str(run/'workspace'),'<WORKSPACE>');dev.append(hashlib.sha256(t.encode()).hexdigest())
  assert dev==['dfe6cbc895d83f791ff27a34290681efbfd78af8b952122823d3bfc705b0ac39','2a9df9db8c89ecb8b44c695a5fba7b6b4f9c18a160286fd9fbc2381fdc6a6552','6ded806e3cdbb35599ecaf8742574bc5274908472b1729090010c404c2151e8e']
  behavior=q['observed_route']
  if sd=='SD14-05':behavior='clarification_stop'
  if sd=='SD14-06':behavior='out_of_scope_stop'
  if sd in ['SD14-11','SD14-12']:behavior='read_only_review' if q['quality_score']==4 else 'incorrect_stop_or_partial_review'
  if q['quality_score'] in [1,2] and behavior=='completed':behavior='incorrect_stop' if not q['tracked_nonignored_changed_paths'] else 'partial_or_preservation_failure'
  read=delivery(run)
  row={'run_id':f'old-std14-{reason}-r2-{sd}-i{slot["iteration"]}','case_id':sd,'source_case':q['source_case'],'iteration':slot['iteration'],'quality_score':q['quality_score'],'valid':True,'criteria':q['criteria'],'behavior':behavior,'total_tokens':q['total_tokens'],'elapsed_seconds':q['elapsed_seconds'],'session_count':u['session_count'],'cached_input_tokens':sum(s['usage'].get('cached_input_tokens',0) for s in u['sessions']),'source_hashes':{name:sha(run/name) for name in ['start.json','launch.json','run.json','usage.json','command-evidence.json','final.txt','correspondence-packet-r1.json','independent-assessment-r1.json','quality-result-r1.json']},'raw_evidence_directory':str(run),'read_diagnostic':read,'tracked_nonignored_changed_paths':q['tracked_nonignored_changed_paths'],'ignored_runtime_outputs':q['ignored_runtime_outputs'],'model_delivery':{'normalized_developer_hashes':dev,'turn_record_sha256':turns}}
  rows.append(row)
 a=load(settings/'batch-0-complete.json');b=load(settings/'batch-1-complete.json');assert len(rows)==28
 per={sd:{'scores':[r['quality_score'] for r in rows if r['case_id']==sd],'tokens':stats([r['total_tokens'] for r in rows if r['case_id']==sd]),'elapsed_seconds':stats([r['elapsed_seconds'] for r in rows if r['case_id']==sd]),'behaviors':[r['behavior'] for r in rows if r['case_id']==sd]} for sd in pre['fixed_conditions']['case_revisions']}
 result={'schema_version':'standard14-old-material-correspondence-measurement/r2','source_target_id':'the-caption','reasoning_effort':reason,'model':'gpt-6-astra','valid_runs':28,'cases':rows,'per_case':per,'per_iteration':{str(i):{'total_tokens':sum(r['total_tokens'] for r in rows if r['iteration']==i),'elapsed_seconds':sum(r['elapsed_seconds'] for r in rows if r['iteration']==i),'quality_score_sum':sum(r['quality_score'] for r in rows if r['iteration']==i)} for i in [1,2]},'by_behavior':{k:{'n':len([r for r in rows if r['behavior']==k]),'tokens':stats([r['total_tokens'] for r in rows if r['behavior']==k]),'elapsed_seconds':stats([r['elapsed_seconds'] for r in rows if r['behavior']==k])} for k in sorted({r['behavior'] for r in rows})},'score_counts':dict(collections.Counter(str(r['quality_score']) for r in rows)),'all_agent_total_tokens':sum(r['total_tokens'] for r in rows),'elapsed_seconds_sum':sum(r['elapsed_seconds'] for r in rows),'measurement_campaign_wall_seconds':b['ended_epoch']-a['started_epoch'],'batch_wall_seconds':[a['ended_epoch']-a['started_epoch'],b['ended_epoch']-b['started_epoch']],'max_workers':24,'read_bytes_total':sum(r['read_diagnostic']['serialized_tool_output_utf8_bytes'] for r in rows),'storage':storage(settings),'generic_layer4_registered':False,'in_dedicated_run_pool':False,'preflight_sha256':sha(settings/'preflight.json'),'internal_time_intervals':None}
 result['content_sha256']=identity_sha256(result);save(settings/'final-result-r2.json',result);print({k:result[k] for k in ['reasoning_effort','valid_runs','score_counts','all_agent_total_tokens','elapsed_seconds_sum','measurement_campaign_wall_seconds']},flush=True)
if __name__=='__main__':main(sys.argv[1])
