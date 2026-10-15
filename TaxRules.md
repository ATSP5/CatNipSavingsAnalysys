Podatki od oszczędności:
- podatek Belki 19% od odsetek i zysków kapitałowych,
- dla złota inwestycyjnego PIT od zysku tylko przy sprzedaży przed upływem pół roku od końca miesiąca zakupu.

**Dlaczego tu jest:** przepisy podatkowe są w jednym miejscu, wspólnym dla wszystkich symulatorów. Zmiana stawki działa więc jednakowo dla kont, obligacji, funduszy i złota. Jest podłączony do SavingsAccountSimulator, TreasuryBondSimulator i MarketAssetSimulator.

## belka_pct
Stawka podatku Belki w % (0–100, domyślnie 19). Wyższa stawka wydłuża czas dojścia wszystkich instrumentów poza złotem trzymanym dłużej niż pół roku.

## gold_pit_pct
Stawka PIT od zysku ze szybkiej sprzedaży złota w % (0–100, domyślnie 12, pierwszy próg skali).

## gold_tax_free_after_months
Po ilu miesiącach od końca miesiąca zakupu sprzedaż złota jest wolna od podatku (≥ 0, domyślnie 6).

## belka_on(gain)
19% od dodatniego zysku (liczba albo tablica numpy); strata daje 0.

## gold_pit_on(gain)
PIT od dodatniego zysku ze złota.

## tax
Wyjście bloku: zwraca ten obiekt podłączonym blokom.
