"""保存監査の失敗predicateの検出接続。生trace再演とは区別する。"""
import json,hashlib
from pathlib import Path
from grader_r6 import Evidence,grade
from old_new_campaign_r2 import REPO,TARGET
FILES=['candidate276-execution-control-luna6-medium-standard14-n5-quality-audit-r1_2026-09-25.json','sol61-c147-c276-free-low-medium-standard14-n5-cli0159_2026-09-30-c147-medium-quality-audit.json','free-sol61-low-standard14-new-n5_2026-10-03-quality-audit.json','candidate276-execution-control-sol6-low-standard14-n5-quality-audit-r1_2026-09-26.json','candidate276-execution-control-sol6-medium-standard14-n5-quality-audit-r1_2026-09-26.json']
MAP={'TC-F07-DEPENDENCY-PROVENANCE-PAIR':('SD14-09',['F07-P-C1','F07-P-C2','F07-P-C3']),'TC-A02-REPOSITORY-RESOLVABLE-V4-ROUTING':('SD14-14',['A02-C1','A02-C2','A02-C3']),'TC-F10-ENTRYPOINT-INVENTORY-REVIEW':('SD14-11',['F10-C1','F10-C2','F10-C3']),'TC-F10-MONTHLY-FORMAT-TEST-REVIEW':('SD14-12',['F10-R-C1','F10-R-C2','F10-R-C3'])}
rows=[]
for name in FILES:
 p=REPO/'evaluations/results'/name;j=json.loads(p.read_text())
 for r in j['runs']:
  if r['candidate_score']==4 or r['case_id'] not in MAP:continue
  sd,ids=MAP[r['case_id']];fail=r['failures'];pred=dict.fromkeys(ids,True)
  if sd=='SD14-09':pred=dict.fromkeys(ids,False)
  elif sd=='SD14-11':pred[ids[0]]=pred[ids[1]]=False
  elif sd=='SD14-12':pred[ids[0]]=False
  elif sd=='SD14-14':pred[ids[0]]=False
  q=grade(sd,Evidence(predicates=pred,effect_predicates=pred))
  assert q['valid'] and q['quality_score']<4
  rows.append({'run_id':r['run_id'],'case_id':sd,'audit':str(p.relative_to(REPO)),'audit_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'saved_historical_score':r['candidate_score'],'saved_failures':fail,'mapped_missing_predicates':pred,'new_detector_rejects_full_success':True,'predicate_diagnostic_score':q['quality_score'],'raw_trace_replayed':False,'historical_score_rewritten':False})
result={'schema_version':'standard14-historical-failure-predicate-correspondence/r1','mapped_audited_failures':len(rows),'historical_non_a01_failures_total':10,'all_raw_failure_replay_certified':False,'rows':rows,'unmapped_saved_results':['f51b4e9814ad40b6a69a261cee3d8a61:4cdf14fc96a645fda1321a978ba35071','f51b4e9814ad40b6a69a261cee3d8a61:992d910948574b5aa594d391504734fc','f51b4e9814ad40b6a69a261cee3d8a61:F07起動'],'limitation':'保存監査の欠落predicateが全成功にならない接続だけを確認。元のdiff・終了応答・tool traceを専用素材で再演した証明ではない。既存点数は変更しない。'}
(TARGET/'registrations/stage5-historical-failure-correspondence-r1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(len(rows))
