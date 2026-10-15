from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class SavingsDeposit:
    """Jedna wpłata z historii oszczędności (arkusz: Data, Kwota)."""

    day: date
    amount: float
