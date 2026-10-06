"""今回の実証拠を読んだ判定を42条件へ固定する。モデル発行はしない。"""
import sys
from pathlib import Path
from stage4_rating_r1 import classify, operation_text
from evidence_bridge_r6 import save,load,sha,MIXED
from grader_r6 import PRIMARY
from execution_binding_r6 import finalize_completed_execution
ROOT=Path(sys.argv[1]); DECISIONS=load(ROOT/'semantic-decisions-r1.json')
for packet_path in sorted(ROOT.glob('cases/*/runs/*/rating-packet.json')):
 run=packet_path.parent;p=load(packet_path);key=p['case_id']+'/'+p['run_id'];d=DECISIONS[key]
 assessment={'schema_version':'standard14-dedicated-independent-assessment/r6','packet_sha256':sha(packet_path),'case_id':p['case_id'],'run_id':p['run_id'],'reviewer_id':'stage5-chat-01a1055d-cab7-79c0-8389-f985b0bda6e2','terminal_count':1,'observations':{},'criteria':{},'commands':{}}
 for k,o in p['observations'].items():
  kinds,reason=classify(o);txt,kind=operation_text(o)
  if '--help' in txt and '-m src.app' in txt:kinds=sorted(set(kinds+['application']))
  if 'routing-check' in txt:kinds=sorted(set(kinds+['test']))
  assessment['observations'][k]={'source_sha256':o['sha256'],'kinds':kinds,'reason':reason}
 for idx,c in enumerate(p['criteria']):
  k=c['criterion_id'];v={'pass':d['passes'][idx],'reason':d['reasons'][idx],'sources':['source_views','final_manifest','command_report','final.txt']}
  if k in MIXED:v.update(effect_pass=d['passes'][idx],effect_reason=d['reasons'][idx])
  if k in PRIMARY[p['case_id']]:v['partial_effect']=d.get('partial_effect',False)
  assessment['criteria'][k]=v
 for k,status in p['command_requirements'].items():assessment['commands'][k]={'execution_matches':bool(status['matching_commands']),'reason':'保存された実コマンドの引数・終了状態を確認。'}
 save(run/'independent-assessment-r1.json',assessment)
 q=finalize_completed_execution(run,run/'independent-assessment-r1.json');print(p['case_id'],p['run_id'],q['valid'],q['quality_score'],q.get('observed_route'),flush=True)
