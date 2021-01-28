import asyncio

import logging

from agent import Agent
from agent_helpers import message_filter
from data.data_formats import MarketStatus, TextData
from data.mock_data_generator import gen_fact_pattern

log = logging.getLogger(Agent.Qualitative_FAAgent)


def print(*args, **kwargs):
    log.info(f"{args=}")


class QualitativeFAAgent:
    publish = None
    display = None

    def __init__(self, *args, **kwargs):
        log.info(f"{self} Start")

    async def start(self):
        # await self.publish("AgentTwo", "Hi Agent 2")
        pass

    async def accept_message(self, agent, message):
        await self.qualitative_facts_analysis(agent=agent, status=message)
        await self.market_status(agent=agent, status=message)

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        pass

    @message_filter(message_type=TextData, param_name="status")
    async def qualitative_facts_analysis(self, agent, status: TextData):
        print(f"{agent=},{status=}")

    @message_filter(message_type=MarketStatus, param_name="status")
    async def market_status(self, agent, status: MarketStatus):
        pass
