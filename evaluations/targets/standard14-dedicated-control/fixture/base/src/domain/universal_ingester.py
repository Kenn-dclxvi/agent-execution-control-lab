import json
import os
from datetime import datetime
from typing import Optional, Literal, List, Dict, Any
from src.config.settings import DATA_DIR, DIR_COLLECTION_HISTORY
from src.domain.ledger_schema import ShadowAssetRecord, ShadowLedger
from src.domain.market_units_snapshot import (MARKET_UNITS_CSV, MarketUnitsSnapshotError, UnitsResolution, load_market_units_csv, load_units_snapshot, snapshot_path)
from src.lib.logger import setup_logger
from src.lib.timeline_controller import TimelineController
logger = setup_logger(__name__)
class UniversalIngester:
    def __init__(self, funds_csv_path=None, external_assets_path=None, portfolio_basis_path=None, history_dir=None, units_snapshot_dir=None, timeline=None, is_closed_fn=None):
        self.funds_csv_path = funds_csv_path or MARKET_UNITS_CSV
        self.ssot_a_path = self.funds_csv_path
        self.units_snapshot_dir = units_snapshot_dir
        self.timeline = timeline or TimelineController()
    def build_shadow_ledger(
        self,
        target_date: Optional[str] = None,
        units_mode: Literal["daily", "strict"] = "daily",
        allow_live_csv_in_strict: bool = False,
    ) -> ShadowLedger:
        active_date = target_date or datetime.now().strftime("%Y-%m-%d")
        resolution = self._resolve_market_units(active_date, units_mode, allow_live_csv_in_strict)
        assets = [ShadowAssetRecord(asset_key=r['asset_key'], name=r['name'], asset_class=r['asset_class'], currency=r['currency'], units=float(r['units'])) for r in resolution['items']]
        return ShadowLedger(active_date, self.ssot_a_path, resolution['source'], assets)
    def run(self, target_date=None, output_path=None):
        ledger = self.build_shadow_ledger(target_date)
        if output_path:
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(ledger.model_dump(), f, ensure_ascii=False, indent=2)
        return ledger

    def _resolve_market_units(
        self,
        target_date: str,
        units_mode: Literal["daily", "strict"],
        allow_live_csv_in_strict: bool,
    ) -> UnitsResolution:
        if units_mode not in {"daily", "strict"}:
            raise ValueError(f"units_mode must be 'daily' or 'strict', got: {units_mode}")

        snapshot = snapshot_path(target_date, self.units_snapshot_dir)
        if os.path.exists(snapshot):
            try:
                return {
                    "items": load_units_snapshot(snapshot, target_date, self.ssot_a_path),
                    "source": {
                        "type": "SNAPSHOT",
                        "path": snapshot,
                        "snapshot_target_date": target_date,
                    },
                }
            except MarketUnitsSnapshotError as exc:
                if units_mode == "strict":
                    raise
                logger.warning(f"[Guard] Invalid market units snapshot; falling back to live CSV: {snapshot} ({exc})")
                return self._load_live_market_units()

        if units_mode == "strict" and not allow_live_csv_in_strict:
            raise MarketUnitsSnapshotError(f"market units snapshot missing: {snapshot}")

        logger.warning(f"[Guard] Market units snapshot missing; falling back to live CSV: {snapshot}")
        return self._load_live_market_units()

    def _load_live_market_units(self) -> UnitsResolution:
        return {
            "items": self._load_fund_config(),
            "source": {
                "type": "LIVE_CSV",
                "path": self.ssot_a_path,
            },
        }

    def _load_fund_config(self) -> List[Dict[str, Any]]:
        try:
            funds = load_market_units_csv(self.ssot_a_path)
            for row in funds:
                row["units"] = float(row["units"])
            return funds
        except FileNotFoundError:
            logger.warning(f"[Guard] v4 market units config missing: {self.ssot_a_path}")
        except Exception as exc:
            logger.error(f"[Guard] Failed to read v4 market units config: {exc}")
        return []
