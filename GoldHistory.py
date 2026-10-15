import math
from dataclasses import dataclass
from typing import Dict, Tuple

TROY_OUNCE_G = 31.1034768


@dataclass(frozen=True)
class GoldHistory:
    """Cena złota NBP w zł za gram (próba 1000), notowania dzienne."""

    days: Tuple[str, ...]
    prices_per_gram: Tuple[float, ...]
    source: str

    @property
    def latest_per_gram(self) -> float:
        return self.prices_per_gram[-1]

    @property
    def latest_per_ounce(self) -> float:
        return self.latest_per_gram * TROY_OUNCE_G

    @property
    def years(self) -> float:
        first, last = self.days[0], self.days[-1]
        return (int(last[:4]) - int(first[:4])) + (int(last[5:7]) - int(first[5:7])) / 12

    @property
    def cagr(self) -> float:
        """Średnioroczny wzrost ceny w zł w całej dostępnej historii."""
        return (self.prices_per_gram[-1] / self.prices_per_gram[0]) ** (1 / self.years) - 1

    @property
    def volatility(self) -> float:
        """Roczna zmienność z miesięcznych stóp zwrotu (ostatnie notowanie każdego miesiąca)."""
        closes = list(self.month_end().values())
        returns = [math.log(b / a) for a, b in zip(closes, closes[1:])]
        mean = sum(returns) / len(returns)
        variance = sum((r - mean) ** 2 for r in returns) / (len(returns) - 1)
        return math.sqrt(variance * 12)

    def month_end(self) -> Dict[str, float]:
        closes = {}
        for day, price in zip(self.days, self.prices_per_gram):
            closes[day[:7]] = price
        return closes
