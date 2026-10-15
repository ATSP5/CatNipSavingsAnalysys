from dataclasses import dataclass
from typing import Tuple

from CpiReading import CpiReading


@dataclass(frozen=True)
class CpiHistory:
    """Miesięczna inflacja CPI z GUS, od najstarszego miesiąca."""

    readings: Tuple[CpiReading, ...]
    source: str

    @property
    def latest(self) -> CpiReading:
        return self.readings[-1]

    def average_yoy(self, years: int) -> float:
        """Średnioroczna inflacja z ostatnich `years` lat, liczona z indeksów miesiąc do miesiąca."""
        recent = self.readings[-12 * years:]
        index = 1.0
        for reading in recent:
            index *= 1 + reading.mom_pct / 100
        return (index ** (12 / len(recent)) - 1) * 100 if recent else 0.0
