import math
from typing import Optional

import numpy as np

from MarketAssetSpec import MarketAssetSpec
from Scenario import Scenario
from TaxRules import TaxRules
from ValueCurve import ValueCurve


class MarketAssetSimulator:
    """Złoto, fundusz, ETF: co miesiąc kupuje za wpłatę po cenie z kosztem zakupu, wycenia przy sprzedaży.

    Bez `rng` cena rośnie równo o oczekiwany zwrot; z `rng` — `paths` ścieżek Monte Carlo (rozkład
    log-normalny z podaną zmiennością, średni zwrot taki sam). Fundusz/ETF: Belka od łącznego zysku przy
    sprzedaży. Złoto: bez podatku po pół roku od końca miesiąca zakupu, wcześniej PIT od zysku z partii.
    """

    def __init__(self, tax: TaxRules):
        self.tax = tax

    def asset_sim(self) -> "MarketAssetSimulator":
        return self

    def simulate(self, spec: MarketAssetSpec, scenario: Scenario, cash: np.ndarray, paths: int = 0,
                 rng: Optional[np.random.Generator] = None) -> ValueCurve:
        months = scenario.months
        cash = np.asarray(cash[:months + 1], dtype=float)
        growth = self._price_paths(spec, months, paths, rng)               # (ścieżki, miesiące), start 1.0
        buy = 1 / (1 + spec.buy_cost_pct / 100)
        sell = 1 - spec.sell_cost_pct / 100
        units = np.cumsum(cash * buy / growth, axis=1)
        proceeds = units * growth * sell
        basis = np.cumsum(cash)
        if spec.tax == "gold":
            proceeds = proceeds - self._gold_short_term_tax(cash, growth, buy * sell)
            curve = ValueCurve(proceeds=proceeds, basis=np.broadcast_to(basis, proceeds.shape).copy())
        else:
            curve = ValueCurve(proceeds=proceeds, basis=np.broadcast_to(basis, proceeds.shape).copy(),
                               deferred_tax_rate=self.tax.belka)
        if rng is None:
            return ValueCurve(curve.proceeds[0], curve.basis[0], curve.deferred_tax_rate)
        return curve

    @staticmethod
    def _price_paths(spec: MarketAssetSpec, months: int, paths: int, rng) -> np.ndarray:
        drift = math.log(1 + spec.expected_return_pct / 100) / 12
        if rng is None or paths <= 0:
            return np.exp(drift * np.arange(months + 1))[None, :]
        sigma = spec.volatility_pct / 100 / math.sqrt(12)
        steps = rng.normal(drift - sigma ** 2 / 2, sigma, size=(paths, months))
        return np.exp(np.concatenate((np.zeros((paths, 1)), np.cumsum(steps, axis=1)), axis=1))

    def _gold_short_term_tax(self, cash: np.ndarray, growth: np.ndarray, round_trip: float) -> np.ndarray:
        """PIT od partii kupionych w ostatnich 6 miesiącach (sprzedaż przed upływem pół roku)."""
        tax = np.zeros_like(growth)
        months = growth.shape[1]
        for lag in range(self.tax.gold_tax_free_after_months + 1):
            bought = np.arange(months - lag)
            sold = bought + lag
            gain = cash[bought] * (round_trip * growth[:, sold] / growth[:, bought] - 1)
            tax[:, sold] += self.tax.gold_pit_on(gain)
        return tax
