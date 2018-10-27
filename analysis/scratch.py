import pandas as pd
import quandl as qd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

aapl  = pd.read_csv('data/AAPL_OHLC', index_col='Date',parse_dates=True)
csco  = pd.read_csv('data/CSCO_OHLC', index_col='Date',parse_dates=True)
amzn  = pd.read_csv('data/AMZN_OHLC', index_col='Date',parse_dates=True)
ibm  = pd.read_csv('data/IBM_OHLC', index_col='Date',parse_dates=True)

# %%
# TR = max[(high-low), abs(high-close-prev), abs(low-clos-prev)]
def average_true_range(df):
    high_low = pd.Series(df['Adj. High'] - df['Adj. Low'])
    close_high = pd.Series(abs(df['Adj. Close'] - df['Adj. High']))
    close_low = pd.Series(abs(df['Adj. Close'] - df['Adj. Low']))
    atr = pd.concat([high_low, close_high, close_low], axis=1)
    df['TR'] = atr.max(axis=1)
    df['ATR'] = (df['TR'].shift(1)*13 + df['TR'])/14
    # Remove the outliers
    # q = df["ATR"].quantile(0.99)
    # df['ATR'] = df[df['ATR'] > q]
    # df['ATR'] = (df['ATR'] - df['ATR'].min()) / (df['ATR'].max() - df['ATR'].min())
    return df

aapl = average_true_range(aapl)
csco = average_true_range(csco)
ibm = average_true_range(ibm)
amzn = average_true_range(amzn)

aapl[['ATR','Adj. Close']].plot(alpha=0.2, x='ATR', y='Adj. Close', kind='scatter',figsize=(10,5))
# csco['ATR'].plot(figsize=(18,2), alpha=0.2)
# amzn['ATR'].plot(figsize=(18,2), alpha=0.2)
# ibm['ATR'].plot(figsize=(18,2), alpha=0.2)
plt.savefig('Outliers.png')
plt.show()

# daily['year'] = daily.index.year
# daily['day'] = daily.index.day
# daily['month'] = daily.index.month
#
# hey = daily.pivot(index='day', columns=['year,month'], values='Adj. Close', aggfunc=np.sum)







# proxy = 'http://sin2.sme.zscalertwo.net:80'
#
# os.environ['http_proxy'] = proxy
# os.environ['HTTP_PROXY'] = proxy
# os.environ['https_proxy'] = proxy
# os.environ['HTTPS_PROXY'] = proxy
