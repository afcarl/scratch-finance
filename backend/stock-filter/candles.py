import client
import pandas as pd
import numpy as np
import display as d

df = pd.read_csv('./equities.csv', index_col='symbol')
for index, item in df.iterrows():
    symbol = item.name
    equity = client.get_last(symbol)
    #normalize
    norm_equity = equity.drop(['date','volume'], axis=1)
    min_equity = norm_equity['low'].min()
    max_equity = norm_equity['high'].max()
    norm_equity = (norm_equity - min_equity) / (max_equity - min_equity)

    norm_volume = equity.drop(['date','open', 'high', 'low', 'close'], axis=1)
    min_volume = norm_volume['volume'].min()
    max_volume = norm_volume['volume'].max()
    norm_volume = (norm_volume - min_volume) / (max_volume - min_volume)

    d.plot(symbol, norm_equity, norm_volume)
    
print("Done.")
