import pandas as pd
import talib
import matplotlib.pyplot as plt
from pandas import DataFrame


class Indicator:
    def __init__(
        self,
        obLevel: int,
        osLevel: int,
        length: int,
    ) -> None:
        self.obLevel = obLevel
        self.osLevel = osLevel
        self.length = length
        self.df: DataFrame = pd.read_csv("binance_data.csv")

    def get_indicator(self) -> DataFrame:
        src = self.df["close"]

        ep = 2 * self.length - 1

        auc = talib.EMA((src - src.shift(1)).clip(lower=0), timeperiod=ep)
        adc = talib.EMA((src.shift(1) - src).clip(lower=0), timeperiod=ep)

        self.df["x1"] = (self.length - 1) * (
            adc * self.obLevel / (100 - self.obLevel) - auc
        )
        self.df["x2"] = (self.length - 1) * (
            adc * self.osLevel / (100 - self.osLevel) - auc
        )

        self.df["ub"] = src + self.df["x1"].where(
            self.df["x1"] >= 0,
            self.df["x1"] * (100 - self.obLevel) / self.obLevel,
        )
        self.df["lb"] = src + self.df["x2"].where(
            self.df["x2"] >= 0,
            self.df["x2"] * (100 - self.osLevel) / self.osLevel,
        )

        return self.df

    def build_plot(self) -> None:
        plt.plot(self.df["ub"], label="Resistance", color="red", linewidth=2)
        plt.plot(self.df["lb"], label="Support", color="green", linewidth=2)
        plt.plot(
            (self.df["ub"] + self.df["lb"]) / 2,
            label="RSI Midline",
            color="gray",
            linewidth=1,
        )
        plt.title("RSI Bands")
        plt.legend()

        plt.show()


# if __name__ == "__main__":
#     obLevel = 70
#     osLevel = 30
#     length = 14
#     indicator = Indicator(obLevel, osLevel, length)
#     indicator.get_indicator()
#     indicator.build_plot()
