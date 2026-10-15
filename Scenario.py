from dataclasses import dataclass

import numpy as np

from ScenarioParams import ScenarioParams


@dataclass(frozen=True)
class Scenario:
    """Miesięczne ścieżki makro: miesiąc 0 = dziś, miesiąc t = t miesięcy od dziś.

    cpi_yoy[t + LAG] to inflacja r/r za miesiąc kalendarzowy t (LAG miesięcy wstecz jest już znane z GUS).
    """

    LAG = 2                            # dziś znamy inflację sprzed 2 miesięcy

    params: ScenarioParams
    cpi_yoy: np.ndarray                # w %, długość horizon + LAG + 1
    ref_rate: np.ndarray               # w %, długość horizon + 1
    price_index: np.ndarray            # poziom cen, 1.0 dziś, długość horizon + 1

    @property
    def months(self) -> int:
        return self.params.horizon_months

    def cpi_at(self, month: int) -> float:
        """Inflacja r/r za miesiąc kalendarzowy `month` (ujemny = przeszłość)."""
        index = min(max(month + self.LAG, 0), len(self.cpi_yoy) - 1)
        return float(self.cpi_yoy[index])

    def ref_at(self, month: int) -> float:
        return float(self.ref_rate[min(max(month, 0), len(self.ref_rate) - 1)])
