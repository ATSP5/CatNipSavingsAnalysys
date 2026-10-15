class AnalysisSettings:
    """Stałe analizy: cel, zakres miesięcznych wpłat, horyzont, Monte Carlo i pliki wejściowe."""

    def __init__(self, target_pln: float = 400000.0, contribution_min: float = 3500.0,
                 contribution_max: float = 4000.0, horizon_years: int = 20, mc_paths: int = 500,
                 seed: int = 2026, history_file: str = "Savings.xlsx", input_folder: str = "Input",
                 cpi_history_from_year: int = 2010):
        if target_pln <= 0:
            raise ValueError("target_pln musi być dodatni")
        if not 0 < contribution_min <= contribution_max:
            raise ValueError("wymagane 0 < contribution_min <= contribution_max")
        if not 1 <= horizon_years <= 40:
            raise ValueError("horizon_years: od 1 do 40 lat")
        self.target_pln = float(target_pln)
        self.contribution_min = float(contribution_min)
        self.contribution_max = float(contribution_max)
        self.horizon_years = int(horizon_years)
        self.mc_paths = int(mc_paths)
        self.seed = int(seed)
        self.history_file = history_file
        self.input_folder = input_folder
        self.cpi_history_from_year = int(cpi_history_from_year)

    def settings(self) -> "AnalysisSettings":
        return self
