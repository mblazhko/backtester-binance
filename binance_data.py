import asyncio

from binance.client import AsyncClient
import pandas as pd
from pandas import DataFrame


class BinanceData:
    def __init__(
        self, symbol: str, interval: str, start_date: str, end_date: str
    ) -> None:
        self.symbol = symbol
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date

    async def get_binance_data(self) -> DataFrame:
        # make client
        client = await AsyncClient().create()

        # get klines
        klines = await client.get_historical_klines(
            self.symbol, self.interval, self.start_date, self.end_date
        )

        # make DataFrame from gotten data
        df = pd.DataFrame(
            klines,
            columns=[
                "timestamp",
                "open",
                "high",
                "low",
                "close",
                "volume",
                "close_time",
                "quote_asset_volume",
                "number_of_trades",
                "taker_buy_base_asset_volume",
                "taker_buy_quote_asset_volume",
                "ignore",
            ],
        )
        # transform "timestamp" to datetime type
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)

        # save DataFrame as CSV file
        df.to_csv("binance_data.csv")

        await client.close_connection()

        return df


if __name__ == "__main__":
    symbol = "BTCUSDT"
    interval = AsyncClient.KLINE_INTERVAL_1MINUTE
    start_date = "2019-10-01"
    end_date = "2023-10-01"

    binance_data = BinanceData(symbol, interval, start_date, end_date)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(binance_data.get_binance_data())
