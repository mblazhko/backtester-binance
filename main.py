from backtester import Backtester
from strategies import Strategy


def run_backtester(ob_level: int, os_level: int, length: int, initial_balance: int):
    strategy = Strategy(ob_level, os_level, length)
    backtester = Backtester(strategy)

    return backtester.run_backtest(initial_balance)


def print_metrics(results: dict) -> None:
    total_trades = len(results["trades"])
    winning_trades = len(
        [trade for trade in results["trades"] if trade["pnl"] > 0])
    losing_trades = len(
        [trade for trade in results["trades"] if trade["pnl"] < 0])
    winrate = (winning_trades / total_trades) * 100

    total_pnl = results["balance"] - 100
    profit_factor = abs(sum([trade["pnl"] for trade in results["trades"] if
                             trade["pnl"] > 0]) / sum(
        [trade["pnl"] for trade in results["trades"] if trade["pnl"] < 0]))

    print(f"Total PnL: {round(total_pnl, 2)}")
    print(f"Total Trades: {total_trades}")
    print(f"Winning Trades: {winning_trades}")
    print(f"Losing Trades: {losing_trades}")
    print(f"Winrate: {winrate}%")
    print(f"Profit Factor: {profit_factor}")


if __name__ == '__main__':
    results = run_backtester(
        ob_level=70, os_level=30, length=14, initial_balance=100
    )
    print_metrics(results)