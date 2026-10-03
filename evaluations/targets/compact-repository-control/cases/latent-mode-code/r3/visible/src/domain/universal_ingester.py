"""日次／再計算の入力契約: docs/how-to/market-units-migration-spec.md。"""
import csv
import json
from datetime import date
from pathlib import Path
from typing import Literal


class MarketUnitsSnapshotError(ValueError):
    pass


def snapshot_path(target_date, snapshot_dir):
    date.fromisoformat(target_date)
    return Path(snapshot_dir) / ("collection_units_" + target_date.replace("-", "") + ".json")


def validate_items(items):
    if not isinstance(items, list) or not items:
        raise MarketUnitsSnapshotError("snapshot items must not be empty")
    seen = set()
    result = []
    for row in items:
        if not isinstance(row, dict):
            raise MarketUnitsSnapshotError("invalid item")
        key = str(row.get("asset_key") or "").strip()
        try:
            units = float(row["units"])
        except (KeyError, ValueError, TypeError) as exc:
            raise MarketUnitsSnapshotError("units must be numeric") from exc
        if not key or key in seen:
            raise MarketUnitsSnapshotError("missing or duplicate asset_key")
        seen.add(key)
        result.append({"asset_key": key, "units": units})
    return result


def load_units_snapshot(path, target_date, ssot_a_path):
    try:
        payload = json.loads(Path(path).read_text())
        if (not isinstance(payload, dict)
                or payload.get("schema_version") != "market_units_snapshot.v1"
                or payload.get("snapshot_type") != "FULL_SNAPSHOT"
                or payload.get("target_date") != target_date
                or payload.get("source", {}).get("ssot_a_path") != str(ssot_a_path)):
            raise MarketUnitsSnapshotError("snapshot input contract mismatch")
        return validate_items(payload.get("items"))
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        raise MarketUnitsSnapshotError("invalid snapshot: " + str(exc)) from exc


class UniversalIngester:
    def __init__(self, funds_csv_path="data/collection/market_units.csv",
                 units_snapshot_dir="data/current", external_assets=None):
        self.ssot_a_path = str(funds_csv_path)
        self.units_snapshot_dir = units_snapshot_dir
        self.external_assets = list(external_assets or [])

    def build_shadow_ledger(self, target_date,
                            units_mode: Literal["daily", "strict"] = "daily",
                            allow_live_csv_in_strict=False):
        resolution = self._resolve_market_units(target_date, units_mode, allow_live_csv_in_strict)
        assets = [{"asset_key": row["asset_key"], "units": row["units"],
                   "source": "MARKET_UNITS", "current_value_jpy": row["units"] * 100}
                  for row in resolution["items"]]
        assets += [{"asset_key": row["asset_key"], "source": "ABSOLUTE_AMOUNT",
                    "current_value_jpy": float(row["amount"])} for row in self.external_assets]
        return {"target_date": target_date, "ssot_a_path": self.ssot_a_path,
                "units_source": resolution["source"], "assets": assets,
                "total_value_jpy": sum(row["current_value_jpy"] for row in assets)}

    def run(self, target_date, output_path=None):
        ledger = self.build_shadow_ledger(target_date)
        if output_path is not None:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
        return ledger

    def _resolve_market_units(self, target_date, units_mode, allow_live_csv_in_strict):
        if units_mode not in ("daily", "strict"):
            raise ValueError("unknown units mode")
        snapshot = snapshot_path(target_date, self.units_snapshot_dir)
        if snapshot.exists():
            try:
                return {"items": load_units_snapshot(snapshot, target_date, self.ssot_a_path),
                        "source": {"type": "SNAPSHOT", "path": str(snapshot),
                                   "snapshot_target_date": target_date}}
            except MarketUnitsSnapshotError:
                if units_mode == "strict":
                    raise
                return self._load_live_market_units()
        if units_mode == "strict" and not allow_live_csv_in_strict:
            raise MarketUnitsSnapshotError("missing snapshot: " + str(snapshot))
        return self._load_live_market_units()

    def _load_live_market_units(self):
        with open(self.ssot_a_path, newline="") as handle:
            items = validate_items(list(csv.DictReader(handle)))
        return {"items": items, "source": {"type": "LIVE_CSV", "path": self.ssot_a_path}}
