import asyncio

import logging

from agent import Agent
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
        print(f"{agent=} {message=}")
        pattern = gen_fact_pattern()
        await self.publish(Agent.Decision_Agent, pattern.to_dict())

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        pass