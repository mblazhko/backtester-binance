from strategies import Strategy


class Backtester:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def run_backtest(self, initial_balance: int):
        signals = self.strategy.get_signals()

        # Початковий баланс у доларах
        balance = initial_balance
        position = None

        trades = []

        for i, signal in enumerate(signals):
            if signal["action"]:
                if position is not None:
                    # Закрити попередню позицію перед відкриттям нової
                    trade_result = self.close_position(
                        position, self.strategy.df["close"][i]
                    )
                    balance += trade_result["pnl"]
                    trades.append(trade_result)

                position = {
                    "entry_price": signal["entry price"],
                    "TP": signal["TP"],
                    "SL": signal["SL"],
                }
            elif position is not None:
                # Перевірити умови для закриття поточної позиції
                if (
                    self.strategy.df["close"][i] >= position["TP"]
                    or self.strategy.df["close"][i] <= position["SL"]
                ):
                    trade_result = self.close_position(
                        position, self.strategy.df["close"][i]
                    )
                    balance += trade_result["pnl"]
                    trades.append(trade_result)
                    position = None

        # Закрити будь-яку відкриту позицію в кінці тестування
        if position is not None:
            trade_result = self.close_position(
                position, self.strategy.df["close"].iloc[-1]
            )
            balance += trade_result["pnl"]
            trades.append(trade_result)

        return {"balance": balance, "trades": trades}

    def close_position(self, position, close_price):
        pnl = 0
        if close_price >= position["TP"]:
            pnl = (position["TP"] / position["entry_price"] - 1) * 100
        elif close_price <= position["SL"]:
            pnl = (position["SL"] / position["entry_price"] - 1) * 100

        return {"entry_price": position["entry_price"], "exit_price": close_price, "pnl": pnl}