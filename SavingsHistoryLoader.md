Czyta historię wpłat z pierwszego arkusza pliku Excel (kolumny `Data` i `Kwota`) i zwraca ją jako SavingsHistory. Suma wpłat staje się kapitałem startowym symulacji.

**Dlaczego tu jest:** parsowanie pliku użytkownika (nagłówki, daty jako numery seryjne Excela, puste wiersze) dzieje się raz, na brzegu programu. Dalej krążą już typowane rekordy SavingsDeposit. Jest podłączony do SavingsAnalyzer.

## locator
InputFileLocator: znajduje plik w folderze Input.

## settings
AnalysisSettings: nazwa pliku `history_file`.

## history()
Wyjście bloku: SavingsHistory z wpłatami posortowanymi po dacie.
- Brak pliku: pusta historia i komunikat, kapitał startowy 0 zł.
- Brak kolumny `Data` albo `Kwota` w pierwszym wierszu: `ValueError`.
- Wiersze z pustą datą lub kwotą są pomijane.
- Kwoty mogą być ujemne (wypłaty); zmniejszają wtedy kapitał startowy.

Wymaga pakietu `openpyxl` (na liście pakietów uruchomienia).

## _to_date(value)
Zamienia wartość komórki na datę: obiekt daty, numer seryjny Excela (liczba dni od 1899-12-30) albo tekst `RRRR-MM-DD`. Inny format daje `ValueError`.
