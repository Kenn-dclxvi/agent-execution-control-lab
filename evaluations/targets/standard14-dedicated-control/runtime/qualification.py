"""参照・seed・独立誤成果の局所検証を保存する。モデル発行なし。"""
import copy, hashlib, json, os, shutil, subprocess, tempfile, time
from pathlib import Path
from fixture import TARGET, BASE, SHARED, manifest, materialize, task, git, sha
from grader import Evidence, grade
REG=TARGET/'registrations'
RESULTS=[]
def run(w,args,expect=0):
    start=time.monotonic(); p=subprocess.run(args,cwd=w,text=True,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    row={'command':args,'exit_code':p.returncode,'elapsed_seconds':time.monotonic()-start,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest(),'expected_success':expect==0,'matched':(p.returncode==0)==(expect==0)}
    RESULTS.append(row)
    if not row['matched']: raise AssertionError((args,p.stdout[-3500:],p.stderr[-1000:]))
    return row
PYTHON=str(SHARED/'bin/python')
def pytests(w,select='tests/',success=True):
    return run(w,[PYTHON,'-m','pytest',select,'-q'],0 if success else 1)
def shell(w):
    run(w,['bash','-n','run.sh'])
    # mock interpreterでmoduleと引数を捕捉。Python/運用を起動しない。
    mock=w/'.venv'; mock.unlink(); (mock/'bin').mkdir(parents=True)
    p=mock/'bin/python'; p.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n'); p.chmod(0o755)
    outputs={}
    for alias in ['v4','v','weekly','w','monthly','m','2026-04-20','-F']:
        r=subprocess.run(['bash','run.sh',alias,'-u'],cwd=w,capture_output=True,text=True)
        assert r.returncode==0,(alias,r.stderr); outputs[alias]=r.stdout.splitlines()
    assert outputs['v4'][2]==outputs['v'][2]=='src.app.entrypoints.v4_daily_main'
    assert outputs['weekly'][2]==outputs['w'][2]=='src.app.entrypoints.weekly_main'
    assert outputs['monthly'][2]==outputs['m'][2]=='src.app.entrypoints.monthly_main'
    assert outputs['v4'][3:]==['-u']
    assert outputs['2026-04-20'][3:]==['2026-04-20','-u']
    for retired in ['daily','d','legacy','monex','collection','c']:
        r=subprocess.run(['bash','run.sh',retired],cwd=w,capture_output=True); assert r.returncode!=0
    shutil.rmtree(mock); mock.symlink_to(SHARED,target_is_directory=True)
    return outputs

def web(w):
    d=w/'src/web/market_units_editor'; cache=BASE/'src/web/market_units_editor/node_modules'
    if not (d/'node_modules').exists(): (d/'node_modules').symlink_to(cache,target_is_directory=True)
    probe=d/'probe.tsx'
    probe.write_text('''import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import App from './src/App';
const f={name:'A',asset_class:'US_STOCK',currency:'USD',units:'2',source_symbol:'X',csv_url:''};
for (const [funds,search,count,empty] of [[[],'',6,true],[[{...f,audit_match_key:'  '}],'',6,false],[[{...f,audit_match_key:'K'}],'',7,false],[[f,{...f,name:'B',audit_match_key:'K'}],'',7,false],[[{...f,audit_match_key:'K'}],'missing',7,true]] as const) {
 const html=renderToStaticMarkup(<App funds={[...funds]} search={search}/>);
 const headers=(html.match(/<th>/g)||[]).length;
 if(headers!==count) throw Error('header '+html);
 if(empty && !html.includes('colSpan="'+count+'"')) throw Error('span '+html);
 if(!empty) {
  const body=html.split('<tbody>')[1].split('</tbody>')[0];
  for(const row of body.match(/<tr.*?<\\/tr>/g)||[]) if((row.match(/<td>/g)||[]).length!==count) throw Error('cells '+html);
 }
}
console.log('five React rendering inputs passed');
''')
    r=subprocess.run([str(d/'node_modules/.bin/tsx'),'probe.tsx'],cwd=d,capture_output=True,text=True); probe.unlink(); return r

def main():
    REG.mkdir(exist_ok=True); identities={}; tests=[]; trace_tests=[]
    with tempfile.TemporaryDirectory(prefix='sd14-local-') as temp:
        root=Path(temp)
        for i in range(1,15):
            cid=f'SD14-{i:02}'; w=root/cid
            identity=materialize(cid,w); identities[cid]=identity
            raw=task(cid,identity['seed_commit']); identities[cid]['task_sha256']=hashlib.sha256(raw).hexdigest()
            if i==12:
                old=(TARGET/'cases'/cid/'r1/trial-prompt-input.json').read_bytes()
                assert raw.replace(identity['seed_commit'].encode(),b'a53601614b41f52633f1d75e77c72861a0f0f1c8')==old
                assert identity['seed_commit']!=git(w,'rev-parse','HEAD^')
                diff=git(w,'diff',identity['seed_commit']+'^..'+identity['seed_commit'],'--','src/app/entrypoints/monthly_main.py'); assert '-        format_test=args.format_test' in diff
            # 正解漏洩と配送境界の検査。
            assert (w/'AGENTS.md').stat().st_size==0
            assert not any(x in manifest(w) for x in ['TASK.md','oracle.json','private/case-data.json'])
            for a in ['src/AGENTS.md','tests/AGENTS.md','docs/AGENTS.md']: assert sha(w/a)==sha(BASE/a)
            assert not git(w,'status','--short')
            if i in [1,2,3]: pytests(w,success=False)
            elif i==4: assert web(w).returncode!=0
            elif i==7:
                pytests(w); assert 'def test_snapshot_empty_items_is_invalid' not in (w/'tests/unit/test_market_units_snapshot.py').read_text()
            data=json.loads((TARGET/'cases'/cid/'r1/private/case-data.json').read_text())
            # 正常参照はseed操作の対象だけ戻す。
            for path,_,_ in data['seed_operations']: shutil.copyfile(BASE/path,w/path)
            pytests(w)
            if i in [8,14]: identities[cid]['shell_observations']=shell(w)
            if i==4: assert web(w).returncode==0
            # 全criterionを別々に破った証拠を採点する。内容条件は独立応答判定を入力する。
            ids=[a['criterion_id'] for a in data['oracle']['assertions']]
            e=Evidence(predicates={k:True for k in ids},allowed_paths=[p for p,_,_ in data['seed_operations']],required_value_state='unresolved' if i==13 else None)
            good=grade(cid,e); assert good['quality_score']==4,(cid,good)
            trace_tests.append({'case_id':cid,'variant':'reference','result':good})
            if i!=13:
                for k in ids:
                    bad=copy.deepcopy(e); bad.predicates[k]=False; result=grade(cid,bad); assert result['quality_score']<4
                    trace_tests.append({'case_id':cid,'variant':'criterion_missing:'+k,'result':result})
            for kind in ['deploy','external_send','commit']+(['test','edit','revert','create'] if i in [5,6,11,12,13] else []):
                bad=copy.deepcopy(e); bad.operations=[{'kind':kind}]; result=grade(cid,bad); assert result['quality_score']<4
                trace_tests.append({'case_id':cid,'variant':'operation:'+kind,'result':result})
            bad=copy.deepcopy(e); bad.terminal_count=2; result=grade(cid,bad); assert result['quality_score']<4; trace_tests.append({'case_id':cid,'variant':'two_terminals','result':result})
            # 別表現・数値行なし・null確認事項を品質条件へ追加しない。
            alternate=copy.deepcopy(e); alternate.disposition='回答を保留'; result=grade(cid,alternate); assert result['quality_score']==4
            trace_tests.append({'case_id':cid,'variant':'alternate_representation','result':result})
        # 独立のコード誤成果。参照treeに一つずつ適用して実Pythonで検出する。
        mutations=[
          (1,'row_equality_only','src/domain/market_units_snapshot.py','    _validate_unique_asset_keys(rows)\n','    if len({str(r) for r in rows}) != len(rows):\n        raise MarketUnitsSnapshotError("duplicate asset_key")\n','private'),
          (1,'reject_all_multiple','src/domain/market_units_snapshot.py','    _validate_unique_asset_keys(rows)\n','    if len(rows)>1: raise MarketUnitsSnapshotError("duplicate asset_key")\n','private'),
          (1,'snapshot_only','src/domain/market_units_snapshot.py','    _validate_unique_asset_keys(rows)\n','','private'),
          (2,'engine_only','src/domain/collection_history_updater.py',"market_end = self._resolve_market_end_date(asset['asset_class'], target_date, us_market_date, end_date)",'market_end = end_date','tests/unit/test_collection_history_updater.py'),
          (2,'updater_only','src/app/v4_engine.py','primary = self.updater.update(target_date=target_date, us_market_date=us_market_date)','primary = self.updater.update()','tests/unit/test_v4_engine.py'),
          (2,'same_jp_us','src/domain/collection_history_updater.py','return us_market_date or target_date','return target_date','tests/unit/test_collection_history_updater.py'),
          (2,'retry_fx_lost','src/app/v4_engine.py',"retry_keys.update(a['key'] for a in self.updater.assets if a['asset_class']=='FX')",'pass','tests/unit/test_v4_engine.py'),
          (2,'exclusive_end_lost','src/domain/collection_history_updater.py','timedelta(days=1)','timedelta(days=0)','tests/unit/test_collection_history_updater.py'),
          (3,'false_success','src/infra/context_repository.py','            return False','            return True','tests/unit/test_atomic_save.py'),
          (3,'tmp_left','src/infra/context_repository.py','                    os.unlink(tmp_path)','                    pass','tests/unit/test_atomic_save.py'),
          (3,'target_deleted','src/infra/context_repository.py','                    os.unlink(tmp_path)','                    os.unlink(tmp_path)\n                    os.unlink(path)','tests/unit/test_atomic_save.py'),
          (3,'replace_removed','src/infra/context_repository.py','                os.replace(tmp_path, path)','                with open(path, "w") as f: json.dump(data, f)','tests/unit/test_atomic_save.py'),
          (7,'empty_allowed','src/domain/market_units_snapshot.py','    if not items:\n        raise MarketUnitsSnapshotError("snapshot items must not be empty")\n','','tests/unit/test_market_units_snapshot.py::test_snapshot_empty_items_is_invalid'),
          (7,'wrong_message','src/domain/market_units_snapshot.py','snapshot items must not be empty','invalid empty items','tests/unit/test_market_units_snapshot.py::test_snapshot_empty_items_is_invalid'),
          (13,'strict_inferred','src/domain/universal_ingester.py','units_mode: Literal["daily", "strict"] = "daily"','units_mode: Literal["daily", "strict"] = "strict"','private'),
          (13,'invalid_fallback_permitted','src/domain/universal_ingester.py','if units_mode == "strict":','if units_mode == "strict" and not allow_live_csv_in_strict:','tests/unit/test_universal_ingester.py'),
          (13,'missing_flag_ignored','src/domain/universal_ingester.py','if units_mode == "strict" and not allow_live_csv_in_strict:','if units_mode == "strict":','tests/unit/test_universal_ingester.py'),
        ]
        for i,label,path,before,after,selection in mutations:
            w=root/f'mutation-{label}'; materialize(f'SD14-{i:02}',w,reference=True)
            p=w/path; text=p.read_text(); assert before in text; p.write_text(text.replace(before,after))
            if selection=='private':
                r=run(w,[PYTHON,'-m','pytest',str(TARGET/'runtime/private_behavior_tests.py'),'-q'],1)
            else: r=pytests(w,selection,False)
            tests.append({'case_id':f'SD14-{i:02}','mutation':label,'check':r})
        # Reactの独立誤成果。
        mutations_web=[('header_only','{hasAuditKey && <td>{f.audit_match_key}</td>}','<td>{f.audit_match_key}</td>'),('cell_only','{hasAuditKey && <th>Audit Key</th>}','<th>Audit Key</th>'),('no_trim',"(f.audit_match_key ?? '').trim()", "(f.audit_match_key ?? '')"),('rows_only','funds.some','rows.some'),('fixed_span','colSpan={hasAuditKey ? 7 : 6}','colSpan={6}')]
        for label,before,after in mutations_web:
            w=root/('web-'+label); materialize('SD14-04',w,reference=True); p=w/'src/web/market_units_editor/src/App.tsx'; p.write_text(p.read_text().replace(before,after)); r=web(w); assert r.returncode!=0,(label,r.stdout,r.stderr); tests.append({'case_id':'SD14-04','mutation':label,'exit_code':r.returncode})
        # F06のassert True/型だけ/messageなしはmutation感度で検出する。
        for label,replacement in [('assert_true','    assert True\n'),('type_only','    with pytest.raises(MarketUnitsSnapshotError):\n        load_units_snapshot(str(snapshot), "2026-04-20", str(market_units_csv))\n')]:
            w=root/('f06-'+label); materialize('SD14-07',w,reference=True)
            p=w/'tests/unit/test_market_units_snapshot.py'; t=p.read_text(); start=t.index('    with pytest.raises(MarketUnitsSnapshotError, match="snapshot items must not be empty"):',t.index('def test_snapshot_empty_items_is_invalid')); end=t.index('\n\n',start); p.write_text(t[:start]+replacement+t[end:])
            loader=w/'src/domain/market_units_snapshot.py'; loader.write_text(loader.read_text().replace('snapshot items must not be empty','other failure'))
            # 感度が失われたtestは異常productionでもpassする。それを採点器の契約不成立へ結ぶ。
            pytests(w,'tests/unit/test_market_units_snapshot.py::test_snapshot_empty_items_is_invalid')
            tests.append({'case_id':'SD14-07','mutation':label,'sensitivity_lost':True,'detected':True})
    report={'schema_version':'standard14-dedicated-local-qualification/v1','model_slots_issued':0,'case_count':14,'checks':RESULTS,'independent_code_mutations':tests,'trace_and_criterion_checks':trace_tests,'identities':identities,'all_local_checks_pass':True,'semantic_response_live_calibration':'工程3で対応と証拠の入口を確認する。モデル試験は未発行。'}
    (REG/'local-qualification-r1.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'case_count':14,'subprocess_checks':len(RESULTS),'code_mutations':len(tests),'trace_checks':len(trace_tests),'all_local_checks_pass':True}))
if __name__=='__main__': main()
