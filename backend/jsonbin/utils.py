import requests
import pandas as pd
import os
from common import client
from common import indicators

def put_json(json):
    url = 'https://api.jsonbin.io/b/5badfc4d8713b17b52b0b603'
    key = os.environ['JSONBIN_KEY']
    headers = {'secret-key': key}
    response = requests.put(url, json=json, headers=headers).json()
    return response

def create_json(df):
    json = [dict([(colname, row[i]) for i, colname in enumerate(df.columns)])
        for row in df.values ]
    return json

def plot(df):
    # plot
    plt.figure(figsize=(5,2))
    df.norm_ema_rsi.plot(legend=True, title=df.symbol)
    df.smoothed_close.plot(legend=True)
    plt.axhline(y=0, color='black', linestyle='--', alpha=0.2)
    plt.annotate('%0.2f' % df.norm_ema_rsi.tail(1),
        xy=(1, df.norm_ema_rsi.tail(1)),
        xytext=(8, 0),
        xycoords=('axes fraction', 'data'),
        textcoords='offset points')
    plt.ylim([-100,100])
    plt.show()

def initialize(path):
    df = pd.read_csv(path, index_col='symbol')
    df['strength_index'] = pd.Series()
    df['price'] = pd.Series()
    df['norm_close'] = pd.Series()
    return df

def populate(df):
    for index, item in df.iterrows():
        # only do the PSEi for now_ts
        if(not item.psei):
            continue

        # retrieve history
        symbol = item.name
        item = client.get_history(symbol, days=400)

        # calculate the indicators
        item = indicators.relative_strength_index(item, n=14)
        item = indicators.ema(item, "rsi", n=30)

        # normalize and smoothen
        item['norm_ema_rsi'] = (item['ema_rsi'] - 0.5) * 200
        item['norm_close'] = ((item['close'] - item['close'].min()) /
            (item['close'].max() - item['close'].min())) * 100
        item['smoothed_close'] = item['norm_close'].rolling(
            window=5,
            win_type='gaussian',
            center=True).mean(std=3).shift(2)

        # remove all NA -- cleanup
        # not really neccessary...
        # item = item.dropna()
        # just take last 200 rows
        # item = item.tail(200)
        # item.reset_index(drop=True, inplace=True)

        # add to df dataframe
        if item.shape[0] > 0:
            df.loc[symbol,'strength_index'] = item['norm_ema_rsi'].tail(1).values
            df.loc[symbol,'price'] = item['close'].tail(1).values
            df.loc[symbol,'norm_close'] = item['norm_close'].tail(1).values

    df.reset_index(inplace=True)
    df = df.dropna()
    return df
