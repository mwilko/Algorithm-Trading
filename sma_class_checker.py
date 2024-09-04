from sma_backtest import SMABacktester

tester = SMABacktester("AAPL", 50, 200, "2010-1-1", "2020-1-1")
tester.test_strategy()
tester.plot_results()
