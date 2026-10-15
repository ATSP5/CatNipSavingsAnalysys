from dataclasses import dataclass


@dataclass(frozen=True)
class ScenarioParams:
    """Założenia makro na przyszłość: ścieżka inflacji i stopy referencyjnej NBP."""

    horizon_months: int
    cpi_start_pct: float              # ostatni odczyt GUS
    cpi_long_pct: float               # poziom, do którego inflacja dochodzi
    cpi_converge_months: int
    ref_start_pct: float              # dzisiejsza stopa NBP
    ref_end_pct: float
    ref_converge_months: int
