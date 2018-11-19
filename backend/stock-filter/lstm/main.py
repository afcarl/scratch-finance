from keras.models import load_model

import client
import pandas as pd
import numpy as np
import display

model = load_model('model')

df = pd.read_csv('./equities.csv', index_col='symbol')
for index, item in df.iterrows():
    symbol = item.name
    if item.psei:
        equity = client.get_last(symbol)

        #normalize
        norm_equity = equity.drop(['date','volume'], axis=1)
        min_equity = norm_equity['low'].min()
        max_equity = norm_equity['high'].max()
        norm_equity = (norm_equity - min_equity) / (max_equity - min_equity)
        norm_equity = norm_equity.reset_index(drop=True)

        norm_volume = equity.drop(['date','open', 'high', 'low', 'close'], axis=1)
        min_volume = norm_volume['volume'].min()
        max_volume = norm_volume['volume'].max()
        norm_volume = (norm_volume - min_volume) / (max_volume - min_volume)
        norm_volume = norm_volume.reset_index(drop=True)

        norm_sample = norm_equity.join(norm_volume)

        sample = norm_sample.values

        if sample.shape[0] > 0:
            sample = sample.reshape(1, 10, 5)
            predicted = model.predict(sample)
            predicted = np.reshape(predicted, (predicted.size,))
            predicted = predicted[0]
            predicted = predicted * 100

            display.plot(symbol, norm_equity, norm_volume)
            print(symbol, '%.2f' % predicted)

print('Done.')
