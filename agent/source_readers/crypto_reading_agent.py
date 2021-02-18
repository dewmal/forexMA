import asyncio
import json
import logging
from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager

from agent import Agent
from agent.source_readers.converters import binance_message as bm
from utils.timeit import log_time
from utils.web_socket import websocket_connect

log = logging.getLogger(Agent.Crypto_Reading_Agent)

# Testnet
# api_key = "DsX2h7xFTdc9tVXtIV0a3kOjENMG29CSgVRjuplqXy6NXamj1dYE6w5r5w0lwY3x"
# api_secret = "crx9ynLNAdDTBEuck4hJRsen1ZPxpFpfUWnuxeogHAICYk7CupgCg2Kz009gX99M"
#
#
# Original
api_key = "tbsnZy6h4RLcG98qqH6OhlLvOXwTGzBYKfOBK9Q1Z0VN8YlazFfWDRenHtJAcoyC"
api_secret = "JmiUiVlP3aH2NZm269YjV4Yp4zATKu1OJfQpdXIITSBgMHxJXlUB1Gajj1gz9XCD"


class CryptoReadingAgent:
    last_time_values = {}

    def __init__(self, *args, **kwargs):
        self.bm = BinanceWebSocketApiManager(exchange="binance.com-testnet")
        # self.bm.start_all_mark_price_socket(lambdmm

    @log_time(logger=log, log_off=False)
    async def all_market_price(self, data):
        # for dt in data:
        await self.publish(Agent.Market_Trend_Analysing_Agent, data)
        await self.publish(Agent.Market_Equilibrium_Analysing_Agent, data)
        log.info(f"{len(data)=}")

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
        await asyncio.wait([all_market_data_reader], return_when=asyncio.ALL_COMPLETED)

        # self.bm.create_stream("arr", "!ticker", output="UnicornFy")
        #
        # while True:
        #     stream_buffer = self.bm.pop_stream_data_from_stream_buffer()
        #     if stream_buffer:
        #         await self.all_market_price(data=stream_buffer)
        #     #
