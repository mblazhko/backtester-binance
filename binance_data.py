import asyncio

from binance.client import AsyncClient
import pandas as pd
from pandas import DataFrame


async def get_binance_data(
    symbol: str, interval: str, start_date: str, end_date: str
) -> DataFrame:
    client = await AsyncClient().create()
    klines = await client.get_historical_klines(
        symbol, interval, start_date, end_date
    )
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
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df.to_csv("binance_data.csv")

    await client.close_connection()

    return df


if __name__ == "__main__":
    symbol = "BTCUSDT"
    interval = AsyncClient.KLINE_INTERVAL_1MINUTE
    start_date = "2019-10-01"
    end_date = "2023-10-01"

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        get_binance_data(symbol, interval, start_date, end_date)
    )
