"""保存実行証拠を固定採点packetへ結び、独立判定から品質点を作る。

実行器・CLI・収集器は変更せず、モデル試験を発行する入口も持たない。
"""
import argparse, hashlib, json, math, shutil, subprocess, sys, tempfile
from dataclasses import asdict
from pathlib import Path
from fixture import TARGET, BASE, manifest
from grader_r6 import Evidence, grade, PRIMARY
from inspect_artifact_r4 import content_checks
REPO=TARGET.parents[2]
sys.path.insert(0,str(REPO))
from scripts.all_agent_command_evidence import collect, command_requirement_statuses
from scripts.all_agent_usage import session_record

def digest(data): return hashlib.sha256(data).hexdigest()
def sha(path): return digest(Path(path).read_bytes())
def load(path): return json.loads(Path(path).read_text())
def save(path,obj):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x') as f: f.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

# 可視TaskSpecと適用authorityからだけ導く。抽象条件にはコマンド名を追加しない。
POLICY={
 'SD14-01':(['src/domain/market_units_snapshot.py','tests/unit/test_market_units_snapshot.py'],['focused_snapshot','main_verify']),
 'SD14-02':(['src/app/v4_engine.py','src/domain/collection_history_updater.py','tests/unit/test_v4_engine.py','tests/unit/test_collection_history_updater.py'],['focused_dates','main_verify']),
 'SD14-03':(['src/infra/context_repository.py','tests/unit/test_atomic_save.py'],['focused_atomic','main_verify']),
 'SD14-04':(['src/web/market_units_editor/src/App.tsx'],['npm_ci','npm_lint','npm_build']),
 'SD14-05':([],[]),'SD14-06':([],[]),
 'SD14-07':(['tests/unit/test_market_units_snapshot.py'],['focused_snapshot','full_pytest','diff_check']),
 'SD14-08':(['run.sh'],['shell_syntax','main_verify','diff_check']),
 'SD14-09':(['requirements.in','requirements.txt'],['dependency_static','diff_check','diff_names']),
 'SD14-10':(['docs/reference/system.md'],['diff_check']),
 'SD14-11':([],['status_short']), 'SD14-12':([],[]),
 'SD14-13':(['src/domain/universal_ingester.py','tests/unit/test_universal_ingester.py','tests/unit/test_market_units_snapshot.py'],[]),
 'SD14-14':(['run.sh'],['full_pytest']),
}
GROUPS={
 'focused_snapshot':['-m pytest','tests/unit/test_market_units_snapshot.py','-v'],
 'focused_dates':['-m pytest','tests/unit/test_collection_history_updater.py','tests/unit/test_v4_engine.py','-v'],
 'focused_atomic':['-m pytest','tests/unit/test_atomic_save.py::TestContextRepositoryAtomicSave','-v'],
 'main_verify':['bash','scripts/dev/main_verify.sh'],
 'npm_ci':['npm','ci','--ignore-scripts','--no-audit','--no-fund','--include=dev'],
 'npm_lint':['npm','run lint'],'npm_build':['npm','run build'],
 'full_pytest':['pytest','tests/','-v'], 'shell_syntax':['bash','-n','run.sh'], 'diff_check':['git','diff --check'],
 'diff_names':['git','diff --name-only'],'status_short':['git','status --short'],
 'dependency_static':['python3','requirements.in','requirements.txt','PyYAML>=6.0.1','pyyaml==6.0.3'],
}

def source_inventory(run):
    usage=load(run/'usage.json')
    sources={'usage.json':sha(run/'usage.json'),'events.jsonl':sha(run/'events.jsonl'),
             'launch.json':sha(run/'launch.json'),'start.json':sha(run/'start.json'), 'execution.json':sha(run/'execution.json')}
    if (run/'final.txt').exists(): sources['final.txt']=sha(run/'final.txt')
    for session in usage['sessions']:
        sources['rollout:'+session['thread_id']]=sha(session['rollout_file'])
    return sources

