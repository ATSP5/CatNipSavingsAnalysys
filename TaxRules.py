import numpy as np


class TaxRules:
    """Podatki od oszczędności: Belka 19% od odsetek i zysków kapitałowych; złoto — PIT tylko przy szybkiej sprzedaży."""

    def __init__(self, belka_pct: float = 19.0, gold_pit_pct: float = 12.0, gold_tax_free_after_months: int = 6):
        self.belka = belka_pct / 100
        self.gold_pit = gold_pit_pct / 100
        self.gold_tax_free_after_months = gold_tax_free_after_months

    def tax(self) -> "TaxRules":
        return self

    def belka_on(self, gain):
        """Podatek Belki od zysku (liczba lub tablica numpy); strata podatku nie daje."""
        return self.belka * np.maximum(gain, 0.0)

    def gold_pit_on(self, gain):
        """Sprzedaż złota przed upływem pół roku od końca miesiąca zakupu: PIT od dochodu (skala 12%)."""
        return self.gold_pit * np.maximum(gain, 0.0)
