from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ValueCurve:
    """Wartość oszczędności w każdym miesiącu przy sprzedaży/wykupie wszystkiego w tym miesiącu.

    proceeds — co wpływa na konto po opłatach i podatkach liczonych od pojedynczej pozycji;
    basis    — koszt nabycia (suma wpłat);
    deferred_tax_rate — Belka od łącznego zysku, pobierana dopiero przy sprzedaży (fundusz, ETF).
    Tablice mają kształt (miesiące,) albo (ścieżki Monte Carlo, miesiące). Wszystko jest liniowe względem
    wpłat, więc krzywe dla kapitału startowego i dla wpłaty 1 zł można składać: a·A + c·B.
    """

    proceeds: np.ndarray
    basis: np.ndarray
    deferred_tax_rate: float = 0.0

    def scaled_sum(self, other: "ValueCurve", a: float, b: float) -> "ValueCurve":
        return ValueCurve(a * self.proceeds + b * other.proceeds, a * self.basis + b * other.basis,
                          self.deferred_tax_rate)

    @property
    def net(self) -> np.ndarray:
        if not self.deferred_tax_rate:
            return self.proceeds
        return self.proceeds - self.deferred_tax_rate * np.maximum(self.proceeds - self.basis, 0.0)

    @property
    def is_stochastic(self) -> bool:
        return self.proceeds.ndim == 2
