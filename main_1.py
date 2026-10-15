from AnalysisSettings import AnalysisSettings
from NbpRateClient import NbpRateClient
from ScenarioBuilder import ScenarioBuilder
from TaxRules import TaxRules
from InputFileLocator import InputFileLocator
from SavingsAccountSimulator import SavingsAccountSimulator
from TreasuryBondSimulator import TreasuryBondSimulator
from MarketAssetSimulator import MarketAssetSimulator
from SavingsHistoryLoader import SavingsHistoryLoader
from GusInflationClient import GusInflationClient
from NbpGoldClient import NbpGoldClient
from InstrumentSimulators import InstrumentSimulators
from TodayMarketBuilder import TodayMarketBuilder
from SavingsAnalyzer import SavingsAnalyzer
from SavingsSimulatorPage import SavingsSimulatorPage

def main():
	settings = AnalysisSettings()
	reference_rate = NbpRateClient()
	scenarios = ScenarioBuilder()
	tax = TaxRules()

	data_1 = settings.settings()
	data_2 = reference_rate.reference_rate()
	data_3 = scenarios.scenarios()
	data_4 = tax.tax()
	locator = InputFileLocator(data_1)
	data_5 = locator.locator()
	account_sim = SavingsAccountSimulator(data_4)
	data_6 = account_sim.account_sim()
	bond_sim = TreasuryBondSimulator(data_4)
	data_7 = bond_sim.bond_sim()
	asset_sim = MarketAssetSimulator(data_4)
	data_8 = asset_sim.asset_sim()
	history = SavingsHistoryLoader(data_5, data_1)
	data_9 = history.history()
	inflation = GusInflationClient(data_1, data_5)
	data_10 = inflation.inflation()
	gold_history = NbpGoldClient(data_5)
	data_11 = gold_history.gold_history()
	simulators = InstrumentSimulators(data_6, data_7, data_8)
	data_12 = simulators.simulators()
	market = TodayMarketBuilder(data_2, data_10, data_11)
	data_13 = market.market()
	analyzer = SavingsAnalyzer(data_1, data_9, data_13, data_3, data_12)
	data_14 = analyzer.analyzer()
	page = SavingsSimulatorPage(data_14)
	page.show()
	pass

if __name__ == "__main__":
	main()
