Strona interaktywna w zakładce Output: kiedy uzbiera się cel (suwak, domyślnie 400 tys. zł) w każdym instrumencie — ranking, cel przeliczony na dzisiejsze i przyszłe złote, wykres wartości netto w czasie, rozrzut Monte Carlo, inflacja GUS, oferty kont i obligacji, historia wpłat, założenia i źródła. Każda zmiana kontrolki woła `SavingsAnalyzer.evaluate` i rysuje stronę od nowa (0,04–0,5 s).

**Dlaczego tu jest:** sam widok bez logiki obliczeń; wszystko liczy SavingsAnalyzer (wejście `analyzer`). Wyjście `show` jest podłączone do Main. Stan startuje od `SavingsAnalyzer.defaults()` (parametry na dziś), a przycisk „Przywróć parametry z dziś” do nich wraca.

## analyzer
Wejście: SavingsAnalyzer.

## contribution (3 000–5 000 zł, krok 50)
Wpłata miesięczna. Wyższa skraca czas dojścia.

## target (suwak 50 000–2 000 000 zł, krok 10 000; domyślnie `AnalysisSettings.target_pln` = 400 000)
Kwota celu. Jak ją rozumieć, mówi `target_mode`. Wyższa wydłuża czas dojścia wszystkich instrumentów; poza zakresem suwaka wartość ustawić można tylko w AnalysisSettings.

## target_mode (radio: `future` / `today`; domyślnie `future`)
Przełącznik wartość przyszła / wartość dzisiejsza:
- **future — wartość przyszła:** cel to `target` zł nominalnie w dniu uzbierania; w dzisiejszych pieniądzach jest wart mniej (o wzrost cen do tego dnia).
- **today — wartość dzisiejsza:** cel to siła nabywcza `target` dzisiejszych zł; nominalnie rośnie z założoną inflacją, więc w dniu uzbierania trzeba mieć więcej. Czas dojścia wydłuża się (zwykle o 1,5–4 lata).

Zastąpił dawny przełącznik `real_target`.

## Sekcja „Cel w dzisiejszych i przyszłych złotych”
Dwie karty z `r.target_view`: **Najszybciej** (pierwszy instrument rankingu) i **Najwolniej** (ostatni instrument rankingu, który osiąga cel w horyzoncie). Każda pokazuje datę i czas dojścia przy wybranej wpłacie, instrument, cel w dzisiejszych zł, cel w dniu uzbierania (nominalnie) oraz wzrost cen do tego dnia. Instrumenty, które nie osiągają celu w horyzoncie, są policzone w opisie. Zależy od wszystkich parametrów makro (inflacja przelicza złote dzisiejsze na przyszłe).

## start_capital (≥ 0 zł, krok 1 000)
Kapitał startowy; domyślnie suma historii wpłat.

## horizon_years (5–30 lat)
Horyzont symulacji i wykresów. Instrument, który nie dojdzie do celu w horyzoncie, nie liczy się jako „najwolniejszy”.

## index_contributions (przełącznik)
Wpłaty rosnące z inflacją. Skraca czas dojścia.

## cpi_start, cpi_long (−1…12 %, krok 0,1); cpi_months (0–60)
Inflacja dziś, docelowa i czas dojścia do niej. Wpływa na obligacje indeksowane, wartości realne i przeliczenie celu na dzisiejsze/przyszłe zł.

## ref_end (0–10 %, krok 0,25); ref_months (0–36)
Docelowa stopa NBP i czas dojścia do niej. Wpływa na ROR, DOR i konta.

## erste_rate (0–8 %), erste_limit (zł), erste_std (0–5 %)
Stawka Erste do limitu, limit i stawka ponad limitem.

## repeat_promo (przełącznik)
Promocje banków odnawiane bez końca (przenoszenie środków).

## gold_return (−5…15 %), gold_vol (0–40 %), gold_premium (0–10 %), gold_discount (0–10 %)
Oczekiwany wzrost ceny złota, zmienność, marża zakupu i dyskonto skupu.

## fund_return (0–10 %)
Zwrot funduszu obligacji po opłatach.

## etf_return (−2…15 %), etf_vol (0–40 %)
Oczekiwany zwrot i zmienność ETF akcyjnego.

## include_family (przełącznik)
Pokazuje obligacje ROS/ROD (tylko 800+).

## chart_real (przełącznik)
Wykres w dzisiejszych złotych. Przy `target_mode = today` linia celu jest wtedy pozioma.

## fan_key (etf / gold / fund)
Instrument na wykresie rozrzutu Monte Carlo.

## setup(), reset()
Ustawienie i przywrócenie parametrów z `defaults()` (także `target` i `target_mode`).

## prepare()
Liczy wynik i dane dla znaczników strony, w tym `tv` (= `r.target_view`), `target_mode_text` i `missing_text`.

## target_mode_text(view), missing_text(view)
Opis wybranego trybu celu nad kartami oraz dopisek o liczbie instrumentów, które nie osiągają celu w horyzoncie.

## main_figure(result, values), fan_figure(result, values)
Wykresy Plotly: wartość netto z przerywaną linią celu oraz pasmo p10–p90 z medianą.

## SERIES_COLORS
Kolory serii wykresu głównego.

## show
Wyjście: pokazuje lub odświeża stronę w zakładce Output.
