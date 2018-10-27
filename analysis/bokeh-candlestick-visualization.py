# this is an experiment to test the bokeh library

# %%
from bokeh.plotting import figure, show, output_file

# %%
from math import pi
import pandas as pd
import generic_utils as utils

# %%
df = utils.get_dataframe("CSCO")

# %%
mids = (df.Open + df.Close)/2
spans = abs(df.Close-df.Open)

inc = df.Close > df.Open
dec = df.Open > df.Close
w = 12*60*60*1000 # half day in ms

output_file("candlestick.html", title="candlestick.py example")

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

p = figure(x_axis_type="datetime", tools=TOOLS, plot_width=1000, toolbar_location="left")

p.segment(df.date, df.high, df.date, df.low, color="black")
p.rect(df.date[inc], mids[inc], w, spans[inc], fill_color="#D5E1DD", line_color="black")
p.rect(df.date[dec], mids[dec], w, spans[dec], fill_color="#F2583E", line_color="black")

p.title = "MSFT Candlestick"
p.xaxis.major_label_orientation = pi/4
p.grid.grid_line_alpha=0.3

show(p)  # Open a browser
