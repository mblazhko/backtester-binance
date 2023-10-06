import pandas as pd
import talib
import matplotlib.pyplot as plt
from pandas import DataFrame


class Indicator:
    def __init__(
        self,
        ob_level: int,
        os_level: int,
        length: int,
        df: DataFrame
    ) -> None:
        self.ob_level = ob_level
        self.os_level = os_level
        self.length = length
        self.df = df

    def get_indicator(self) -> DataFrame:
        src = self.df["close"]

        ep = 2 * self.length - 1

        auc = talib.EMA((src - src.shift(1)), timeperiod=ep)
        adc = talib.EMA((src.shift(1) - src), timeperiod=ep)

        self.df["CCI"] = talib.CCI(
            self.df["high"], self.df["low"], self.df["close"], timeperiod=30
        )

        self.df["x1"] = (self.length - 1) * (
            adc * self.ob_level / (100 - self.ob_level) - auc
        )
        self.df["x2"] = (self.length - 1) * (
            adc * self.os_level / (100 - self.os_level) - auc
        )

        self.df["ub"] = src + self.df["x1"].where(
            self.df["x1"] >= 0,
            self.df["x1"] * (100 - self.ob_level) / self.ob_level,
        )
        self.df["lb"] = src + self.df["x2"].where(
            self.df["x2"] >= 0,
            self.df["x2"] * (100 - self.os_level) / self.os_level,
        )

        return self.df

    def build_plot(self, indicators_df: DataFrame) -> None:
        plt.plot(indicators_df["ub"], label="Resistance", color="red", linewidth=2)
        plt.plot(indicators_df["lb"], label="Support", color="green", linewidth=2)
        plt.plot(
            (indicators_df["ub"] + indicators_df["lb"]) / 2,
            label="RSI Midline",
            color="gray",
            linewidth=1,
        )
        plt.title("RSI Bands")
        plt.legend()

        plt.show()


if __name__ == "__main__":
    ob_level = 70
    os_level = 30
    length = 14
    df = pd.read_csv("binance_data.csv")
    indicator = Indicator(ob_level, os_level, length, df)
    indicators_df = indicator.get_indicator()
    indicator.build_plot(indicators_df)
