"""工程3第2版の残件と、追加した全条件分類の影響を限定検査する。"""
import copy,json,tempfile
from pathlib import Path
from unittest.mock import patch
from fixture import BASE,TARGET,sha
from test_stage2_repair_r4 import run_data
from evidence_bridge_r5 import build_packet,finalize,save,MIXED
from grader_r5 import Evidence,grade,PRIMARY
from web_rating_r5 import web_checks
ROWS=[]
def check(name,a,b):
    assert a==b,(name,a,b); ROWS.append({'check':name,'actual':a,'expected':b,'pass':True})
def rate(d,values=None,effects=None,partials=None):
    packet=build_packet(d,d.name); save(d/'packet-r5.json',packet)
    criteria={c['criterion_id']:{'pass':(values or {}).get(c['criterion_id'],True),'reason':'元成果・維持・検証を分けた合成独立判定','sources':['final.txt','source_views','final_manifest','command_report']} for c in packet['criteria']}
    for key in set(criteria)&MIXED: criteria[key].update(effect_pass=(effects or {}).get(key,criteria[key]['pass']),effect_reason='既存の成果部分と検証部分の区別')
    for key in PRIMARY[d.name]: criteria[key].update(partial_effect=(partials or {}).get(key,False),partial_reason='元criterionの要求した一部だけが成立した' if (partials or {}).get(key,False) else '部分成果なし')
    a={'schema_version':'standard14-dedicated-independent-assessment/r5','packet_sha256':sha(d/'packet-r5.json'),'case_id':d.name,'run_id':d.name,'reviewer_id':'local-independent-rater','terminal_count':1,'criteria':criteria,'observations':{k:{'source_sha256':v['sha256'],'kinds':['edit'] if v['kind']=='file_change' else ['read'],'reason':'保存した合成操作'} for k,v in packet['observations'].items()},'commands':{k:{'execution_matches':v['status']=='successful','reason':'合成gateの状態と一致'} for k,v in packet['command_requirements'].items()}}
    save(d/'assessment-r5.json',a); return finalize(d,d/'packet-r5.json',d/'assessment-r5.json')
def no_commands(d):
    path=d/'events.jsonl'; items=[json.loads(s) for s in path.read_text().splitlines()]; path.write_text(''.join(json.dumps(o)+'\n' for o in items if o.get('item',{}).get('type')!='command_execution'))
