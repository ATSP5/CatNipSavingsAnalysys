Rekord danych: jedna możliwość odkładania pieniędzy w porównaniu — konto, obligacja albo instrument rynkowy.

**Dlaczego tu jest:** analizator traktuje wszystkie instrumenty jednakowo (wiersz rankingu, krzywa), a InstrumentSimulators wybiera symulator po rodzaju `spec`.

## key
Identyfikator: `erste`, `acc_<bank>`, `bond_<KOD>`, `gold`, `fund`, `etf`. Ten sam klucz służy w pamięci podręcznej i na wykresach.

## label
Nazwa w rankingu.

## group
Konto, Obligacje, Złoto, Fundusz albo ETF.

## risk
Opis ryzyka w rankingu.

## spec
AccountOffer, BondSpec albo MarketAssetSpec (już z parametrami ze strony).

## is_account, is_market
Rodzaj instrumentu. Konto liczone jest bez skalowania, instrument rynkowy z Monte Carlo.
