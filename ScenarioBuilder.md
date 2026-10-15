Buduje scenariusz makro (Scenario): miesięczne ścieżki inflacji r/r i stopy referencyjnej NBP (przejście liniowe od wartości dzisiejszej do docelowej) oraz poziom cen do przeliczenia na dzisiejsze złote.

**Dlaczego tu jest:** założenia makro są oddzielone od instrumentów. Każdy symulator dostaje ten sam scenariusz, więc porównanie jest spójne. Jest podłączony do SavingsAnalyzer.

## build(params)
Scenario dla ScenarioParams:
- `cpi_start_pct` → `cpi_long_pct` w ciągu `cpi_converge_months` miesięcy (0 oznacza od razu wartość docelową),
- `ref_start_pct` → `ref_end_pct` w ciągu `ref_converge_months`,
- poziom cen = iloczyn miesięcznych przyrostów `(1 + inflacja r/r)^(1/12)`; 1,0 dziś.

Wyższa inflacja podnosi oprocentowanie COI, EDO, ROS i ROD, ale też obniża wartość wszystkiego w dzisiejszych złotych i podnosi cel realny. Wyższa stopa NBP podnosi ROR, DOR i stawki kont.

## scenarios
Wyjście bloku: zwraca ten obiekt podłączonym blokom.
