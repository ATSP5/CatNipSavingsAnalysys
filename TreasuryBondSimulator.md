Symuluje kupowanie obligacji skarbowych. Co miesiąc kupuje nową serię za:
- wpłatę,
- wypłacone odsetki (ROR, DOR, COI — po Belce),
- kwoty z wykupionych serii (rollover).

Wartość w danym miesiącu to kwota po przedterminowym wykupie wszystkiego: kapitał + naliczone odsetki − opłata za wcześniejszy wykup (nie wyższa niż odsetki) − 19% od odsetek pomniejszonych o opłatę.

**Dlaczego tu jest:** zasady obligacji (kapitalizacja roczna, wypłaty kuponów, indeksacja inflacją z odczytu sprzed 2 miesięcy, opłaty) to osobna, dobrze sprawdzalna logika. Wynik jest liniowy względem wpłat, więc SavingsAnalyzer liczy go raz dla 1 zł i skaluje. Jest podłączony do InstrumentSimulators.

## tax
TaxRules: Belka od odsetek i zysków przy wykupie.

## simulate(spec, scenario, cash)
ValueCurve (wartość na rękę po wykupie w każdym miesiącu).
- `spec`: BondSpec.
- `cash`: wpłaty w każdym miesiącu (≥ 0).

Wynik sprawdzony ręcznie: 100 zł w EDO przy inflacji 3,4% daje po 10 latach 155,99 zł netto.

## _year_rate(spec, scenario, lot, year)
Oprocentowanie roku odsetkowego:
- rok 0 (i obligacje stałe): stawka pierwszego okresu,
- później: max(inflacja, 0) + marża; inflacja to odczyt GUS ogłoszony w miesiącu przed początkiem okresu.

## _month_rate(spec, scenario, lot, month)
Oprocentowanie miesiąca dla ROR i DOR: w pierwszym miesiącu stawka z oferty, potem stopa NBP + marża.

## _events(spec, scenario, lot, held)
Wypłaty na początku miesiąca: kupony, kapitalizacja, wykup. Zwraca gotówkę po podatku i informację, czy seria została wykupiona.

## _redemption_value(spec, scenario, lot, held)
Wartość serii przy przedterminowym wykupie w miesiącu `held` od zakupu.

## bond_sim
Wyjście bloku: zwraca ten obiekt podłączonym blokom.
