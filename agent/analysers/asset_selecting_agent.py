import logging

from agent import Agent
from utils.timeit import log_time, error_log

log = logging.getLogger(Agent.Asset_Selecting_Agent)


class AssetSelectingAgent:

    def __init__(self, *args, **kwargs):
        pass

    @log_time(logger=log, log_off=False)
    @error_log(logger=log)
    async def accept_message(self, agent, message):
        market_values = message["data"]
        market_values.sort(reverse=True, key=lambda x: x["P"])
        log.info(f"{market_values[0]}")
