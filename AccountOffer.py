from dataclasses import dataclass, replace
from typing import Optional


@dataclass(frozen=True)
class AccountOffer:
    """Oferta konta oszczędnościowego: stawka do limitu, standard powyżej limitu i po promocji."""

    key: str
    bank: str
    product: str
    promo_rate_pct: float
    limit_pln: float
    promo_months: Optional[int]          # None = stawka obowiązuje stale (przy spełnionych warunkach)
    standard_rate_pct: float
    conditions: str
    source: str

    @property
    def label(self) -> str:
        return "%s — %s" % (self.bank, self.product)

    def with_changes(self, **changes) -> "AccountOffer":
        return replace(self, **changes)
