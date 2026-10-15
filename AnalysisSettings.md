Ustawienia analizy w jednym miejscu: cel oszczędzania, zakres miesięcznych wpłat, horyzont, liczba symulacji Monte Carlo i pliki wejściowe.

**Dlaczego tu jest:** to jedyne źródło konfiguracji, podłączone do InputFileLocator, SavingsHistoryLoader, GusInflationClient i SavingsAnalyzer. Żaden inny blok nie trzyma własnych stałych. Konstruktor sprawdza wartości od razu, więc błędna konfiguracja zatrzymuje uruchomienie na starcie, a nie w połowie obliczeń.

## target_pln
Cel w zł (> 0, inaczej `ValueError`). Domyślnie 400 000. To wartość startowa na stronie (pole „Cel”). Wyższy cel wydłuża czas dojścia wszystkich instrumentów.

## contribution_min, contribution_max
Dolna i górna wpłata miesięczna w zł; wymagane 0 < min ≤ max, inaczej `ValueError`. Domyślnie 3 500 i 4 000. Ranking pokazuje czas dojścia przy obu kwotach, a suwak wpłaty startuje od ich średniej.

## horizon_years
Horyzont symulacji w latach (1–40, inaczej `ValueError`). Domyślnie 20. Instrument, który nie osiągnie celu w horyzoncie, ma czas „nie w horyzoncie”. Dłuższy horyzont oznacza wolniejsze przeliczanie strony.

## mc_paths
Liczba ścieżek Monte Carlo dla złota, funduszu i ETF (≥ 0). Domyślnie 500. Przy 0 nie ma mediany, zakresu p10–p90 ani wykresu rozrzutu. Więcej ścieżek daje stabilniejsze percentyle, ale wolniejszą stronę.

## seed
Ziarno losowania (liczba całkowita). Domyślnie 2026. Daje te same wyniki przy każdym uruchomieniu. Ścieżki dla kapitału i dla wpłat używają tego samego ziarna, więc sumowanie krzywych jest poprawne.

## history_file
Nazwa pliku Excel z historią wpłat (domyślnie `Savings.xlsx`). Gdy pliku brak, kapitał startowy wynosi 0 zł.

## input_folder
Folder z danymi obok `.catnip` (domyślnie `Input`). Wielkość liter ma znaczenie w Dockerze.

## cpi_history_from_year
Od którego roku pobierać inflację z GUS (domyślnie 2010; sensownie 1982–bieżący rok). Wpływa na średnią z 10 lat na kafelku i na długość wykresu inflacji.

## settings
Wyjście bloku: zwraca ten obiekt podłączonym blokom.
