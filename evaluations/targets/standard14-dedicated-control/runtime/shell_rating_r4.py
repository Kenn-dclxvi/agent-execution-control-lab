"""run.shを独立な模擬Pythonで実行し、起動先と周辺の経路を照合する。"""
import shutil,subprocess,tempfile
from pathlib import Path
from fixture import BASE
ARGS=[[],['v4','-u'],['v','-u'],['weekly','-u'],['w','-u'],['monthly','-u'],['m','-u'],['2026-04-20','-u'],['-F','-u'],[''],['daily'],['d'],['legacy'],['monex'],['collection'],['c'],['-h'],['--help'],['help'],['unknown']]
def observe(source):
    with tempfile.TemporaryDirectory(prefix='sd14-shell-rating-') as tmp:
        w=Path(tmp); shutil.copy2(source,w/'run.sh'); (w/'.venv/bin').mkdir(parents=True)
        p=w/'.venv/bin/python'; p.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n'); p.chmod(0o755)
        syntax=subprocess.run(['bash','-n','run.sh'],cwd=w,capture_output=True)
        if syntax.returncode: return None
        rows=[]
        for args in ARGS:
            proc=subprocess.run(['bash','run.sh',*args],cwd=w,capture_output=True,text=True,timeout=10)
            rows.append((proc.returncode,proc.stdout.replace(str(w),'<workspace>'),proc.stderr.replace(str(w),'<workspace>')))
        return rows

def routing(workspace):
    expected=observe(BASE/'run.sh'); actual=observe(Path(workspace)/'run.sh')
    if actual is None: return False,False
    main=all(actual[i]==expected[i] for i in [1,2])
    surrounding=all(actual[i]==expected[i] for i in range(len(ARGS)) if i not in [1,2])
    # Web起動は外部操作せず、当該関数とcase armの原文保持を確認する。
    def web_source(p):
        s=p.read_text(); return (s[s.index('is_usable_node_binary()'):s.index('SCRIPT_DIR=')],s[s.index('  collection-web|cw|'):s.index('  -h|--help|')])
    surrounding=surrounding and web_source(Path(workspace)/'run.sh')==web_source(BASE/'run.sh')
    return main,surrounding
