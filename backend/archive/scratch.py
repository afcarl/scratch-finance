
# import client
# import indicators
# import utils
# import pandas as pd
# import numpy as np
#
# final_string = "["
# stocks = ["GLO"]#
# company_name = ["GLO"] #,"AEV","AGI","ALI","AP","BDO","BPI","DMC","EDC","EMP","FGEN","GLO","GTCAP","ICT","JFC","LTG","MBT","MEG","MER","MPI","PCOR","RLC","SCC","SECB","SM","SMC","SMPH","TEL","URC"]
#
#
# for i, stock in enumerate(stocks):
#     dd = client.get_history(stock, convertTime=False, days=400)
#     dd = indicators.ema_close(dd)
#
#     dd["date"] = dd.date.apply(lambda x: x * 1000) # convert timestamp
#     dd = indicators.ac(dd)
#     dd = utils.get_signals(dd)
#
#
#     stock_id = "\"id\": \"{0}\"".format(stock)
#     stock_name = "\"name\": \"{0}\"".format(company_name[i])
#     stock_data =  "\"ohlc\": " + dd[["date","open","high","low","close"]].to_json(orient="values")
#     stock_combined = "{ " + stock_id + ", " + stock_name + ", " + stock_data + ","
#     stock_close = "\"close\": " + dd[dd["ema_close"] != 0][["date","ema_close"]].to_json(orient="values") + ","
#     indicator_ac = "\"ac\": " + dd[["date","ac"]].to_json(orient="values") + ","
#     signal = "\"signal\": " + dd[dd["signal"] != 0][["date","signal"]].to_json(orient="values")
#     final_string = final_string + stock_combined + stock_close + indicator_ac + signal + "}"
#
#     if i < len(stocks) - 1:
#         final_string = final_string + ", "
#
# final_string = final_string + "]"
#
# print(final_string)
# %%
import client
import indicators
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# %%
# Read JSON file for

# %%
stocks = ["AC","AEV","AGI","ALI","AP","BDO","BPI","DMC","EDC","EMP","FGEN","GLO","GTCAP","ICT","JFC","LTG","MBT","MEG","MER","MPI","PCOR","RLC","SCC","SECB","SM","SMC","SMPH","TEL","URC"]
scatter = pd.DataFrame(index=stocks, columns=["strength", "price", "range"])

for stock in stocks:
    df = client.get_history(stock, days=365)
    df = indicators.relative_strength_index(df, n=14)
    df = indicators.ema_rsi(df, n=5)

    df_norm = df[["ema_rsi", "rsi"]]
    # df_norm = (df_norm - 0.50) * 2 * 100
    ema_rsi = df_norm["ema_rsi"] # .rolling(window=5, win_type="gaussian", center=True).mean(std=3)
    ema_rsi = (ema_rsi - 0.5)
    ema_rsi = ema_rsi * 200
    # ema_rsi = ema_rsi.rolling(window=5, win_type="gaussian", center=True).mean(std=3)
    # ema_rsi = ema_rsi.shift(2)

    rsi = df["rsi"]
    rsi = (rsi - 0.5) * 200

    close = df["close"]

    scatter.loc[stock].strength = ema_rsi.iloc[-1]
    scatter.loc[stock].price = close.iloc[-1]
    close = (((close - close.min()) / (close.max() - close.min()))) * 100
    close_smoothed = close.rolling(window=5, win_type="gaussian", center=True).mean(std=3)
    close_smoothed = close_smoothed.shift(2)
    plt.figure(figsize=(15,2))
    ema_rsi.plot(legend=True, title=stock)
    close_smoothed.plot(legend=True, title=stock)
    plt.axhline(y=0, color="black", linestyle="--", alpha=0.2)
    plt.annotate("%0.2f" % ema_rsi.tail(1), xy=(1, ema_rsi.tail(1)), xytext=(8, 0),
             xycoords=("axes fraction", "data"), textcoords="offset points")
    plt.xlim([200,250])
    plt.show()

# %%
# scatter = scatter.astype(np.float)
# plt.figure(figsize=(8,8))
# plt.scatter(scatter.price,scatter.strength, alpha=0.5)
# plt.xscale("log")
#
# for index, row in scatter.iterrows():
#    plt.annotate(row.name, (row.price, row.strength))
#
# plt.axhline(y=0, color="black", linestyle="--", alpha=0.2)
# plt.ylim([-100,100])
# plt.show()


print(scatter.to_json(orient="index"))


#
# import pymongo
# from pymongo import MongoClient
# import os
#
# # username = os.environ["mongo_username"]
# # password = os.environ["mongo_password"]
# username = "admin-monkey"
# password = "admin-monkey123"
#
# print("Connecting to mLab with username: %s" % username)
# client = MongoClient("mongodb://%s:%s@ds231360.mlab.com:31360" % (username, password))
#
# db = client.quantmonkey
# rec = db.recommendations
#
# rec.insert_one({"a":1
