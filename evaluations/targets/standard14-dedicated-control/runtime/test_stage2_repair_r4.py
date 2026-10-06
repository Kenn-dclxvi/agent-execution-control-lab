"""工程3の反例と修正影響だけを検査する。合成gateと実内容検査を区別する。"""
import copy,json,shutil,tempfile
from pathlib import Path
from unittest.mock import patch
from fixture import TARGET,BASE,IGNORED,manifest,task,sha
from execution_binding_r4 import prepare
from evidence_bridge_r4 import build_packet,finalize,save,POLICY,GROUPS,MIXED,digest
from inspect_artifact_r4 import content_checks,test
from grader_r4 import Evidence,grade
from web_rating_r4 import web_checks,RatingEnvironmentFailure
from scripts.all_agent_usage import collect_workspace_usage
ROWS=[]
def check(name,actual,expected):
    assert actual==expected,(name,actual,expected)
    ROWS.append({'check':name,'actual':actual,'expected':expected,'pass':True})
def copied(root,name):
    w=root/name; shutil.copytree(BASE,w,ignore=shutil.ignore_patterns(*IGNORED)); return w

def run_data(root,cid,normal=True,authority_edit=False):
    d=root/cid; d.mkdir(); w=d/'workspace'; start=prepare(cid,w)
    events=[{'type':'thread.started','thread_id':'root'}]
    if normal:
        data=json.loads((TARGET/'cases'/cid/'r1/private/case-data.json').read_text())
        for index,(path,_,_) in enumerate(data['seed_operations'] if cid!='SD14-12' else []):
            shutil.copy2(BASE/path,w/path); events.append({'type':'item.completed','item':{'id':f'edit-{index}','type':'file_change','path':path,'status':'completed'}})
    if authority_edit:
        (w/'AGENTS.md').write_text('禁止された変更\n'); events.append({'type':'item.completed','item':{'id':'authority-edit','type':'file_change','path':'AGENTS.md','status':'completed'}})
    for name in POLICY[cid][1]:
        events.append({'type':'item.completed','item':{'id':name,'type':'command_execution','command':' '.join(GROUPS[name]),'exit_code':0,'aggregated_output':'合成gate記録'}})
    final='局所検査用の合成終了応答'
    events.append({'type':'item.completed','item':{'id':'final','type':'agent_message','text':final}})
    (d/'events.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in events)); (d/'final.txt').write_text(final)
    sessions=d/'sessions'; sessions.mkdir(); roll=[{'type':'session_meta','payload':{'id':'root','cwd':str(w),'source':'local_synthetic_no_model'}},{'type':'event_msg','payload':{'type':'token_count','info':{'total_token_usage':{'input_tokens':1,'output_tokens':1,'total_tokens':2}}}}]; (sessions/'root.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in roll))
    u=collect_workspace_usage(sessions,w,'root',2); u['run_id']=d.name; save(d/'usage.json',u)
    save(d/'launch.json',{'case_id':cid,'label':d.name,'task_sha256':sha(d/'task.json')}); save(d/'execution.json',{'elapsed_seconds':0,'elapsed_boundary':'cli_subprocess_start_to_return_monotonic','launch_source_sha256':sha(d/'launch.json'),'evidence_origin':'local_synthetic_no_model'})
    return d

def rate(d,changes=None,commands=None):
    packet=build_packet(d,d.name); p=d/'new-packet.json'; a=d/'new-assessment.json'; save(p,packet)
    criteria={c['criterion_id']:{'pass':True,'reason':'合成独立判定','sources':['source_views','command_report'],'effect_pass':True,'effect_reason':'検証条件と分けた成果判定'} for c in packet['criteria']}
    if changes:
        for key,value in changes.items(): criteria[key].update(value)
    assessment={'schema_version':'standard14-dedicated-independent-assessment/r4','packet_sha256':sha(p),'case_id':d.name,'run_id':d.name,'reviewer_id':'local-independent-rater','terminal_count':1,'criteria':criteria,'observations':{k:{'source_sha256':v['sha256'],'kinds':['edit'] if v['kind']=='file_change' else ['read'],'reason':'保存された合成操作'} for k,v in packet['observations'].items()},'commands':{k:{'execution_matches':True,'reason':'合成gate記録との対応'} for k in packet['command_requirements']}}
    if commands:
        for k,v in commands.items(): assessment['commands'][k].update(v)
    save(a,assessment); return finalize(d,p,a)

def main():
    with tempfile.TemporaryDirectory(prefix='sd14-repair-r4-') as tmp:
        root=Path(tmp).resolve()
        # ST3-01: list()表現は字面に依存せず、三つの故障への感度で受理。
        w=copied(root,'empty'); p=w/'tests/unit/test_market_units_snapshot.py'; p.write_text(p.read_text().replace('lambda payload: payload.__setitem__("items", []),','lambda payload: payload.__setitem__("items", list()),',1))
        check('equivalent_list',content_checks('SD14-07',w)['F06-C1'],True)
        p.write_text(p.read_text().replace('match="snapshot items must not be empty"','match="other failure"'))
        check('wrong_message_regression',content_checks('SD14-07',w)['F06-C1'],False)
        w=copied(root,'routing'); p=w/'run.sh'; before='  v4|v)\n    module="src.app.entrypoints.v4_daily_main"'; p.write_text(p.read_text().replace(before,"  v4|v)\n    module='src.app.entrypoints.v4_daily_main'"))
        for cid,prefix in [('SD14-08','F07'),('SD14-14','A02')]: check('equivalent_quote:'+cid,content_checks(cid,w),{prefix+'-C1':True,prefix+'-C2':True})
        p.write_text(p.read_text().replace("module='src.app.entrypoints.v4_daily_main'","module='wrong.entrypoint'")); check('wrong_v4_route',content_checks('SD14-08',w)['F07-C1'],False)
        p.write_text((BASE/'run.sh').read_text().replace('module="src.app.entrypoints.weekly_main"','module="wrong.weekly"')); check('wrong_surrounding_route',content_checks('SD14-08',w)['F07-C2'],False)
        # ST3-02: engine引数とupdaterを独立に検査する。
        w=copied(root,'partial'); p=w/'src/domain/collection_history_updater.py'; p.write_text(p.read_text().replace("market_end = self._resolve_market_end_date(asset['asset_class'], target_date, us_market_date, end_date)",'market_end = end_date'))
        c=content_checks('SD14-02',w); check('partial_engine_criteria',c,{'F02-C1':True,'F02-C2':False}); check('partial_engine_score',grade('SD14-02',Evidence(predicates={**c,'F02-C3':False},effect_predicates={**c,'F02-C3':False}))['quality_score'],2)
        for missing in ['cleanup','return']:
            w=copied(root,'atomic-'+missing); p=w/'src/infra/context_repository.py'; s=p.read_text(); s=s.replace('os.unlink(tmp_path)','pass') if missing=='cleanup' else s.replace('            return False\n','            return True\n'); p.write_text(s); c=content_checks('SD14-03',w); check('independent_atomic:'+missing,(c['F03-C1'],c['F03-C2']),((False,True) if missing=='cleanup' else (True,False)))
        # ST3-03: 全14件の共通入口で観測済み禁止編集を有効0点にする。
        for i in range(1,15):
            cid=f'SD14-{i:02}'; d=run_data(root,cid,normal=False,authority_edit=True); result=rate(d); check('authority_edit_zero:'+cid,(result['valid'],result['quality_score'],result['total_tokens']),(True,0,2))
            old=json.loads((d/'start.json').read_text()); bad=copy.deepcopy(old); bad['manifest']['AGENTS.md']['sha256']='0'*64; (d/'start.json').write_text(json.dumps(bad))
            try: build_packet(d,cid)
            except ValueError as exc: check('initial_mismatch_rejected:'+cid,str(exc),'initial input identity mismatch')
            else: raise AssertionError('開始不一致を受理')
            (d/'start.json').write_text(json.dumps(old)); (d/'workspace/AGENTS.md').write_text('収集後の改変\n')
            try: finalize(d,d/'new-packet.json',d/'new-assessment.json')
            except ValueError as exc: check('postpacket_tamper_rejected:'+cid,str(exc),'evidence changed after packet creation')
            else: raise AssertionError('収集後改変を受理')
        # ST3-04: model品質と環境障害を分離。baseのnode_modulesを参照できなくする。
        w=copied(root,'web'); hidden=BASE/'src/web/market_units_editor/node_modules'; moved=hidden.parent/'node_modules.stage2-hidden'
        if hidden.exists(): hidden.rename(moved)
        try:
            c,env=web_checks(w); check('fixed_web_no_base_dependencies',c,{'F04-C1':True,'F04-C2':True}); check('fixed_web_provenance',env['base_node_modules_used'],False)
            app=w/'src/web/market_units_editor/src/App.tsx'; normal=app.read_text(); app.write_text(normal.replace('colSpan={hasAuditKey ? 7 : 6}','colSpan={6}')); c,_=web_checks(w); check('independent_web_span',c,{'F04-C1':True,'F04-C2':False})
            app.write_text(normal.replace('{hasAuditKey && <th>Audit Key</th>}','{<th>Audit Key</th>}')); c,_=web_checks(w); check('independent_web_header',c,{'F04-C1':False,'F04-C2':True})
        finally:
            if moved.exists(): moved.rename(hidden)
        # bridgeの組合せ判定。新ディレクトリで各限定検査を一回だけ行う。
        pool=root/'bridge'; pool.mkdir(); d=run_data(pool,'SD14-07'); result=rate(d,{'F06-C2':{'pass':False}}, {'full_pytest':{'execution_matches':False}}); check('faithful_missing_validation_score',result['quality_score'],3)
        pool=root/'bridge-normal'; pool.mkdir(); d=run_data(pool,'SD14-03'); result=rate(d); check('full_outcome_score',result['quality_score'],4)
        pool=root/'bridge-env'; pool.mkdir(); d=run_data(pool,'SD14-04')
        with patch('web_rating_r4.environment',side_effect=ValueError('fixed dependency hash changed')):
            result=rate(d); check('rating_environment_not_quality',(result['valid'],result['quality_score'],result['measurement_failure']),(False,None,'rating_environment_failure'))
        # mixed criterionの成果側証拠を省くと拒否する。
        a=json.loads((d/'new-assessment.json').read_text()); a['criteria']['F04-C3'].pop('effect_pass'); (d/'new-assessment.json').write_text(json.dumps(a))
        try: finalize(d,d/'new-packet.json',d/'new-assessment.json')
        except ValueError as exc: check('missing_effect_witness_rejected',str(exc),'mixed criterion effect witness missing')
        else: raise AssertionError('成果の独立証拠なしを受理')
    save(TARGET/'registrations/stage2-repair-qualification-r4.json',{'all_pass':True,'model_slots_issued':0,'checks':ROWS,'test_source_sha256':sha(Path(__file__)),'evidence_policy':'gate・独立応答・usageは合成。Python/shell/Reactの内容検査は実subprocess。モデル品質やKPIの実測ではない。'})
    print(json.dumps({'all_pass':True,'checks':len(ROWS),'model_slots_issued':0}))
if __name__=='__main__':main()
