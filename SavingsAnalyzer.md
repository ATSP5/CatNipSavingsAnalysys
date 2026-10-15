Liczy, w którym miesiącu każdy instrument da cel (domyślnie 400 tys. zł) na rękę — po podatku Belki, opłatach i kosztach sprzedaży — przy wpłatach 3 500 i 4 000 zł oraz przy wpłacie wybranej na stronie. Cel można traktować jako wartość przyszłą (nominalne zł w dniu uzbierania) albo dzisiejszą (siła nabywcza, nominalnie rosnąca z inflacją) i przelicza go na obie miary w dniu uzbierania najszybszą i najwolniejszą drogą. Dla złota, funduszu i ETF dodaje medianę, zakres p10–p90 i szansę osiągnięcia celu w horyzoncie z Monte Carlo. Wypisuje ranking w konsoli.

**Dlaczego tu jest:** jedyny punkt, w którym parametry ze strony zamieniają się w wynik. Strona SavingsSimulatorPage (wejście `analyzer`) jest tylko widokiem. Obligacje i instrumenty rynkowe są liniowe względem wpłat, dlatego krzywe dla 1 zł kapitału i 1 zł wpłaty są liczone raz na scenariusz i trzymane w pamięci podręcznej. Zmiana suwaka wpłaty lub celu tylko je skaluje/porównuje (ok. 0,04 s), a pełne przeliczenie scenariusza trwa ok. 0,3 s.

## settings
AnalysisSettings: cel, zakres wpłat, horyzont, liczba ścieżek, ziarno.

## history
SavingsHistory: kapitał startowy.

## market
MarketAssumptions: dane na dziś.

## scenarios
ScenarioBuilder.

## simulators
InstrumentSimulators.

## TARGET_MODES
Dozwolone wartości `target_mode`: `"future"` (wartość przyszła) i `"today"` (wartość dzisiejsza).

## defaults()
Parametry na dziś, od których startuje strona:
- `contribution` = średnia z zakresu wpłat, `start_capital` = suma historii, `target` = `AnalysisSettings.target_pln`,
- `target_mode` = `"future"`, `index_contributions` = False,
- `cpi_start` = `cpi_long` = ostatni odczyt GUS (inflacja dzisiejsza utrzymana), `cpi_months` = 24,
- `ref_end` = dzisiejsza stopa NBP, `ref_months` = 12,
- parametry Erste z oferty, `repeat_promo` = False, `include_family` = False,
- złoto: wzrost i zmienność z historii NBP, marża 3%, dyskonto 2%,
- fundusz: 4,3% / 1%, ETF: 7% / 16%,
- `fan_key` = `etf`, `chart_real` = False.

## instruments(p)
Lista instrumentów z nałożonymi parametrami strony:
- Erste i pozostałe konta,
- obligacje (ROS i ROD tylko przy `include_family`),
- złoto, fundusz, ETF.

## evaluate(p)
AnalysisResult. Ranking jest sortowany po czasie dojścia przy wybranej wpłacie; przy równym czasie wygrywa wyższa wartość końcowa. „Najlepszy bank” to najszybsza oferta konta poza Erste. Krzywa celu w miesiącu t: `target` (tryb `future`) albo `target · indeks cen[t]` (tryb `today`). Każdy wiersz rankingu ma kolumny „Cel w tym dniu [zł]” (nominalnie w dniu osiągnięcia) i „Cel w dzisiejszych zł [zł]”; „—”, gdy cel nie pada w horyzoncie.

Wpływ parametrów:
- **wpłata:** wyższa skraca czas dojścia wszystkich instrumentów,
- **target:** wyższy cel wydłuża czas dojścia,
- **target_mode = today:** cel rośnie z inflacją, czas wydłuża się o 1,5–4 lata, a nominalna kwota w dniu uzbierania jest wyższa od `target`; przy `future` kwota w dzisiejszych zł jest niższa od `target`,
- **wpłaty indeksowane:** wpłaty rosną z inflacją, czas się skraca,
- **horyzont:** dłuższy daje dłuższe wykresy i może dopuścić wolniejsze instrumenty do „najwolniej”,
- **makro:** inflacja i stopa NBP według ScenarioBuilder; inflacja wyznacza też przeliczenie dzisiejsze ↔ przyszłe zł.

## today_mode(p)
True dla `target_mode = "today"`, False dla `"future"` (także gdy klucza brak). Inna wartość → `ValueError`.

## _target_view(ranking, scenario, target, p)
Słownik dla `AnalysisResult.target_view`: `today_mode`, `target` (sformatowany), `missing` (ile instrumentów rankingu nie osiąga celu w horyzoncie), `fastest` i `slowest`. Najszybszy = pierwszy z rankingu; najwolniejszy = ten z najdłuższym czasem spośród osiągających cel w horyzoncie.

## _target_point(row, scenario, target)
Dla jednego instrumentu: `instrument`, `date` (RRRR-MM), `duration`, `nominal` (cel w zł w dniu uzbierania), `today` (cel w dzisiejszych zł = nominal / indeks cen), `prices` (wzrost cen od dziś do tego dnia). Bez instrumentu — kreski i „nie w horyzoncie”.

## _target_at(values, months)
Wartość krzywej celu w miesiącu `months`, zaokrąglona do zł; „—” dla `None`.

## months_to(net, target), months_to_paths(net, target)
Pierwszy miesiąc, w którym wartość na rękę ≥ cel (dla wszystkich ścieżek naraz w wariancie Monte Carlo). `None` albo nieskończoność oznacza brak celu w horyzoncie.

## duration(months), month_label(months), pln(value)
Formatowanie: „6 l. 8 m.”, „2033-02”, „30 110”.

## print_baseline()
Ranking dla parametrów domyślnych w konsoli oraz cel najszybciej/najwolniej: nominalnie i w dzisiejszych zł.

## analyzer
Wyjście bloku: wypisuje ranking i zwraca ten obiekt.
