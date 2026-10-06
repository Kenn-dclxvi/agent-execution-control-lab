"""設計側だけで使う独立入力。workspaceへ配送しない。"""
import csv, json, inspect
from pathlib import Path
from unittest.mock import patch
import pytest
from src.domain.market_units_snapshot import load_market_units_csv, MarketUnitsSnapshotError, load_units_snapshot, create_units_snapshot
from src.app.monthly_engine import MonthlyEngine
from src.domain.universal_ingester import UniversalIngester

@pytest.mark.parametrize('rows',[
 [{'name':'A','audit_match_key':' K '},{'name':'B','audit_match_key':'K'}],
 [{'name':'A','asset_class':' us_stock ','currency':'usd','source_symbol':'X'},{'name':'B','asset_class':'US_STOCK','currency':'USD','source_symbol':'X'}],
 [{'name':'Same'},{'name':' Same '}],
])
def test_csv_generated_duplicate(tmp_path,rows):
    path=tmp_path/'a.csv'
    with path.open('w') as f:
        writer=csv.DictWriter(f,fieldnames=['name','asset_class','currency','units','source_symbol','audit_match_key','csv_url']); writer.writeheader()
        for r in rows: writer.writerow(dict(units='2',**r))
    with pytest.raises(MarketUnitsSnapshotError,match='duplicate asset_key'): load_market_units_csv(str(path))
def test_csv_distinct_normalization(tmp_path):
    path=tmp_path/'a.csv'; path.write_text('name,asset_class,currency,units,source_symbol,audit_match_key,csv_url,enabled\n A , us_stock , usd ,2,X,,,false\nB,US_STOCK,USD,3,Y,,,true\n')
    items=load_market_units_csv(str(path)); assert [i['asset_key'] for i in items]==['US_STOCK:USD:X','US_STOCK:USD:Y']; assert items[0]['enabled']=='false'
def test_current_default():
    assert inspect.signature(UniversalIngester.build_shadow_ledger).parameters['units_mode'].default=='daily'
def test_monthly_effects(tmp_path):
    sent=[]; engine=MonthlyEngine(str(tmp_path),sent.append,completed=True)
    assert 'format_test' in engine.run(format_test=True,force_send=True)
    assert not sent
    assert engine.run(force_send=False)=={'skipped':True}
    engine.run(force_send=True); assert len(sent)==1
