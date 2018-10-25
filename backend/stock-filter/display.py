import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def plot(symbol, bars, volume):
    figure = plt.figure()
    candle_plot = figure.add_subplot(111, aspect='equal')

    count = 0
    total = bars.shape[0]
    factor = 5
    volsize = (factor/2) + 0.2
    while count < total:
        open  = bars.loc[count, 'open'] * factor
        high  = bars.loc[count, 'high'] * factor
        low   = bars.loc[count, 'low'] * factor
        close = bars.loc[count, 'close'] * factor
        vol   = volume.loc[count, 'volume'] * (factor/2)

        body = math.fabs(close - open)
        shadow_tail = min(close, open) - low
        shadow_head = high - max(close, open)
        if close >= open:
            color = "green"
        else:
            color = "red"

        offset = count + (count * 0.04)
        # body
        candle_plot.add_patch(
             patches.Rectangle(
                (offset + 0, 0.0),
                0.5, vol,
                facecolor="black",
                edgecolor="black",
                alpha=0.2,
                fill=True
            )
        )

        # shadow_tail
        candle_plot.add_patch(
            patches.Rectangle(
                (offset + 0.25, low + volsize),
                0.01, shadow_tail,
                color=color,
                alpha=0.4,
                fill=True
            )
        )

        # body
        candle_plot.add_patch(
             patches.Rectangle(
                (offset + 0, shadow_tail + low + volsize),
                0.5, body,
                facecolor=color,
                edgecolor=color,
                alpha=0.6,
                fill=True
            )
        )

        # shadow_head
        candle_plot.add_patch(
            patches.Rectangle(
                (offset + 0.25, body + shadow_tail + low + volsize),
                0.01, shadow_head,
                color=color,
                alpha=0.4,
                fill=True
            )
        )
        count += 1

    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("./candles/{}".format(symbol))
    plt.close()
