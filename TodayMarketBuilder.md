Składa parametry rynku „na dziś” w jeden rekord MarketAssumptions.

Dane pobierane na żywo:
- stopa NBP,
- inflacja GUS,
- historia złota.

Oferty spisane ze źródeł (stan 13.10.2026), bo nie mają darmowego API:
- 10 kont oszczędnościowych,
- 8 rodzajów obligacji skarbowych,
- złoto, fundusz krótkoterminowych obligacji skarbowych i globalny ETF akcyjny,
- źródła.

**Dlaczego tu jest:** wszystkie dane „na dziś” są w jednym miejscu, więc aktualizacja ofert to zmiana tego jednego bloku. Strona startuje z tych wartości, a suwaki je nadpisują. Jest podłączony do SavingsAnalyzer.

**Aktualizacja:** oferty kont zmieniają się co kilka tygodni, a obligacje co miesiąc (komunikat MF). Przy ponownej analizie przepisz je ze źródeł z metody `sources()`.

## reference_rate
NbpRate z NbpRateClient.

## inflation
CpiHistory z GusInflationClient.

## gold_history
GoldHistory z NbpGoldClient.

## OFFERS_AS_OF
Data spisania ofert (2026-10-13).

## AVERAGE_STANDARD_RATE
Średnia stawka standardowa kont po promocji (0,86%, moneteo IX 2026). Dotyczy banków, które jej nie podają. Wyższa wartość skraca czas dojścia kont po skończonej promocji.

## market()
Wyjście bloku: MarketAssumptions; podatek Belki stały 19%.

## accounts()
Oferty kont jako AccountOffer:
- Erste Konto Pro (4,5% do 100 tys. zł, stawka stała przy aktywności na koncie; ponad limitem 0,5%),
- promocje: Credit Agricole 6,5%, Nest 6,1%, VeloBank 6%, Pekao 5,7%, ING 5,5%, mBank 5,5%, Millennium 5,25%, BOŚ 7%.

Ich `promo_months` to okres promocji w miesiącach.

## bonds()
Oferta obligacji MF z października 2026 jako BondSpec:
- OTS 2,00%,
- ROR 4,00% (potem stopa NBP),
- DOR 4,15% (potem stopa NBP + 0,15 pp),
- TOS 4,40%,
- COI 4,75% (potem inflacja + 1,5 pp),
- EDO 5,35% (potem inflacja + 2 pp),
- ROS 5,00% i ROD 5,60% (tylko dla rodzin 800+).

Opłaty za wcześniejszy wykup według edolabs.pl.

## assets()
- Złoto: wzrost = średnia z historii NBP, zmienność z historii, marża zakupu 3%, dyskonto skupu 2%.
- Fundusz: 4,3%/rok, zmienność 1%.
- ETF: 7%/rok, zmienność 16%, przewalutowanie 0,5% w każdą stronę.

## sources()
Lista `(opis, adres)` pokazywana na stronie.
