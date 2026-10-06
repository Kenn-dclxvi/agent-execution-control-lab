from datetime import date, timedelta
class CollectionHistoryUpdater:
    def __init__(self, assets, fetch):
        self.assets, self.fetch = assets, fetch
    def _resolve_market_end_date(self, asset_class, target_date, us_market_date, end_date):
        if end_date:
            return end_date
        if asset_class in {'US_STOCK', 'COMMODITIES', 'FX'}:
            return us_market_date or target_date
        return target_date
    def update(self, target_date=None, us_market_date=None, only_keys=None, end_date=None):
        records = []
        for asset in self.assets:
            if only_keys is not None and asset['key'] not in only_keys:
                continue
            market_end = self._resolve_market_end_date(asset['asset_class'], target_date, us_market_date, end_date)
            exclusive_end = (date.fromisoformat(market_end) + timedelta(days=1)).isoformat() if market_end else None
            records.append(self.fetch(asset['key'], end=exclusive_end))
        return records
