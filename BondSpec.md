Rekord danych: detaliczna obligacja skarbowa z bieżącej oferty MF (cena 100 zł).

**Dlaczego tu jest:** opisuje każdą serię kilkoma polami, a TreasuryBondSimulator liczy je jednym algorytmem według `kind`. Nowa seria to więc nowy rekord w TodayMarketBuilder.

## code, name
Kod (OTS, ROR, DOR, TOS, COI, EDO, ROS, ROD) i opis. `label` = „Obligacje KOD (opis)”.

## term_months
Okres do wykupu w miesiącach (≥ 1). Po wykupie kwota jest reinwestowana w nową serię.

## first_rate_pct
Oprocentowanie pierwszego okresu w % (≥ 0). W obligacjach stałych (OTS, TOS) obowiązuje przez cały okres.

## kind
- `monthly_ref`: odsetki co miesiąc, po pierwszym miesiącu stopa NBP + marża (ROR, DOR),
- `fixed_capitalized`: stała stopa, kapitalizacja roczna (OTS, TOS),
- `cpi_yearly_coupon`: od 2. roku inflacja + marża, odsetki wypłacane co rok (COI),
- `cpi_capitalized`: od 2. roku inflacja + marża, kapitalizacja roczna (EDO, ROS, ROD).

## margin_pct
Marża w pp (≥ 0) ponad stopę NBP albo inflację. Wyższa oznacza szybszy wzrost.

## early_fee_pln
Opłata za wcześniejszy wykup za obligację 100 zł (≥ 0), nie wyższa niż naliczone odsetki. W OTS ustawiona na 100, co oznacza utratę odsetek. Wyższa opłata obniża wartość na rękę przed terminem wykupu.

## family_only
`True` dla ROS i ROD (tylko beneficjenci 800+). Są pokazywane tylko przy przełączniku „Pokaż obligacje rodzinne”.

## with_changes(**changes)
Kopia z podmienionymi polami.
