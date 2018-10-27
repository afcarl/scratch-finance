import pandas as pd
import numpy as np
import generic_utils as utils
import matplotlib.pyplot as plt

df = utils.get_dataframe("CSCO")
close_norm = utils.normalize(df['Adj. Close'].values)

# %%
max = 1260
profit_overall = np.zeros(max)
profit_average = np.zeros(max)
percentage_win = np.zeros(max)
percentage_loss = np.zeros(max)
trades = np.zeros(max)

for idx in np.arange(1, max):
    (highs, lows) = utils.get_peaks_and_troughs(close_norm, idx)
    (average_profit, overall_profit, trades_total, trades_win, trades_lose) = utils.evaluate(close_norm, utils.convert_index_to_signals(len(close_norm), highs, lows))
    profit_average[idx] = average_profit
    profit_overall[idx] = overall_profit
    percentage_win[idx] = (trades_win/trades_total) * 100
    percentage_loss[idx] = (trades_lose/trades_total) * 100
    trades[idx] = trades_total
# %%
percentage_win[7]

# %%
limit_lower = 300
limit_higher = 350
fig = plt.figure(figsize=(10, 10))
fig.subplots_adjust(hspace=0.4, wspace=0.4)
ax1 = fig.add_subplot(4, 1, 1, xlim=(limit_lower, limit_higher))
plt.title('Average Profit')
ax1.plot(profit_average)
ax2 = fig.add_subplot(4, 1, 2, xlim=(limit_lower, limit_higher))
ax2.plot(profit_overall)
plt.title('Overall Profit')
ax3 = fig.add_subplot(4, 1, 3, xlim=(limit_lower, limit_higher))
ax3.plot(trades)
plt.title('Total Trades')
ax4 = fig.add_subplot(4, 1, 4, xlim=(limit_lower, limit_higher))
ax4.plot(percentage_win)
plt.title('Percentage Win')
plt.show()
# print(average_profit)
# print((trades_win/trades_total)*100)
# utils.create_graph(close_norm, highs, lows)

# %%
(highs, lows) = utils.get_peaks_and_troughs(close_norm, 40)
(average_profit, overall_profit, trades_total, trades_win, trades_lose) = utils.evaluate(close_norm, utils.convert_index_to_signals(len(close_norm), highs, lows))

fig = plt.figure(figsize=(10, 10))
fig.subplots_adjust(hspace=0.4, wspace=0.4)
ax1 = fig.add_subplot(4, 1, 1)
plt.title('Average Profit')
