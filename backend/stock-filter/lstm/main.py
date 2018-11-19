from keras.models import load_model

import client
import pandas as pd
import numpy as np
import display

print('Loading...')
model = load_model('model')

print('Reading file...')
df = pd.read_csv('./equities.csv', index_col='symbol')

print('Iterating...')
for index, item in df.iterrows():
    symbol = item.name

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
    # drop those that dont have proper shape
    if sample.shape[0] > 0 and sample.shape[0] == 10:
        sample = sample.reshape(1, 10, 5)
        predicted = model.predict(sample)
        predicted = np.reshape(predicted, (predicted.size,))
        predicted = predicted[0] # get the prediction
        predicted = predicted * 100 # turn it to percentage

        print(symbol, '%.2f' % predicted, 'PSEi' if item.psei else 'not PSEi')
        display.plot(symbol, norm_equity, norm_volume)
# TODO TEST THE VERACITY OF THE MODEL!!!
print('Done.')
