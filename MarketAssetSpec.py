from dataclasses import dataclass, replace


@dataclass(frozen=True)
class MarketAssetSpec:
    """Instrument o zmiennej cenie (złoto, fundusz, ETF): oczekiwany zwrot, zmienność i koszty transakcji.

    tax: "belka" — 19% od łącznego zysku przy sprzedaży (fundusz, ETF);
         "gold"  — złoto inwestycyjne: bez podatku po pół roku od końca miesiąca zakupu, wcześniej PIT.
    """

    key: str
    name: str
    expected_return_pct: float
    volatility_pct: float
    buy_cost_pct: float                  # marża mennicy / przewalutowanie przy zakupie
    sell_cost_pct: float                 # dyskonto skupu / przewalutowanie przy sprzedaży
    tax: str
    start_price: float
    note: str

    def with_changes(self, **changes) -> "MarketAssetSpec":
        return replace(self, **changes)