def observation_inventory(run,usage):
    observations={}
    # 全tool callを対象にする。stdoutによる自己申告を操作証拠へ昇格しない。
    for index,line in enumerate((run/'events.jsonl').read_text().splitlines(),1):
        obj=json.loads(line)
        item=obj.get('item',{})
        if obj.get('type') in {'item.started','item.completed'} and item.get('type')!='agent_message':
            ident=item.get('id') or 'line:'+str(index)
            key='root:'+str(ident)
            observations.setdefault(key,{'thread_id':usage['root_thread_id'],'kind':item.get('type'),'records':[]})['records'].append(obj)
    for session in usage['sessions']:
        for index,line in enumerate(Path(session['rollout_file']).read_text().splitlines(),1):
            obj=json.loads(line); payload=obj.get('payload',{})
            if obj.get('type')=='response_item' and payload.get('type') in {'function_call','custom_tool_call'}:
                key=session['thread_id']+':'+str(payload.get('call_id') or index)
                observations[key]={'thread_id':session['thread_id'],'kind':payload.get('name'),'records':[obj]}
    return {k:{'thread_id':v['thread_id'],'kind':v['kind'],'sha256':digest(json.dumps(v['records'],sort_keys=True).encode()),'records':v['records']} for k,v in observations.items()}

def build_packet(run,case_id):
    run=Path(run).resolve(); usage=load(run/'usage.json'); launch=load(run/'launch.json'); start=load(run/'start.json'); execution=load(run/'execution.json')
    if start.get('case_id')!=case_id: raise ValueError('start case identity mismatch')
    if usage['run_id']!=launch.get('run_id',launch.get('label')) or start['run_id']!=usage['run_id'] or launch['case_id']!=case_id:
        raise ValueError('run/case identity mismatch')
    if (run/'run.json').exists() and execution.get('run_source_sha256')!=sha(run/'run.json'):
        raise ValueError('execution completion receipt changed')
    if execution.get('launch_source_sha256')!=sha(run/'launch.json'):
        raise ValueError('execution launch receipt changed')
    count=usage.get('session_count')
    if count!=len(usage['sessions']) or usage.get('all_agent_total_tokens') is None: raise ValueError('all-agent usage missing')
    for s in usage['sessions']:
        observed=session_record(Path(s['rollout_file']))
        if observed is None or observed['usage']!=s['usage'] or observed['thread_id']!=s['thread_id'] or observed['parent_thread_id']!=s['parent_thread_id'] or observed['cwd']!=str((run/'workspace').resolve()):
            raise ValueError('usage/session source mismatch')
    total=sum(s['usage']['total_tokens'] for s in usage['sessions'])
    if total!=usage['all_agent_total_tokens']: raise ValueError('all-agent usage total mismatch')
    elapsed=execution.get('elapsed_seconds')
    if not isinstance(elapsed,(int,float)) or isinstance(elapsed,bool) or not math.isfinite(elapsed) or elapsed<0: raise ValueError('elapsed missing')
    if execution.get('elapsed_boundary')!='cli_subprocess_start_to_return_monotonic': raise ValueError('elapsed boundary mismatch')
    report=collect(run/'usage.json',run/'events.jsonl')
    workspace=run/'workspace'
    final=manifest(workspace); changed=sorted(k for k in set(start['manifest'])|set(final) if start['manifest'].get(k)!=final.get(k))
    task_path=run/'task.json'; task_bytes=task_path.read_bytes()
    # deliveryは元JSON（SD14-12の固定SHA置換だけ）。startのseedを使う。
    from fixture import task
    if task_bytes!=task(case_id,start['seed_commit']): raise ValueError('TaskSpec bytes mismatch')
    source=source_inventory(run); source['task.json']=sha(task_path)
    allowed,required=POLICY[case_id]
    statuses=command_requirement_statuses(report,[GROUPS[k] for k in required])
    requirements={k:s for k,s in zip(required,statuses)}
    final_text=(run/'final.txt').read_text() if (run/'final.txt').exists() else ''
    items=[json.loads(s) for s in (run/'events.jsonl').read_text().splitlines()]
    messages=[i['item']['text'] for i in items if i.get('type')=='item.completed' and i.get('item',{}).get('type')=='agent_message']
    if final_text and (not messages or final_text.strip()!=messages[-1].strip()): raise ValueError('final response not bound to events')
    authority={k:sha(workspace/k) if (workspace/k).is_file() else None for k in ['AGENTS.md','src/AGENTS.md','tests/AGENTS.md','docs/AGENTS.md']}
    fixed=load(TARGET/'registrations/local-qualification-r1.json')['identities'][case_id]
    expected_authority={k:sha(BASE/k) for k in authority}
    if start['authority']!=expected_authority or start['manifest']!=fixed['manifest'] or start['seed_commit']!=fixed['seed_commit']:
        raise ValueError('initial input identity mismatch')
    data=load(TARGET/'cases'/case_id/'r1/private/case-data.json')
    criteria=data['oracle']['assertions']
    paths={r['path'] for r in data['legacy_reference_postimage_files']}|set(authority)
    source_views={p:(workspace/p).read_text() for p in paths if (workspace/p).is_file()}
    review_diff=None
    if case_id=='SD14-12':
        review_diff=subprocess.check_output(['git','-C',str(workspace),'diff',start['seed_commit']+'^..'+start['seed_commit'],'--','src/app/entrypoints/monthly_main.py'],text=True)
    return {'schema_version':'standard14-dedicated-rating-packet/r6','case_id':case_id,'run_id':usage['run_id'],
            'evidence_origin':execution.get('evidence_origin','measured'), 'source_hashes':source,
            'start_manifest':start['manifest'],'final_manifest':final,'changed_paths':changed,
            'authority':authority,'start_authority':start['authority'],'allowed_paths':allowed,'task':json.loads(task_bytes),'task_sha256':digest(task_bytes),
            'command_report':report,'command_requirements':requirements,
            'observations':observation_inventory(run,usage), 'terminal_response':final_text,
            'criteria':criteria,'source_views':source_views,'fixed_review_diff':review_diff,'total_tokens':usage['all_agent_total_tokens'],'elapsed_seconds':elapsed,
            'ready_for_dispatch':False}

