from typing import Optional

import numpy as np

from Instrument import Instrument
from MarketAssetSimulator import MarketAssetSimulator
from SavingsAccountSimulator import SavingsAccountSimulator
from Scenario import Scenario
from TreasuryBondSimulator import TreasuryBondSimulator
from ValueCurve import ValueCurve


class InstrumentSimulators:
    """Kieruje instrument do właściwego symulatora: konto, obligacje albo instrument rynkowy."""

    def __init__(self, account_sim: SavingsAccountSimulator, bond_sim: TreasuryBondSimulator,
                 asset_sim: MarketAssetSimulator):
        self.account_sim = account_sim
        self.bond_sim = bond_sim
        self.asset_sim = asset_sim

    def simulators(self) -> "InstrumentSimulators":
        return self

    def run(self, instrument: Instrument, scenario: Scenario, cash: np.ndarray, repeat_promo: bool = False,
            paths: int = 0, seed: Optional[int] = None) -> ValueCurve:
        if instrument.is_account:
            return self.account_sim.simulate(instrument.spec, scenario, cash, repeat_promo)
        if instrument.is_market:
            rng = np.random.default_rng(seed) if seed is not None and paths > 0 else None
            return self.asset_sim.simulate(instrument.spec, scenario, cash, paths, rng)
        return self.bond_sim.simulate(instrument.spec, scenario, cash)

    @staticmethod
    def is_linear(instrument: Instrument) -> bool:
        """Obligacje i instrumenty rynkowe skalują się liniowo z wpłatami; konto nie (limit kwoty)."""
        return not instrument.is_account
