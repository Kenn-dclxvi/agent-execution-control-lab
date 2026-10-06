"""新系列の初回28件を不変保存し、全担当usage・時間・配送・保存量を集計する。"""
import collections, datetime, hashlib, json, os, statistics, sys
from pathlib import Path
from types import SimpleNamespace
from fixture import TARGET, sha, manifest
from evidence_bridge_r6 import save, load
from stage4_campaign_r2 import ROOT, REPO
sys.path.insert(0,str(REPO))
from scripts.atomic_run_registry import build_record, load_pool, write_or_verify, select_runs, aggregate_selection
from scripts.evaluation_loop import TOKEN_ACCOUNTING, identity_sha256

def main():
    pre=load(ROOT/'preflight-r4.json');pool=load_pool(ROOT/'atomic-registry',pre['atomic_pool_key']);slots=[s for batch in pre['batches'] for s in batch]
    assert len(slots)==28
    developer_hashes=['dfe6cbc895d83f791ff27a34290681efbfd78af8b952122823d3bfc705b0ac39','2a9df9db8c89ecb8b44c695a5fba7b6b4f9c18a160286fd9fbc2381fdc6a6552','6ded806e3cdbb35599ecaf8742574bc5274908472b1729090010c404c2151e8e']
    rows=[];atomic=[];diagnostics=[]
    for slot in slots:
        cid=slot['case_id'];run=ROOT/'cases'/cid/'runs'/slot['label'];q=load(run/'quality-result-r6.json');p=load(run/'rating-packet.json');usage=load(run/'usage.json');launch=load(run/'launch.json')
        assert q['valid'] and q['evidence_origin']=='measured' and q['packet_sha256']==sha(run/'rating-packet.json')
        assert launch['task_sha256']==pre['identities'][cid]['task_sha256']
        assert p['start_manifest']==pre['identities'][cid]['manifest'] and p['final_manifest']==manifest(run/'workspace')
        assert usage['all_agent_total_tokens']==sum(s['usage']['total_tokens'] for s in usage['sessions'])==q['total_tokens']
        assert len(usage['sessions'])==usage['session_count']
        assert not (run/'codex-home/auth.json').exists() and (run/'codex-home/config.toml').stat().st_size==0
        isolation=load(run/'instruction-isolation-before.json'); assert isolation['model_catalog_sha256']==pre['model_catalog_delivery']['source_sha256'] and isolation['root_agents_bytes']==0 and not isolation['ancestor_instruction_files']
        tool_bytes=0;outputs=[];tools=[];turns=[];root_developers=[]
        for s in usage['sessions']:
            meta=None
            for l in Path(s['rollout_file']).open():
                obj=json.loads(l);data=obj['payload']
                if obj['type']=='session_meta':meta=data
                if obj['type']=='turn_context':
                    assert data['model']=='gpt-6-astra' and data['effort']=='low' and data['approval_policy']=='never' and data['sandbox_policy']['network_access'] is False
                    turns.append({'thread_id':s['thread_id'],'model':data['model'],'reasoning':data['effort'],'network_access':False,'record_sha256':hashlib.sha256(l.encode()).hexdigest()})
                if obj['type']=='response_item':
                    if data.get('type') in ['function_call_output','custom_tool_call_output']:
                        body=data.get('output','');raw=(body if isinstance(body,str) else json.dumps(body,ensure_ascii=False)).encode();tool_bytes+=len(raw);outputs.append(hashlib.sha256(raw).hexdigest())
                    if data.get('type') in ['function_call','custom_tool_call']:
                        tools.append(data.get('name'))
                    if data.get('type')=='message' and data.get('role')=='developer' and s['thread_id']==usage['root_thread_id']:
                        t=''.join(c.get('text','') for c in data.get('content',[]));t=t.replace(str(run/'codex-home'),'<RUN_HOME>').replace(str(run/'workspace'),'<WORKSPACE>');root_developers.append(hashlib.sha256(t.encode()).hexdigest())
            assert hashlib.sha256(meta['base_instructions']['text'].encode()).hexdigest()==pre['conditions']['agent_environment']['base_instructions_sha256']
        assert root_developers==developer_hashes
        # A02の任意の追加routing検査と--help起動は、読取りとは別の動作診断として補足する。
        supplements={}
        if cid=='SD14-14' and slot['iteration']==2:
            for key,o in p['observations'].items():
                record=o['records'][-1];item=record.get('item',{});payload=record.get('payload',{});text=item.get('command') or payload.get('input') or payload.get('arguments') or ''
                kinds=[]
                if 'routing-check' in text:kinds.append('test')
                if '-m src.app.entrypoints.v4_daily_main --help' in text:kinds.append('application')
                if kinds:supplements[key]={'source_sha256':o['sha256'],'kinds':kinds,'reason':'実行部分をstubにしたrouting検査と正規入口の--help起動。許可内で、点数には変更を加えない。'}
        behavior= q.get('observed_route','completed')
        if cid=='SD14-05':behavior='clarification_stop'
        if cid=='SD14-06':behavior='out_of_scope_stop'
        if cid in ['SD14-11','SD14-12']:behavior='read_only_review'
        rid=f'standard14-dedicated-low-20261004-{cid}-i{slot["iteration"]}'
        source_hashes={name:sha(run/name) for name in ['start.json','launch.json','run.json','usage.json','events.jsonl','final.txt','command-evidence.json','execution.json','rating-packet.json','independent-assessment-r1.json','quality-result-r6.json','wall-clock.json']}
        row={'run_id':rid,'local_run_id':slot['label'],'sample_id':slot['sample_id'],'case_id':cid,'iteration':slot['iteration'],'valid':True,'quality_score':q['quality_score'],'criteria':q['criteria'],'behavior':behavior,'total_tokens':q['total_tokens'],'elapsed_seconds':q['elapsed_seconds'],'session_count':usage['session_count'],'cached_input_tokens':sum(s['usage'].get('cached_input_tokens',0) for s in usage['sessions']),'changed_paths':p['changed_paths'],'command_requirements':{k:v['status'] for k,v in p['command_requirements'].items()},'raw_evidence_directory':str(run),'source_hashes':source_hashes,'model_delivery_verification':{'task_source_sha256':launch['task_sha256'],'initial_catalog_source_sha256':isolation['model_catalog_sha256'],'base_instructions_match':True,'normalized_developer_hashes':root_developers,'model_turns':turns},'read_diagnostic':{'serialized_tool_output_utf8_bytes':tool_bytes,'tool_output_count':len(outputs),'exact_repeated_output_count':len(outputs)-len(set(outputs)),'observed_tool_names':sorted(set(tools)),'limitation':'配送された保存tool出力のUTF-8量。意味上の読了量やtoken量ではない。'},'operation_supplements':supplements}
        rows.append(row)
        effective=dict(pool['effective_conditions_by_case'][cid]);fixture=effective.pop('fixture');effective.pop('case_id')
        record=build_record(run_id=rid,prompt_identity=pool['prompt_set_identity'],case_id=cid,fixture=fixture,effective_common=effective,provenance={'max_workers':24,'batch':0 if int(cid[-2:])<=12 else 1,'dispatch_iteration':slot['iteration']},sample_id=slot['sample_id'],accounting=TOKEN_ACCOUNTING,quality_score=q['quality_score'],total_tokens=q['total_tokens'],elapsed_seconds=q['elapsed_seconds'],source={'kind':'standard14_dedicated_stage4_measured','raw_evidence_directory':str(run),'source_hashes':source_hashes,'measurement_gate':'28件の実測成立と保存証拠を工程4で確認。bridge単体の非登録状態は上書きしない。'})
        assert record['comparison_block_key']==pool['comparison_block_keys'][cid]
        write_or_verify(ROOT/'atomic-registry/runs'/f"{record['atomic_run_id']}.json",record,{'registered_at','record_content_sha256'});atomic.append(record['atomic_run_id'])
        # CLI全区間をKPIとして保持し、0.159.0で未観測の内部区間を補完しない。
        diagnostics.append({'run_id':rid,'contract':'execution-time-recording/r1','elapsed_seconds':q['elapsed_seconds'],'elapsed_boundary':'cli_subprocess_start_to_return_monotonic','clock':'fixed_executor_perf_counter','startup_seconds':None,'work_seconds':None,'shutdown_seconds':None,'interval_evidence_class':'unavailable','missing_reasons':['initial_input_delivery_not_observable','monotonic_clock_mapping_unavailable','subinterval_collector_does_not_support_0.159.0'],'source_sha256':source_hashes['run.json']})
    registry=ROOT/'atomic-registry';selection=ROOT/'selection-n2.json'
    select_runs(SimpleNamespace(registry=str(registry),pool_key=pool['pool_key'],count=2,case_id=None,output=str(selection)))
    aggregate_selection(SimpleNamespace(registry=str(registry),selection=str(selection),output=str(ROOT/'analysis-n2.json')))
    batch0=load(ROOT/'batch-0-complete-r2.json');batch1=load(ROOT/'batch-1-complete-r2.json')
    def stats(values):return {'sum':sum(values),'mean':statistics.mean(values),'median':statistics.median(values),'maximum':max(values)}
    cases={cid:{'scores':[r['quality_score'] for r in rows if r['case_id']==cid],'tokens':stats([r['total_tokens'] for r in rows if r['case_id']==cid]),'elapsed_seconds':stats([r['elapsed_seconds'] for r in rows if r['case_id']==cid]),'behaviors':[r['behavior'] for r in rows if r['case_id']==cid]} for cid in pool['case_ids']}
    files=[p for p in ROOT.rglob('*') if p.is_file() and not p.is_symlink()];logical=sum(p.stat().st_size for p in files);allocated=sum(p.stat().st_blocks*512 for p in files)
    storage={'measurement_root':str(ROOT),'snapshot_before_result_export':True,'files':len(files),'logical_bytes':logical,'allocated_bytes_stat_blocks':allocated,'measured_peak_bytes':None,'peak_unobserved':True,'apfs_shared_physical_usage':None,'shared_python_logical_bytes_not_included':True,'note':'準備・固定fixture・個別workspace・独立Node cache・保存証拠の保持量。APFS clone共有分の専有物理量とは区別する。'}
    result={'schema_version':'standard14-dedicated-stage4-result/r1','result_id':'standard14-dedicated-free-astra-low-n2_2026-10-04-r1','target_id':'standard14-dedicated-control','set_id':'dedicated14-r1','prompt_set_identity':pool['prompt_set_identity'],'model':'gpt-6-astra','reasoning_effort':'low','actual_work_model':pre['actual_work_model'],'planned_slots':28,'model_slots_issued':28,'completed_model_slots':28,'valid_runs':28,'invalid_runs':0,'automatic_retries':0,'stage4_measurement_complete':True,'measurement_gate_pass':True,'score_counts':dict(collections.Counter(str(r['quality_score']) for r in rows)),'quality_score_mean':statistics.mean(r['quality_score'] for r in rows),'all_agent_total_tokens':sum(r['total_tokens'] for r in rows),'elapsed_seconds_sum':sum(r['elapsed_seconds'] for r in rows),'measurement_campaign_wall_seconds':batch1['ended_epoch']-batch0['started_epoch'],'batch_wall_seconds':[batch0['wall_elapsed_seconds'],batch1['wall_elapsed_seconds']],'between_batches_seconds':batch1['started_epoch']-batch0['ended_epoch'],'max_workers':24,'actual_batch_sizes':[24,4],'per_case':cases,'per_iteration':{str(i):{'quality_score_sum':sum(r['quality_score'] for r in rows if r['iteration']==i),'total_tokens':sum(r['total_tokens'] for r in rows if r['iteration']==i),'elapsed_seconds':sum(r['elapsed_seconds'] for r in rows if r['iteration']==i)} for i in [1,2]},'by_behavior':{b:{'n':len([r for r in rows if r['behavior']==b]),'total_tokens':sum(r['total_tokens'] for r in rows if r['behavior']==b),'elapsed_seconds':sum(r['elapsed_seconds'] for r in rows if r['behavior']==b)} for b in sorted({r['behavior'] for r in rows})},'cases':rows,'execution_preflight':'registrations/stage4-preflight-r4.json','execution_preflight_sha256':sha(TARGET/'registrations/stage4-preflight-r4.json'),'atomic':{'registry':str(registry),'pool_key':pool['pool_key'],'record_ids':atomic,'selection_sha256':sha(selection),'analysis_sha256':sha(ROOT/'analysis-n2.json'),'saved_individual_measured_runs':28,'generic_layer4_result_exported':False},'time_diagnostics':diagnostics,'storage':storage,'read_bytes_total':sum(r['read_diagnostic']['serialized_tool_output_utf8_bytes'] for r in rows),'limitations':['N2の中央値は2件の平均。再現率・将来保証として扱わない。','旧系列比較・難しさ同等性・低コスト認定は行わない。旧Node実行時点との同一性は未証明。','保存model catalog原本のSHAとAstra選択定義を固定。一覧の非対象model項目と日時の更新は別診断。','内部時間区間と実行中storage peakは未観測。推計で補完しない。','Medium/Highと旧素材の追加測定は未発行。'],'local_controller_failure':{'model_slots_issued':0,'prior_receipt':str(ROOT/'batch-0-complete.json'),'repair_revision':'stage4_campaign_r2.py','measurement_retry':False}}
    result['result_content_sha256']=identity_sha256(result)
    save(TARGET/'results'/f"{result['result_id']}.json",result)
    save(ROOT/'final-result-r1.json',result)
    save(TARGET/'registrations/stage4-output-verification-r1.json',{'schema_version':'standard14-dedicated-stage4-output-verification/r1','result_path':f"results/{result['result_id']}.json",'result_file_sha256':sha(TARGET/'results'/f"{result['result_id']}.json"),'result_content_sha256':result['result_content_sha256'],'quality_count':28,'all_agent_usage_count':28,'time_count':28,'atomic_record_count':28,'stage3_frozen_inputs_preserved':all(sha(Path(p))==h for p,h in pre['fixed_sources'].items()),'auth_remaining':len(list((ROOT/'cases').glob('*/authentication-source/auth.json')))+len(list((ROOT/'cases').glob('*/runs/*/codex-home/auth.json'))),'external_executor_source_modified':False,'commit_push_pr_merge':False,'measurement_complete':True})
    print(json.dumps({k:result[k] for k in ['stage4_measurement_complete','valid_runs','score_counts','all_agent_total_tokens','elapsed_seconds_sum','measurement_campaign_wall_seconds','actual_work_model']},ensure_ascii=False))

if __name__=='__main__':main()
