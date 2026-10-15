from dataclasses import dataclass, replace


@dataclass(frozen=True)
class BondSpec:
    """Detaliczna obligacja skarbowa z bieżącej oferty MF (cena 100 zł).

    kind:
      monthly_ref        — odsetki co miesiąc, po 1. miesiącu stopa referencyjna NBP + marża (ROR, DOR)
      fixed_capitalized  — stała stopa, odsetki kapitalizowane co rok i wypłacane przy wykupie (OTS, TOS)
      cpi_yearly_coupon  — 1. rok stała, potem inflacja + marża, odsetki wypłacane co rok (COI)
      cpi_capitalized    — 1. rok stała, potem inflacja + marża, kapitalizacja roczna (EDO, ROS, ROD)
    """

    code: str
    name: str
    term_months: int
    first_rate_pct: float
    kind: str
    margin_pct: float
    early_fee_pln: float                 # za 1 obligację (100 zł); nie więcej niż naliczone odsetki
    family_only: bool = False            # ROS/ROD: tylko beneficjenci 800+

    @property
    def label(self) -> str:
        return "Obligacje %s (%s)" % (self.code, self.name)

    def with_changes(self, **changes) -> "BondSpec":
        return replace(self, **changes)
