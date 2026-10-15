Pobiera miesięczną inflację CPI (ogółem, Polska) z GUS i zwraca CpiHistory: inflacja r/r i m/m dla każdego miesiąca.

Źródła danych:
1. Plik CSV GUS ze wskaźnikami od 1982 r. — jedno zapytanie, ale aktualizowany z opóźnieniem.
2. API Dziedzinowej Bazy Wiedzy (`api-dbw.stat.gov.pl`, zmienna 305) — tylko dla miesięcy, których brak w CSV. Do 2025 r. przekrój 739, od 2026 r. przekrój 1722.

**Dlaczego tu jest:** inflacja jest podstawą całej analizy. Indeksuje obligacje COI, EDO, ROS i ROD, wyznacza wartość „w dzisiejszych zł” i cel realny, a ostatni odczyt jest domyślną inflacją na stronie. API GUS ma limit zapytań (odpowiada 429 i każe czekać ok. 25 s), dlatego ostrożność — pytania po kolei, przerwy, kopia lokalna — jest w tym jednym bloku. Jest podłączony do TodayMarketBuilder.

## settings
AnalysisSettings: `cpi_history_from_year`.

## locator
InputFileLocator: folder `output` na kopię `gus_cpi.json`.

## inflation()
Wyjście bloku: CpiHistory.
- Kopia młodsza niż `CACHE_HOURS` (24 h) jest używana bez pobierania.
- Gdy sieć nie działa, używa starszej kopii.
- Bez sieci i bez kopii zgłasza `RuntimeError`.

## PAUSE_S
Przerwa między zapytaniami (0,4 s). Po odpowiedzi 429 klient czeka tyle, ile podaje nagłówek `Retry-After` (najwyżej 60 s), i próbuje do 4 razy.

## CACHE_HOURS
Ważność kopii lokalnej w godzinach (24). Przy 0 dane pobierają się przy każdym uruchomieniu (wolniej i bliżej limitu zapytań).
