import asyncio
import logging
from datetime import datetime

from agent import Agent
from utils.timeit import log_time
from utils.web_socket import websocket_connect
from agent.source_readers.converters import binance_message as bm

log = logging.getLogger(Agent.Crypto_Reading_Agent)


class CryptoReadingAgent:
    last_time_values = {}

    def __init__(self, *args, **kwargs):
        pass

    @log_time(logger=log, log_off=True)
    async def all_market_price(self, data):
        # for dt in data:
        await self.publish(Agent.Market_Trend_Analysing_Agent, data)
        # log.info(f"{len(data)=}")

    @log_time(logger=log, log_off=False)
    async def read_asset_market_price(self, data):
        if "k" in data:
            name: str = data["s"]
            if name:
                start_time = data["k"]["t"]

                last_start_time = 0
                last_value = None

                if name in self.last_time_values:
                    last_start_time = self.last_time_values[name]["time"]
                    last_value = self.last_time_values[name]["value"]

                if last_start_time < start_time and last_value:
                    status = bm.get_market_status_from_kline(last_value)
                    log.info(f"{status=}")
                    await self.display(status.to_dict())

                self.last_time_values[name] = {
                    "time": start_time,
                    "value": data
                }

            # await self.display(status.to_dict())

    async def execute(self, *args, **kwargs):
        uri = "wss://stream.binance.com:9443/ws"
        all_market_data_reader = websocket_connect(f"{uri}/!ticker@arr", None, self.all_market_price)
        read_market_price = websocket_connect(f"{uri}", {
            "method": "SUBSCRIBE",
            "params":
                [
                    "1inchusdt@kline_1m"
                ],
            "id": 1
        }, self.read_asset_market_price)
        await asyncio.wait([all_market_data_reader], return_when=asyncio.ALL_COMPLETED)
