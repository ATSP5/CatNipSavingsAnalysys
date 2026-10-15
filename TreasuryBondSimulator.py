from typing import List

import numpy as np

from BondLot import BondLot
from BondSpec import BondSpec
from Scenario import Scenario
from TaxRules import TaxRules
from ValueCurve import ValueCurve


class TreasuryBondSimulator:
    """Co miesiąc kupuje nową serię obligacji za wpłatę, wypłacone odsetki (po Belce) i wykupione serie.

    Wartość w miesiącu t to kwota po przedterminowym wykupie wszystkiego: kapitał + naliczone odsetki
    − opłata za wcześniejszy wykup (nie wyższa niż odsetki) − 19% podatku od odsetek pomniejszonych o opłatę.
    Inflacja dla okresu odsetkowego to odczyt GUS ogłoszony w miesiącu przed jego początkiem.
    """

    def __init__(self, tax: TaxRules):
        self.tax = tax

    def bond_sim(self) -> "TreasuryBondSimulator":
        return self

    def simulate(self, spec: BondSpec, scenario: Scenario, cash: np.ndarray) -> ValueCurve:
        months = scenario.months
        lots: List[BondLot] = []
        proceeds = np.zeros(months + 1)
        for t in range(months + 1):
            available = float(cash[t])
            still_active = []
            for lot in lots:
                received, matured = self._events(spec, scenario, lot, t - lot.start)
                available += received
                if not matured:
                    still_active.append(lot)
            lots = still_active
            if available > 0:
                lots.append(BondLot(principal=available, start=t, value=available))
            proceeds[t] = sum(self._redemption_value(spec, scenario, lot, t - lot.start) for lot in lots)
        return ValueCurve(proceeds=proceeds, basis=np.cumsum(cash[:months + 1]))

    # --- odsetki ------------------------------------------------------------------------------------
    def _year_rate(self, spec: BondSpec, scenario: Scenario, lot: BondLot, year: int) -> float:
        if year == 0 or spec.kind == "fixed_capitalized":
            return spec.first_rate_pct / 100
        inflation = scenario.cpi_at(lot.start + 12 * year - 2)
        return (max(inflation, 0.0) + spec.margin_pct) / 100

    def _month_rate(self, spec: BondSpec, scenario: Scenario, lot: BondLot, month: int) -> float:
        if month == 1:
            return spec.first_rate_pct / 100
        return (scenario.ref_at(lot.start + month - 1) + spec.margin_pct) / 100

    def _events(self, spec: BondSpec, scenario: Scenario, lot: BondLot, held: int):
        """Wypłaty na początku miesiąca: (gotówka po podatku, czy seria wykupiona)."""
        if held <= 0:
            return 0.0, False
        matured = held >= spec.term_months
        if spec.kind == "monthly_ref":
            coupon = lot.principal * self._month_rate(spec, scenario, lot, held) / 12
            return coupon - self.tax.belka_on(coupon) + (lot.principal if matured else 0.0), matured
        if spec.kind == "cpi_yearly_coupon":
            if held % 12 and not matured:
                return 0.0, False
            year = (held - 1) // 12
            coupon = lot.principal * self._year_rate(spec, scenario, lot, year) * (held - 12 * year) / 12
            return coupon - self.tax.belka_on(coupon) + (lot.principal if matured else 0.0), matured
        if held % 12 == 0 or matured:                                   # kapitalizacja roczna / wykup
            year = (held - 1) // 12
            lot.value *= 1 + self._year_rate(spec, scenario, lot, year) * (held - 12 * year) / 12
        if matured:
            return lot.value - self.tax.belka_on(lot.value - lot.principal), True
        return 0.0, False

    def _redemption_value(self, spec: BondSpec, scenario: Scenario, lot: BondLot, held: int) -> float:
        if spec.kind == "monthly_ref" or held <= 0:
            return lot.principal if spec.kind == "monthly_ref" else lot.value
        year, within = divmod(held, 12)
        rate = self._year_rate(spec, scenario, lot, year)
        if spec.kind == "cpi_yearly_coupon":
            gross = lot.principal * (1 + rate * within / 12)
        else:
            gross = lot.value * (1 + rate * within / 12)
        interest = gross - lot.principal
        fee = min(spec.early_fee_pln / 100 * lot.principal, interest)
        return gross - fee - self.tax.belka_on(interest - fee)
