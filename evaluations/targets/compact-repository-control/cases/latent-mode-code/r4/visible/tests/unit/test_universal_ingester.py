import json
import tempfile
import unittest
from pathlib import Path
from src.domain.universal_ingester import UniversalIngester


class LedgerConsumerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.csv = self.root / "market_units.csv"
        self.csv.write_text("asset_key,units\nFundA,9\n")
        self.day = "2026-04-20"
        self.ingester = UniversalIngester(self.csv, self.root, [{"asset_key": "Cash", "amount": 25}])

    def test_default_ledger_merges_market_and_absolute_assets(self):
        ledger = self.ingester.build_shadow_ledger(self.day)
        self.assertEqual(ledger["total_value_jpy"], 925)
        self.assertEqual([a["source"] for a in ledger["assets"]], ["MARKET_UNITS", "ABSOLUTE_AMOUNT"])

    def test_run_inherits_default_and_records_target_date(self):
        ledger = self.ingester.run(self.day)
        self.assertEqual(ledger["units_source"]["type"], "LIVE_CSV")
        self.assertEqual(ledger["target_date"], self.day)

    def test_run_without_output_does_not_create_artifact(self):
        self.ingester.run(self.day)
        self.assertEqual([p.name for p in self.root.iterdir()], ["market_units.csv"])

    def test_run_serializes_ledger_when_output_is_requested(self):
        output = self.root / "out" / "ledger.json"
        ledger = self.ingester.run(self.day, output)
        self.assertEqual(json.loads(output.read_text()), ledger)