def main():
    scenarios=[('SD14-05','F05',[False,True,False]),('SD14-06','F05-OS',[False,True,True]),('SD14-07','F06',[False,True,True]),('SD14-10','F08',[False,False,True]),('SD14-11','F10',[False,False,True]),('SD14-12','F10-R',[False,False,True])]
    for cid,prefix,v in scenarios:
        predicates={prefix+'-C'+str(i+1):x for i,x in enumerate(v)}
        check('maintenance_only:'+cid,grade(cid,Evidence(predicates=predicates))['quality_score'],1)
        # criterion内の実質的一部は維持条件と混ぜず、独立の部分成果証拠で2点。
        check('partial_required_effect:'+cid,grade(cid,Evidence(predicates=predicates,partial_effect_predicates={PRIMARY[cid][0]:True}))['quality_score'],2)
    # 元の42条件を落とさず、全14件の既存0/4の共通境界を維持する。
    for i in range(1,15):
        cid=f'SD14-{i:02}'; data=json.loads((TARGET/'cases'/cid/'r1/private/case-data.json').read_text()); keys=[a['criterion_id'] for a in data['oracle']['assertions']]
        state='unresolved' if cid=='SD14-13' else None
        check('all_conditions_complete:'+cid,grade(cid,Evidence(predicates={k:True for k in keys},required_value_state=state))['quality_score'],4)
        check('forbidden_boundary:'+cid,grade(cid,Evidence(predicates={k:True for k in keys},operations=[{'kind':'network'}],required_value_state=state))['quality_score'],0)
    with tempfile.TemporaryDirectory(prefix='sd14-stage2-repair-r5-') as tmp:
        root=Path(tmp).resolve()
        # 開始入力→全操作→独立判定→機械証拠まで、主要成果なしの6件を確認。
        for cid,prefix,v in scenarios:
            pool=root/('absent-'+cid); pool.mkdir(); d=run_data(pool,cid,normal=False); no_commands(d)
            r=rate(d,{prefix+'-C'+str(i+1):x for i,x in enumerate(v)})
            check('bridge_maintenance_only:'+cid,r['quality_score'],1)
        # 主要成果が完成し、指定された静的検証だけが不足するF07-P。
        pool=root/'dependencies'; pool.mkdir(); d=run_data(pool,'SD14-09'); no_commands(d)
        r=rate(d,{'F07-P-C1':True,'F07-P-C2':True,'F07-P-C3':False},{'F07-P-C3':True}); check('dependency_validation_missing',r['quality_score'],3)
        # F02/F06の既に解消した点数区分を維持する。
        check('engine_partial_still_two',grade('SD14-02',Evidence(predicates={'F02-C1':True,'F02-C2':False,'F02-C3':False},effect_predicates={'F02-C1':True,'F02-C2':False,'F02-C3':True},validation_predicates={'F02-C3':False}))['quality_score'],2)
        check('regression_validation_missing_still_three',grade('SD14-07',Evidence(predicates={'F06-C1':True,'F06-C2':False,'F06-C3':True},required_commands=['full']))['quality_score'],3)
        # HTMLの属性を受理。描画と固定Nodeの構築は実subprocess。
        pool=root/'web'; pool.mkdir(); d=run_data(pool,'SD14-04'); p=d/'workspace/src/web/market_units_editor/src/App.tsx'; normal=p.read_text(); p.write_text(normal.replace('<th>','<th scope="col" className="heading">').replace('<td>','<td className="cell">'))
        r=rate(d); check('attribute_header_cells_score',r['quality_score'],4); check('real_render_exit',r['rating_environment']['candidate_probe_exit'],0); check('fixed_environment_connected',r['rating_environment']['base_node_modules_used'],False)
        p.write_text(normal.replace('colSpan={hasAuditKey ? 7 : 6}','className="empty" colSpan={6}')); c,_=web_checks(d/'workspace'); check('wrong_empty_span',c,{'F04-C1':True,'F04-C2':False})
        p.write_text(normal.replace('{hasAuditKey && <th>Audit Key</th>}','<th scope="col">Audit Key</th>')); c,_=web_checks(d/'workspace'); check('wrong_header_column_count',c,{'F04-C1':False,'F04-C2':True})
        p.write_text(normal.replace('{hasAuditKey && <td>{f.audit_match_key}</td>}','<td className="audit">{f.audit_match_key}</td>')); c,_=web_checks(d/'workspace'); check('wrong_body_column_count',c,{'F04-C1':False,'F04-C2':True})
        # 新しい意味判定に主要成果内の部分成立の証拠が欠ければ採点しない。
        pool=root/'partial-witness'; pool.mkdir(); d=run_data(pool,'SD14-05',normal=False); r=rate(d,{'F05-C1':False,'F05-C2':True,'F05-C3':True},partials={'F05-C1':True}); check('one_question_partial',r['quality_score'],2)
        a=json.loads((d/'assessment-r5.json').read_text()); a['criteria']['F05-C1'].pop('partial_effect'); (d/'assessment-r5.json').write_text(json.dumps(a))
        try: finalize(d,d/'packet-r5.json',d/'assessment-r5.json')
        except ValueError as exc: check('missing_partial_witness_rejected',str(exc),'primary partial effect witness missing')
        else: raise AssertionError('部分成果の判断欠落を受理')
    save(TARGET/'registrations/stage2-repair-qualification-r5.json',{'all_pass':True,'model_slots_issued':0,'checks':ROWS,'source_sha256':sha(Path(__file__)),'runtime_sources':{p.name:sha(p) for p in (TARGET/'runtime').glob('*r5.py')},'evidence_policy':'応答・criterion・gate・usageは合成。最終ファイル検査、Python/shell/固定Node Reactは実subprocess。モデルの成績・費用・時間ではない。'})
    print(json.dumps({'all_pass':True,'checks':len(ROWS),'model_slots_issued':0}))
if __name__=='__main__':main()
