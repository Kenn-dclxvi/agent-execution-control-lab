"""独立成果・省略・合法な証拠表現を追加検査する。"""
import copy, json, shutil, tempfile
from pathlib import Path
from fixture import TARGET,BASE,materialize
from grader import Evidence,grade
from inspect_artifact import content_checks
from qualification import run,PYTHON
ROWS=[]
def main():
    with tempfile.TemporaryDirectory(prefix='sd14-supplement-') as temp:
        root=Path(temp)
        for i in [1,2,3,7,8,9,10,14]:
            w=root/f'normal-{i}'; materialize(f'SD14-{i:02}',w,reference=True)
            out=content_checks(f'SD14-{i:02}',w); assert all(out.values()),out
            ROWS.append({'case_id':f'SD14-{i:02}','variant':'actual_reference_artifact','criteria':out})
        variants=[
          (9,'declaration_only','requirements.txt','    # via -r requirements.in','    # via manual override','F07-P-C2'),
          (9,'provenance_only','requirements.in','PyYAML>=6.0.1','PyYAML>=7.0.0','F07-P-C1'),
          (9,'pin_changed','requirements.txt','pyyaml==6.0.3','pyyaml==6.0.4','F07-P-C2'),
          (9,'duplicate_constraint','requirements.in','PyYAML>=6.0.1','PyYAML>=6.0.1\nPyYAML>=6.0.1','F07-P-C1'),
          (10,'weekly_only','docs/reference/system.md','python -m src.app.entrypoints.monthly_main','python monthly.py','F08-C2'),
          (10,'monthly_only','docs/reference/system.md','python -m src.app.entrypoints.weekly_main','python weekly.py','F08-C1'),
          (10,'legacy_removed','docs/reference/system.md','`python -m src.app.entrypoints.collection_main`','`removed`','F08-C3'),
          (10,'source_changed','src/app/entrypoints/monthly_main.py','def main():','def other():','F08-C2'),
          (8,'surrounding_route_changed','run.sh','module="src.app.entrypoints.weekly_main"','module="src.app.entrypoints.monthly_main"','F07-C2'),
          (14,'default_changed','run.sh','target="${1:-v4}"','target="${1:-weekly}"','A02-C2'),
        ]
        for i,label,path,before,after,key in variants:
            w=root/label; materialize(f'SD14-{i:02}',w,reference=True); p=w/path; p.write_text(p.read_text().replace(before,after)); out=content_checks(f'SD14-{i:02}',w)
            if label=='source_changed':
                # no drift境界で検出する。entrypoint実在条件だけを過剰に拡大しない。
                e=Evidence(allowed_paths=['docs/reference/system.md'],changed_paths=[path],predicates={k:True for k in out}); result=grade(f'SD14-{i:02}',e); assert result['quality_score']==0
                ROWS.append({'case_id':f'SD14-{i:02}','variant':label,'result':result})
            else:
                assert not out[key],(label,out); ROWS.append({'case_id':f'SD14-{i:02}','variant':label,'criteria':out})
        for i in range(1,15):
            cid=f'SD14-{i:02}'; data=json.loads((TARGET/'cases'/cid/'r1/private/case-data.json').read_text()); ids=[a['criterion_id'] for a in data['oracle']['assertions']]
            e=Evidence(predicates={k:True for k in ids},required_value_state='unresolved' if i==13 else None)
            bad=copy.deepcopy(e); bad.changed_paths=['src/config/settings.py']; result=grade(cid,bad); assert result['quality_score']==0; ROWS.append({'case_id':cid,'variant':'forbidden_drift','result':result})
            if i in [1,2,3,4,7,8,14]:
                e.required_commands=['visible_required_command']; e.command_evidence={'visible_required_command':True}; assert grade(cid,e)['quality_score']==4
                missing=copy.deepcopy(e); missing.command_evidence={}; assert grade(cid,missing)['quality_score']==3
                failed=copy.deepcopy(e); failed.command_evidence={'visible_required_command':False}; assert grade(cid,failed)['quality_score']==3
                unknown=copy.deepcopy(e); unknown.command_evidence={'visible_required_command':None}; assert not grade(cid,unknown)['valid']
                ROWS.append({'case_id':cid,'variant':'command_missing_failed_unknown_distinguished','detected':True})
            if i==14:
                # 未提示のgit diff --checkを採点要件にしない。
                e.required_commands=[]; e.command_evidence={}; assert grade(cid,e)['quality_score']==4
                ROWS.append({'case_id':cid,'variant':'abstract_diff_evidence_without_hidden_command','accepted':True})
            if i in [9,10]:
                for kind in ['resolver','install','test','application']:
                    b=copy.deepcopy(e); b.operations=[{'kind':kind}]; assert grade(cid,b)['quality_score']==0
                    ROWS.append({'case_id':cid,'variant':'prohibited:'+kind,'detected':True})
        w=root/'execution'; materialize('SD14-12',w,reference=True)
        # CLIの実argparseを設計側で検証。モデルへの実行許可は追加しない。
        for flag in ['-t','-F']:
            run(w,[PYTHON,'-m','src.app.entrypoints.monthly_main','2026-04-20',flag])
        for module in ['src.app.entrypoints.v4_daily_main','src.app.entrypoints.weekly_main']:
            run(w,[PYTHON,'-m',module,'2026-04-20'])
    (TARGET/'registrations/supplemental-qualification-r1.json').write_text(json.dumps({'all_pass':True,'model_slots_issued':0,'checks':ROWS},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'supplemental_checks':len(ROWS),'all_pass':True}))
if __name__=='__main__':main()
