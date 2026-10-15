Rekord danych: obligacje jednej serii kupione w jednym miesiącu. Zmienny rekord — TreasuryBondSimulator aktualizuje `value` przy kapitalizacji.

**Dlaczego tu jest:** każda seria ma własny termin, oprocentowanie i opłatę, więc symulator śledzi je osobno. Wartość całości to suma serii.

## principal
Kwota nominalna serii w zł (> 0).

## start
Miesiąc zakupu (0 = dziś). Wyznacza rocznice odsetkowe i odczyt inflacji dla serii.

## value
Wartość po ostatniej kapitalizacji w zł. Na starcie równa `principal`.
