import json
import tempfile
import unittest
from pathlib import Path
from src.domain.universal_ingester import (
    UniversalIngester, MarketUnitsSnapshotError, snapshot_path, load_units_snapshot,
)


class MarketUnitsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.csv = self.root / "market_units.csv"
        self.csv.write_text("asset_key,units\nFundA,9\n")
        self.day = "2026-04-20"
        self.ingester = UniversalIngester(self.csv, self.root)

    def snapshot(self, **changes):
        payload = {"schema_version": "market_units_snapshot.v1", "snapshot_type": "FULL_SNAPSHOT",
                   "target_date": self.day, "source": {"ssot_a_path": str(self.csv)},
                   "items": [{"asset_key": "FundA", "units": "2.5"}]}
        payload.update(changes)
        path = snapshot_path(self.day, self.root)
        path.write_text(json.dumps(payload))
        return path

    def test_snapshot_adoption_records_actual_source_and_canonical_path(self):
        path = self.snapshot()
        ledger = self.ingester.build_shadow_ledger(self.day)
        self.assertEqual(ledger["ssot_a_path"], str(self.csv))
        self.assertEqual(ledger["units_source"], {"type": "SNAPSHOT", "path": str(path), "snapshot_target_date": self.day})
        self.assertEqual(ledger["assets"][0]["units"], 2.5)

    def test_default_daily_missing_falls_back_to_current_csv(self):
        self.assertEqual(self.ingester.build_shadow_ledger(self.day)["units_source"]["type"], "LIVE_CSV")

    def test_default_daily_invalid_falls_back_to_current_csv(self):
        self.snapshot(target_date="2026-04-19")
        self.assertEqual(self.ingester.build_shadow_ledger(self.day)["assets"][0]["units"], 9)

    def test_strict_missing_blocks(self):
        with self.assertRaises(MarketUnitsSnapshotError):
            self.ingester.build_shadow_ledger(self.day, "strict")

    def test_strict_missing_explicitly_allows_current_csv(self):
        self.assertEqual(self.ingester.build_shadow_ledger(self.day, "strict", True)["units_source"]["type"], "LIVE_CSV")

    def test_invalid_snapshot_even_with_allow_flag_blocks(self):
        self.snapshot(target_date="2026-04-19")
        with self.assertRaises(MarketUnitsSnapshotError):
            self.ingester.build_shadow_ledger(self.day, "strict", True)

    def test_strict_valid_snapshot_does_not_read_current_csv(self):
        self.snapshot()
        self.csv.unlink()
        self.assertEqual(self.ingester.build_shadow_ledger(self.day, "strict")["assets"][0]["units"], 2.5)

    def test_invalid_snapshot_contracts(self):
        cases = [{"target_date": "2026-04-19"}, {"schema_version": "wrong"},
                 {"snapshot_type": "PARTIAL"}, {"source": {"ssot_a_path": "other.csv"}},
                 {"items": []}, {"items": [{"asset_key": "A", "units": "bad"}]},
                 {"items": [{"asset_key": "A", "units": "1"}, {"asset_key": " A ", "units": "2"}]}]
        for changes in cases:
            with self.subTest(changes=changes):
                path = self.snapshot(**changes)
                with self.assertRaises(MarketUnitsSnapshotError):
                    load_units_snapshot(path, self.day, self.csv)
                self.assertEqual(self.ingester.build_shadow_ledger(self.day)["units_source"]["type"], "LIVE_CSV")
                with self.assertRaises(MarketUnitsSnapshotError):
                    self.ingester.build_shadow_ledger(self.day, "strict", True)

    def test_unreadable_json_uses_mode_policy(self):
        snapshot_path(self.day, self.root).write_text("{")
        self.assertEqual(self.ingester.build_shadow_ledger(self.day)["units_source"]["type"], "LIVE_CSV")
        with self.assertRaises(MarketUnitsSnapshotError):
            self.ingester.build_shadow_ledger(self.day, "strict")

    def test_other_date_snapshot_is_not_target_date_input(self):
        self.snapshot()
        with self.assertRaises(MarketUnitsSnapshotError):
            self.ingester.build_shadow_ledger("2026-04-21", "strict")

    def test_unknown_mode_rejected(self):
        with self.assertRaises(ValueError):
            self.ingester.build_shadow_ledger(self.day, "unknown")
