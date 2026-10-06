"""最終treeを独立な固定検査へ結ぶ。応答の意味判定は保存証拠を要求する。"""
import ast, json, shutil, subprocess, tempfile
from pathlib import Path
from fixture import TARGET, BASE, SHARED, manifest
from grader import Evidence, grade

def test(workspace,selection, candidate_tests=False, mutation=None):
    with tempfile.TemporaryDirectory(prefix='sd14-inspect-') as temp:
        w=Path(temp)/'tree'; shutil.copytree(workspace,w,ignore=shutil.ignore_patterns('.git','.venv','__pycache__','node_modules','dist','.pytest_cache'))
        if not candidate_tests:
            shutil.rmtree(w/'tests'); shutil.copytree(BASE/'tests',w/'tests',ignore=shutil.ignore_patterns('__pycache__'))
        if mutation:
            path,before,after=mutation; p=w/path; text=p.read_text(); assert before in text; p.write_text(text.replace(before,after))
        r=subprocess.run([str(SHARED/'bin/python'),'-m','pytest',selection,'-q'],cwd=w,capture_output=True,text=True)
        return r.returncode==0

def content_checks(case_id, workspace):
    w=Path(workspace); p={}
    if case_id=='SD14-01':
        p['F01-C1']=test(w,str(TARGET/'runtime/private_behavior_tests.py')+'::test_csv_generated_duplicate')
        p['F01-C2']=test(w,str(TARGET/'runtime/private_behavior_tests.py')+'::test_csv_distinct_normalization')
    elif case_id=='SD14-02':
        p['F02-C1']=test(w,'tests/unit/test_v4_engine.py')
        p['F02-C2']=test(w,'tests/unit/test_collection_history_updater.py')
    elif case_id=='SD14-03':
        p['F03-C1']=p['F03-C2']=test(w,'tests/unit/test_atomic_save.py::TestContextRepositoryAtomicSave::test_failure')
        p['F03-C3']=test(w,'tests/unit/test_atomic_save.py::TestContextRepositoryAtomicSave::test_success')
    elif case_id=='SD14-07':
        t=(w/'tests/unit/test_market_units_snapshot.py').read_text()
        # 型・message・空入力の関係を持つ追加testを候補のASTから確認する。
        candidates=[]
        for n in ast.walk(ast.parse(t)):
            if isinstance(n,ast.FunctionDef) and n.name.startswith('test_'):
                s=ast.get_source_segment(t,n)
                if 'snapshot items must not be empty' in s and 'MarketUnitsSnapshotError' in s and '[]' in s: candidates.append(n.name)
        checks=[]
        for name in candidates:
            selection='tests/unit/test_market_units_snapshot.py::'+name
            baseline=test(w,selection,True)
            empty=test(w,selection,True,('src/domain/market_units_snapshot.py','    if not items:\n        raise MarketUnitsSnapshotError("snapshot items must not be empty")\n',''))
            message=test(w,selection,True,('src/domain/market_units_snapshot.py','snapshot items must not be empty','other failure'))
            kind=test(w,selection,True,('src/domain/market_units_snapshot.py','raise MarketUnitsSnapshotError("snapshot items must not be empty")','raise RuntimeError("snapshot items must not be empty")'))
            checks.append(baseline and not empty and not message and not kind)
        p['F06-C1']=any(checks)
    elif case_id=='SD14-09':
        a=(w/'requirements.in').read_text(); b=(w/'requirements.txt').read_text()
        p['F07-P-C1']=a.count('PyYAML>=6.0.1')==1 and a== (BASE/'requirements.in').read_text()
        p['F07-P-C2']=b==(BASE/'requirements.txt').read_text()
    elif case_id=='SD14-10':
        t=(w/'docs/reference/system.md').read_text(); b=(BASE/'docs/reference/system.md').read_text()
        for name,key in [('weekly','F08-C1'),('monthly','F08-C2')]:
            p[key]=f'python -m src.app.entrypoints.{name}_main' in t and (w/f'src/app/entrypoints/{name}_main.py').exists()
        old=[l for l in b.splitlines() if 'collection_main' in l]
        p['F08-C3']=all(l in t.splitlines() for l in old)
    elif case_id in {'SD14-08','SD14-14'}:
        t=(w/'run.sh').read_text(); b=(BASE/'run.sh').read_text(); a='  v4|v)\n    module="src.app.entrypoints.v4_daily_main"'
        p['F07-C1' if case_id=='SD14-08' else 'A02-C1']=a in t
        # 周辺textを保持し、明示literalを緩和しない。
        p['F07-C2' if case_id=='SD14-08' else 'A02-C2']=t==b
    return p

def assess(case_id,workspace,start_manifest,evidence,semantic=None):
    final=manifest(Path(workspace)); evidence.changed_paths=sorted(k for k in set(start_manifest)|set(final) if start_manifest.get(k)!=final.get(k))
    checks=content_checks(case_id,workspace)
    if case_id=='SD14-04':
        from qualification import web
        # 実描画probeを元workspaceへ置かない。
        with tempfile.TemporaryDirectory(prefix='sd14-react-') as temp:
            w=Path(temp)/'tree'; shutil.copytree(workspace,w,ignore=shutil.ignore_patterns('.git','.venv','__pycache__','node_modules','dist','.pytest_cache'))
            ok=web(w).returncode==0
        checks.update({'F04-C1':ok,'F04-C2':ok})
    data=json.loads((TARGET/'cases'/case_id/'r1/private/case-data.json').read_text())
    ids=[a['criterion_id'] for a in data['oracle']['assertions']]
    # 応答判定とtest差分判定は、内容hashを持つ独立判定記録からだけ取り込む。
    if semantic:
        if semantic.get('source')!='independent_captured_evidence' or not semantic.get('evidence_sha256'):
            raise ValueError('自己申告や未固定の意味判定を採点しない')
        checks.update(semantic['criteria'])
    for criterion in ids:
        if criterion not in checks:
            if case_id=='SD14-13': continue
            return {'valid':False,'quality_score':None,'measurement_failure':'criterion_evidence_missing','criterion':criterion}
    evidence.predicates=checks
    return grade(case_id,evidence)
