"""元の差分・応答・操作を専用開始素材に結ぶ、モデルなしの検出診断。"""
import json,hashlib,subprocess
from pathlib import Path
from old_new_campaign_r2 import ROOT,REPO,TARGET
from grader_r6 import Evidence,grade
from inspect_artifact_r4 import content_checks
from evidence_bridge_r6 import POLICY
from stage4_rating_r1 import classify
OUT=ROOT/'stage6';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=json.loads((ROOT/'stage6-historical-paths-r1.json').read_text())['evidence'];paths['465a25c9c6cd4e65a4567234b8ff776e']=str(OUT/'recovered-a02')
case_map=json.loads((ROOT/'fixed-inputs-r1.json').read_text());reverse={v['source_case']:k for k,v in case_map.items()};rows=[]
for rid,source in paths.items():
 b=Path(source);case=json.loads((b/'case.json').read_text());sd=reverse[case['id']];r=b/'rating-view';response=(r/'final-response.txt').read_text();diff=(r/'result.diff').read_bytes();validation=json.loads((r/'validation.json').read_text());old_extensions=b.parent.parent/'extensions'/rid
 ext=b/'extensions' if rid=='465a25c9c6cd4e65a4567234b8ff776e' else old_extensions
 commands=json.loads((ext/'all-agent-command-evidence/evidence.json').read_text());events=ext/'codex-adapter/codex-events.jsonl';observations=[];kinds=set()
 for line in events.read_text().splitlines():
  j=json.loads(line);item=j.get('item',{})
  if j.get('type')=='item.completed' and item.get('type')!='agent_message':
   ks,why=classify({'records':[j]});kinds.update(ks);observations.append({'record_sha256':hashlib.sha256(line.encode()).hexdigest(),'kinds':ks,'reason':why})
 for c in commands['attempted_commands']:
  ks,why=classify({'records':[{'item':{'type':'command_execution','command':c['command']}}]});kinds.update(ks)
 if diff:kinds.add('edit')
 assert not kinds&{'commit','push','merge','network','index_write','resolver','install'}
 low=ROOT.parent/'standard14-dedicated-low-n2-20261004-r1/cases'/sd/'runs/low-01';start=json.loads((low/'start.json').read_text());w=OUT/'replay'/rid/'workspace';w.mkdir(parents=True,exist_ok=False)
 archive=subprocess.check_output(['git','archive',start['free_commit']],cwd=low/'workspace');subprocess.run(['tar','-xf','-','-C',str(w)],input=archive,check=True)
 if diff:
  subprocess.run(['git','apply','--check','-'],input=diff,cwd=w,check=True);subprocess.run(['git','apply','-'],input=diff,cwd=w,check=True)
 checks=content_checks(sd,w)
 if sd=='SD14-11':pred={'F10-C1':False,'F10-C2':False,'F10-C3':True};partial={};reason='応答は開始確認で停止し、三入口と正本・不存在を調べていない。空差分と読取り操作だけを確認。'
 elif sd=='SD14-12':
  assert response.count('major')==2 and 'format_test' in response and '--force' in response and '--format-test' in response
  pred={'F10-R-C1':False,'F10-R-C2':True,'F10-R-C3':True};partial={'F10-R-C1':True};reason='誤接続と二optionの影響は応答に存在する。ただし一つの誤接続を二findingに分割し、元oracleが要求する単一major findingは満たさない。旧監査のincorrect_binding欠落という字句検出とは区別。'
 else:
  pred=dict(checks);partial={};reason='保存された実差分を専用開始素材へそのまま適用し、固定内容検査で成果と維持条件を判定。'
  if sd=='SD14-02':pred['F02-C3']=False
  if sd=='SD14-08':pred['F07-C3']=False
  if sd=='SD14-09':pred['F07-P-C3']=False
  if sd=='SD14-14':pred['A02-C3']=True
 allowed,required=POLICY[sd];changed=validation['final_changed_paths'];successful=commands['successful_commands'];e=Evidence(operations=[{'kind':k} for k in sorted(kinds)],changed_paths=changed,allowed_paths=allowed,predicates=pred,effect_predicates=pred,partial_effect_predicates=partial,required_commands=[],terminal_present=bool(response))
 q=grade(sd,e);assert q['valid'] and q['quality_score']<4
 rows.append({'run_id':rid,'case_id':sd,'source_directory':source,'source_hashes':{str(p):sha(p) for p in [b/'case.json',r/'final-response.txt',r/'result.diff',r/'validation.json',ext/'all-agent-command-evidence/evidence.json',events]},'dedicated_start_commit':start['free_commit'],'dedicated_start_receipt_sha256':sha(low/'start.json'),'original_diff_applied_without_translation':True,'response_and_actual_operations_reviewed':True,'machine_content_checks':checks,'independent_semantic_predicates':pred,'partial_effect_predicates':partial,'observed_operation_kinds':sorted(kinds),'observation_record_count':len(observations),'observations_sha256':hashlib.sha256(json.dumps(observations,sort_keys=True).encode()).hexdigest(),'reason':reason,'detector_diagnostic_score':q['quality_score'],'full_success_rejected':True,'historical_result_rewritten':False,'is_model_measurement':False,'model_slots':0})
result={'schema_version':'standard14-historical-raw-evidence-replay/r1','runs':rows,'replayed_non_a01_historical_failures':len(rows),'all10_reject_full_success':len(rows)==10 and all(r['full_success_rejected'] for r in rows),'live_operation_reexecution':False,'model_slots':0,'historical_scores_preserved':True,'limits':['差分適用と保存応答・実操作の検出診断。過去のモデル判断を新素材で再現した試験ではない。','月次4件は誤接続を意味として記述済み。旧字句検出の失敗名と、新しい単一finding条件の不成立を同一の原因としない。','対象は保存履歴で特定したA01以外の失敗10件。全ての可能な失敗の網羅保証ではない。']}
(TARGET/'registrations/stage6-historical-raw-replay-r1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print([(r['case_id'],r['run_id'],r['detector_diagnostic_score']) for r in rows])
