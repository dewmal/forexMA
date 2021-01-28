import json
from typing import List

from data.data_formats import MarketStatus


def convert_message_to_environment(message) -> List[MarketStatus]:
    message = json.loads(message)
    if "ohlc" in message:
        ohlc = message["ohlc"]
        time_stamp = int(ohlc["open_time"])
        asset_name = ohlc["symbol"]
        open, high, low, close = float(ohlc["open"]), float(ohlc["high"]), float(ohlc["low"]), float(
            ohlc["close"])

        return [MarketStatus(
            time_stamp=time_stamp,
            asset_name=asset_name,
            open=open,
            high=high,
            low=low,
            close=close
        )]
    elif "candles" in message:
        candles = message["candles"]
        status_list = []
        for candle in candles:
            time_stamp = int(candle["epoch"])
            asset_name = message["echo_req"]["ticks_history"]
            open, high, low, close = float(candle["open"]), float(candle["high"]), float(candle["low"]), float(
                candle["close"])
            status_list.append(MarketStatus(
                time_stamp=time_stamp,
                asset_name=asset_name,
                open=open,
                high=high,
                low=low,
                close=close
            ))
        return status_list
