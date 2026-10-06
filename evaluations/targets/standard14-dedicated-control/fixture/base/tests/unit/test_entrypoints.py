from pathlib import Path
import ast
import pytest
@pytest.mark.parametrize('name,engine', [('v4_daily','V4PortfolioEngine'),('monthly','MonthlyEngine'),('weekly','WeeklyEngine')])
def test_current_entrypoint(name,engine):
    path=Path('src/app/entrypoints')/(name+'_main.py')
    tree=ast.parse(path.read_text())
    assert any(isinstance(n,ast.FunctionDef) and n.name=='main' for n in ast.walk(tree))
    assert any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id==engine for n in ast.walk(tree))
def test_retired_absent():
    for name in ['daily_main','collection_main']:
        assert not (Path('src/app/entrypoints')/(name+'.py')).exists()
