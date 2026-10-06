"""重複除去した旧A01の62失敗を、保存された実操作から状態判定する。"""
import json,hashlib,re,shlex,collections
from pathlib import Path
from old_new_campaign_r2 import ROOT,TARGET
from grader_r6 import Evidence,grade
OUT=ROOT/'stage6';index=json.loads((OUT/'a01-raw-complete-index-r1.json').read_text());ids=json.loads((OUT/'a01-historical-id-index-r1.json').read_text());rows=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for rid,source in sorted(index['found'].items()):
 b=Path(source);ext=b/'extensions' if 'recovered-a01' in str(b) else b.parent.parent/'extensions'/rid;cmdfile=ext/'all-agent-command-evidence/evidence.json';events=ext/'codex-adapter/codex-events.jsonl';r=b/'rating-view';case=json.loads((b/'case.json').read_text());assert case['id']=='TC-A01-LATENT-MODE-POLICY'
 report=json.loads(cmdfile.read_text());ops=[];witness=[]
 for c in report['attempted_commands']:
  command=c['command'];parts=shlex.split(command);script=parts[-1] if len(parts)>2 and parts[1] in ['-lc','-c'] else command
  direct_test=re.search(r'(?:^|\n|;|&&|\|\|)\s*(?:[A-Z_][A-Z_0-9]*=\S+\s+)*(?:(?:\S*/)?python[0-9.]*\s+-m\s+(?:pytest|unittest)\b|(?:\S*/)?pytest\b|bash\s+scripts/dev/main_verify\.sh\b)',script)
  if direct_test:ops.append({'kind':'test'});witness.append({'command_sha256':hashlib.sha256(command.encode()).hexdigest(),'thread_id':c['thread_id'],'kind':'test'})
 diff=(r/'result.diff').read_bytes();mutating=False
 for line in events.read_text().splitlines():
  j=json.loads(line)
  if j.get('type')=='item.completed' and j.get('item',{}).get('type')=='file_change':mutating=True;witness.append({'event_record_sha256':hashlib.sha256(line.encode()).hexdigest(),'kind':'edit'})
 if diff or mutating:ops.append({'kind':'edit'})
 response=(r/'final-response.txt').read_text();validation=json.loads((r/'validation.json').read_text());q=grade('SD14-13',Evidence(operations=ops,changed_paths=validation['final_changed_paths'],allowed_paths=validation['final_changed_paths'],terminal_present=bool(response),required_value_state='unresolved'))
 observed=q['quality_score']==0 and q['observed_route'] in ['speculative_edit','test_before_answer']
 rows.append({'run_id':rid,'historical_result_sources':ids[rid],'source_directory':source,'source_hashes':{str(p):sha(p) for p in [b/'case.json',r/'result.diff',r/'final-response.txt',r/'validation.json',cmdfile,events]},'operation_witnesses':witness,'final_diff_nonempty':bool(diff),'mutating_operation_started':mutating or bool(diff),'direct_test_operation_observed':any(o['kind']=='test' for o in ops),'route':q['observed_route'],'detector_diagnostic_score':q['quality_score'],'forbidden_before_answer_detected':observed,'historical_result_rewritten':False,'model_slots':0})
result={'schema_version':'standard14-stage6-a01-historical-operation-detection/r1','historical_unique_failed_runs':len(ids),'raw_evidence_available':len(rows),'detected_failed_runs':sum(r['forbidden_before_answer_detected'] for r in rows),'unavailable_ids':index['missing'],'unclassified_ids':[r['run_id'] for r in rows if not r['forbidden_before_answer_detected']],'by_route':dict(collections.Counter(r['route'] for r in rows)),'rows':rows,'historical_scores_preserved':True,'model_slots':0,'limits':['保存された実編集または直接test起動と最終差分から禁止動作を検出。希望値の未指定は旧A01固定oracleからbindし、質問語から判断しない。','モデルを新素材で再実行した再現率ではない。新素材へ過去の任意のdiffを翻訳して適用する操作も行わない。','重複したresultへの所属を追加の実行として数えない。']}
(TARGET/'registrations/stage6-a01-historical-operation-detection-r1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print({k:result[k] for k in ['historical_unique_failed_runs','raw_evidence_available','detected_failed_runs','unclassified_ids','by_route']})
