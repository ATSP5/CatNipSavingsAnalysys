Rekord danych: instrument o zmiennej cenie (złoto, fundusz, ETF) — oczekiwany zwrot, zmienność, koszty transakcji i reguła podatkowa.

**Dlaczego tu jest:** trzy instrumenty różnią się tylko parametrami, więc MarketAssetSimulator liczy je jednym modelem. Strona podmienia zwrot, zmienność i koszty przez `with_changes`.

## key, name, note
Identyfikator (`gold`, `fund`, `etf`), nazwa i opis założeń.

## expected_return_pct
Oczekiwany roczny wzrost ceny w %. Na stronie: złoto −5…15, fundusz 0…10, ETF −2…15. Wyższy oznacza krótszy czas dojścia.

## volatility_pct
Roczna zmienność w %. Na stronie: złoto 0…40, ETF 0…40, fundusz z danych (1%). Wyższa poszerza zakres p10–p90 i obniża szansę w horyzoncie.

## buy_cost_pct, sell_cost_pct
Koszt zakupu (marża mennicy, przewalutowanie) i sprzedaży (dyskonto skupu) w %, na stronie 0–10. Obniżają wartość na rękę.

## tax
- `belka`: 19% od łącznego zysku przy sprzedaży (fundusz, ETF),
- `gold`: PIT tylko przy sprzedaży przed upływem pół roku.

## start_price
Cena startowa (dla złota cena uncji z NBP). Model liczy względne zmiany ceny, więc sama wartość nie wpływa na wynik.

## with_changes(**changes)
Kopia z podmienionymi polami.
