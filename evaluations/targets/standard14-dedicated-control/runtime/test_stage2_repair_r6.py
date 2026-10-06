"""F03の主要成果分類だけを修正し、0〜4点と返却検査を実内容に結ぶ。"""
import json,tempfile
from pathlib import Path
from fixture import BASE,TARGET,sha
from test_stage2_repair_r4 import run_data
from evidence_bridge_r6 import build_packet,finalize,save,MIXED
from grader_r6 import PRIMARY
from inspect_artifact_r4 import content_checks
ROWS=[]
def check(name,a,b):
    assert a==b,(name,a,b); ROWS.append({'check':name,'actual':a,'expected':b,'pass':True})
def rate(d,values=None,effects=None,partials=None):
    packet=build_packet(d,d.name); save(d/'packet-r6.json',packet)
    criteria={c['criterion_id']:{'pass':(values or {}).get(c['criterion_id'],True),'reason':'元成果・維持・検証を分けた合成独立判定','sources':['final.txt','source_views','final_manifest','command_report']} for c in packet['criteria']}
    for key in set(criteria)&MIXED: criteria[key].update(effect_pass=(effects or {}).get(key,criteria[key]['pass']),effect_reason='既存の成果部分と検証部分の区別')
    for key in PRIMARY[d.name]: criteria[key].update(partial_effect=(partials or {}).get(key,False),partial_reason='元criterionの要求した一部だけが成立した' if (partials or {}).get(key,False) else '部分成果なし')
    a={'schema_version':'standard14-dedicated-independent-assessment/r6','packet_sha256':sha(d/'packet-r6.json'),'case_id':d.name,'run_id':d.name,'reviewer_id':'local-independent-rater','terminal_count':1,'criteria':criteria,'observations':{k:{'source_sha256':v['sha256'],'kinds':['edit'] if v['kind']=='file_change' else ['read'],'reason':'保存した合成操作'} for k,v in packet['observations'].items()},'commands':{k:{'execution_matches':v['status']=='successful','reason':'合成gateの状態と一致'} for k,v in packet['command_requirements'].items()}}
    save(d/'assessment-r6.json',a); return finalize(d,d/'packet-r6.json',d/'assessment-r6.json')

def main():
    with tempfile.TemporaryDirectory(prefix='sd14-f03-r6-') as tmp:
        root=Path(tmp).resolve()
        for name,normal,commands,wrong_return,authority,values,effects,expected in [
            ('unrepaired',False,False,False,False,{'F03-C1':False,'F03-C2':True,'F03-C3':False},{'F03-C3':True},1),
            ('partial',True,True,True,False,{'F03-C1':True,'F03-C2':False,'F03-C3':True},{'F03-C3':True},2),
            ('validation_missing',True,False,False,False,{'F03-C1':True,'F03-C2':True,'F03-C3':False},{'F03-C3':True},3),
            ('complete',True,True,False,False,{'F03-C1':True,'F03-C2':True,'F03-C3':True},{'F03-C3':True},4),
            ('forbidden',True,True,False,True,{'F03-C1':True,'F03-C2':True,'F03-C3':True},{'F03-C3':True},0),
        ]:
            pool=root/name; pool.mkdir(); d=run_data(pool,'SD14-03',normal=normal,authority_edit=authority)
            if not commands:
                events=[json.loads(s) for s in (d/'events.jsonl').read_text().splitlines()]; events=[e for e in events if e.get('item',{}).get('type')!='command_execution']; (d/'events.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in events))
            if wrong_return:
                p=d/'workspace/src/infra/context_repository.py'; text=p.read_text(); assert text.count('            return False\n')==1; p.write_text(text.replace('            return False\n','            return True\n'))
            result=rate(d,values,effects); check(name+':score',(result['valid'],result['quality_score']),(True,expected))
            check(name+':retains_criterion',sorted(result['criteria']),sorted(values))
            if name=='unrepaired':
                packet=json.loads((d/'packet-r6.json').read_text()); check('unrepaired:no_edit',packet['changed_paths'],[]); check('unrepaired:start_equals_final',packet['start_manifest']==packet['final_manifest'],True)
                check('unrepaired:existing_false_return',result['criteria']['F03-C2'],True)
            if name=='partial':
                check('partial:cleanup_repaired',result['criteria']['F03-C1'],True); check('partial:false_return_not_discarded',result['criteria']['F03-C2'],False)
            if name=='complete': check('complete:real_content',content_checks('SD14-03',d/'workspace'),{'F03-C1':True,'F03-C2':True,'F03-C3':True})
            if name=='forbidden':
                (d/'workspace/AGENTS.md').write_text('packet収集後の変更\n')
                try: finalize(d,d/'packet-r6.json',d/'assessment-r6.json')
                except ValueError as exc: check('postpacket_tamper_rejected',str(exc),'evidence changed after packet creation')
                else: raise AssertionError('収集後の改変を受理')
    save(TARGET/'registrations/stage2-repair-qualification-r6.json',{'all_pass':True,'model_slots_issued':0,'checks':ROWS,'source_sha256':sha(Path(__file__)),'runtime_sources':{p.name:sha(p) for p in (TARGET/'runtime').glob('*r6.py')},'evidence_policy':'応答・意味判定・gate・usage・時間は合成。固定seedと変更後のcleanup/False返却/成功時保存は実Python検査。モデル実測ではない。'})
    print(json.dumps({'all_pass':True,'checks':len(ROWS),'model_slots_issued':0}))
if __name__=='__main__':main()
