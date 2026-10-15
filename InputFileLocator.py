from pathlib import Path
from typing import List

from AnalysisSettings import AnalysisSettings


class InputFileLocator:
    """Znajduje pliki projektu: folder z plikiem .catnip lokalnie, /app w Dockerze; tworzy folder output."""

    def __init__(self, settings: AnalysisSettings):
        self.input_folder = settings.input_folder

    def locator(self) -> "InputFileLocator":
        return self

    def find_input(self, file_name: str) -> Path:
        candidates = []
        for root in self.project_roots():
            candidates += [root / self.input_folder / file_name, root / file_name]
        for candidate in candidates:
            if candidate.is_file():
                return candidate
        raise FileNotFoundError("Nie znaleziono %s w folderze '%s' obok pliku .catnip (szukano: %s)"
                                % (file_name, self.input_folder, ", ".join(str(c.parent) for c in candidates[:4])))

    def output_folder(self) -> Path:
        folder = self.project_roots()[0] / "output"
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    @staticmethod
    def project_roots() -> List[Path]:
        """Foldery z plikiem .catnip najpierw; nigdy korzeń systemu (w Dockerze dirname('/app') == '/')."""
        here = Path(__file__).resolve().parent
        roots = []
        for folder in (Path.cwd(), here, here.parent):
            if folder not in roots and folder != Path(folder.anchor):
                roots.append(folder)
        return sorted(roots, key=lambda folder: not any(folder.glob("*.catnip")))
