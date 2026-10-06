"""固定Node/cacheから独立にinstallし、描画の二条件を分離する。"""
import json,shutil,subprocess,tempfile
from html.parser import HTMLParser
from pathlib import Path
from fixture import BASE,IGNORED,TARGET,sha
from node_environment_r3 import environment,REG
class RatingEnvironmentFailure(RuntimeError): pass
PROBE='''import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import App from './src/App';
const f={name:'A',asset_class:'US_STOCK',currency:'USD',units:'2',source_symbol:'X',csv_url:''};
const rows=[];
for(const [funds,search,count,empty] of [[[],'',6,true],[[{...f,audit_match_key:'  '}],'',6,false],[[{...f,audit_match_key:'K'}],'',7,false],[[f,{...f,name:'B',audit_match_key:'K'}],'',7,false],[[{...f,audit_match_key:'K'}],'missing',7,true]] as const){
 const html=renderToStaticMarkup(<App funds={[...funds]} search={search}/>);
 rows.push({html,count,empty,rowCount:funds.filter(f=>f.name.includes(search)).length});
}
console.log(JSON.stringify(rows));
'''
class TableStructure(HTMLParser):
    def __init__(self):
        super().__init__(); self.section=None; self.headers=0; self.rows=[]; self.row=None; self.table_depth=0
    def handle_starttag(self,tag,attrs):
        if tag=='table': self.table_depth+=1
        if self.table_depth!=1: return
        if tag in {'thead','tbody'}: self.section=tag
        elif self.section=='thead' and tag=='th': self.headers+=1
        elif self.section=='tbody' and tag=='tr': self.row=[]
        elif self.section=='tbody' and self.row is not None and tag in {'td','th'}: self.row.append(dict(attrs))
    def handle_endtag(self,tag):
        if self.table_depth==1:
            if tag=='tr' and self.section=='tbody' and self.row is not None: self.rows.append(self.row); self.row=None
            if tag in {'thead','tbody'}: self.section=None
        if tag=='table': self.table_depth-=1

def rendered_predicates(rows):
    headers_cells=[]; spans=[]
    for r in rows:
        dom=TableStructure(); dom.feed(r['html']); count=r['count']
        headers_cells.append(dom.headers==count and (r['empty'] or (len(dom.rows)==r['rowCount'] and all(len(cells)==count for cells in dom.rows))))
        spans.append(not r['empty'] or (len(dom.rows)==1 and len(dom.rows[0])==1 and dom.rows[0][0].get('colspan')==str(count)))
    return {'F04-C1':all(headers_cells),'F04-C2':all(spans)}

def web_checks(workspace):
    with tempfile.TemporaryDirectory(prefix='sd14-fixed-web-rating-') as tmp:
        tmp=Path(tmp); w=tmp/'web'; source=Path(workspace)/'src/web/market_units_editor'
        shutil.copytree(source,w,ignore=shutil.ignore_patterns(*IGNORED))
        # package/lockはモデル差分を実行せず、固定原文から依存を構築する。
        fixed=BASE/'src/web/market_units_editor'
        for name in ['package.json','package-lock.json']: shutil.copy2(fixed/name,w/name)
        try:
            env=environment(tmp/'environment')
            ci=subprocess.run(['npm','ci','--ignore-scripts','--no-audit','--no-fund','--include=dev'],cwd=w,env=env,capture_output=True,text=True)
            if ci.returncode: raise RatingEnvironmentFailure('fixed dependency installation failed')
            check=w/'environment-probe.tsx'; check.write_text("import React from 'react'; import {renderToStaticMarkup} from 'react-dom/server'; if(renderToStaticMarkup(<b>x</b>)!=='<b>x</b>') throw Error('environment');")
            tsx=[str(tmp/'environment/bin/node'),str(w/'node_modules/tsx/dist/cli.mjs')]
            preflight=subprocess.run([*tsx,check.name],cwd=w,env=env,capture_output=True)
            if preflight.returncode: raise RatingEnvironmentFailure('fixed React runtime failed')
        except (ValueError,OSError) as exc: raise RatingEnvironmentFailure(str(exc)) from exc
        (w/'probe.tsx').write_text(PROBE)
        proc=subprocess.run([*tsx,'probe.tsx'],cwd=w,env=env,capture_output=True,text=True)
        if proc.returncode: predicates={'F04-C1':False,'F04-C2':False}
        else:
            try: rows=json.loads(proc.stdout)
            except json.JSONDecodeError: predicates={'F04-C1':False,'F04-C2':False}
            else: predicates=rendered_predicates(rows)
        return predicates,{'binding_sha256':sha(REG),'closure_sha256':sha(TARGET/'registrations/node-dynamic-closure-r4.json'),'package_sha256':sha(fixed/'package.json'),'lock_sha256':sha(fixed/'package-lock.json'),'offline_install_exit':ci.returncode,'react_runtime_exit':preflight.returncode,'candidate_probe_exit':proc.returncode,'base_node_modules_used':False}
