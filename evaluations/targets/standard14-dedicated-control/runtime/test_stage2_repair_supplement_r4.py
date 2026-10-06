"""主要成果・検証不足の組合せと最終版の開始識別を補足する。"""
import ast,copy,json,tempfile
from pathlib import Path
from fixture import BASE,TARGET,sha
from evidence_bridge_r4 import build_packet,finalize,save
from grader_r4 import Evidence,grade
from inspect_artifact_r4 import content_checks
from test_stage2_repair_r4 import run_data,rate,copied
ROWS=[]
def check(name,a,b):
    assert a==b,(name,a,b); ROWS.append({'check':name,'actual':a,'expected':b,'pass':True})
def main():
    with tempfile.TemporaryDirectory(prefix='sd14-repair-supplement-') as tmp:
        root=Path(tmp).resolve()
        d=run_data(root,'SD14-02'); updater=d/'workspace/src/domain/collection_history_updater.py'; data=json.loads((TARGET/'cases/SD14-02/r1/private/case-data.json').read_text())
        for path,before,after in data['seed_operations']:
            if path=='src/domain/collection_history_updater.py': updater.write_text(updater.read_text().replace(before,after))
        r=rate(d,{'F02-C2':{'pass':False},'F02-C3':{'pass':False,'effect_pass':True}}); check('bridge_engine_only_partial',r['quality_score'],2)
        check('no_primary_effect_not_promoted_by_preservation',grade('SD14-02',Evidence(predicates={'F02-C1':False,'F02-C2':False,'F02-C3':False},effect_predicates={'F02-C1':False,'F02-C2':False,'F02-C3':True},validation_predicates={'F02-C3':False}))['quality_score'],1)
        for case,prefix in [('SD14-01','F01'),('SD14-02','F02'),('SD14-03','F03'),('SD14-04','F04'),('SD14-08','F07'),('SD14-14','A02')]:
            predicates={prefix+'-C1':True,prefix+'-C2':True,prefix+'-C3':False}; effects={k:True for k in predicates}
            check('major_effect_validation_only:'+case,grade(case,Evidence(predicates=predicates,effect_predicates=effects,validation_predicates={prefix+'-C3':False},required_commands=['full'],command_evidence={}))['quality_score'],3)
        # classに配置する同等テストもmutation感度で受理する。
        w=copied(root,'class-regression'); p=w/'tests/unit/test_market_units_snapshot.py'; text=p.read_text(); start=text.index('def test_snapshot_empty_items_is_invalid('); node=next(n for n in ast.parse(text).body if isinstance(n,ast.FunctionDef) and n.name=='test_snapshot_empty_items_is_invalid'); end=sum(len(line) for line in text.splitlines(keepends=True)[:node.end_lineno]); fn=text[start:end]; fn=fn.replace('def test_snapshot_empty_items_is_invalid(', 'def test_snapshot_empty_items_is_invalid(self, ',1); p.write_text(text[:start]+'class TestSnapshotEmpty:\n'+''.join('    '+line+'\n' for line in fn.splitlines())+text[end:]); check('equivalent_class_regression',content_checks('SD14-07',w)['F06-C1'],True)
        start=json.loads((d/'start.json').read_text()); start['case_id']='SD14-03'; (d/'start.json').write_text(json.dumps(start))
        try: build_packet(d,'SD14-02')
        except ValueError as exc: check('start_case_swap_rejected',str(exc),'start case identity mismatch')
        else: raise AssertionError('開始case取り違えを受理')
    sources={p.name:sha(p) for p in (TARGET/'runtime').glob('*r4.py')}
    save(TARGET/'registrations/stage2-repair-supplement-r4.json',{'all_pass':True,'model_slots_issued':0,'checks':ROWS,'implementation_sources':sources,'evidence_policy':'gateと意味判定は合成。内容検査は実subprocess。工程3の合格を主張しない。'})
    print(json.dumps({'all_pass':True,'checks':len(ROWS),'model_slots_issued':0}))
if __name__=='__main__':main()
