import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


class SMABacktester():
    def __init__(self, symbol, SMA_S, SMA_L, start, end):
        self.symbol = symbol
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.start = start
        self.end = end
        self.results = None
        self.get_data()

    def get_data(self):
        raw = yf.download(self.symbol, start=self.start, end=self.end)
        data = raw.Close.to_frame()
        data['returns'] = np.log(data['Close'] / data['Close'].shift(1))
        data['SMA_S'] = data['Close'].rolling(self.SMA_S).mean()
        data['SMA_L'] = data['Close'].rolling(self.SMA_L).mean()
        data.dropna(inplace=True)
        self.data = data

    def test_strategy(self):
        data = self.data.copy().dropna()
        data['position'] = np.where(data['SMA_S'] > data['SMA_L'], 1, -1)
        data['strategy'] = data['position'].shift(1) * data['returns']
        data.dropna(inplace=True)

        data['returnsbh'] = data['returns'].cumsum().apply(np.exp)
        data['returnstrategy'] = data['strategy'].cumsum().apply(np.exp)
        perf = data['returnstrategy'].iloc[-1]
        outperf = perf - data['returnstrategy'].iloc[-1]
        self.results = data

        ret = np.exp(data[['returns', 'strategy']].sum())
        std = data[['returns', 'strategy']].std() * np.sqrt(252)

        return round(perf, 6), round(outperf, 6)

    def plot_results(self):
        if self.results is None:
            print('No results to plot')
        else:
            title = f'{self.symbol} | SMA_S = {self.SMA_S} | SMA_L = {self.SMA_L}'
            self.results[['returnsbh', 'returnstrategy']].plot(
                title=title, figsize=(12, 8))
            plt.show()