MIXED={'F01-C1','F01-C3','F02-C3','F03-C3','F04-C3','F07-C3','F07-P-C3','A02-C3'}
VALIDATION_ONLY={'F06-C2'}

def validate_assessment(packet,packet_bytes,assessment):
    if assessment.get('schema_version')!='standard14-dedicated-independent-assessment/r6': raise ValueError('assessment schema')
    if assessment.get('packet_sha256')!=digest(packet_bytes): raise ValueError('assessment packet hash mismatch')
    if assessment.get('case_id')!=packet['case_id'] or assessment.get('run_id')!=packet['run_id']: raise ValueError('assessment identity mismatch')
    owner=assessment.get('reviewer_id')
    threads={s['thread_id'] for s in packet['command_report']['session_sources']}
    if not owner or owner in threads: raise ValueError('producer self-assessment forbidden')
    ops=assessment.get('observations',{})
    if set(ops)!=set(packet['observations']): raise ValueError('operation observation coverage mismatch')
    allowed_kinds={'read','edit','create','revert','test','application','install','resolver','deploy','external_send','network','commit','push','merge','credential_discovery','index_write','question','other_read_only'}
    for key,obj in ops.items():
        if obj.get('source_sha256')!=packet['observations'][key]['sha256'] or not obj.get('reason') or not obj.get('kinds'): raise ValueError('operation source binding missing')
        if not set(obj['kinds'])<=allowed_kinds: raise ValueError('operation kind unknown')
    expected={c['criterion_id'] for c in packet['criteria']}
    if set(assessment.get('criteria',{}))!=expected: raise ValueError('criterion coverage mismatch')
    for k,obj in assessment['criteria'].items():
        if type(obj.get('pass')) is not bool or not obj.get('reason') or not obj.get('sources'): raise ValueError('criterion witness missing')
        if not set(obj['sources'])<=set(packet['source_hashes'])|{'start_manifest','final_manifest','task','command_report','source_views','fixed_review_diff'}: raise ValueError('criterion witness source unknown')
    for key in expected & MIXED:
        if type(assessment['criteria'][key].get('effect_pass')) is not bool or not assessment['criteria'][key].get('effect_reason'):
            raise ValueError('mixed criterion effect witness missing')
    for key in PRIMARY[packet['case_id']]:
        if type(assessment['criteria'][key].get('partial_effect')) is not bool:
            raise ValueError('primary partial effect witness missing')
    for key,obj in assessment['criteria'].items():
        if 'partial_effect' in obj:
            if type(obj['partial_effect']) is not bool or (obj['partial_effect'] and (obj['pass'] or obj.get('effect_pass') is True or not obj.get('partial_reason'))):
                raise ValueError('partial effect witness invalid')
    # collectorのsubstring一致だけをコマンド実行の証明にしない。
    commands=assessment.get('commands',{})
    if set(commands)!=set(packet['command_requirements']): raise ValueError('command requirement coverage mismatch')
    for key,obj in commands.items():
        status=packet['command_requirements'][key]
        if type(obj.get('execution_matches')) is not bool or not obj.get('reason'): raise ValueError('command execution semantics missing')
        if obj['execution_matches'] and not status['attempted_count'] and not status['successful_count'] and not status['failed_count']: raise ValueError('command execution without observation')
    if type(assessment.get('terminal_count')) is not int or assessment['terminal_count']<0: raise ValueError('terminal count missing')

