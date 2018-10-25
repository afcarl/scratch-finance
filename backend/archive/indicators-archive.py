from collections import namedtuple
import pandas as pd

def heiken_ashi(df):
    df['ha_close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    nt = namedtuple('nt', ['open','close'])
    previous_row = nt(df.loc[0,'open'],df.loc[0,'close'])
    i = 0
    for row in df.itertuples():
        ha_open = (previous_row.open + previous_row.close) / 2
        df.loc[i,'ha_open'] = ha_open
        previous_row = nt(ha_open, row.close)
        i += 1

    df['ha_high'] = df[['ha_open','ha_close','high']].max(axis=1)
    df['ha_low'] = df[['ha_open','ha_close','low']].min(axis=1)
    return df

def ema_volume(df, n=20):
    ema = pd.Series(df['volume'].ewm(span=n, min_periods=n).mean(), name='ema_volume')
    df = df.join(ema)
    return df

def ema_rsi(df, n=20):
    ema = pd.Series(df['rsi'].ewm(span=n, min_periods=n).mean(), name='ema_rsi')
    df = df.join(ema)
    return df

def ema_close(df, n=9):
    ema = pd.Series(df['close'].ewm(span=n, min_periods=n).mean(), name='ema_close').shift(-1)
    df = df.join(ema)
    return df

def relative_strength_index(df, n=14):
    i = 0
    UpI = [0]
    DoI = [0]
    while i + 1 <= df.index[-1]:
        UpMove = df.loc[i + 1, 'high'] - df.loc[i, 'high']
        DoMove = df.loc[i, 'low'] - df.loc[i + 1, 'low']
        if UpMove > DoMove and UpMove > 0:
            UpD = UpMove
        else:
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0:
            DoD = DoMove
        else:
            DoD = 0
        DoI.append(DoD)
        i = i + 1
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(UpI.ewm(span=n, min_periods=n).mean())
    NegDI = pd.Series(DoI.ewm(span=n, min_periods=n).mean())
    RSI = pd.Series(PosDI / (PosDI + NegDI), name='rsi')
    df = df.join(RSI)
    return df


def ac(df):
    median_price = pd.Series(df['high'] - df['low'])
    sma_5 = pd.Series(median_price.rolling(window=5, min_periods=5).mean())
    sma_34 = pd.Series(median_price.rolling(window=34, min_periods=24).mean())
    ao = sma_5 - sma_34
    sma_ao = pd.Series(ao.rolling(window=5, min_periods=5).mean())
    ac = pd.Series(ao - sma_ao, name="ac")
    df['ac'] = ac.fillna(0)
    return df

def previous_close(df):
    p_close = pd.Series(df['close'].rolling(window=2, min_periods=2).apply(lambda x: x[1] - x[0]))
    df['previous_close'] = p_close
    return df
