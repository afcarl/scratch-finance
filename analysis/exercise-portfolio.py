# %%
import pandas as pd
import quandl as qd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
start = pd.to_datetime('2012-01-01')
end   = pd.to_datetime('2017-01-01')

aapl  = qd.get('WIKI/AAPL', start_date=start, end_date=end)
cisco = qd.get('WIKI/CSCO.11',start_date=start, end_date=end)
ibm   = qd.get('WIKI/IBM.11' ,start_date=start, end_date=end)
amzn  = qd.get('WIKI/AMZN.11',start_date=start, end_date=end)

# %%

def bma_6(x):
    return ((x[5] + (5*x[4]) + (10*x[3]) + (10*x[2]) + (5*x[1]) + x[0]) / 32)

aapl['Binomial MA 6'] = aapl['Adj. Close'].rolling(6).apply(bma_6)

def bma_5(x):
    return ((x[4] + (4*x[3]) + (6*x[2]) + (4*x[1]) + x[0]) / 16)

aapl['Binomial MA 5'] = aapl['Adj. Close'].rolling(5).apply(bma_5)

def bma_4(x):
    return ((x[3] + (2*x[2]) + (2*x[1]) + x[0]) / 6)

aapl['Binomial MA 4'] = aapl['Adj. Close'].rolling(4).apply(bma_4)


# def hp(x):
#     alpha = 0.2
#     return ( (1 - ((alpha/2)**2)) * x[] )
# %%
# TEMA = 3 * EMA - 3 * EMA(EMA) + EMA(EMA(EMA))
# def tema(ema):
#     ema = pd.Series(ema)
#     ema1 = ema.ewm(span=5, min_periods=5).mean()
#     ema2 = ema1.ewm(span=5, min_periods=5).mean()
#     ema = ema.values
#     ema1 = ema1.values
#     ema2 = ema2.values
#     return pd.Series( ema[12] - (3 * ema1[12]) + ema2[12] )
#
# aapl['TEMA'] = aapl['Adj. Close'].rolling(13).apply(tema)

# %%
aapl['EWMA Short'] = aapl['Adj. Close'].ewm(span=5, min_periods=5).mean()
aapl['EWMA Long'] = aapl['Adj. Close'].ewm(span=30, min_periods=30).mean()
aapl['Standard MA'] = aapl['Adj. Close'].rolling(5).mean()

# %%
aapl[['Adj. Close', 'EWMA Short', 'Binomial MA 6', 'Binomial MA 5' ]].plot(figsize=(18,9),xlim=['2014-11-01', '2014-12-28'],ylim=[100,115])
plt.show()


# %%
for stock_df in (aapl,cisco,ibm,amzn):
    stock_df['Normalized Return'] = stock_df['Adj. Close'] / stock_df.iloc[0]['Adj. Close']

# %%
print(aapl.head())

# %%
# 30% aapl, 20% cisco, 40% ibm, 10% amznS
# multiplying by allocation
for stock_df, alloc in zip((aapl,cisco,ibm,amzn),[.3,.2,.4,.1]):
    stock_df['Allocation'] = stock_df['Normalized Return'] * alloc

# %%
total_investment = 1000000
for stock_df in (aapl,cisco,ibm,amzn):
    stock_df['Position Values'] = stock_df['Allocation'] * total_investment

# %%
all_pos_vals = [aapl['Position Values'], cisco['Position Values'], ibm['Position Values'], amzn['Position Values']]
portfolio_val = pd.concat(all_pos_vals, axis=1)
portfolio_val.columns = ['AAPL', 'CISCO', 'IBM', 'AMZN']
portfolio_val['Total Position'] = portfolio_val.sum(axis=1)
# %%
portfolio_val['Total Position'].plot(figsize=(10,8))
plt.show()

# %%
portfolio_val.drop('Total Position', axis=1).plot(figsize=(10,8))
plt.show()

# %%
portfolio_val['Daily Return'] = portfolio_val['Total Position'].pct_change(1)
portfolio_val['Daily Return'].plot(kind='kde')
plt.show()

# %%
cummulative_return = 100 * (portfolio_val['Total Position'][-1]/portfolio_val['Total Position'][0]-1)

# %%
# Sharpe Ratio
daily_return_mean = portfolio_val['Daily Return'].mean()
daily_return_std =  portfolio_val['Daily Return'].std()
sr = daily_return_mean / daily_return_std

# %%
# Annualize the Sharpe Ratio
business_days = 252
asr = (business_days**0.5) * sr
asr
