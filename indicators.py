import pandas as pd
import talib
import matplotlib.pyplot as plt

df = pd.read_csv("binance_data.csv")

obLevel = 70
osLevel = 30
length = 14

src = df["close"]

ep = 2 * length - 1

auc = talib.EMA((src - src.shift(1)).clip(lower=0), timeperiod=ep)
adc = talib.EMA((src.shift(1) - src).clip(lower=0), timeperiod=ep)

df["x1"] = (length - 1) * (adc * obLevel / (100 - obLevel) - auc)
df["x2"] = (length - 1) * (adc * osLevel / (100 - osLevel) - auc)

df["ub"] = (
        src + df["x1"].where(df["x1"] >= 0,
                             df["x1"] * (100 - obLevel) / obLevel)
)
df["lb"] = (
        src + df["x2"].where(df["x2"] >= 0,
                             df["x2"] * (100 - osLevel) / osLevel)
)

if __name__ == '__main__':
    plt.plot(df['ub'], label="Resistance", color='red', linewidth=2)
    plt.plot(df['lb'], label="Support", color='green', linewidth=2)
    plt.plot(
        (df['ub'] + df['lb']) / 2,
        label="RSI Midline",
        color='gray',
        linewidth=1
    )
    plt.title("RSI Bands")
    plt.legend()

    plt.show()
