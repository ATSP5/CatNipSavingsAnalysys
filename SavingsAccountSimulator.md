Symuluje konto oszczędnościowe miesiąc po miesiącu:
- wpłata,
- odsetki — stawka promocyjna do limitu, standardowa powyżej limitu i po promocji,
- kapitalizacja miesięczna, Belka od każdej kapitalizacji.

Stawki przesuwają się razem ze stopą NBP w scenariuszu.

**Dlaczego tu jest:** konto jest jedynym instrumentem nieliniowym względem wpłat (limit kwoty z wyższą stawką), więc nie da się go liczyć krzywą dla 1 zł jak obligacji czy funduszy. Ma własny symulator liczony dla każdej kwoty osobno. Jest podłączony do InstrumentSimulators.

## tax
TaxRules: Belka od odsetek.

## simulate(offer, scenario, cash, repeat_promo)
ValueCurve z saldem na początku każdego miesiąca (po wpłacie).
- `cash`: wpłaty w każdym miesiącu (zł ≥ 0).
- `repeat_promo`: `True` oznacza, że stawka promocyjna obowiązuje stale (zakładamy przenoszenie środków do kolejnych promocji). To wyraźnie skraca czas dojścia kont z krótką promocją.
- Stawka = stawka z oferty + (stopa NBP w danym miesiącu − dzisiejsza), nie mniej niż 0.

## account_sim
Wyjście bloku: zwraca ten obiekt podłączonym blokom.
