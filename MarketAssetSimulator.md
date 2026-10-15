Symuluje instrumenty o zmiennej cenie: złoto, fundusz i ETF. Co miesiąc kupuje za wpłatę po cenie powiększonej o koszt zakupu, a wartość liczy przy sprzedaży (po koszcie sprzedaży i podatku).
- Bez generatora losowego: cena rośnie równo o oczekiwany zwrot.
- Z generatorem: `paths` ścieżek log-normalnych o podanej zmienności.

**Dlaczego tu jest:** jeden model ceny i trzy reguły podatkowe:
- fundusz i ETF: Belka od łącznego zysku przy sprzedaży (odroczona),
- złoto: PIT tylko od partii kupionych w ostatnich 6 miesiącach.

Wynik jest liniowy względem wpłat, więc SavingsAnalyzer liczy go raz dla 1 zł. Jest podłączony do InstrumentSimulators.

## tax
TaxRules.

## simulate(spec, scenario, cash, paths, rng)
ValueCurve. Kształt `(miesiące,)` bez losowania albo `(ścieżki, miesiące)` z losowaniem.
- `paths`: liczba ścieżek (≥ 0; 0 lub brak `rng` oznacza wariant bez losowania).
- `rng`: generator numpy. To samo ziarno daje te same ścieżki dla kapitału i dla wpłat.

Wpływ parametrów `spec`:
- wyższy `expected_return_pct` skraca czas dojścia,
- wyższy `volatility_pct` poszerza zakres p10–p90,
- koszty zakupu i sprzedaży obniżają wartość na rękę.

## _price_paths(spec, months, paths, rng)
Mnożnik ceny od dziś (1,0). Dryf = ln(1 + zwrot)/12 − σ²/2, więc średnia ścieżek rośnie o oczekiwany zwrot.

## _gold_short_term_tax(cash, growth, round_trip)
PIT od zysku partii złota sprzedanych przed upływem 6 miesięcy.

## asset_sim
Wyjście bloku: zwraca ten obiekt podłączonym blokom.
