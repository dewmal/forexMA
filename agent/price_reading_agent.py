import asyncio

import logging

from agent import Agent
from data.mock_data_generator import gen_market_status

log = logging.getLogger(Agent.Price_Reading_Agent)


def print(*args, **kwargs):
    log.info(f"{args=}")


class PriceReadingAgent:
    publish = None
    display = None

    def __init__(self, *args, **kwargs):
        log.info(f"{self} Start")

    async def start(self):
        # await self.publish("AgentTwo", "Hi Agent 2")
        pass

    async def accept_message(self, agent, message):
        pass

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        while True:
            status = gen_market_status()
            await self.publish(Agent.Quantitative_FAAgent, status.to_dict())
            await self.display(status.to_dict())
            await asyncio.sleep(2)
