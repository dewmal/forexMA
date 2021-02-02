import logging
from datetime import datetime

from agent import Agent
from utils.timeit import log_time
from utils.web_socket import websocket_connect

log = logging.getLogger(Agent.Crypto_Reading_Agent)


class CryptoReadingAgent:
    last_time_values = {}

    def __init__(self, *args, **kwargs):
        pass

    @log_time(logger=log)
    async def all_market_price(self, data):
        for dt in data:
            name: str = dt["s"]
            if name:
                close_time = dt["C"]
                close_time = datetime.fromtimestamp(close_time / 1000)
                seconds = int(close_time.timestamp() // 60)

                last_seconds = 0
                last_value = None

                if name in self.last_time_values:
                    last_seconds = self.last_time_values[name]["time"]
                    last_value = self.last_time_values[name]["value"]

                if last_seconds < seconds and last_value:
                    close_time, close_price = last_value["C"], last_value["c"]
                    self.display(last_value)

                self.last_time_values[name] = {
                    "time": seconds,
                    "value": dt
                }

    async def execute(self, *args, **kwargs):
        uri = "wss://stream.binance.com:9443/ws"
        read_market_price = websocket_connect(f"{uri}/!ticker@arr", None, self.all_market_price)
        await read_market_price
