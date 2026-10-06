"""最終treeを独立な固定検査へ結ぶ。応答の意味判定は保存証拠を要求する。"""
import ast, json, shutil, subprocess, tempfile
from pathlib import Path
from fixture import TARGET, BASE, SHARED, manifest
from grader_r4 import Evidence, grade

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
        p['F02-C1']=test(w,str(TARGET/'runtime/private_rating_checks_r4.py')+'::test_engine_arguments')
        p['F02-C2']=test(w,'tests/unit/test_collection_history_updater.py')
    elif case_id=='SD14-03':
        p['F03-C1']=test(w,str(TARGET/'runtime/private_rating_checks_r4.py')+'::test_atomic_cleanup')
        p['F03-C2']=test(w,str(TARGET/'runtime/private_rating_checks_r4.py')+'::test_atomic_failure_result')
        p['F03-C3']=test(w,'tests/unit/test_atomic_save.py::TestContextRepositoryAtomicSave::test_success')
    elif case_id=='SD14-07':
        t=(w/'tests/unit/test_market_units_snapshot.py').read_text()
        # 型・message・空入力の関係を持つ追加testを候補のASTから確認する。
        candidates=[]
        def tests(nodes,prefix=''):
            for n in nodes:
                if isinstance(n,ast.ClassDef): yield from tests(n.body,prefix+n.name+'::')
                elif isinstance(n,ast.FunctionDef) and n.name.startswith('test_'): yield prefix+n.name
        try: parsed=ast.parse(t)
        except SyntaxError: return {'F06-C1':False}
        candidates=list(tests(parsed.body))
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
        from shell_rating_r4 import routing
        main,surrounding=routing(w)
        p['F07-C1' if case_id=='SD14-08' else 'A02-C1']=main
        p['F07-C2' if case_id=='SD14-08' else 'A02-C2']=surrounding
    return p
