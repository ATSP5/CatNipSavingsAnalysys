from dataclasses import dataclass


@dataclass(frozen=True)
class NbpRate:
    """Stopa referencyjna NBP."""

    rate_pct: float
    valid_from: str
    source: str
