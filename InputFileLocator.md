Znajduje pliki projektu niezależnie od miejsca uruchomienia: lokalnie (folder z `.catnip`), w Dockerze (`/app`) i w folderze ze źródłami. Tworzy też folder `output` na kopie odpowiedzi API.

**Dlaczego tu jest:** ścieżka Windows nie istnieje w kontenerze, więc logika szukania plików jest w jednym bloku zamiast w każdym kliencie. Jest podłączony do SavingsHistoryLoader (Excel), GusInflationClient (kopia inflacji) i NbpGoldClient (kopia cen złota).

## settings
AnalysisSettings: z niego bierze `input_folder`.

## find_input(file_name)
Ścieżka do pliku. Najpierw szuka w `<projekt>/Input/<plik>`, potem w folderze projektu; foldery z plikiem `.catnip` mają pierwszeństwo. Gdy pliku brak, zgłasza `FileNotFoundError` z listą przeszukanych miejsc.

## output_folder()
Folder `output` obok projektu (tworzony, gdy go brak). Trafiają tam `gus_cpi.json` i `nbp_gold.json`.

## project_roots()
Foldery, w których szukać plików. Nigdy nie zawiera korzenia systemu (w Dockerze rodzicem `/app` jest `/`).

## locator
Wyjście bloku: zwraca ten obiekt podłączonym blokom.
