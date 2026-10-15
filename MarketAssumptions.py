from dataclasses import dataclass
from typing import Tuple

from AccountOffer import AccountOffer
from BondSpec import BondSpec
from CpiHistory import CpiHistory
from GoldHistory import GoldHistory
from MarketAssetSpec import MarketAssetSpec
from NbpRate import NbpRate


@dataclass(frozen=True)
class MarketAssumptions:
    """Parametry rynku na dzień analizy: oferty, stopa NBP, inflacja GUS, złoto, fundusze i źródła."""

    as_of: str
    reference_rate: NbpRate
    inflation: CpiHistory
    gold_history: GoldHistory
    accounts: Tuple[AccountOffer, ...]
    bonds: Tuple[BondSpec, ...]
    assets: Tuple[MarketAssetSpec, ...]
    belka_pct: float
    sources: Tuple[Tuple[str, str], ...]          # (opis, adres)

    def account(self, key: str) -> AccountOffer:
        return next(a for a in self.accounts if a.key == key)

    def asset(self, key: str) -> MarketAssetSpec:
        return next(a for a in self.assets if a.key == key)