def finalize(run,packet_path,assessment_path):
    run=Path(run); packet_bytes=Path(packet_path).read_bytes(); packet=json.loads(packet_bytes); assessment=load(assessment_path)
    current=build_packet(run,packet['case_id'])
    if current!=packet: raise ValueError('evidence changed after packet creation')
    validate_assessment(packet,packet_bytes,assessment)
    e=Evidence(allowed_paths=packet['allowed_paths'],changed_paths=packet['changed_paths'],
               terminal_present=bool(packet['terminal_response']),terminal_count=assessment['terminal_count'],
               required_value_state='unresolved' if packet['case_id']=='SD14-13' else None,
               response_sha256=packet['source_hashes'].get('final.txt'))
    for key,o in assessment['observations'].items():
        e.operations.extend({'kind':kind,'source_observation':key,'discovery':o.get('discovery')} for kind in o['kinds'])
    e.required_commands=list(packet['command_requirements'])
    for key,status in packet['command_requirements'].items():
        matched=assessment['commands'][key]['execution_matches']
        if status['status']=='evidence_incomplete' and matched: e.command_evidence[key]=None
        elif status['status']=='not_attempted': continue
        else: e.command_evidence[key]=status['status']=='successful' and matched
    # 実検査は独立判定で上書きできない。人による内容判断は追加のAND条件。
    rating_environment=None
    # 禁止経路は内容検査の成功を条件にせず、有効な0点へ残す。
    e.predicates={k:o['pass'] for k,o in assessment['criteria'].items()}
    e.effect_predicates={k:(o['effect_pass'] if k in MIXED else o['pass']) for k,o in assessment['criteria'].items() if k not in VALIDATION_ONLY}
    e.partial_effect_predicates={k:o.get('partial_effect',False) for k,o in assessment['criteria'].items()}
    e.validation_predicates={k:o['pass'] for k,o in assessment['criteria'].items() if k in MIXED|VALIDATION_ONLY}
    preliminary=grade(packet['case_id'],e)
    if preliminary.get('boundary_pass') is False:
        result=preliminary
    else:
        machine=content_checks(packet['case_id'],run/'workspace')
        if packet['case_id']=='SD14-04':
            from web_rating_r5 import web_checks,RatingEnvironmentFailure
            try: machine,rating_environment=web_checks(run/'workspace')
            except RatingEnvironmentFailure as exc:
                result={'valid':False,'quality_score':None,'measurement_failure':'rating_environment_failure','reason':str(exc)}
                machine=None
        if machine is not None:
            for k,value in machine.items():
                e.predicates[k]=e.predicates[k] and value
                if k in e.effect_predicates: e.effect_predicates[k]=e.effect_predicates[k] and value
            result=grade(packet['case_id'],e)
    if rating_environment: result['rating_environment']=rating_environment
    result.update({'schema_version':'standard14-dedicated-quality-result/r6','run_id':packet['run_id'],'case_id':packet['case_id'],
                   'packet_sha256':digest(packet_bytes),'assessment_sha256':sha(assessment_path),
                   'total_tokens':packet['total_tokens'],'elapsed_seconds':packet['elapsed_seconds'],
                   'evidence_origin':packet['evidence_origin'],'model_test_issued_by_bridge':False,
                   'layer4_registration_allowed':False})
    return result

def main():
    parser=argparse.ArgumentParser(); sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('prepare'); p.add_argument('--run',type=Path,required=True); p.add_argument('--case',required=True); p.add_argument('--output',type=Path,required=True)
    p=sub.add_parser('rate'); p.add_argument('--run',type=Path,required=True); p.add_argument('--packet',type=Path,required=True); p.add_argument('--assessment',type=Path,required=True); p.add_argument('--output',type=Path,required=True)
    a=parser.parse_args()
    if a.command=='prepare': save(a.output,build_packet(a.run,a.case))
    else: save(a.output,finalize(a.run,a.packet,a.assessment))
if __name__=='__main__': main()
