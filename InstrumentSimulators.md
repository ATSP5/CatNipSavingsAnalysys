Kieruje instrument do właściwego symulatora: konto → SavingsAccountSimulator, obligacje → TreasuryBondSimulator, złoto/fundusz/ETF → MarketAssetSimulator.

**Dlaczego tu jest:** SavingsAnalyzer ma już 5 wejść (najwięcej, ile pozwala blok CatNip). Trzy symulatory trafiają do niego jednym połączeniem przez ten blok, a analizator nie musi wiedzieć, który symulator obsługuje który instrument. Jest podłączony do SavingsAnalyzer.

## account_sim
SavingsAccountSimulator.

## bond_sim
TreasuryBondSimulator.

## asset_sim
MarketAssetSimulator.

## run(instrument, scenario, cash, repeat_promo, paths, seed)
ValueCurve z właściwego symulatora.
- `repeat_promo`: dotyczy tylko kont.
- `paths`, `seed`: dotyczą tylko instrumentów rynkowych; bez `seed` albo przy `paths` = 0 liczy wariant bez losowania.

## is_linear(instrument)
`True` dla obligacji i instrumentów rynkowych (wynik skaluje się z wpłatą), `False` dla kont (limit kwoty).

## simulators
Wyjście bloku: zwraca ten obiekt podłączonym blokom.
