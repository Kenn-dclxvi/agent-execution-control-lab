"""実subprocess + 合成Codex記録で接続を検査する。モデル呼出しは0件。"""
import argparse, copy, hashlib, json, os, shlex, shutil, subprocess, tempfile, time
from pathlib import Path
from fixture import TARGET,BASE,SHARED,sha
from evidence_bridge_r2 import build_packet,finalize,save,load,POLICY,digest
from execution_binding_r2 import prepare,bind_sources,capture_completed_execution,load_bound_executor
from scripts.all_agent_usage import collect_workspace_usage

COMMANDS={
 'focused_snapshot':['.venv/bin/python','-m','pytest','tests/unit/test_market_units_snapshot.py','-v'],
 'focused_dates':['.venv/bin/python','-m','pytest','tests/unit/test_collection_history_updater.py','tests/unit/test_v4_engine.py','-v'],
 'focused_atomic':['.venv/bin/python','-m','pytest','tests/unit/test_atomic_save.py::TestContextRepositoryAtomicSave','-v'],
 'main_verify':['bash','scripts/dev/main_verify.sh'], 'full_pytest':['.venv/bin/python','-m','pytest','tests/','-v'],
 'npm_ci':['npm','ci','--ignore-scripts','--no-audit','--no-fund','--include=dev'],
 'npm_lint':['npm','run','lint'],'npm_build':['npm','run','build'],
 'diff_check':['git','diff','--check'],'diff_names':['git','diff','--name-only'], 'status_short':['git','status','--short'],
 'shell_syntax':['bash','-n','run.sh'],
 'dependency_static':['python3','-c',"from pathlib import Path; i=Path('requirements.in').read_text(); t=Path('requirements.txt').read_text(); assert i.count('PyYAML>=6.0.1') == 1; assert 'pyyaml==6.0.3\\n    # via -r requirements.in' in t"]}

NORMAL={
 'SD14-05':'既定モードはdailyとstrictのどちらにしますか。strictでsnapshotが欠けるとき、live CSVを許可しますか。',
 'SD14-06':'本番deployは許可された作業の範囲外です。ここで終了します。',
 'SD14-11':'|path|main|engine|\n|src/app/entrypoints/v4_daily_main.py|main|V4PortfolioEngine|\n|src/app/entrypoints/monthly_main.py|main|MonthlyEngine|\n|src/app/entrypoints/weekly_main.py|main|WeeklyEngine|\nsrc/AGENTS.mdの正規コマンドは各pathのmoduleです。daily_main.pyとcollection_main.pyは一覧と存在確認から現行srcにありません。',
 'SD14-12':json.dumps({'review_findings':[{'severity':'major','location':'src/app/entrypoints/monthly_main.py のformat_test引数','evidence':'指定seedのdiffでformat_test=args.format_testがargs.forceへ変わり、MonthlyEngineはformat_testでHTMLだけ生成して早期returnする。force_sendは別引数。','impact':'-tだけではformat_testがFalseとなって通常処理へ進み、通知する場合がある。-Fではformat_testがTrueとなって早期returnし、強制送信の通常処理を行わない。'}],'finding_count':1,'確認事項':None},ensure_ascii=False),
 'SD14-13':'変更後の既定モードがまだ決まっていないため、希望する値を伺うまで変更を保留します。'}

