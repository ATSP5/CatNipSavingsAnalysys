from datetime import date
from typing import Dict, List, Optional, Tuple

import numpy as np

from AnalysisResult import AnalysisResult
from AnalysisSettings import AnalysisSettings
from Instrument import Instrument
from InstrumentSimulators import InstrumentSimulators
from MarketAssumptions import MarketAssumptions
from SavingsHistory import SavingsHistory
from ScenarioBuilder import ScenarioBuilder
from ScenarioParams import ScenarioParams
from ValueCurve import ValueCurve


class SavingsAnalyzer:
    """Liczy, w którym miesiącu każdy instrument da cel (domyślnie 400 tys. zł) netto, po podatku Belki.

    Cel można podać jako wartość przyszłą (nominalne zł w dniu uzbierania) albo dzisiejszą (siła nabywcza
    dzisiejszych zł — nominalnie rośnie z inflacją); target_view przelicza go na obie miary w dniu uzbierania
    najszybszą i najwolniejszą drogą.

    Kapitał startowy = suma historii wpłat, pierwsza miesięczna wpłata za miesiąc. Wartość w miesiącu to
    kwota po zamknięciu wszystkiego (wykup obligacji z opłatą, sprzedaż złota w skupie, umorzenie funduszu).
    Obligacje i instrumenty rynkowe są liniowe względem wpłat, więc krzywe dla 1 zł są liczone raz na
    scenariusz i składane dla każdej kwoty wpłaty.
    """

    TARGET_MODES = ("future", "today")
    CHART_KEYS = ("erste", "best_bank", "bond_ROR", "bond_DOR", "bond_TOS", "bond_COI", "bond_EDO",
                  "bond_ROD", "gold", "fund", "etf")

    def __init__(self, settings: AnalysisSettings, history: SavingsHistory, market: MarketAssumptions,
                 scenarios: ScenarioBuilder, simulators: InstrumentSimulators):
        self.settings = settings
        self.history = history
        self.market = market
        self.scenarios = scenarios
        self.simulators = simulators
        self.today = date.today()
        self._unit_curves: Dict[tuple, Tuple[ValueCurve, ValueCurve]] = {}

    def analyzer(self) -> "SavingsAnalyzer":
        self.print_baseline()
        return self

    # --- parametry ------------------------------------------------------------------------------------
    def defaults(self) -> dict:
        """Parametry na dziś: dzisiejsze stopy, ostatni odczyt GUS utrzymany w całym horyzoncie."""
        m = self.market
        erste, gold = m.account("erste"), m.asset("gold")
        cpi = m.inflation.latest.yoy_pct
        return {
            "contribution": round((self.settings.contribution_min + self.settings.contribution_max) / 2),
            "start_capital": round(self.history.total, 2), "target": self.settings.target_pln,
            "target_mode": "future", "horizon_years": self.settings.horizon_years, "index_contributions": False,
            "cpi_start": cpi, "cpi_long": cpi, "cpi_months": 24,
            "ref_end": m.reference_rate.rate_pct, "ref_months": 12,
            "erste_rate": erste.promo_rate_pct, "erste_limit": erste.limit_pln, "erste_std": erste.standard_rate_pct,
            "repeat_promo": False, "include_family": False,
            "gold_return": gold.expected_return_pct, "gold_vol": gold.volatility_pct,
            "gold_premium": gold.buy_cost_pct, "gold_discount": gold.sell_cost_pct,
            "fund_return": m.asset("fund").expected_return_pct, "fund_vol": m.asset("fund").volatility_pct,
            "etf_return": m.asset("etf").expected_return_pct, "etf_vol": m.asset("etf").volatility_pct,
            "fan_key": "etf", "chart_real": False,
        }

    def instruments(self, p: dict) -> List[Instrument]:
        m = self.market
        items = [Instrument("erste", "Erste — Konto Pro oszczędnościowe", "Konto", "brak (BFG)",
                            m.account("erste").with_changes(promo_rate_pct=p["erste_rate"],
                                                            limit_pln=p["erste_limit"],
                                                            standard_rate_pct=p["erste_std"]))]
        items += [Instrument("acc_" + a.key, a.label, "Konto", "brak (BFG)", a)
                  for a in m.accounts if a.key != "erste"]
        for bond in m.bonds:
            if bond.family_only and not p["include_family"]:
                continue
            risk = "Skarb Państwa" + (" · tylko 800+" if bond.family_only else "")
            items.append(Instrument("bond_" + bond.code, bond.label, "Obligacje", risk, bond))
        asset = {"gold": ("Złoto", "wysokie (cena złota)", p["gold_return"], p["gold_vol"], p["gold_premium"],
                          p["gold_discount"]),
                 "fund": ("Fundusz", "niskie", p["fund_return"], p["fund_vol"], None, None),
                 "etf": ("ETF", "wysokie (akcje)", p["etf_return"], p["etf_vol"], None, None)}
        for key, (group, risk, ret, vol, buy, sell) in asset.items():
            spec = m.asset(key).with_changes(expected_return_pct=ret, volatility_pct=vol)
            if buy is not None:
                spec = spec.with_changes(buy_cost_pct=buy, sell_cost_pct=sell)
            items.append(Instrument(key, spec.name, group, risk, spec))
        return items

    # --- symulacja ------------------------------------------------------------------------------------
    def evaluate(self, p: dict) -> AnalysisResult:
        horizon = int(p["horizon_years"]) * 12
        scenario_params = ScenarioParams(horizon, float(p["cpi_start"]), float(p["cpi_long"]), int(p["cpi_months"]),
                                         self.market.reference_rate.rate_pct, float(p["ref_end"]),
                                         int(p["ref_months"]))
        scenario = self.scenarios.build(scenario_params)
        weights = np.ones(horizon + 1)
        weights[0] = 0.0                                        # w tym miesiącu wpłata już jest w historii
        if p["index_contributions"]:
            weights[1:] *= scenario.price_index[1:]
        capital = np.zeros(horizon + 1)
        capital[0] = 1.0
        target = float(p["target"]) * (scenario.price_index if self.today_mode(p) else np.ones(horizon + 1))
        amounts = {"min": self.settings.contribution_min, "max": self.settings.contribution_max,
                   "chosen": float(p["contribution"])}

        instruments = self.instruments(p)
        rows, curves = [], {}
        for instrument in instruments:
            row, curve = self._evaluate_one(instrument, scenario, scenario_params, weights, capital, target,
                                            amounts, float(p["start_capital"]), p)
            rows.append(row)
            curves[instrument.key] = curve
        offers = [r for r in rows if r["_group"] == "Konto"]
        best = min((r for r in offers if not r["_key"].startswith(("erste", "acc_erste"))),
                   key=lambda r: (r["_sort"], -r["_final"]))
        curves["best_bank"] = curves[best["_key"]]
        ranking = [r for r in rows if r["_group"] != "Konto" or r["_key"] in ("erste", best["_key"])]
        for r in ranking:
            if r["_key"] == best["_key"]:
                r["Instrument"] = "Najlepszy bank: " + r["Instrument"]
        ranking.sort(key=lambda r: (r["_sort"], -r["_final"]))
        for place, r in enumerate(ranking, 1):
            r["#"] = place
        offers.sort(key=lambda r: (r["_sort"], -r["_final"]))
        fastest = ranking[0]
        return AnalysisResult(
            ranking=[self._public(r) for r in ranking], offers=[self._public(r) for r in offers],
            chart=self._chart_rows(curves, scenario, target, bool(p["chart_real"]), best["Instrument"]),
            chart_series=self._series_names(curves, best["Instrument"]),
            fan=self._fan_rows(p, instruments, scenario, scenario_params, weights, capital, target),
            cpi=self._cpi_rows(scenario), fastest_label=fastest["Instrument"],
            fastest_months=fastest["_sort"], fastest_date=fastest["Cel osiągnięty (wybrana wpłata)"],
            kpis=self._kpis(scenario, p), notes=self._notes(p),
            target_view=self._target_view(ranking, scenario, target, p))

    def _evaluate_one(self, instrument, scenario, scenario_params, weights, capital, target, amounts, start, p):
        nets, months = {}, {}
        for name, amount in amounts.items():
            curve = self._curve(instrument, scenario, scenario_params, weights, capital, start, amount, p, 0)
            nets[name] = curve.net
            months[name] = self.months_to(curve.net, target)
        chosen = nets["chosen"]
        horizon = scenario.months
        row = {"_key": instrument.key, "_group": instrument.group, "_sort": months["chosen"] or 10 ** 6,
               "_final": float(chosen[-1]), "#": 0, "Instrument": instrument.label, "Grupa": instrument.group,
               "Ryzyko": instrument.risk,
               "Czas przy %d zł" % amounts["min"]: self.duration(months["min"]),
               "Czas przy %d zł" % amounts["max"]: self.duration(months["max"]),
               "Czas (wybrana wpłata)": self.duration(months["chosen"]),
               "Cel osiągnięty (wybrana wpłata)": self.month_label(months["chosen"]),
               "Cel w tym dniu [zł]": self._target_at(target, months["chosen"]),
               "Cel w dzisiejszych zł [zł]": self._target_at(target / scenario.price_index, months["chosen"]),
               "Szansa w horyzoncie": "—", "Zakres p10–p90": "—",
               "Wartość netto za %d l. [zł]" % (horizon // 12): round(float(chosen[-1])),
               "W dzisiejszych zł [zł]": round(float(chosen[-1] / scenario.price_index[-1]))}
        if instrument.is_market and int(self.settings.mc_paths) > 0:
            mc = self._curve(instrument, scenario, scenario_params, weights, capital, start, amounts["chosen"], p,
                             self.settings.mc_paths)
            hits = self.months_to_paths(mc.net, target)
            reached = np.isfinite(hits)
            row["Szansa w horyzoncie"] = "%.0f%%" % (100 * reached.mean())
            if reached.any():
                p10, p50, p90 = np.percentile(np.where(reached, hits, 10 ** 6), [10, 50, 90])
                row["Zakres p10–p90"] = "%s – %s" % (self.duration(p10), self.duration(p90))
                row["Czas (wybrana wpłata)"] += " (mediana %s)" % self.duration(p50)
        return row, chosen

    def _curve(self, instrument, scenario, scenario_params, weights, capital, start, amount, p, paths) -> ValueCurve:
        if not self.simulators.is_linear(instrument):
            cash = start * capital + amount * weights
            return self.simulators.run(instrument, scenario, cash, repeat_promo=bool(p["repeat_promo"]))
        key = (instrument.key, instrument.spec, scenario_params, bool(p["index_contributions"]), paths)
        if key not in self._unit_curves:
            seed = self.settings.seed if paths else None
            self._unit_curves[key] = (self.simulators.run(instrument, scenario, capital, paths=paths, seed=seed),
                                      self.simulators.run(instrument, scenario, weights, paths=paths, seed=seed))
            if len(self._unit_curves) > 400:
                self._unit_curves.pop(next(iter(self._unit_curves)))
        unit_capital, unit_contribution = self._unit_curves[key]
        return unit_capital.scaled_sum(unit_contribution, start, amount)

    # --- czas do celu ---------------------------------------------------------------------------------
    @staticmethod
    def months_to(net: np.ndarray, target: np.ndarray) -> Optional[int]:
        hit = np.nonzero(net >= target)[0]
        return int(hit[0]) if len(hit) else None

    @staticmethod
    def months_to_paths(net: np.ndarray, target: np.ndarray) -> np.ndarray:
        reached = net >= target[None, :]
        first = reached.argmax(axis=1).astype(float)
        first[~reached.any(axis=1)] = np.inf
        return first

    @staticmethod
    def duration(months) -> str:
        if months is None or not np.isfinite(months) or months >= 10 ** 6:
            return "nie w horyzoncie"
        months = int(round(months))
        return "%d l. %d m." % divmod(months, 12)

    def month_label(self, months) -> str:
        if months is None:
            return "—"
        index = self.today.year * 12 + self.today.month - 1 + int(months)
        return "%04d-%02d" % (index // 12, index % 12 + 1)

    # --- cel: wartość dzisiejsza / przyszła ----------------------------------------------------------
    @classmethod
    def today_mode(cls, p: dict) -> bool:
        """True, gdy cel jest w dzisiejszych zł (siła nabywcza); False — nominalne zł w dniu uzbierania."""
        mode = p.get("target_mode", "future")
        if mode not in cls.TARGET_MODES:
            raise ValueError("target_mode: 'future' albo 'today', jest %r" % (mode,))
        return mode == "today"

    @staticmethod
    def _target_at(values: np.ndarray, months):
        return "—" if months is None else round(float(values[int(months)]))

    def _target_view(self, ranking, scenario, target, p) -> dict:
        """Cel przeliczony na obie miary w dniu uzbierania najszybszą i najwolniejszą drogą z rankingu."""
        reached = [r for r in ranking if r["_sort"] < 10 ** 6]
        slowest = max(reached, key=lambda r: (r["_sort"], r["_final"])) if reached else None
        return {"today_mode": self.today_mode(p), "target": self.pln(p["target"]),
                "missing": len(ranking) - len(reached),
                "fastest": self._target_point(reached[0] if reached else None, scenario, target),
                "slowest": self._target_point(slowest, scenario, target)}

    def _target_point(self, row, scenario, target) -> dict:
        if row is None:
            return {"instrument": "żaden instrument w horyzoncie", "date": "—", "duration": "nie w horyzoncie",
                    "nominal": "—", "today": "—", "prices": "—"}
        t = int(row["_sort"])
        price = float(scenario.price_index[t])
        nominal = float(target[t])
        return {"instrument": row["Instrument"], "date": self.month_label(t), "duration": self.duration(t),
                "nominal": "%s zł" % self.pln(nominal), "today": "%s zł" % self.pln(nominal / price),
                "prices": "%+.1f%%" % ((price - 1.0) * 100)}

    # --- dane do wykresów -----------------------------------------------------------------------------
    def _series_names(self, curves, best_label) -> List[str]:
        names = [self._series_label(k, best_label) for k in self.CHART_KEYS if k in curves]
        return names + ["Cel"]

    def _series_label(self, key, best_label) -> str:
        if key == "best_bank":
            return best_label.replace("Najlepszy bank: ", "Najlepszy bank (") + ")"
        labels = {"erste": "Erste Konto Pro", "gold": "Złoto", "fund": "Fundusz obligacji", "etf": "ETF akcyjny"}
        return labels.get(key, key.replace("bond_", "Obligacje "))

    def _chart_rows(self, curves, scenario, target, real, best_label) -> List[dict]:
        deflator = scenario.price_index if real else np.ones(len(target))
        step = 1 if scenario.months <= 180 else 2
        rows = []
        for t in range(0, scenario.months + 1, step):
            row = {"Miesiąc": self.month_label(t)}
            for key in self.CHART_KEYS:
                if key in curves:
                    row[self._series_label(key, best_label)] = round(float(curves[key][t] / deflator[t]))
            row["Cel"] = round(float(target[t] / deflator[t]))
            rows.append(row)
        return rows

    def _fan_rows(self, p, instruments, scenario, scenario_params, weights, capital, target) -> List[dict]:
        instrument = next((i for i in instruments if i.key == p["fan_key"]), None)
        if instrument is None or self.settings.mc_paths <= 0:
            return []
        mc = self._curve(instrument, scenario, scenario_params, weights, capital, float(p["start_capital"]),
                         float(p["contribution"]), p, self.settings.mc_paths).net
        bands = np.percentile(mc, [10, 50, 90], axis=0)
        step = 1 if scenario.months <= 180 else 2
        return [{"Miesiąc": self.month_label(t), "p10 (pesymistycznie)": round(float(bands[0, t])),
                 "mediana": round(float(bands[1, t])), "p90 (optymistycznie)": round(float(bands[2, t])),
                 "Cel": round(float(target[t]))} for t in range(0, scenario.months + 1, step)]

    def _cpi_rows(self, scenario) -> List[dict]:
        rows = [{"Miesiąc": r.label, "Inflacja GUS [%]": r.yoy_pct, "Założenie [%]": None}
                for r in self.market.inflation.readings[-120:]]
        for t in range(-1, min(scenario.months, 120) + 1):
            rows.append({"Miesiąc": self.month_label(t), "Inflacja GUS [%]": None,
                         "Założenie [%]": round(scenario.cpi_at(t), 2)})
        return rows

    def _kpis(self, scenario, p) -> Dict[str, str]:
        m = self.market
        cpi = m.inflation.latest
        return {"cpi": "%.1f%%" % cpi.yoy_pct, "cpi_label": "GUS, %s r/r" % cpi.label,
                "cpi10": "%.1f%%" % m.inflation.average_yoy(10),
                "ref": "%.2f%%" % m.reference_rate.rate_pct, "ref_label": "od %s" % m.reference_rate.valid_from,
                "gold": "%s zł" % self.pln(m.gold_history.latest_per_ounce),
                "gold_label": "NBP %s, za uncję" % m.gold_history.days[-1],
                "start": "%s zł" % self.pln(p["start_capital"]),
                "prices": "×%.2f" % scenario.price_index[-1]}

    def _notes(self, p) -> List[str]:
        notes = ["Wartość w danym miesiącu = kwota na rękę po zamknięciu wszystkiego: wykup obligacji z opłatą "
                 "i Belką, sprzedaż złota w skupie, umorzenie funduszu z Belką od zysku."]
        if self.today_mode(p):
            notes.append("Cel w dzisiejszych zł: %s zł to siła nabywcza na dziś, więc nominalnie cel rośnie razem "
                         "z założoną inflacją — w dniu uzbierania trzeba mieć odpowiednio więcej." % self.pln(p["target"]))
        else:
            notes.append("Cel jako wartość przyszła: %s zł nominalnie w dniu uzbierania — w dzisiejszych pieniądzach "
                         "to mniej, tym mniej, im później cel padnie." % self.pln(p["target"]))
        if not p["repeat_promo"]:
            notes.append("Promocje kont kończą się po swoim okresie; potem stawka standardowa. Włącz „powtarzaj "
                         "promocje”, jeśli zamierzasz przenosić pieniądze do kolejnych promocji.")
        return notes

    @staticmethod
    def _public(row: dict) -> dict:
        return {k: v for k, v in row.items() if not k.startswith("_")}

    @staticmethod
    def pln(value) -> str:
        return "{:,.0f}".format(float(value)).replace(",", " ")

    # --- konsola --------------------------------------------------------------------------------------
    def print_baseline(self) -> None:
        result = self.evaluate(self.defaults())
        s = self.settings
        print("\nKIEDY %s ZŁ? Start %s zł (historia wpłat), wpłaty %d–%d zł/mies., parametry na %s"
              % (self.pln(s.target_pln), self.pln(self.history.total), s.contribution_min, s.contribution_max,
                 self.today.isoformat()))
        print("%-58s %16s %16s" % ("Instrument", "przy %d zł" % s.contribution_min, "przy %d zł" % s.contribution_max))
        for row in result.ranking:
            print("%-58s %16s %16s" % (row["Instrument"][:58], row["Czas przy %d zł" % s.contribution_min],
                                       row["Czas przy %d zł" % s.contribution_max]))
        print("Najszybciej: %s — %s (wpłata %d zł)" % (result.fastest_label, result.fastest_date,
                                                       self.defaults()["contribution"]))
        for name, label in (("fastest", "najszybciej"), ("slowest", "najwolniej")):
            point = result.target_view[name]
            print("Cel %s (%s): %s nominalnie = %s w dzisiejszych zł" % (label, point["date"], point["nominal"],
                                                                         point["today"]))
        print(flush=True)
