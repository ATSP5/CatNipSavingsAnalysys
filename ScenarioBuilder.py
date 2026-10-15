import numpy as np

from Scenario import Scenario
from ScenarioParams import ScenarioParams


class ScenarioBuilder:
    """Buduje ścieżki inflacji i stopy NBP: liniowe przejście od wartości dzisiejszej do docelowej."""

    def scenarios(self) -> "ScenarioBuilder":
        return self

    def build(self, params: ScenarioParams) -> Scenario:
        lag = Scenario.LAG
        steps = np.arange(params.horizon_months + lag + 1)
        cpi = self._glide(params.cpi_start_pct, params.cpi_long_pct, params.cpi_converge_months, steps)
        ref = self._glide(params.ref_start_pct, params.ref_end_pct, params.ref_converge_months,
                          np.arange(params.horizon_months + 1))
        monthly = (1 + cpi[lag:lag + params.horizon_months] / 100) ** (1 / 12)
        price_index = np.concatenate(([1.0], np.cumprod(monthly)))
        return Scenario(params=params, cpi_yoy=cpi, ref_rate=ref, price_index=price_index)

    @staticmethod
    def _glide(start: float, end: float, months: int, steps: np.ndarray) -> np.ndarray:
        if months <= 0:
            return np.full(len(steps), float(end))
        return start + (end - start) * np.minimum(steps / months, 1.0)
