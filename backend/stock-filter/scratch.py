import client
import indicators
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt

# retrieve history
symbol = "AC"
df = client.get_history(symbol, days=800)
df
# %%
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
date_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
# %%
dd = indicators.ema(df, "close", "ema_close", n=200)
dd = dd[date_ago:]

fw_low = dd[date_ago:]['close'].min()
fw_high = dd[date_ago:]['close'].max()

# normalize
dd


# %%
dd[['close','ema_close']].plot()
plt.show()
