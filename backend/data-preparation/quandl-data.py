# %%
import pandas as pd
import quandl as qd
import os
import numpy as np
import matplotlib.pyplot as plt

# %%
qd.ApiConfig.api_key = os.environ['QUANDL_KEY']

# %%
start = pd.to_datetime('2008-01-01')
end   = pd.to_datetime('2018-01-01')

# %%
with open('nasdaq-100.txt', 'r') as f:
    stocks = f.read().splitlines()

# %%
window = 10
future = 10
x, y = [], []

# %%
for stock in stocks:
    try:
        df = qd.get('WIKI/'+stock, start_date=start, end_date=end)
        print(stock)
        df = df.drop(['Open', 'High', 'Low', 'Close', 'Volume', 'Ex-Dividend', 'Split Ratio'], axis=1)
        i = window
        while i + 1 <= df.shape[0] - future:
            dd = df.drop(['Adj. Volume'], axis=1)
            current_mean = dd.iloc[i,].mean()
            fu = dd.iloc[i:i+future]
            max = fu['Adj. High'].max()
            pct_to_max = (max - current_mean) / current_mean
            y.append(pct_to_max)

            # the number of windows will be as follows
            # let w = number of windows, n = total length, and m = window size
            # w = n - (m - 1)
            norm_equity = df.drop(['Adj. Volume'], axis=1)
            norm_equity = norm_equity.iloc[i-window:i]
            min_equity = norm_equity['Adj. Low'].min()
            max_equity = norm_equity['Adj. High'].max()
            norm_equity = (norm_equity - min_equity) / (max_equity - min_equity)
            norm_equity = norm_equity.reset_index(drop=True)

            norm_volume = df.drop(['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close'], axis=1)
            norm_volume = norm_volume.iloc[i-window:i]
            min_volume = norm_volume['Adj. Volume'].min()
            max_volume = norm_volume['Adj. Volume'].max()
            norm_volume = (norm_volume - min_volume) / (max_volume - min_volume)
            norm_volume = norm_volume.reset_index(drop=True)

            norm_sample = norm_equity.join(norm_volume)
            x.append(norm_sample.values)
            i = i + 1
    except Exception as e:
        print(e)

# convert samples to ndarray
x = np.array(x)
y = np.array(y)

# %%
dg = pd.DataFrame(y)
dw = dg[np.abs(dg-dg.mean()) <= (1*dg.std())]
dw.hist(alpha=0.4,bins=200)
plt.show()
