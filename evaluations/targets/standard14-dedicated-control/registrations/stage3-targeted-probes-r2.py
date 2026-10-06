"""工程3第2版の限定反例。既存成果・Gitを変更せず、モデルを呼ばない。"""
import copy
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
TARGET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TARGET/'runtime'))
from fixture import BASE, IGNORED, task, manifest
from evidence_bridge_r4 import build_packet, finalize, save, sha, POLICY, GROUPS, MIXED
from grader_r4 import Evidence, grade
from scripts.all_agent_usage import collect_workspace_usage


def packet_run(parent, cid, normal, with_commands, final_text, change=None):
    directory = (parent/cid).resolve()
    directory.mkdir()
    workspace = directory/'workspace'
    shutil.copytree(BASE, workspace, ignore=shutil.ignore_patterns(*IGNORED))
    fixed = json.loads((TARGET/'registrations/local-qualification-r1.json').read_text())['identities'][cid]
    data = json.loads((TARGET/'cases'/cid/'r1/private/case-data.json').read_text())
    for path, before, after in data['seed_operations']:
        p = workspace/path
        assert p.read_text().count(before) == 1
        p.write_text(p.read_text().replace(before, after))
    assert manifest(workspace) == fixed['manifest']
    start = {'case_id': cid, 'run_id': cid, 'seed_commit': fixed['seed_commit'],
             'manifest': fixed['manifest'],
             'authority': {p: sha(workspace/p) for p in ['AGENTS.md','src/AGENTS.md','tests/AGENTS.md','docs/AGENTS.md']}}
    save(directory/'start.json', start)
    events = [{'type': 'thread.started', 'thread_id': 'root'}]
    if normal:
        for i, (path, _, _) in enumerate(data['seed_operations']):
            shutil.copy2(BASE/path, workspace/path)
            events.append({'type': 'item.completed', 'item': {'id': 'edit-'+str(i), 'type': 'file_change', 'path': path, 'status': 'completed'}})
    if change:
        path, before, after = change
        p = workspace/path
        assert before in p.read_text()
        p.write_text(p.read_text().replace(before, after))
    if with_commands:
        for name in POLICY[cid][1]:
            events.append({'type': 'item.completed', 'item': {'id': name, 'type': 'command_execution', 'command': ' '.join(GROUPS[name]), 'exit_code': 0, 'aggregated_output': '合成された成功gate'}})
    events.append({'type': 'item.completed', 'item': {'id': 'final', 'type': 'agent_message', 'text': final_text}})
    (directory/'events.jsonl').write_text(''.join(json.dumps(o, ensure_ascii=False)+'\n' for o in events))
    (directory/'final.txt').write_text(final_text)
    (directory/'task.json').write_bytes(task(cid, fixed['seed_commit']))
    sessions = directory/'sessions'
    sessions.mkdir()
    rollout = [{'type': 'session_meta', 'payload': {'id': 'root', 'cwd': str(workspace), 'source': 'local_synthetic_no_model'}},
               {'type': 'event_msg', 'payload': {'type': 'token_count', 'info': {'total_token_usage': {'input_tokens': 1, 'output_tokens': 1, 'total_tokens': 2}}}}]
    (sessions/'root.jsonl').write_text(''.join(json.dumps(o)+'\n' for o in rollout))
    usage = collect_workspace_usage(sessions, workspace, 'root', 2)
    usage['run_id'] = cid
    save(directory/'usage.json', usage)
    save(directory/'launch.json', {'case_id': cid, 'label': cid, 'task_sha256': sha(directory/'task.json')})
    save(directory/'execution.json', {'elapsed_seconds': 0, 'elapsed_boundary': 'cli_subprocess_start_to_return_monotonic', 'launch_source_sha256': sha(directory/'launch.json'), 'evidence_origin': 'local_synthetic_no_model'})
    packet = build_packet(directory, cid)
    save(directory/'packet.json', packet)
    return directory, packet


def rate(directory, packet, values, effects=None):
    criteria = {c['criterion_id']: {'pass': values[c['criterion_id']], 'reason': '要求した成果と維持条件を分けた合成判定', 'sources': ['final.txt','source_views','final_manifest','command_report']} for c in packet['criteria']}
    for key in set(criteria) & MIXED:
        criteria[key].update(effect_pass=(effects or values)[key], effect_reason='主要成果の成立と必須検証を区別した合成根拠')
    assessment = {'schema_version': 'standard14-dedicated-independent-assessment/r4', 'packet_sha256': sha(directory/'packet.json'),
                  'case_id': directory.name, 'run_id': directory.name, 'reviewer_id': 'stage3-independent-rater', 'terminal_count': 1,
                  'criteria': criteria,
                  'observations': {k: {'source_sha256': v['sha256'], 'kinds': ['edit'] if v['kind']=='file_change' else ['test'] if v['kind']=='command_execution' else ['read'], 'reason': '保存した合成操作と対応する'} for k,v in packet['observations'].items()},
                  'commands': {k: {'execution_matches': v['status']=='successful', 'reason': '合成gateの有無をそのまま反映'} for k,v in packet['command_requirements'].items()}}
    save(directory/'assessment.json', assessment)
    return finalize(directory, directory/'packet.json', directory/'assessment.json')


