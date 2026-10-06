from src.lib.timeline_controller import TimelineController
from src.domain.collection_history_updater import CollectionHistoryUpdater
class V4PortfolioEngine:
    def __init__(self, updater=None, timeline=None):
        self.updater = updater or CollectionHistoryUpdater([], lambda key, **kwargs: {"key": key, **kwargs})
        self.timeline = timeline or TimelineController()
    def run(self, target_date, missing_keys=()):
        us_market_date = self.timeline.get_us_market_context(target_date).get('trading_date')
        primary = self.updater.update(target_date=target_date, us_market_date=us_market_date)
        retry_keys = set(missing_keys)
        if any(a['key'] in retry_keys and a['asset_class'] in {'US_STOCK','COMMODITIES'} for a in self.updater.assets):
            retry_keys.update(a['key'] for a in self.updater.assets if a['asset_class']=='FX')
        retry = self.updater.update(target_date=target_date, us_market_date=us_market_date, only_keys=retry_keys) if retry_keys else []
        return primary, retry
