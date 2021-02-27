import logging
import os
from agent import Agent
from utils.timeit import log_time

log = logging.getLogger(Agent.Asset_Analysing_Agent)


class AssetAnalysingAgent:

    def __init__(self, *args, **kwargs):
        api = os.environ['BINANCE_API']
        sec = os.environ['BINANCE_SEC']
        log.info(f"{sec=}")

    @log_time(logger=log, log_off=False)
    async def accept_message(self, agent, message):
        log.info(f"{agent=}")
