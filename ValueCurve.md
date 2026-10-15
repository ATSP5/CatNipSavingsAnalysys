Rekord danych: wartość oszczędności w każdym miesiącu przy zamknięciu wszystkiego w tym miesiącu. Tablice mają kształt `(miesiące,)` albo `(ścieżki Monte Carlo, miesiące)`.

**Dlaczego tu jest:** wspólny wynik wszystkich symulatorów. Wynik jest liniowy względem wpłat, więc krzywe dla 1 zł kapitału i 1 zł wpłaty można składać (`scaled_sum`). Podatek odroczony liczy się dopiero po złożeniu, bo Belka dla funduszu i ETF dotyczy łącznego zysku.

## proceeds
Kwota po opłatach i podatkach liczonych od pojedynczej pozycji (zł).

## basis
Koszt nabycia — suma wpłat (zł).

## deferred_tax_rate
Belka od łącznego zysku pobierana przy sprzedaży (0 dla kont, obligacji i złota; 0,19 dla funduszu i ETF).

## scaled_sum(other, a, b)
`a·self + b·other`. Tak analizator składa kapitał startowy (`a`) i wpłatę miesięczną (`b`).

## net
Wartość na rękę: `proceeds` minus odroczona Belka od dodatniego zysku. Porównywana z celem.

## is_stochastic
`True` dla krzywych Monte Carlo (tablica 2D).
