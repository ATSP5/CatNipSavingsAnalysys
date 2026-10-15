Rekord danych: miesięczne ścieżki makro. Miesiąc 0 = dziś, miesiąc t = t miesięcy od dziś.

**Dlaczego tu jest:** wszystkie symulatory dostają ten sam scenariusz, więc różnice między instrumentami wynikają z ich zasad, a nie z różnych założeń. Ma metody odczytu z bezpiecznym indeksowaniem.

## LAG
Opóźnienie publikacji inflacji: 2 miesiące. Dziś znamy odczyt sprzed 2 miesięcy.

## params
ScenarioParams, z których powstał.

## cpi_yoy
Inflacja r/r w % dla miesięcy od −LAG do horyzontu (tablica numpy).

## ref_rate
Stopa NBP w % dla miesięcy 0…horyzont.

## price_index
Poziom cen (1,0 dziś). Wartość w dzisiejszych zł = wartość nominalna / `price_index`; cel realny = cel × `price_index`.

## months
Horyzont w miesiącach.

## cpi_at(month)
Inflacja r/r za miesiąc kalendarzowy `month`. Indeks jest obcinany do zakresu, więc miesiące poza horyzontem dostają wartość skrajną.

## ref_at(month)
Stopa NBP w miesiącu `month` (obcinana tak samo).
