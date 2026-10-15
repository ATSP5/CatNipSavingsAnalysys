import urllib.request
import xml.etree.ElementTree as ElementTree

from NbpRate import NbpRate


class NbpRateClient:
    """Pobiera bieżącą stopę referencyjną z darmowego pliku XML NBP; bez sieci zwraca wartość zapasową."""

    URL = "https://static.nbp.pl/dane/stopy/stopy_procentowe.xml"
    FALLBACK = NbpRate(rate_pct=3.75, valid_from="2026-03-05", source="wartość zapasowa (brak sieci)")

    def __init__(self, timeout_s: float = 15.0):
        self.timeout_s = timeout_s

    def reference_rate(self) -> NbpRate:
        try:
            request = urllib.request.Request(self.URL, headers={"User-Agent": "SavingsAnalysys/1.0"})
            with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
                root = ElementTree.fromstring(response.read())
            position = next(p for p in root.iter("pozycja") if p.get("id") == "ref")
            rate = NbpRate(rate_pct=float(position.get("oprocentowanie").replace(",", ".")),
                           valid_from=position.get("obowiazuje_od", ""), source="NBP stopy_procentowe.xml")
        except Exception as error:
            print("[NBP] nie udało się pobrać stopy (%s) — przyjmuję %.2f%%." % (error, self.FALLBACK.rate_pct))
            rate = self.FALLBACK
        print("[NBP] stopa referencyjna %.2f%% od %s" % (rate.rate_pct, rate.valid_from), flush=True)
        return rate
