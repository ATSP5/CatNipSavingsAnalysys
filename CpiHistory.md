Rekord danych: miesięczna inflacja CPI z GUS od najstarszego miesiąca.

**Dlaczego tu jest:** przenosi inflację z GusInflationClient do TodayMarketBuilder i dalej do analizatora (kafelki, wykres, domyślna inflacja).

## readings
Krotka CpiReading, rosnąco po dacie.

## source
Opis źródła (API, plik CSV albo kopia lokalna).

## latest
Ostatni odczyt. Jego `yoy_pct` to domyślne `cpi_start` i `cpi_long` na stronie.

## average_yoy(years)
Średnioroczna inflacja z ostatnich `years` lat (≥ 1), liczona z indeksów m/m. Pokazywana na kafelku „Inflacja CPI”.
