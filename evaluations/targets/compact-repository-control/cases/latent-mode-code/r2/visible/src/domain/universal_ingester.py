"""日次snapshotを台帳へ取り込む取得処理。"""
class SnapshotUnavailable(ValueError):
    pass

class UniversalIngester:
    def __init__(self, snapshot, live_csv):
        self.snapshot = snapshot
        self.live_csv = live_csv

    def run(self):
        return self.build_shadow_ledger()

    def build_shadow_ledger(self, units_mode="daily", allow_live_csv_in_strict=False):
        resolution = self._resolve_market_units(units_mode, allow_live_csv_in_strict)
        return {"assets": resolution["items"], "units_source": resolution["source"]}

    def _resolve_market_units(self, units_mode, allow_live_csv_in_strict):
        if units_mode not in ("daily", "strict"):
            raise ValueError("unknown units mode")
        if self.snapshot is not None:
            if isinstance(self.snapshot, dict) and isinstance(self.snapshot.get("units"), int):
                return {"items": [{"units": self.snapshot["units"]}], "source": "SNAPSHOT"}
            if units_mode == "strict":
                raise SnapshotUnavailable("invalid snapshot")
            return self._load_live_market_units()
        if units_mode == "strict" and not allow_live_csv_in_strict:
            raise SnapshotUnavailable("missing snapshot")
        return self._load_live_market_units()

    def _load_live_market_units(self):
        return {"items": [{"units": int(self.live_csv())}], "source": "LIVE_CSV"}
