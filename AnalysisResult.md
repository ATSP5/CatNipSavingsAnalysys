Rekord danych: wynik jednej symulacji dla strony, tworzony przez SavingsAnalyzer.evaluate przy każdej zmianie parametru.

**Dlaczego tu jest:** strona dostaje gotowe tabele i serie wykresów, więc nie zawiera logiki obliczeń.

## ranking
Wiersze rankingu posortowane po czasie dojścia przy wybranej wpłacie: czasy przy 3 500 i 4 000 zł oraz przy wybranej wpłacie, data, cel w tym dniu (nominalnie) i w dzisiejszych zł, szansa i zakres z Monte Carlo, wartość netto po horyzoncie (nominalnie i w dzisiejszych zł).

## offers
Wszystkie oferty kont, tym samym układem.

## chart, chart_series
Wartość netto w czasie dla instrumentów z wykresu (nominalnie albo w dzisiejszych zł) i nazwy serii, łącznie z linią „Cel”.

## fan
Percentyle p10/mediana/p90 wybranego instrumentu rynkowego i cel, miesiąc po miesiącu.

## cpi
Inflacja GUS z ostatnich 10 lat i założona ścieżka.

## fastest_label, fastest_months, fastest_date
Najszybszy instrument, liczba miesięcy i data osiągnięcia celu.

## kpis
Teksty kafelków: inflacja, średnia 10 lat, stopa NBP, złoto, kapitał startowy, wzrost cen w horyzoncie.

## notes
Założenia do pokazania na stronie (w tym opis wybranego trybu celu).

## target_view
Słownik (domyślnie pusty) z sekcji „Cel w dzisiejszych i przyszłych złotych”: `today_mode` (bool), `target` (tekst), `missing` (liczba instrumentów bez celu w horyzoncie), `fastest` i `slowest` — każdy z polami `instrument`, `date`, `duration`, `nominal`, `today`, `prices` (teksty gotowe do wyświetlenia). Budowany przez `SavingsAnalyzer._target_view`.
