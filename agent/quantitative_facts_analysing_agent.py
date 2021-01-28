import logging

from agent import Agent
from agent_helpers import message_filter
from data.data_formats import MarketStatus
from data.mock_data_generator import gen_fact_pattern

log = logging.getLogger(Agent.Quantitative_FAAgent)


def print(*args, **kwargs):
    log.info(f"{args=}")


class QuantitativeFAAgent:
    publish = None
    display = None

    def __init__(self, *args, **kwargs):
        log.info(f"{self} Start")

    async def start(self):
        # await self.publish("AgentTwo", "Hi Agent 2")
        pass

    async def accept_message(self, agent, message):
        res = await self.quantitative_facts_analysis(agent=agent, status=message)

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        pass

    @message_filter(message_type=MarketStatus, param_name="status")
    async def quantitative_facts_analysis(self, agent, status: MarketStatus):
        pattern = gen_fact_pattern(time_stamp=status.time_stamp, asset_name=status.asset_name)
        await self.display(pattern.to_dict())
        await self.publish(Agent.Decision_Agent, pattern.to_dict())
