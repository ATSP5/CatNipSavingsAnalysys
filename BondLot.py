from dataclasses import dataclass


@dataclass
class BondLot:
    """Obligacje jednej serii kupione w jednym miesiącu; value = wartość po ostatniej kapitalizacji."""

    principal: float
    start: int
    value: float
