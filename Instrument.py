from dataclasses import dataclass
from typing import Union

from AccountOffer import AccountOffer
from BondSpec import BondSpec
from MarketAssetSpec import MarketAssetSpec


@dataclass(frozen=True)
class Instrument:
    """Jedna możliwość odkładania pieniędzy w porównaniu."""

    key: str
    label: str
    group: str                          # Konto, Obligacje, Złoto, Fundusz, ETF
    risk: str
    spec: Union[AccountOffer, BondSpec, MarketAssetSpec]

    @property
    def is_account(self) -> bool:
        return isinstance(self.spec, AccountOffer)

    @property
    def is_market(self) -> bool:
        return isinstance(self.spec, MarketAssetSpec)
