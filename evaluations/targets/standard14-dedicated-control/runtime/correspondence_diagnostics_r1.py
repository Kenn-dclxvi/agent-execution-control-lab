"""配送と保持量の実測診断。未観測のピークと専有物理量は埋めない。"""
import collections,hashlib,json,re,sys
from pathlib import Path
from evidence_bridge_r6 import save,load
from fixture import manifest

def delivery(run):
 u=load(run/'usage.json');calls={};outputs=[];targets=collections.Counter();m=manifest(run/'workspace')
 for s in u['sessions']:
  for l in Path(s['rollout_file']).open():
   j=json.loads(l);d=j.get('payload',{});t=d.get('type');cid=d.get('call_id')
   if t in ['function_call','custom_tool_call']:
    args=d.get('arguments') or d.get('input') or '';calls[cid]={'tool':d.get('name'),'request_sha256':hashlib.sha256(args.encode()).hexdigest(),'mentioned_visible_paths':[p for p in m if p in args]}
   if t in ['function_call_output','custom_tool_call_output']:
    out=d.get('output','');raw=(out if isinstance(out,str) else json.dumps(out,ensure_ascii=False)).encode();call=calls.get(cid,{})
    outputs.append({'thread_id':s['thread_id'],'call_id':cid,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'truncation_marker':bool(re.search(rb'(?:[Tt]runcated|tokens truncated|original token count)',raw)),**call})
    targets.update(call.get('mentioned_visible_paths',[]))
 return {'serialized_tool_output_utf8_bytes':sum(o['bytes'] for o in outputs),'outputs':outputs,'exact_repeated_output_count':len(outputs)-len({o['sha256'] for o in outputs}),'truncation_marked_outputs':sum(o['truncation_marker'] for o in outputs),'visible_path_mentions_in_requests':dict(targets),'repeated_mentioned_targets':{p:n for p,n in targets.items() if n>1},'limitation':'実配送tool出力と要求中の可視path字句を記録。test/diff引数を含む字句の出現を読了・全file取得と同一視しない。コマンド原文は非公開rolloutを参照。'}

def storage(root):
 groups=collections.defaultdict(lambda:{'logical_bytes':0,'allocated_bytes_stat_blocks':0,'files':0})
 for p in root.rglob('*'):
  if p.is_symlink() or not p.is_file():continue
  rel=p.relative_to(root);parts=rel.parts
  if 'workspace' in parts or 'fixed-fixtures' in parts or 'layer1-sources' in parts or 'environment-checks' in parts:
   if '.git' in parts:k='git_objects' if 'objects' in parts else 'git_metadata_other'
   elif 'node_modules' in parts or '.venv' in parts or 'dist' in parts:k='workspace_dependencies_and_builds'
   elif '__pycache__' in parts or '.pytest_cache' in parts:k='workspace_caches'
   else:k='workspace_visible_files'
  elif 'run-node-environments' in parts or 'controller-node-environment' in parts or 'environment-check' in parts:k='node_environment_copies'
  elif 'layer1' in parts:k='layer1_storage'
  else:k='saved_evidence_and_controller'
  st=p.stat();g=groups[k];g['logical_bytes']+=st.st_size;g['allocated_bytes_stat_blocks']+=st.st_blocks*512;g['files']+=1
 return {'root':str(root),'groups':dict(groups),'retained_logical_bytes':sum(g['logical_bytes'] for g in groups.values()),'allocated_bytes_stat_blocks':sum(g['allocated_bytes_stat_blocks'] for g in groups.values()),'peak_bytes':None,'apfs_exclusive_physical_bytes':None,'shared_dependencies_excluded':True,'snapshot':'終了後の現物保持量。削除・推計・APFS共有分の補正なし。'}

if __name__=='__main__':
 root=Path(sys.argv[1]);out=Path(sys.argv[2]);rows={}
 for p in sorted(root.glob('cases/*/runs/*/usage.json')):rows[str(p.parent.relative_to(root))]=delivery(p.parent)
 save(out,{'schema_version':'standard14-correspondence-diagnostics/r1','delivery':rows,'storage':storage(root)});print('diagnostics',len(rows),flush=True)
