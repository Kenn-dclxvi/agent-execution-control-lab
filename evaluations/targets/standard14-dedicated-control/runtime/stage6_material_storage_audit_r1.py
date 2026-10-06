"""全14件の正本・契約・開始履歴と、同じ実行領域の終了保持量を照合する。"""
import json,hashlib,subprocess,statistics
from pathlib import Path
from old_new_campaign_r2 import ROOT,REPO,TARGET
from correspondence_diagnostics_r1 import storage
from fixture import task
OUT=ROOT/'stage6'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
fixed=read(ROOT/'fixed-inputs-r1.json');accepted=read(TARGET/'registrations/stage3-verdict-r4.json');comparison=read(TARGET/'results/standard14-old-new-comparison-r1.json');cases=[]
for c in accepted['cases']:
 sd=c['case_id'];oldcase=REPO/'evaluations/cases'/c['source_case']/c['source_revision'];newcase=TARGET/'cases'/sd/'r1';op=oldcase/'trial-prompt-input.json';np=newcase/'trial-prompt-input.json';old_task=read(op);new_task=read(np);assert old_task==new_task
 old_contract=read(oldcase/'private/case-data.json');new_contract=read(newcase/'private/case-data.json');assert old_contract['oracle']['assertions']==new_contract['oracle']['assertions']
 old=ROOT/'low/cases'/sd/'runs/low-01';new=ROOT.parent/'standard14-dedicated-low-n2-20261004-r1/cases'/sd/'runs/low-01';os=read(old/'start.json');ns=read(new/'start.json');common_keys=set(os)&set(ns);only_old=sorted(set(os)-set(ns));only_new=sorted(set(ns)-set(os));assert only_old==[] and only_new==['git_objects_allocated_bytes','git_objects_logical_bytes']
 old_delivered=(ROOT/'cases'/sd/'task.txt').read_bytes();new_delivered=(new/'task.json').read_bytes();expected=old_delivered
 if sd=='SD14-12':expected=old_delivered.replace(b'a53601614b41f52633f1d75e77c72861a0f0f1c8',ns['seed_commit'].encode())
 assert expected==new_delivered
 authority={name:{'old':os['authority'][name],'new':ns['authority'][name],'same':os['authority'][name]==ns['authority'][name]} for name in ['AGENTS.md','src/AGENTS.md','tests/AGENTS.md','docs/AGENTS.md']};assert all(v['same'] for v in authority.values())
 original_required_paths=[x['path'] for x in old_contract['fixture']['source_files']];present={p:{'old_present':p in os['manifest'],'new_present':p in ns['manifest']} for p in original_required_paths};assert all(v['old_present'] and v['new_present'] for v in present.values())
 graphs={}
 for name,run,start in [('old',old,os),('new',new,ns)]:
  w=run/'workspace';seed=start['seed_commit'];free=start['free_commit'];delta=subprocess.check_output(['git','diff','--numstat',seed,free],cwd=w,text=True)
  graphs[name]={'seed_commit':seed,'free_commit':free,'seed_to_free_numstat':delta,'seed_to_free_numstat_sha256':hashlib.sha256(delta.encode()).hexdigest(),'root_at_seed_bytes':len(subprocess.check_output(['git','show',seed+':AGENTS.md'],cwd=w)),'root_at_free_bytes':len(subprocess.check_output(['git','show',free+':AGENTS.md'],cwd=w)),'commit_log_sha256':hashlib.sha256(subprocess.check_output(['git','log','-5','--format=%H %P %s',free],cwd=w)).hexdigest()}
 cases.append({'case_id':sd,'criteria':c['criterion_ids'],'original_task_json_same':True,'delivered_task_same_except_declared_monthly_seed':True,'original_42_criterion_semantics_same':True,'authority':authority,'required_source_paths':present,'source_relationship_acceptance_receipt':'registrations/stage3-verdict-r4.json','source_relationship_accepted':c['stage3_acceptance_pass'],'source_bytes_or_path_count_not_used_as_equivalence_proof':True,'start_receipt_keyset_same':False,'start_receipt_keys_only_old':only_old,'start_receipt_keys_only_dedicated':only_new,'common_identity_fields_present':True,'git_start_relationship':graphs,'empirical_difficulty_equivalence':'unproved','source_hashes':{str(p.relative_to(REPO)):sha(p) for p in [op,np,oldcase/'private/case-data.json',newcase/'private/case-data.json']}})
 normalized=[]
for reason in ['low','medium','high']:
 values={}
 for side in ['old','dedicated']:
  rows=[r for r in comparison['rows'] if r['side']==side and r['reasoning_effort']==reason];groups={}
  for row in rows:
   s=storage(Path(row['raw_evidence_directory']))
   for k,v in s['groups'].items():
    g=groups.setdefault(k,{'logical_bytes':0,'allocated_bytes_stat_blocks':0,'files':0})
    for name in g:g[name]+=v[name]
  values[side]={'run_count':len(rows),'groups':groups,'logical_bytes':sum(v['logical_bytes'] for v in groups.values()),'allocated_bytes_stat_blocks':sum(v['allocated_bytes_stat_blocks'] for v in groups.values()),'physical_exclusive_or_peak':None}
 normalized.append({'reasoning_effort':reason,'scope':'28個の完了した個別実行directory。workspace、Git objects、成果・cache・保存証拠を含み、実行directory外の準備原本と共通依存は除外。','measurements':values,'retained_logical_reduction_percent':100*(1-values['dedicated']['logical_bytes']/values['old']['logical_bytes']),'apfs_exclusive_reduction_certified':False,'peak_reduction_certified':False})
shared=storage(ROOT.parent/'standard14-old-new-paired-n2-20261004-r1/fixed-fixtures')
result={'schema_version':'standard14-stage6-material-and-storage-audit/r1','case_count':len(cases),'criterion_count':sum(len(c['criteria']) for c in cases),'cases':cases,'normalized_storage':normalized,'old_shared_prepared14_retained_storage':shared,'model_slots':0,'preflight_schema_compatibility_incomplete':True,'full_comparative_compatibility_certified':False,'source_relationships_preserved_per_accepted_stage3':True,'difficulty_certified':False,'findings':['全14件の元TaskSpec JSONと42条件原文・非root正本は一致。実配送は月次固定seedの宣言済み置換だけ。','旧側のseedからFree開始までのroot削除は履歴の内容差分として見える。専用側は内容差分がない。開始履歴の判断負荷は同等と認定しない。','開始gateの明示的成否値は旧新どちらの開始記録にもなく、成功・失敗のモデル解釈が分かれる。専用開始記録だけにGit容量2項目が存在する。前回のschema一致の記述は誤りであり、完全な比較互換性は認定しない。','終了後の同じ個別実行領域における論理保持量は比較できる。準備原本、APFS共有物理量、実行中ピークはその比較へ混ぜない。']}
(TARGET/'registrations/stage6-material-storage-audit-r1.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print([(r['reasoning_effort'],r['retained_logical_reduction_percent']) for r in normalized])
