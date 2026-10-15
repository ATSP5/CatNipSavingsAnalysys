Rekord danych: oferta konta oszczędnościowego (stawka do limitu, standard powyżej limitu i po promocji).

**Dlaczego tu jest:** jeden kształt dla oferty Erste i wszystkich promocji. SavingsAccountSimulator liczy je tak samo, a strona nadpisuje parametry Erste kopią przez `with_changes`.

## key, bank, product
Identyfikator, bank i nazwa produktu. `label` = „bank — produkt”.

## promo_rate_pct
Stawka do limitu w % (≥ 0). Wyższa skraca czas dojścia, dopóki saldo mieści się w limicie.

## limit_pln
Kwota objęta stawką promocyjną w zł (≥ 0). Przy celu 400 tys. zł saldo szybko przekracza limit, a nadwyżka ma tylko stawkę standardową.

## promo_months
Okres promocji w miesiącach (≥ 0) albo `None`, gdy stawka obowiązuje stale (Erste przy aktywności na koncie). Krótka promocja to zwykle 3 miesiące, potem stawka standardowa.

## standard_rate_pct
Stawka ponad limitem i po promocji w % (≥ 0). Gdy bank jej nie podaje: średnia rynkowa 0,86%.

## conditions, source
Warunki promocji i źródło.

## with_changes(**changes)
Kopia z podmienionymi polami (strona zmienia tak stawkę i limit Erste).
