import asyncio

import logging

from agent import Agent
from agent_helpers import message_filter
from data.data_formats import Action

log = logging.getLogger(Agent.Performance_Analysing_Agent)


def print(*args, **kwargs):
    log.info(f"{args=}")


class PerformanceAnalysingAgent:
    publish = None
    display = None

    performance_data = {

    }

    def __init__(self, *args, **kwargs):
        log.info(f"{self} Start")

    async def start(self):
        # await self.publish("AgentTwo", "Hi Agent 2")
        pass

    async def accept_message(self, agent, message):
        await self.performance_analysis(agent=agent, action=message)

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        pass

    @message_filter(message_type=Action, param_name="action")
    async def performance_analysis(self, agent, action: Action):
        print(f"{agent=},{action=}")
        agent_performance = 0
        count = 1
        if agent in self.performance_data:
            agent_performance = self.performance_data[agent]
            count = 2

        agent_performance = (agent_performance + action.reward) / count
        self.performance_data[agent] = agent_performance

        await self.display({
            "name": agent,
            "performance": agent_performance
        })
