import sys, getopt
import pandas as pd

df = pd.read_pickle('./equities.pkl')
print(df.query(sys.argv[1]).to_string(justify='left'))
