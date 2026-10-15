from datetime import date

from AccountOffer import AccountOffer
from BondSpec import BondSpec
from CpiHistory import CpiHistory
from GoldHistory import GoldHistory
from MarketAssetSpec import MarketAssetSpec
from MarketAssumptions import MarketAssumptions
from NbpRate import NbpRate


class TodayMarketBuilder:
    """Składa parametry „na dziś”: dane pobierane na żywo (NBP, GUS, złoto) i oferty spisane ze źródeł.

    Oferty kont i obligacji nie mają darmowego API — są wpisane poniżej z datą i źródłem (stan 13.10.2026).
    """

    OFFERS_AS_OF = "2026-10-13"
    AVERAGE_STANDARD_RATE = 0.86          # średnia stawka standardowa kont oszczędnościowych, moneteo IX 2026

    def __init__(self, reference_rate: NbpRate, inflation: CpiHistory, gold_history: GoldHistory):
        self.reference_rate = reference_rate
        self.inflation = inflation
        self.gold_history = gold_history

    def market(self) -> MarketAssumptions:
        return MarketAssumptions(
            as_of=date.today().isoformat(), reference_rate=self.reference_rate, inflation=self.inflation,
            gold_history=self.gold_history, accounts=self.accounts(), bonds=self.bonds(),
            assets=self.assets(), belka_pct=19.0, sources=self.sources())

    def accounts(self):
        std = self.AVERAGE_STANDARD_RATE
        ranking = "moneteo.com ranking kont oszczędnościowych, 09.10.2026"
        return (
            AccountOffer("erste", "Erste Bank Polska", "Konto Pro oszczędnościowe", 4.5, 100000, None, 0.5,
                         "4,5% do 100 tys. zł przy aktywności na koncie w poprzednim miesiącu (regulamin do "
                         "30.11.2026 — zakładamy przedłużanie); powyżej limitu 0,5%", ranking),
            AccountOffer("erste_platinum", "Erste Bank Polska", "Konto Pro oszczędnościowe Platinum", 4.5, 150000,
                         None, 0.5, "jak wyżej, limit 150 tys. zł dla klientów Erste Platinum", ranking),
            AccountOffer("bos", "BOŚ Bank", "Konto Cyfrowy Zysk", 7.0, 30000, 4, std,
                         "nowi klienci, do 31.01.2027; analizy.pl: oferta wygaszana", ranking),
            AccountOffer("credit_agricole", "Credit Agricole", "Rachunek Oszczędzam Plus", 6.5, 100000, 3, 0.1,
                         "nowi klienci, nowe środki, 100 dni; potem 0,1%", ranking),
            AccountOffer("nest", "Nest Bank", "Nest Konto Oszczędnościowe", 6.1, 25000, 3, std,
                         "nowi klienci, 90 dni", ranking),
            AccountOffer("velo", "VeloBank", "Elastyczne Konto Oszczędnościowe", 6.0, 100000, 3, std,
                         "nowi klienci, 92 dni", ranking),
            AccountOffer("pekao", "Bank Pekao", "Konto Oszczędnościowe", 5.7, 100000, 3, std,
                         "nowi klienci, 92 dni", ranking),
            AccountOffer("ing", "ING Bank Śląski", "Otwarte Konto Oszczędnościowe", 5.5, 400000, 3, std,
                         "Bonus na start, 3 miesiące, nowe lub nieaktywne konta", ranking),
            AccountOffer("mbank", "mBank", "Moje Cele (z mKonto Intensive)", 5.5, 200000, 6, std,
                         "nowi klienci z mKonto Intensive, 180 dni", ranking),
            AccountOffer("millennium", "Bank Millennium", "Konto Oszczędnościowe Profit", 5.25, 200000, 3, std,
                         "nowe środki, 91 dni", ranking),
        )

    @staticmethod
    def bonds():
        return (
            BondSpec("OTS", "3-miesięczne", 3, 2.00, "fixed_capitalized", 0.0, 100.0),
            BondSpec("ROR", "roczne", 12, 4.00, "monthly_ref", 0.00, 0.50),
            BondSpec("DOR", "2-letnie", 24, 4.15, "monthly_ref", 0.15, 0.70),
            BondSpec("TOS", "3-letnie stałoprocentowe", 36, 4.40, "fixed_capitalized", 0.0, 1.00),
            BondSpec("COI", "4-letnie indeksowane", 48, 4.75, "cpi_yearly_coupon", 1.50, 2.00),
            BondSpec("EDO", "10-letnie emerytalne", 120, 5.35, "cpi_capitalized", 2.00, 3.00),
            BondSpec("ROS", "6-letnie rodzinne", 72, 5.00, "cpi_capitalized", 2.00, 2.00, family_only=True),
            BondSpec("ROD", "12-letnie rodzinne", 144, 5.60, "cpi_capitalized", 2.50, 3.00, family_only=True),
        )

    def assets(self):
        gold = self.gold_history
        return (
            MarketAssetSpec("gold", "Złoto fizyczne (sztabki 1 oz)", round(gold.cagr * 100, 2),
                            round(gold.volatility * 100, 1), 3.0, 2.0, "gold", gold.latest_per_ounce,
                            "Cena NBP; oczekiwany wzrost = średnia z historii NBP od %s. Sztabka 1 oz kosztuje "
                            "ok. 1–4%% ponad spot, skup płaci ok. 2%% poniżej spotu." % gold.days[0]),
            MarketAssetSpec("fund", "Fundusz krótkoterminowych obligacji skarbowych (np. PZU Sejf+)", 4.3, 1.0,
                            0.0, 0.0, "belka", 100.0,
                            "Lider grupy 12M: PZU Sejf+ +5,45% (Bankier, 4.08.2026); na przyszłość ok. 4,3% po "
                            "opłatach — rentowność krótkich obligacji przy stopie NBP 3,75%."),
            MarketAssetSpec("etf", "Globalny ETF akcyjny (np. Vanguard FTSE All-World / iShares MSCI ACWI)", 7.0,
                            16.0, 0.5, 0.5, "belka", 100.0,
                            "Długoterminowy zwrot akcji globalnych w zł ok. 7%/rok, zmienność ok. 16%; "
                            "przewalutowanie ok. 0,5% w każdą stronę, makler bez prowizji."),
        )

    @staticmethod
    def sources():
        return (
            ("Inflacja CPI — GUS, API Dziedzinowej Bazy Wiedzy (zmienna 305)", "https://api-dbw.stat.gov.pl"),
            ("Stopa referencyjna NBP", "https://static.nbp.pl/dane/stopy/stopy_procentowe.xml"),
            ("Cena złota NBP", "https://api.nbp.pl/api/cenyzlota"),
            ("Oferta obligacji skarbowych, październik 2026 — MF",
             "https://www.gov.pl/web/finanse/oferta-oszczednosciowych-obligacji-skarbowych---pazdziernik-2026-r"),
            ("Opłaty za wcześniejszy wykup obligacji", "https://edolabs.pl/porownanie-obligacji"),
            ("Ranking kont oszczędnościowych, 09.10.2026", "https://moneteo.com/rankingi/konta-oszczednosciowe"),
            ("Erste Konto Pro oszczędnościowe",
             "https://moneteo.com/analizy/konto-pro-oszczednosciowe-erste-bank-polska"),
            ("Fundusze dłużne krótkoterminowe — stopy zwrotu",
             "https://www.bankier.pl/fundusze/notowania/ARK65/konkurencja"),
        )
