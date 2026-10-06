import json
import pytest
from src.domain.universal_ingester import UniversalIngester
from src.domain.market_units_snapshot import create_units_snapshot, MarketUnitsSnapshotError
@pytest.mark.parametrize('state', ['valid','missing','invalid'])
@pytest.mark.parametrize('mode,allow', [('daily',False),('strict',False),('strict',True)])
def test_mode_resolution(tmp_path,state,mode,allow):
    csv=tmp_path/'units.csv'; csv.write_text('name,asset_class,currency,units,source_symbol,audit_match_key,csv_url\nAlpha,US_STOCK,USD,2,ALPHA,,\n')
    snapshot=tmp_path/'collection_units_20260420.json'
    if state!='missing':
        payload=create_units_snapshot(str(csv),'2026-04-20')
        if state=='invalid': payload['items']=[]
        snapshot.write_text(json.dumps(payload))
    ingester=UniversalIngester(funds_csv_path=str(csv),units_snapshot_dir=str(tmp_path))
    fails=mode=='strict' and (state=='invalid' or state=='missing' and not allow)
    if fails:
        with pytest.raises(MarketUnitsSnapshotError): ingester.build_shadow_ledger('2026-04-20',mode,allow)
    else:
        ledger=ingester.build_shadow_ledger('2026-04-20',mode,allow)
        assert ledger.units_source['type']==('SNAPSHOT' if state=='valid' else 'LIVE_CSV')
        assert ledger.ssot_a_path==str(csv)
        assert ledger.assets[0].units==2
        assert ledger.assets[0].asset_key=='US_STOCK:USD:ALPHA'
def test_invalid_mode(tmp_path):
    with pytest.raises(ValueError): UniversalIngester().build_shadow_ledger('2026-04-20','other')
def test_run_default_propagation(tmp_path,monkeypatch):
    ingester=UniversalIngester(); calls=[]
    class Ledger:
        def model_dump(self): return {'target_date':'2026-04-20'}
    monkeypatch.setattr(ingester,'build_shadow_ledger', lambda *a,**kw: (calls.append((a,kw)) or Ledger()))
    ingester.run('2026-04-20',str(tmp_path/'out.json'))
    assert calls==[(('2026-04-20',),{})]
    assert json.loads((tmp_path/'out.json').read_text())=={'target_date':'2026-04-20'}
