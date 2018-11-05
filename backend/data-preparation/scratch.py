import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from common import client

df = client.get_history("ALI", days=999)
window = 10
future = 30
x, y = [], []
i = window
while i + 1 <= df.shape[0] - future:
    dd = df.drop(['date','volume'], axis=1)
    current_mean = dd.iloc[i,].mean()
    fu = dd.iloc[i:i+future]
    max = fu['high'].max()
    pct_to_max = (max - current_mean) / current_mean
    y.append(pct_to_max)

    # the number of windows will be as follows
    # let w = number of windows, n = total length, and m = window size
    # w = n - (m - 1)
    norm_equity = df.drop(['date','volume'], axis=1)
    norm_equity = norm_equity.iloc[i-window:i]
    min_equity = norm_equity['low'].min()
    max_equity = norm_equity['high'].max()
    norm_equity = (norm_equity - min_equity) / (max_equity - min_equity)
    norm_equity = norm_equity.reset_index(drop=True)

    norm_volume = df.drop(['date','open', 'high', 'low', 'close'], axis=1)
    norm_volume = norm_volume.iloc[i-window:i]
    min_volume = norm_volume['volume'].min()
    max_volume = norm_volume['volume'].max()
    norm_volume = (norm_volume - min_volume) / (max_volume - min_volume)
    norm_volume = norm_volume.reset_index(drop=True)

    norm_sample = norm_equity.join(norm_volume)
    x.append(norm_sample.values)
    i = i + 1

# convert samples to ndarray
x = np.array(x)
y = np.array(y)

# next step:
# return tuple x, y - OK
# return tuple x_train, y_train, x_test, y_test using scikit learn
