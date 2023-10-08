from app.indicators import Indicator
import pandas as pd


class Strategy:
    def __init__(self, ob_level, os_level, length, df):
        self.ob_level = ob_level
        self.os_level = os_level
        self.length = length
        self.indicator = Indicator(
            ob_level, os_level, length, df
        )
        self.df = self.indicator.get_indicator()

    def get_signals(self):
        signals = []

        for i in range(len(self.df)):
            if (
                self.df["close"][i] > self.df["ub"][i]
                and self.df["CCI"][i] < -100
            ):
                signal = {
                    "action": True,
                    "entry price": self.df["close"][i],
                    "TP": self.df["close"][i] * 1.01,  # TP 1%
                    "SL": self.df["close"][i] * 0.996,  # SL 0.4%
                }
            elif (
                self.df["close"][i] < self.df["lb"][i]
                and self.df["CCI"][i] > 120
            ):
                signal = {
                    "action": True,
                    "entry price": self.df["close"][i],
                    "TP": self.df["close"][i] * 1.011,  # TP 1.1%
                    "SL": self.df["close"][i] * 0.995,  # SL 0.5%
                }
            else:
                signal = {"action": False}

            signals.append(signal)

        return signals
