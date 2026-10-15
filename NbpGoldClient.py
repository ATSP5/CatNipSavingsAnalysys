import json
import urllib.request
from datetime import date, timedelta

from GoldHistory import GoldHistory
from InputFileLocator import InputFileLocator


class NbpGoldClient:
    """Pobiera historię ceny złota z API NBP (api.nbp.pl/api/cenyzlota, od 2013 r., okna po 367 dni)."""

    URL = "https://api.nbp.pl/api/cenyzlota/%s/%s?format=json"
    FIRST_DAY = date(2013, 1, 2)

    def __init__(self, locator: InputFileLocator, timeout_s: float = 30.0):
        self.cache_file = locator.output_folder() / "nbp_gold.json"
        self.timeout_s = timeout_s

    def gold_history(self) -> GoldHistory:
        try:
            days, prices = self._download()
            self.cache_file.write_text(json.dumps({"days": days, "prices": prices}), encoding="utf-8")
            source = "NBP API cenyzlota"
        except Exception as error:
            payload = json.loads(self.cache_file.read_text(encoding="utf-8"))   # brak kopii = błąd z opisem
            days, prices = payload["days"], payload["prices"]
            source = "NBP (zapisana kopia, brak sieci: %s)" % type(error).__name__
        history = GoldHistory(days=tuple(days), prices_per_gram=tuple(prices), source=source)
        print("[NBP] złoto %s: %.2f zł/g = %.0f zł/uncja; od %s średnio %+.1f%%/rok, zmienność %.1f%%"
              % (history.days[-1], history.latest_per_gram, history.latest_per_ounce, history.days[0],
                 history.cagr * 100, history.volatility * 100), flush=True)
        return history

    def _download(self):
        days, prices, start, today = [], [], self.FIRST_DAY, date.today()
        while start <= today:
            end = min(start + timedelta(days=366), today)
            request = urllib.request.Request(self.URL % (start.isoformat(), end.isoformat()),
                                             headers={"User-Agent": "SavingsAnalysys/1.0"})
            with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                for quote in json.loads(response.read().decode("utf-8")):
                    days.append(quote["data"])
                    prices.append(float(quote["cena"]))
            start = end + timedelta(days=1)
        return days, prices
