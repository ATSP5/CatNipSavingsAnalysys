Rekord danych: parametry rynku na dzień analizy — oferty kont i obligacji, stopa NBP, inflacja GUS, złoto, fundusz i ETF, stawka Belki, źródła.

**Dlaczego tu jest:** przenosi wszystkie dane „na dziś” z TodayMarketBuilder do SavingsAnalyzer jednym połączeniem (blok ma najwyżej 5 wejść).

## as_of
Data analizy.

## reference_rate, inflation, gold_history
NbpRate, CpiHistory, GoldHistory.

## accounts, bonds, assets
Krotki AccountOffer, BondSpec, MarketAssetSpec.

## belka_pct
Stawka Belki w % (19).

## sources
Krotka `(opis, adres)` źródeł dla strony.

## account(key), asset(key)
Oferta konta albo instrument rynkowy po kluczu. Nieznany klucz daje `StopIteration`.
