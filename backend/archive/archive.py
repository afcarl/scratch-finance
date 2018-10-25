
# get buy signals
def get_signals(df):
    # start at 2 cause we need at least 2 days prior to test
    # for i in range(2, df.shape[0]):
    #     ac = df.loc[i-2:i,"ac"].values # ac 2 days ago to now
    #     if ac[0] < 0 and ac[1] < 0 and ac[0] < ac[1] and ac[1] < ac[2] and ac[2] > 0:
    #         df.loc[i,"signal"] = 1
    #     elif ac[0] > 0 and ac[1] > 0 and ac[0] > ac[1] and ac[1] > ac[2] and ac[2] < 0:
    #         df.loc[i,"signal"] = -1
    #     else:
    #         df.loc[i,"signal"] = 0
    #     i += 1
    # df = df.fillna(0)
    # return df

    for i in range(30, df.shape[0]):
        # if its green, and opens higher than the previous high, and the body is longer than the top wick
        if df.loc[i,"open"] < df.loc[i,"close"] and \
            df.loc[i-1,"high"] <= df.loc[i,"open"] and \
            df.loc[i,"high"]/df.loc[i,"close"] < df.loc[i,"close"]/df.loc[i,"open"]:
            df.loc[i,"signal"] = 1
            bars = 1
            while (df.loc[i-bars,"high"] < df.loc[i,"high"] and bars < 30):
                bars = bars + 1
            df.loc[i,"bars"] = bars
        else:
            df.loc[i,"signal"] = 0
    df.loc[0,"bars"] = 0
    df = df.fillna(0)
    return df

def print_signals():
    stocks = ["AC","AEV","AGI","ALI","AP","BDO","BPI","DMC","EDC","EMP","FGEN","GLO","GTCAP","ICT","JFC","LTG","MBT","MEG","MER","MPI","PCOR","RLC","SCC","SECB","SM","SMC","SMPH","TEL","URC"]
    for stock in stocks:
        dd = client.get_history(stock)
        dd = get_signals(dd)
        print(dd.tail())
