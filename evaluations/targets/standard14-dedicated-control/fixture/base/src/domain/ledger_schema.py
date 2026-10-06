from dataclasses import dataclass, asdict
@dataclass
class ShadowAssetRecord:
    asset_key: str
    name: str
    asset_class: str
    currency: str
    units: float
@dataclass
class UnitsSource:
    type: str
    path: str
    snapshot_target_date: str | None = None
    def __getitem__(self, key):
        return getattr(self, key)
@dataclass
class ShadowLedger:
    target_date: str
    ssot_a_path: str
    units_source: UnitsSource | dict
    assets: list
    def __post_init__(self):
        if isinstance(self.units_source, dict):
            self.units_source = UnitsSource(**self.units_source)
    def model_dump(self):
        return asdict(self)
