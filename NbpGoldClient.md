Pobiera historię ceny złota z API NBP (`api.nbp.pl/api/cenyzlota`, zł za gram, od 2013-01-02) w oknach po 367 dni i zwraca GoldHistory.

**Dlaczego tu jest:** cena złota w zł z historii daje trzy parametry na dziś: cenę uncji, średnioroczny wzrost (domyślny oczekiwany wzrost złota) i zmienność (dla Monte Carlo). Jest podłączony do TodayMarketBuilder.

## locator
InputFileLocator: plik kopii `output/nbp_gold.json`.

## timeout_s
Limit czasu jednego zapytania w sekundach (> 0, domyślnie 30).

## gold_history()
Wyjście bloku: GoldHistory. Po udanym pobraniu zapisuje kopię. Gdy sieć nie działa, czyta kopię; bez kopii zgłasza błąd odczytu pliku (`FileNotFoundError`).
