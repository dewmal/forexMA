import asyncio
import logging
from datetime import datetime, timedelta

import aiohttp
import numpy as np

from agent import Agent
from utils.timeit import log_time

log = logging.getLogger(Agent.Market_Trend_Analysing_Agent)


async def fetch(session, url, id=None):
    """Execute an http call async
    Args:
        session: contexte for making the http call
        url: URL to call
    Return:
        responses: A dict like object containing http response
    """
    async with session.get(url) as response:
        resp = await response.json()
        if not id:
            return resp
        return {
            "id": id,
            "data": resp
        }


class MarketTrendAnalysingAgent:
    history = {}
    max_minutes = 60 * 5
    best_assets = 10

    def __init__(self, *args, **kwargs):
        pass

    @log_time(logger=log, log_off=True)
    async def accept_message(self, agent, message):
        max_length = 0
        for dt in message:
            time = datetime.fromtimestamp(int(dt["C"]) / 1000)
            name = dt["s"]
            if name not in self.history:
                self.history[name] = [dt]
            else:
                self.history[name].append(dt)
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
                # await self.display(top_changes)
                depths = await self.fetch_all_market_depth([v["name"] for v in top_changes])
                balance_powers = await self.analyse_depth(depths)
                if balance_powers:
                    top_changes = [{
                        **list(filter(lambda x: x["name"] == tc["name"], balance_powers))[0],
                        **tc} for tc in top_changes]
                    log.info(f"{top_changes =}")
                    await self.display(top_changes)

            except Exception as e:
                log.error(f"{e}")

    async def analyse_depth(self, depths):
        async def analyse(depth):
            name = depth["id"]
            data = depth["data"]
            asks = np.array(data["asks"]).astype(np.float)
            bids = np.array(data["bids"]).astype(np.float)
            asks_pow = np.sum(np.prod(asks, axis=1))
            bids_pow = np.sum(np.prod(bids, axis=1))
            balance = asks_pow - bids_pow

            return {
                "name": name,
                "balance": float(balance),
                "direction": "UP" if asks_pow > bids_pow else "DOWN"
            }

        return await asyncio.gather(*[analyse(depth) for depth in depths], return_exceptions=True)

    async def fetch_all_market_depth(self, symbols):
        """ Gather many HTTP call made async
        Args:
            cities: a list of string
        Return:
            responses: A list of dict like object containing http response
        """
        async with aiohttp.ClientSession() as session:
            tasks = []
            for symbol in symbols:
                url = f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=100"
                tasks.append(
                    fetch(
                        session, url, id=symbol
                    )
                )
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            return responses

    async def analyse_order_depth(self, symbol):
        url = f""
