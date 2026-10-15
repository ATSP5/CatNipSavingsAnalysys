Rekord danych: założenia makro — ścieżka inflacji i stopy NBP. Niezmienny i hashowalny, dlatego służy też jako klucz pamięci podręcznej krzywych w SavingsAnalyzer.

**Dlaczego tu jest:** jedna paczka parametrów, z której ScenarioBuilder buduje Scenario.

## horizon_months
Horyzont w miesiącach (12–480, z `horizon_years`).

## cpi_start_pct
Inflacja dziś w % (na stronie −1…12; domyślnie ostatni odczyt GUS).

## cpi_long_pct
Inflacja docelowa w % (−1…12). Wyższa podnosi oprocentowanie obligacji indeksowanych, ale obniża wartość w dzisiejszych złotych.

## cpi_converge_months
W ilu miesiącach inflacja dochodzi do docelowej (0–60; 0 oznacza od razu).

## ref_start_pct
Dzisiejsza stopa NBP w %.

## ref_end_pct
Docelowa stopa NBP w % (0–10). Wyższa podnosi ROR, DOR i stawki kont.

## ref_converge_months
W ilu miesiącach stopa dochodzi do docelowej (0–36).
