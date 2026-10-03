"""モード仕様の原文を保持し、運用移行の節だけを別文書へ分離する。"""
import re,hashlib
def separate(source):
 sections=list(re.finditer(r"^## (10|11|12|13)\. .*?$",source,re.M))
 assert len(sections)==4
 main=source;blocks=[];pairs=[]
 for match in sections:
  start=match.start();following=re.search(r"^## \d+\. ",source[match.end():],re.M)
  end=match.end()+following.start() if following else len(source)
  block=source[start:end];heading=match.group()
  stub=heading+"\n\n[この節の原文：運用移行の仕様](market-units-migration-operations.md)\n\n---\n\n"
  main=main.replace(block,stub,1);blocks.append(block);pairs.append((stub,block))
 restored=main
 for stub,block in pairs:restored=restored.replace(stub,block,1)
 assert restored==source
 companion="# Market Units 運用移行の仕様\n\n[仕様全体の入口](market-units-migration-spec.md)\n\n"+"".join(blocks)
 return main,companion,{"restored_bytes_equal":True,"original_sha256":hashlib.sha256(source.encode()).hexdigest(),"moved_sections":[10,11,12,13],"original_bytes":len(source.encode()),"main_bytes":len(main.encode()),"moved_original_bytes":sum(len(x.encode()) for x in blocks)}
