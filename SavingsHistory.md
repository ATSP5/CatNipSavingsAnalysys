Rekord danych: historia wpłat z pliku wejściowego. Suma jest kapitałem startowym symulacji.

**Dlaczego tu jest:** przenosi historię z SavingsHistoryLoader do SavingsAnalyzer jednym połączeniem. Ma kilka prostych właściwości odczytu (suma, średnia, wiersze tabeli) używanych przez analizator i stronę.

## deposits
Krotka SavingsDeposit posortowana po dacie (może być pusta).

## source
Nazwa pliku albo „brak pliku”.

## total
Suma wpłat w zł. Domyślny kapitał startowy (pole „Kapitał startowy” na stronie): wyższy kapitał oznacza krótszy czas dojścia.

## monthly_average
Średnia wpłata na miesiąc kalendarzowy od pierwszej do ostatniej wpłaty (0 przy pustej historii). Tylko informacyjnie.

## rows()
Wiersze tabeli „Twoja historia wpłat”: Data, Wpłata, Narastająco.