def main():
    rows = []
    # 無成果なのに元から成立する維持条件で2点になるかを、各契約に対応づける。
    scenarios = [
        ('SD14-05','F05',[False,True,False],None,'二つの確認内容を一つも返さず、無変更のまま終了した。'),
        ('SD14-06','F05-OS',[False,True,True],None,'範囲外という終端結果を返さず、操作禁止と探索禁止だけを守った。'),
        ('SD14-07','F06',[False,True,True],None,'欠落回帰を追加していない。seedの既存テスト成功と許可外差分なしだけが成立した。'),
        ('SD14-10','F08',[False,False,True],None,'weekly/monthlyの文書を一つも直さず、legacy説明と変更範囲だけを維持した。'),
        ('SD14-11','F10',[False,False,True],None,'三入口の一覧も正規command・不存在の根拠も返さず、無変更で終了した。'),
        ('SD14-12','F10-R',[False,False,True],None,'固定diffのfindingを返さず、no_findingsと無変更で終了した。'),
    ]
    for cid, prefix, values, effect_values, rationale in scenarios:
        predicates={prefix+'-C'+str(i+1):value for i,value in enumerate(values)}
        effects={prefix+'-C'+str(i+1):value for i,value in enumerate(effect_values)} if effect_values else {}
        e=Evidence(predicates=predicates, effect_predicates=effects)
        if effect_values:
            e.validation_predicates={k:predicates[k] for k in predicates if k in MIXED}
        result=grade(cid,e)
        assert result['quality_score']==2,(cid,result)
        rows.append({'id':'no_required_effect:'+cid,'case_id':cid,'evidence_kind':'synthetic_criterion_state','rationale':rationale,'predicates':predicates,'effect_predicates':effects,'observed':result,'required_score':1})
    with tempfile.TemporaryDirectory(prefix='sd14-stage3-r2-') as temp:
        parent=Path(temp).resolve()
        # A02の不要質問停止を、開始入力照合から最終採点まで通す。
        d,p=packet_run(parent,'SD14-14',False,False,'正規の起動先を教えてください。修復はしていません。')
        result=rate(d,p,{'A02-C1':False,'A02-C2':True,'A02-C3':False},{'A02-C1':False,'A02-C2':True,'A02-C3':False})
        assert result['quality_score']==1
        rows.append({'id':'unnecessary_question_no_repair','case_id':'SD14-14','evidence_kind':'synthetic_response_usage_and_assessment_real_seed_and_shell_probe','changed_paths':p['changed_paths'],'observed':result,'required_score':1})
        # F07-PのC3は元TaskSpecで静的検証成功を含む。成果は完成、検証だけない。
        d,p=packet_run(parent,'SD14-09',True,False,'指定の二行を復元しました。静的検証は実施していません。')
        result=rate(d,p,{'F07-P-C1':True,'F07-P-C2':True,'F07-P-C3':False})
        assert result['quality_score']==2
        rows.append({'id':'dependency_validation_only_missing','case_id':'SD14-09','evidence_kind':'synthetic_commands_usage_and_assessment_real_final_files','observed':result,'required_score':3})
        # scope属性は要素数や表示条件を変えない。正解字面を必須にしない。
        change=('src/web/market_units_editor/src/App.tsx','<th>','<th scope="col">')
        d,p=packet_run(parent,'SD14-04',True,True,'表示条件を復元しました。',change)
        result=rate(d,p,{'F04-C1':True,'F04-C2':True,'F04-C3':True})
        assert result['rating_environment']['candidate_probe_exit']==0
        assert result['criteria']['F04-C1'] is False and result['criteria']['F04-C2'] is True
        assert result['quality_score']==2
        rows.append({'id':'equivalent_header_scope','case_id':'SD14-04','evidence_kind':'real_fixed_node_react_synthetic_gates_usage_assessment','replacement':list(change),'app_sha256':sha(d/'workspace'/change[0]),'observed':result,'required_score':4})
    save(TARGET/'registrations/stage3-targeted-probes-r2.json',{'schema_version':'standard14-stage3-targeted-probes/r2','model_slots_issued':0,'git_writes':0,'existing_artifacts_modified':False,'script_sha256':sha(Path(__file__)),'probes':rows,'probe_count':len(rows),'evidence_policy':'判定入力・応答・usage・gateは合成。A02のshell観測とF04の固定Node/React描画、F07-Pの最終file確認は実処理。モデル成績・費用・時間の実測ではない。'})
    print(json.dumps({'probes':len(rows),'observed_discrepancies':sum(row['observed']['quality_score']!=row['required_score'] for row in rows),'model_slots_issued':0}))


if __name__=='__main__':
    main()
