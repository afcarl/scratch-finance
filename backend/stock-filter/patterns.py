# Bullish Reversals

def hammer():
    (((high - low)> 3 * (open - close)) and
    ( (close - low) / (.001 + high - low) > 0.6 ) and
    ( (open  - low) / (.001 + high - low) > 0.6))


morning_star
# During a downtrend, the market strengthens the bearish trend with a long black candlestick. The second candlestick trades within a small range and closes at or near its open. This scenario generally shows the potential for a rally, as many positions have been changed. Confirmation of the reversal is given by the white third candlestick. The stronger the white third body the more significant the pattern is.

# check if downtrend
# first candlestick is a long black candlestick
# second candlestick is small and closes near the open
# third candlestick is white and the bigger the body, the more significant the pattern

close[2] < open[2]
max(open[1], close[1]) < close[2]

open > max(open[1], close[1])
close > open )

three_inside_up

three_outside_up