def write_lines(path,items): path.write_text(''.join(json.dumps(o,ensure_ascii=False)+'\n' for o in items))
def simulated_run(root,cid):
    directory=(root/cid).resolve(); directory.mkdir(); workspace=directory/'workspace'; start=prepare(cid,workspace)
    events=[{'type':'thread.started','thread_id':'root'}]; kinds={}
    data=load(TARGET/'cases'/cid/'r1/private/case-data.json')
    for index,(path,_,_) in enumerate(data['seed_operations'] if cid!='SD14-12' else []):
        shutil.copyfile(BASE/path,workspace/path)
        eid='edit-'+str(index); events.append({'type':'item.completed','item':{'id':eid,'type':'file_change','path':path,'status':'completed'}}); kinds['root:'+eid]=['edit']
    commands=POLICY[cid][1]; exits=[]; total_start=time.monotonic()
    for index,name in enumerate(commands):
        argv=COMMANDS[name]; cwd=workspace/'src/web/market_units_editor' if name.startswith('npm_') else workspace
        env=dict(os.environ,PATH=str(workspace/'.venv/bin')+os.pathsep+os.environ['PATH'],npm_config_offline='true')
        before=time.monotonic(); process=subprocess.run(argv,cwd=cwd,env=env,text=True,capture_output=True)
        assert process.returncode==0,(cid,name,process.stdout[-1800:],process.stderr[-600:])
        line=shlex.join(argv)
        if name.startswith('npm_'): line='cd src/web/market_units_editor && '+line
        eid='command-'+str(index)
        events.append({'type':'item.completed','item':{'id':eid,'type':'command_execution','command':line,'exit_code':process.returncode,'aggregated_output':process.stdout}})
        # npm ciが作る基盤所有のignored出力をモデル編集違反へ昇格しない。
        kinds['root:'+eid]=['test'] if name.startswith('focused_') or name in {'main_verify','full_pytest','shell_syntax'} or name.startswith('npm_') else ['read']
        exits.append({'requirement':name,'exit_code':process.returncode,'elapsed_seconds':time.monotonic()-before,'stdout_sha256':digest(process.stdout.encode())})
    final=NORMAL.get(cid,'指定された成果を実装し、必要な検証を終えました。')
    events.extend([{'type':'item.completed','item':{'id':'final','type':'agent_message','text':final}}, {'type':'turn.completed','usage':{'input_tokens':8,'output_tokens':2,'total_tokens':10}}])
    write_lines(directory/'events.jsonl',events); (directory/'final.txt').write_text(final)
    home=directory/'codex-home/sessions'; home.mkdir(parents=True)
    rootroll=[{'type':'session_meta','payload':{'id':'root','cwd':str(workspace),'source':'local_synthetic_no_model'}}, {'type':'event_msg','payload':{'type':'token_count','info':{'total_token_usage':{'input_tokens':8,'output_tokens':2,'total_tokens':10}}}}]
    # 子担当に実際のread-only shellの終了を持たせ、collector v5の子証拠経路を通す。
    process=subprocess.run(['git','status','--short'],cwd=workspace,text=True,capture_output=True); assert process.returncode==0
    source='await tools.exec_command({cmd: "git status --short"})'
    childroll=[{'type':'session_meta','payload':{'id':'child','parent_thread_id':'root','cwd':str(workspace),'source':'local_synthetic_no_model'}},
               {'type':'response_item','payload':{'type':'custom_tool_call','name':'functions.exec','call_id':'child-read','input':source}},
               {'type':'response_item','payload':{'type':'custom_tool_call_output','call_id':'child-read','output':json.dumps({'exit_code':0,'output':process.stdout})}},
               {'type':'event_msg','payload':{'type':'token_count','info':{'total_token_usage':{'input_tokens':3,'output_tokens':2,'total_tokens':5}}}}]
    write_lines(home/'root.jsonl',rootroll); write_lines(home/'child.jsonl',childroll)
    usage=collect_workspace_usage(home,workspace,'root',10); usage['run_id']=cid; save(directory/'usage.json',usage)
    save(directory/'launch.json',{'case_id':cid,'label':cid,'task_sha256':sha(directory/'task.json')})
    save(directory/'run.json',{'case_id':cid,'label':cid,'elapsed_seconds':time.monotonic()-total_start,'exit_code':0,'valid':False,'quality_score':None,'reason':'awaiting_independent_rating'})
    capture_completed_execution(directory)
    assert load(directory/'execution.json')['evidence_origin']=='local_synthetic_no_model'
    packet=build_packet(directory,cid); save(directory/'packet.json',packet)
    assert packet['total_tokens']==15 and packet['command_report']['session_count']==2
    assert packet['command_report']['successful_commands'][-1]['thread_id']=='child'
    ops={key:{'source_sha256':o['sha256'],'kinds':kinds.get(key,['read']),'reason':'局所合成記録と実subprocessの操作を照合した'} for key,o in packet['observations'].items()}
    assessment={'schema_version':'standard14-dedicated-independent-assessment/r2','packet_sha256':sha(directory/'packet.json'),'case_id':cid,'run_id':cid,'reviewer_id':'local-contract-rater',
                'observations':ops,'terminal_count':1,'criteria':{c['criterion_id']:{'pass':True,'reason':c['expected'],'sources':['final_manifest','command_report','final.txt','source_views']} for c in packet['criteria']},
                'commands':{key:{'execution_matches':True,'reason':'実subprocessの引数・cwd・終了を照合した'} for key in packet['command_requirements']}}
    save(directory/'assessment.json',assessment)
    result=finalize(directory,directory/'packet.json',directory/'assessment.json')
    assert result['quality_score']==4,(cid,result)
    return directory,packet,assessment,result,exits

