import asyncio

import logging
import numpy as np
from agent import Agent
from agent_helpers import message_filter
from data.data_formats import MarketStatus, TextData, MarketDirection
from simpletransformers.classification import ClassificationModel

log = logging.getLogger(Agent.Qualitative_FAAgent)


def print(*args, **kwargs):
    log.info(f"{args=}")


class QualitativeFAAgent:
    publish = None
    display = None

    def __init__(self, *args, **kwargs):
        pass

    async def start(self):
        self.model = ClassificationModel('bert', 'model_data/qualitative/checkpoint-484-epoch-1', num_labels=3,
                                         args={'reprocess_input_data': False, 'overwrite_output_dir': False},
                                         use_cuda=False)

    async def accept_message(self, agent, message):
        await self.qualitative_facts_analysis(agent=agent, status=message)
        await self.market_status(agent=agent, status=message)

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        pass

    @message_filter(message_type=TextData, param_name="status")
    async def qualitative_facts_analysis(self, agent, status: TextData):
        res = self.get_result(status.text)
        print(f"{res=}")

    @message_filter(message_type=MarketStatus, param_name="status")
    async def market_status(self, agent, status: MarketStatus):
        pass

    def get_result(self, statement):
        result = self.model.predict([statement])
        pos = np.where(result[1][0] == np.amax(result[1][0]))
        pos = int(pos[0])
        sentiment_dict = {0: MarketDirection.STAY, 1: MarketDirection.SELL, 2: MarketDirection.BUY}
        return sentiment_dict[pos]
