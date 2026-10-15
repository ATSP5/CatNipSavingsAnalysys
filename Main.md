Punkt wejścia programu. CatNip generuje jego treść z grafu (`main_1.py`): tworzy bloki w kolejności połączeń, przekazuje wyniki do konstruktorów i na końcu wywołuje `show()` strony SavingsSimulatorPage.

**Dlaczego tu jest:** główny blok projektu, w którym kończy się przepływ. Nie ma własnej logiki, więc zmiany robi się w blokach, a nie tutaj.

## page
Wejście: wyjście `show` strony SavingsSimulatorPage. Strona działa dalej po zakończeniu przepływu (KeepAlive), dopóki jej nie zamkniesz.

## Uruchomienie
Pakiety ręczne: `openpyxl` (numpy jest już w obrazie `python:3.11-slim` na tym komputerze; na czystym obrazie trzeba wpisać `numpy openpyxl` i używać CatNip z poprawionym sprawdzaniem pakietów). W CatNip 1.2.6 kontrolki strony nie reagują w Dockerze — do pracy z suwakami używaj venv:3.11.
