"""独立criterionごとの振る舞い。model-visibleなfixtureへは配送しない。"""
from unittest.mock import patch

def test_engine_arguments():
    from src.app.v4_engine import V4PortfolioEngine
    class U:
        assets=[{'key':'US','asset_class':'US_STOCK'},{'key':'FX','asset_class':'FX'}]
        def __init__(self): self.calls=[]
        def update(self,**kw): self.calls.append(kw); return []
    class T:
        def get_us_market_context(self,d): return {'trading_date':'2026-04-17'}
    u=U(); V4PortfolioEngine(u,T()).run('2026-04-20',['US'])
    assert len(u.calls)==2
    assert all(c['target_date']=='2026-04-20' and c['us_market_date']=='2026-04-17' for c in u.calls)
    assert u.calls[1]['only_keys']=={'US','FX'}

def failed_save(tmp_path):
    from src.infra import context_repository as m
    target=tmp_path/'context_20260420.json'; target.write_text('old')
    with patch.object(m,'DIR_CURRENT',str(tmp_path)),patch.object(m.os,'replace',side_effect=OSError('failure')):
        result=m.ContextRepository().save({'a':1},'2026-04-20')
    return result,target

def test_atomic_cleanup(tmp_path):
    _,target=failed_save(tmp_path)
    assert target.read_text()=='old'
    assert not list(tmp_path.glob('*.json.tmp'))

def test_atomic_failure_result(tmp_path):
    result,_=failed_save(tmp_path)
    assert result is False
