import json
import logging

import websockets

from agent import Agent
from data.data_formats import MarketStatus
from utils.binary_api_helpers import convert_message_to_environment
from utils.web_socket import websocket_connect

log = logging.getLogger(Agent.Price_Reading_Agent)


def print(*args, **kwargs):
    log.info(f"{args=}")


class PriceReadingAgent:
    publish = None
    display = None
    last_candle: MarketStatus = None

    def __init__(self, *args, **kwargs):
        self.__binary_host = "wss://ws.binaryws.com/websockets/v3?app_id=1089"

    async def start(self):
        await websocket_connect(self.__binary_host, {
            "ticks_history": "frxEURUSD",
            "adjust_start_time": 1,
            "count": 50,
            "end": "latest",
            "start": 1,
            "style": "candles",
            "subscribe": 1
        }, self.process_message)

    async def process_message(self, message):
        price_status_list = convert_message_to_environment(message)
        for status in price_status_list:
            if not self.last_candle:
                self.last_candle = status

            if self.last_candle.time_stamp < status.time_stamp:
                await self.publish(Agent.Quantitative_FAAgent, self.last_candle)
                await self.publish(Agent.Performance_Analysing_Agent, self.last_candle)
                await self.publish(Agent.Decision_Agent, self.last_candle)
                await self.display(self.last_candle.to_dict())

            self.last_candle = status

    async def accept_message(self, agent, message):
        pass

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        pass
        # async with websockets.connect(self.__binary_host) as websocket:
        #     await websocket.send(json.dumps({
        #         "ticks_history": "frxEURUSD",
        #         "adjust_start_time": 1,
        #         "count": 50,
        #         "end": "latest",
        #         "start": 1,
        #         "style": "candles",
        #         "subscribe": 1
        #     }))
        #
        #     async for message in websocket:
