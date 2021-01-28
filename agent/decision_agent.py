import asyncio

import logging

from agent import Agent
from agent_helpers import message_filter
from data.data_formats import FactPattern
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
        await self.pattern_analysis(agent=agent, pattern=message)

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        pass

    @message_filter(message_type=FactPattern, param_name="pattern")
    async def pattern_analysis(self, agent, pattern: FactPattern):
        action = gen_action(time_stamp=pattern.time_stamp, asset_name=pattern.asset_name)
        await self.display(action.to_dict())
        await self.publish(Agent.Performance_Analysing_Agent, action.to_dict())