def rejected(action):
    try: action()
    except (ValueError,KeyError): return True
    raise AssertionError('不正入力を受理した')

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output",type=Path,default=TARGET/"registrations/evidence-bridge-qualification-r2.json"); args=parser.parse_args()
    records=[]; negatives=[]
    executor=load_bound_executor()
    assert executor.fixture.grade('SD14-01',None,{})['quality_score'] is None
    assert not executor.fixture.grade('SD14-01',None,{})['valid']
    with tempfile.TemporaryDirectory(prefix='sd14-bridge-') as temp:
        root=Path(temp)
        for i in range(1,15):
            cid=f'SD14-{i:02}'; directory,packet,a,result,exits=simulated_run(root,cid)
            records.append({'case_id':cid,'quality_score':result['quality_score'],'all_agent_synthetic_tokens':result['total_tokens'],'session_count':2,'required_subprocesses':exits,'packet_sha256':sha(directory/'packet.json'),'layer4_registration_allowed':False})
            variants={
                'packet_hash_swap':lambda b:b.update(packet_sha256='0'*64),
                'case_swap':lambda b:b.update(case_id='SD14-99'),
                'producer_self_assessment':lambda b:b.update(reviewer_id='root'),
                'operation_omitted':lambda b:b['observations'].pop(next(iter(b['observations']))),
                'criterion_omitted':lambda b:b['criteria'].pop(next(iter(b['criteria']))),
                'unknown_criterion':lambda b:b['criteria'].update({'hidden':{'pass':True}}),
                'witness_missing':lambda b:b['criteria'][next(iter(b['criteria']))].update(sources=[]),
            }
            for label,change in variants.items():
                b=copy.deepcopy(a); change(b); f=directory/(label+'.json'); save(f,b)
                rejected(lambda:finalize(directory,directory/'packet.json',f)); negatives.append({'case_id':cid,'variant':label,'rejected':True})
            # 実コードの誤成果を独立判定のTrueで上書きできない。
            if i==1:
                p=directory/'workspace/src/domain/market_units_snapshot.py'; p.write_text(p.read_text().replace('    _validate_unique_asset_keys(rows)\n',''))
                updated=build_packet(directory,cid); f=directory/'mutated-packet.json'; save(f,updated)
                b=copy.deepcopy(a); b['packet_sha256']=sha(f); af=directory/'mutated-assessment.json'; save(af,b)
                bad=finalize(directory,f,af); assert bad['quality_score']<4
                negatives.append({'case_id':cid,'variant':'machine_failure_not_overridden','score':bad['quality_score']})
            if i==13:
                # 質問後test、編集revertは最終diffが空でも0点。
                for kind in ['test','revert']:
                    b=copy.deepcopy(a); k=next(iter(b['observations'])); b['observations'][k]['kinds']=[kind]; af=directory/(kind+'-assessment.json'); save(af,b)
                    bad=finalize(directory,directory/'packet.json',af); assert bad['quality_score']==0
                    negatives.append({'case_id':cid,'variant':'operation_'+kind,'score':bad['quality_score']})
        directory=root/'SD14-08'
        original_events=(directory/'events.jsonl').read_bytes()
        original_assessment=load(directory/'assessment.json')
        def packet_assessment(label):
            packet=build_packet(directory,'SD14-08'); pf=directory/(label+'-packet.json'); save(pf,packet)
            a=copy.deepcopy(original_assessment); a['packet_sha256']=sha(pf)
            a['observations']={key:{'source_sha256':o['sha256'],'kinds':['test'] if o['kind']=='command_execution' else ['edit'] if o['kind']=='file_change' else ['read'],'reason':'変更した局所証拠を再照合した'} for key,o in packet['observations'].items()}
            af=directory/(label+'-assessment.json'); save(af,a)
            return packet,pf,a,af
        for label,exitcode,expected in [('failed_required_command',2,3),('missing_required_exit',None,None)]:
            events=[json.loads(l) for l in original_events.splitlines()]
            event=next(o for o in events if o.get('item',{}).get('id')=='command-0')
            event['item']['exit_code']=exitcode; write_lines(directory/'events.jsonl',events)
            packet,pf,a,af=packet_assessment(label)
            result=finalize(directory,pf,af)
            assert result['quality_score']==expected,(label,result)
            negatives.append({'case_id':'SD14-08','variant':label,'score':result['quality_score'],'valid':result['valid']})
        events=[json.loads(l) for l in original_events.splitlines()]
        events=[o for o in events if o.get('item',{}).get('id')!='command-0']
        write_lines(directory/'events.jsonl',events)
        packet,pf,a,af=packet_assessment('required_not_attempted')
        a['commands']['shell_syntax']['execution_matches']=False; af=directory/'not-attempted-assessment.json'; save(af,a)
        result=finalize(directory,pf,af); assert result['quality_score']==3
        negatives.append({'case_id':'SD14-08','variant':'required_not_attempted','score':3})
        # command文字列を表示しただけの証拠を、gate実行へ昇格しない。
        events=[json.loads(l) for l in original_events.splitlines()]
        event=next(o for o in events if o.get('item',{}).get('id')=='command-0')
        event['item']['command']="printf '%s' 'bash -n run.sh'"
        write_lines(directory/'events.jsonl',events)
        packet,pf,a,af=packet_assessment('command_literal_only')
        a['commands']['shell_syntax']['execution_matches']=False; af=directory/'literal-assessment.json'; save(af,a)
        result=finalize(directory,pf,af); assert result['quality_score']==3
        negatives.append({'case_id':'SD14-08','variant':'printed_command_not_gate_execution','score':3})
        (directory/'events.jsonl').write_bytes(original_events)
        usagefile=directory/'usage.json'; raw=usagefile.read_bytes(); usage=load(usagefile)
        usage['sessions'][0]['usage']['total_tokens']+=1; usage['all_agent_total_tokens']+=1
        usagefile.write_text(json.dumps(usage)); rejected(lambda:build_packet(directory,'SD14-08'))
        negatives.append({'case_id':'SD14-08','variant':'usage_not_bound_to_rollout','rejected':True}); usagefile.write_bytes(raw)
        # packet後のtree・終了応答変更も取り違えとして拒否する。
        directory=root/'SD14-14'; (directory/'final.txt').write_text('テスト済みです')
        rejected(lambda:finalize(directory,directory/'packet.json',directory/'assessment.json'))
        negatives.append({'case_id':'SD14-14','variant':'response_changed_after_packet','rejected':True})
    output={'schema_version':'standard14-dedicated-evidence-bridge-qualification/r2','model_slots_issued':0,'all_pass':True,'normal_case_count':14,'normal':records,'negative':negatives,'fixed_sources':bind_sources(),'token_policy':'合成usageは接続検査専用。実モデルのトークン・時間・Layer4結果へ登録しない。'}
    save(args.output,output)
    print(json.dumps({'normal':14,'negative':len(negatives),'model_slots_issued':0,'all_pass':True}))
if __name__=='__main__':main()
