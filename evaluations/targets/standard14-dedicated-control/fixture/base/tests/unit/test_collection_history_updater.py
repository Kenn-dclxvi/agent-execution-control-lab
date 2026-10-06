from src.domain.collection_history_updater import CollectionHistoryUpdater
import pytest
ASSETS = [dict(key=c, asset_class=c) for c in ['JP_STOCK','US_STOCK','COMMODITIES','FX']]
@pytest.mark.parametrize('us,explicit,expected', [
 ('2026-04-17', None, ['2026-04-21','2026-04-18','2026-04-18','2026-04-18']),
 (None, None, ['2026-04-21']*4),
 ('2026-04-17', '2026-04-10', ['2026-04-11']*4)])
def test_market_end_dates(us, explicit, expected):
    calls=[]
    updater=CollectionHistoryUpdater(ASSETS, lambda key, **kw: calls.append((key,kw['end'])))
    updater.update(target_date='2026-04-20', us_market_date=us, end_date=explicit)
    assert [v for k,v in calls] == expected
