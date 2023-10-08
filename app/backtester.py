from app.strategies import Strategy


class Backtester:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy

    def run_backtest(self, initial_balance: int):
        signals = self.strategy.get_signals()

        # Start balance in usd
        balance = initial_balance
        position = None

        trades = []

        for i, signal in enumerate(signals):
            if signal["action"]:
                if position is not None:
                    # close previous position before open new one
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
                # check conditions before close position
                if (
                    self.strategy.df["close"][i] >= position["TP"]
                    or self.strategy.df["close"][i] <= position["SL"]
                    or self.strategy.df["close"][i]
                    == position["TP"]
                    == position["SL"]
                ):
                    trade_result = self.close_position(
                        position, self.strategy.df["close"][i]
                    )
                    balance += trade_result["pnl"]
                    trades.append(trade_result)
                    position = None

        # close any existing position before testing
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

        return {
            "entry_price": position["entry_price"],
            "exit_price": close_price,
            "pnl": pnl,
        }
