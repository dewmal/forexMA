import json
import logging

import websockets

from agent import Agent
from data.data_formats import MarketStatus
from utils.binary_api_helpers import convert_message_to_environment

log = logging.getLogger(Agent.Price_Reading_Agent)


def print(*args, **kwargs):
    log.info(f"{args=}")


class PriceReadingAgent:
    publish = None
    display = None

    def __init__(self, *args, **kwargs):
        self.__binary_host = "wss://ws.binaryws.com/websockets/v3?app_id=1089"

    async def start(self):
        # await self.publish("AgentTwo", "Hi Agent 2")
        pass

    async def accept_message(self, agent, message):
        pass

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        async with websockets.connect(self.__binary_host) as websocket:
            await websocket.send(json.dumps({
                "ticks_history": "frxEURUSD",
                "adjust_start_time": 1,
                "count": 50,
                "end": "latest",
                "start": 1,
                "style": "candles",
                "subscribe": 1
            }))

            last_candle: MarketStatus = None
            async for message in websocket:
                price_status_list = convert_message_to_environment(message)
                for status in price_status_list:
                    if last_candle == None:
                        last_candle = status

                    if last_candle.time_stamp < status.time_stamp:
                        await self.publish(Agent.Quantitative_FAAgent, last_candle)
                        await self.publish(Agent.Performance_Analysing_Agent, last_candle)
                        await self.publish(Agent.Decision_Agent, last_candle)
                        await self.display(last_candle.to_dict())

                    last_candle = status
