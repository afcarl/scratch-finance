# %%
import pandas as pd

stocks = pd.read_csv("data/equities.csv", index_col="symbol")
stocks = stocks.drop(columns=["id"])

sectors = pd.read_csv("data/sector.csv", index_col="id")
subsectors = pd.read_csv("data/subsector.csv", index_col="id")
psei = pd.read_csv("data/psei.csv", index_col="symbol")

stocks["sector"] = stocks["sector"].map(sectors["name"])
stocks["subsector"] = stocks["subsector"].map(subsectors["name"])
stocks = pd.merge(stocks, psei, left_index=True, right_index=True, how="left")
stocks["psei"] = stocks["psei"].fillna(False)

stocks.to_csv("data/stocks.csv")
