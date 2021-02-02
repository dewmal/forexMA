import asyncio
import logging
from datetime import datetime, timedelta
import numpy as np

from agent import Agent
from utils.timeit import log_time

log = logging.getLogger(Agent.Market_Trend_Analysing_Agent)


class MarketTrendAnalysingAgent:
    history = {}
    max_minutes = 60 * 5
    best_assets = 10

    def __init__(self, *args, **kwargs):
        pass

    @log_time(logger=log, log_off=True)
    async def accept_message(self, agent, message):
        for dt in message:
            max_length = 0
            time = datetime.fromtimestamp(int(dt["C"]) / 1000)
            name = dt["s"]
            if dt["s"] not in self.history:
                self.history[dt['s']] = [dt]
            else:
                self.history[dt['s']].append(dt)
            while True:
                if len(self.history[name]) > 0:
                    time_diff: timedelta = time - datetime.fromtimestamp(
                        int(self.history[name][0]["C"]) / 1000)
                    if time_diff.total_seconds() > 60 * 5:
                        pp = self.history[name].pop(0)
                        continue
                break

            if len(self.history[name]) > max_length:
                max_length = len(self.history[name])

        changes = []
        for v in self.history:
            recods = self.history[v]
            if recods and len(recods) > 0:
                recods = np.array([c['c'] for c in recods]).astype(np.float)
                change = ((np.max(recods) - np.min(recods)) * len(recods)) / (np.max(recods) * max_length)
                if change > 0:
                    # log.info(f"{v} = {change}")
                    changes.append({
                        "name": v,
                        "change": round(change, 4),
                        "length": len(recods)
                    })
        changes_ar = np.array([c["change"] for c in changes]).astype(np.float)
        idx_list = np.argsort(-changes_ar)[:self.best_assets]
        top_changes = [changes[id] for id in idx_list]
        # log.info("-------")
        if len(top_changes) > 0:
            try:
                await self.display(top_changes)
            except Exception as e:
                log.error(f"{e}")
