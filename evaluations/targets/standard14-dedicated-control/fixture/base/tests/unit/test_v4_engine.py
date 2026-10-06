from src.app.v4_engine import V4PortfolioEngine
from src.domain.collection_history_updater import CollectionHistoryUpdater
class Timeline:
    def get_us_market_context(self, target_date):
        assert target_date=='2026-04-20'
        return {'trading_date':'2026-04-17'}
def test_primary_retry_dates_and_fx():
    calls=[]
    assets=[dict(key=c,asset_class=c) for c in ['JP_STOCK','US_STOCK','COMMODITIES','FX']]
    updater=CollectionHistoryUpdater(assets, lambda key, **kw: calls.append((key,kw['end'])))
    V4PortfolioEngine(updater,Timeline()).run('2026-04-20', ['US_STOCK'])
    assert calls == [('JP_STOCK','2026-04-21'),('US_STOCK','2026-04-18'),('COMMODITIES','2026-04-18'),('FX','2026-04-18'),('US_STOCK','2026-04-18'),('FX','2026-04-18')]
