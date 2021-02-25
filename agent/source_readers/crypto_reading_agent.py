import asyncio
import logging
from datetime import datetime

from cryptoxlib.clients.binance.BinanceClient import BinanceClient
from cryptoxlib.clients.binance.BinanceWebsocket import BestOrderBookTickerSubscription, AllMarketTickersSubscription

from agent import Agent
from agent.source_readers.converters import binance_message as bm
from utils.timeit import log_time

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
    exit_request = True

    def __init__(self, *args, **kwargs):
        self.client = BinanceClient(api_key, api_secret, api_trace_log=True)

    async def all_market_ticker_update(self, response) -> None:
        await self.publish(Agent.Market_Correlation_Analysing_Agent, response)

    async def execute(self, *args, **kwargs):
        self.client.compose_subscriptions([
            AllMarketTickersSubscription(callbacks=[self.all_market_ticker_update]),
        ])
        # Execute all websockets asynchronously
        while self.exit_request:
            try:
                await self.client.start_websockets()
            except Exception as e:
                log.error(e, e.args)
                await asyncio.sleep(0.5)

        await self.client.close()

        log.info("Workgin")

    @log_time(logger=log, log_off=False)
    async def all_market_price(self, data):
        # for dt in data:
        await self.publish(Agent.Market_Trend_Analysing_Agent, data)
        await self.publish(Agent.Market_Equilibrium_Analysing_Agent, data)

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
