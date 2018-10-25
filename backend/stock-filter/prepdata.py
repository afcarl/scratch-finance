import client
import indicators
import pandas as pd

df = pd.read_csv('equities.csv', index_col='symbol')
df['price'] = pd.Series()
df['average_volatility'] = pd.Series()
df['average_volume'] = pd.Series()

for index, item in df.iterrows():
    symbol = item.name
    equity = client.get_history(symbol)
    equity = indicators.day_range_pct(equity)
    equity = indicators.ema(equity, 'volume', 'ema_volume')
    equity = equity.join(pd.Series(equity['ema_volume'] / 1000000, name="vol(M)"))
    equity = indicators.ema(equity, 'day_range_pct', 'ema_day_range_pct')
    if len(equity) > 0:
        df.loc[symbol,'price'] = equity['close'].tail(1).values
        df.loc[symbol,'average_volatility'] = equity['ema_day_range_pct'].tail(1).values
        df.loc[symbol,'average_volume'] = equity['vol(M)'].tail(1).values

df.to_pickle('./equities.pkl')
