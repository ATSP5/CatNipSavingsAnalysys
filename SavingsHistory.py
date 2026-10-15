from dataclasses import dataclass
from typing import Tuple

from SavingsDeposit import SavingsDeposit


@dataclass(frozen=True)
class SavingsHistory:
    """Historia wpłat z pliku wejściowego; suma to kapitał startowy symulacji."""

    deposits: Tuple[SavingsDeposit, ...]
    source: str

    @property
    def total(self) -> float:
        return sum(d.amount for d in self.deposits)

    @property
    def monthly_average(self) -> float:
        """Średnia wpłata na miesiąc kalendarzowy od pierwszej do ostatniej wpłaty."""
        if not self.deposits:
            return 0.0
        first, last = self.deposits[0].day, self.deposits[-1].day
        months = (last.year - first.year) * 12 + last.month - first.month + 1
        return self.total / months

    def rows(self) -> list:
        running, rows = 0.0, []
        for d in self.deposits:
            running += d.amount
            rows.append({"Data": d.day.isoformat(), "Wpłata [zł]": round(d.amount, 2),
                         "Narastająco [zł]": round(running, 2)})
        return rows
