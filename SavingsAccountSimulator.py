import numpy as np

from AccountOffer import AccountOffer
from Scenario import Scenario
from TaxRules import TaxRules
from ValueCurve import ValueCurve


class SavingsAccountSimulator:
    """Konto oszczędnościowe: kapitalizacja miesięczna, Belka od każdej kapitalizacji.

    Stawka promocyjna działa do limitu i przez `promo_months` (None = stale), powyżej limitu i po promocji —
    standardowa. Wszystkie stawki przesuwają się razem ze stopą referencyjną NBP w scenariuszu.
    """

    def __init__(self, tax: TaxRules):
        self.tax = tax

    def account_sim(self) -> "SavingsAccountSimulator":
        return self

    def simulate(self, offer: AccountOffer, scenario: Scenario, cash: np.ndarray,
                 repeat_promo: bool = False) -> ValueCurve:
        months = scenario.months
        balance, invested = 0.0, 0.0
        proceeds, basis = np.zeros(months + 1), np.zeros(months + 1)
        for t in range(months + 1):
            balance += cash[t]
            invested += cash[t]
            proceeds[t], basis[t] = balance, invested
            shift = scenario.ref_at(t) - scenario.params.ref_start_pct
            standard = max(offer.standard_rate_pct + shift, 0.0) / 100
            in_promo = repeat_promo or offer.promo_months is None or t < offer.promo_months
            promo = max(offer.promo_rate_pct + shift, 0.0) / 100 if in_promo else standard
            covered = min(balance, offer.limit_pln)
            interest = (covered * promo + (balance - covered) * standard) / 12
            balance += interest - self.tax.belka_on(interest)
        return ValueCurve(proceeds=proceeds, basis=basis)
