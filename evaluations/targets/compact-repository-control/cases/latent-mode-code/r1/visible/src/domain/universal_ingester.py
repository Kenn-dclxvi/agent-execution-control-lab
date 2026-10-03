"""日次snapshotと現在の取得値を使うmarket units取得。"""
class SnapshotUnavailable(ValueError):
    pass

class UniversalIngester:
    def __init__(self, units_mode="daily"):
        if units_mode not in ("daily", "strict"):
            raise ValueError("unknown units mode")
        self.units_mode = units_mode

    def get_market_units(self, snapshot, live_csv):
        if isinstance(snapshot, dict) and isinstance(snapshot.get("units"), int):
            return snapshot["units"]
        if self.units_mode == "strict":
            raise SnapshotUnavailable("missing or invalid snapshot")
        return int(live_csv())
