Rekord danych: wskaźnik inflacji CPI GUS za jeden miesiąc (ogółem, Polska).

**Dlaczego tu jest:** wspólny kształt odczytu z pliku CSV GUS i z API DBW. Tworzy go GusInflationClient, a zbiera CpiHistory.

## year, month
Rok i miesiąc (1–12).

## yoy_pct
Inflacja r/r w % (analogiczny miesiąc poprzedniego roku = 100, minus 100). Ostatni odczyt jest domyślną inflacją na stronie i bazą indeksacji obligacji.

## mom_pct
Zmiana m/m w % (poprzedni miesiąc = 100, minus 100). Służy do średniej inflacji z 10 lat.

## label
Etykieta `RRRR-MM`.
