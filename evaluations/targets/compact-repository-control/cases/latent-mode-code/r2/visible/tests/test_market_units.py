import unittest
from src.domain.universal_ingester import UniversalIngester, SnapshotUnavailable

class MarketUnitsTests(unittest.TestCase):
    def ingester(self, snapshot):
        return UniversalIngester(snapshot, lambda: 99)

    def test_run_default_daily_snapshot(self):
        self.assertEqual(self.ingester({"units": 12}).run(), {"assets": [{"units": 12}], "units_source": "SNAPSHOT"})

    def test_run_default_daily_missing_falls_back(self):
        self.assertEqual(self.ingester(None).run()["units_source"], "LIVE_CSV")

    def test_run_default_daily_invalid_falls_back(self):
        self.assertEqual(self.ingester({"units": "invalid"}).run()["assets"], [{"units": 99}])

    def test_strict_missing_without_permission_is_error(self):
        with self.assertRaises(SnapshotUnavailable):
            self.ingester(None).build_shadow_ledger("strict")

    def test_strict_missing_with_permission_uses_live(self):
        self.assertEqual(self.ingester(None).build_shadow_ledger("strict", True)["units_source"], "LIVE_CSV")

    def test_strict_invalid_even_with_permission_is_error(self):
        with self.assertRaises(SnapshotUnavailable):
            self.ingester({"units": "invalid"}).build_shadow_ledger("strict", True)

    def test_strict_snapshot_does_not_fetch_live(self):
        def forbidden_live():
            raise AssertionError("live should not be fetched")
        ledger = UniversalIngester({"units": 12}, forbidden_live).build_shadow_ledger("strict")
        self.assertEqual(ledger["units_source"], "SNAPSHOT")

if __name__ == "__main__":
    unittest.main()
