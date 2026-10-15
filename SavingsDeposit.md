Rekord danych: jedna wpłata z historii oszczędności (wiersz arkusza: Data, Kwota). Niezmienny rekord.

**Dlaczego tu jest:** typowana postać wiersza z Excela, tworzona raz w SavingsHistoryLoader. Dalej nikt nie parsuje już komórek. Jako rekord nie ma połączeń na kanwie.

## day
Data wpłaty (`date`).

## amount
Kwota w zł. Dodatnia to wpłata, ujemna — wypłata. Suma kwot jest kapitałem startowym, więc każda złotówka tu skraca czas dojścia do celu.
