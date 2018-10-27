import pandas as pd
import numpy as np
import scipy.signal as scipysig
import matplotlib.pyplot as plt
import seaborn as sns

def get_dataframe(symbol):
    return pd.read_csv('data/{}_OHLC'.format(symbol), index_col='Date',parse_dates=True)

def get_peaks_and_troughs(series, order=10):
    # get the extrema, then make the np.array to a list
    highs = scipysig.argrelextrema(data=series, comparator=np.greater,order=order)[0].tolist()
    lows = scipysig.argrelextrema(data=series, comparator=np.less,order=order)[0].tolist()
    return (highs, lows)

def convert_index_to_signals(length, highs, lows):
    # print('Peaks are %s' % (indexes[0]))
    buy_sell_signals = np.zeros(length)
    for idx in highs:
        buy_sell_signals[idx] = -1
    for idx in lows:
        buy_sell_signals[idx] = 1
    return buy_sell_signals.tolist()

def normalize(series):
    return (series - series[0])


def create_graph(series, highs, lows):
    plt.figure(figsize=(20, 4))
    plt.plot(np.arange(0,len(series)), series, markevery=highs, marker='X', label='points', c='gray', markersize=10, markerfacecolor='red', alpha=0.6)
    plt.plot(np.arange(0,len(series)), series, markevery=lows, marker='X', label='points', c='gray', markersize=10, markerfacecolor='green', alpha=0.6)

def evaluate(prices, signals):
    state_holding = False
    current_profit = 0
    overall_profit = 0
    buy_price = 0
    sell_price = 0
    average_profit = 0
    buy_fees = 0.00295
    sell_fees = 0.00795
    buy_idx = 0
    time_to_hold = 4
    trades_total = 0
    trades_win = 0
    trades_lose = 0
    for idx, signal in enumerate(signals):
        if signal == 1 and not state_holding:
            buy_price = prices[idx] - (prices[idx] * buy_fees)
            buy_idx = idx
            state_holding = True
        elif signal == -1 and state_holding and (time_to_hold < idx - buy_idx):
            sell_price = prices[idx] - (prices[idx] * sell_fees)
            current_profit = sell_price - buy_price
            overall_profit = overall_profit + current_profit
            trades_total = trades_total + 1
            average_profit = (average_profit + current_profit) / trades_total
            if(current_profit > 0):
                trades_win = trades_win + 1
            else:
                trades_lose = trades_lose + 1
            state_holding = False

            # prices_to_plot = prices[buy_idx:idx+1]
            # plt.plot(np.arange(0,len(prices_to_plot)), prices_to_plot, alpha=0.6)
    return average_profit, overall_profit, trades_total, trades_win, trades_lose

# length of the ema window
# ll = 30
#
# df['EMA Adj. Close']  = pd.Series(df['Adj. Close'].ewm(span=ll).mean(), name='EMA Close')
# length = len(df['EMA Adj. Close'].dropna().index)
# y = df['EMA Adj. Close'].dropna().values
# y1 = df['Adj. Close']
#
#
# df['Signal'] = pd.Series(buysellsignals, name='Signals', index=df.index)
# df['Signal'].plot(figsize=(18,6))
# y = shift(y, 1, cval=np.nan)
# y1 = df['Adj. Close'].values

# def normalize()
# df['Norm Adj. Close'] = (df['Adj. Close'] - df['Adj. Close'].min()) / (df['Adj. Close'].max() - df['Adj. Close'].min())(arg):
#     pass
