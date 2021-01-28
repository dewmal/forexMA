import asyncio

import logging

from agent import Agent
from data.mock_data_generator import gen_action

log = logging.getLogger(Agent.Decision_Agent)


def print(*args, **kwargs):
    log.info(f"{args=}")


class DecisionAgent:
    publish = None
    display = None

    def __init__(self, *args, **kwargs):
        log.info(f"{self} Start")

    async def start(self):
        # await self.publish("AgentTwo", "Hi Agent 2")
        pass

    async def accept_message(self, agent, message):
        print(f"{agent=},{message=}")
        action = gen_action()
        await self.display(action.to_dict())
        await self.publish(Agent.Performance_Analysing_Agent, action.to_dict())

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        pass
        # while True:
        #     print("run")
        #     # await self.publish("AgentTwo", "Hello AGENT 2")
        #     await asyncio.sleep(2)
