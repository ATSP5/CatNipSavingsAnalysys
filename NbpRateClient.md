Pobiera bieżącą stopę referencyjną NBP z darmowego pliku XML (`static.nbp.pl/dane/stopy/stopy_procentowe.xml`).

**Dlaczego tu jest:** stopa NBP wyznacza oprocentowanie obligacji ROR i DOR (stopa + marża) i jest punktem wyjścia ścieżki stóp, z którą przesuwają się stawki kont oszczędnościowych. Jest podłączony do TodayMarketBuilder.

## timeout_s
Limit czasu zapytania w sekundach (> 0, domyślnie 15).

## FALLBACK
Wartość zapasowa, gdy nie ma sieci: 3,75% od 2026-03-05. Wtedy w konsoli pojawia się komunikat, a analiza liczy się dalej na tej wartości.

## reference_rate()
Wyjście bloku: NbpRate (stopa w %, data obowiązywania, źródło).
