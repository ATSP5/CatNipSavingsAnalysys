Rekord danych: dzienne ceny złota NBP w zł za gram, z właściwościami odczytu (cena uncji, średni wzrost, zmienność).

**Dlaczego tu jest:** przenosi historię z NbpGoldClient do TodayMarketBuilder, który bierze z niej domyślne parametry złota.

## days, prices_per_gram
Daty notowań i ceny w zł/g (rosnąco).

## source
Opis źródła (API albo kopia lokalna).

## latest_per_gram, latest_per_ounce
Ostatnia cena za gram i za uncję trojańską (31,1035 g). Uncja jest pokazywana na kafelku.

## years
Długość historii w latach.

## cagr
Średnioroczny wzrost ceny w zł w całej historii (ułamek; od 2013 r. ok. 8,8%). Domyślny oczekiwany wzrost złota na stronie. To historia, a nie prognoza, i bardzo silnie wpływa na pozycję złota w rankingu.

## volatility
Roczna zmienność z miesięcznych stóp zwrotu (ułamek; ok. 16%). Domyślna zmienność złota w Monte Carlo — szerokość zakresu p10–p90.

## month_end()
Ostatnie notowanie każdego miesiąca.
