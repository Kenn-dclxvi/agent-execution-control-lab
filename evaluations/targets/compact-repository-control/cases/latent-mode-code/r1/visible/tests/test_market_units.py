import unittest
from src.domain.universal_ingester import UniversalIngester, SnapshotUnavailable

class MarketUnitsTests(unittest.TestCase):
    def test_default_daily_uses_snapshot(self):
        self.assertEqual(UniversalIngester().get_market_units({"units": 12}, lambda: 99), 12)

    def test_default_daily_falls_back_when_snapshot_missing(self):
        self.assertEqual(UniversalIngester().get_market_units(None, lambda: 99), 99)

    def test_default_daily_falls_back_when_snapshot_invalid(self):
        self.assertEqual(UniversalIngester().get_market_units({"units": "invalid"}, lambda: 99), 99)

    def test_strict_missing_snapshot_is_error(self):
        with self.assertRaises(SnapshotUnavailable):
            UniversalIngester("strict").get_market_units(None, lambda: 99)

    def test_strict_uses_snapshot_without_live_fetch(self):
        def forbidden_live():
            raise AssertionError("live should not be fetched")
        self.assertEqual(UniversalIngester("strict").get_market_units({"units": 12}, forbidden_live), 12)

if __name__ == "__main__":
    unittest.main()
