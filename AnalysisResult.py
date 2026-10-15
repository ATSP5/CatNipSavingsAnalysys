from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AnalysisResult:
    """Wynik jednej symulacji dla strony raportu: ranking, wykresy i podsumowanie."""

    ranking: List[dict]
    offers: List[dict]
    chart: List[dict]
    chart_series: List[str]
    fan: List[dict]
    cpi: List[dict]
    fastest_label: str
    fastest_months: float
    fastest_date: str
    kpis: Dict[str, str] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
    target_view: Dict[str, object] = field(default_factory=dict)
