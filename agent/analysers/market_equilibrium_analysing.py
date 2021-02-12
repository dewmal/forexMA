import asyncio
import logging
import traceback
from datetime import datetime, timedelta

import aiohttp
import numpy as np

from agent import Agent
from anlytics.helpers import peak_detection
from utils.timeit import log_time

log = logging.getLogger(Agent.Market_Equilibrium_Analysing_Agent)


class MarketEquilibriumAnalysingAgent:
    history = {}
    max_minutes = 60 * 5
    best_assets = 10
    top_count = {

    }

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
                    if time_diff.total_seconds() > self.max_minutes:
                        pp = self.history[name].pop(0)
                        continue
                break

            if len(self.history[name]) > max_length:
                max_length = len(self.history[name])

        accepted_length = max_length * 0.95
        # log.info(f"{accepted_length=}")
        detected_assets = []
        if max_length > 100:
            for key, his in self.history.items():
                if len(his) > accepted_length:
                    close_prices = np.array([p["c"] for p in his]).astype(np.float)
                    idxs, peaks_points = peak_detection(close_prices)

                    max_peak_p = np.max(peaks_points)
                    min_peak_p = np.min(peaks_points)
                    max_diff = max_peak_p - min_peak_p
                    changes = []
                    for idx in range(len(peaks_points) - 1):
                        p_val = close_prices[idxs[idx]]
                        p_val_next = close_prices[idxs[idx + 1]]
                        if (p_val != max_peak_p and p_val_next != min_peak_p) and (
                                p_val != min_peak_p and p_val_next != max_peak_p):
                            diff = abs(p_val - p_val_next)
                            diff_precentage = diff / max_diff
                            changes.append(diff_precentage)

                    peak_avg = np.average(np.array([changes]))

                    detected_assets.append({
                        "name": key,
                        "peaks_count": 0,
                        "peak_average": float(peak_avg)
                    })

        if len(detected_assets) > 0:
            changes_ar = np.array([c["peak_average"] for c in detected_assets]).astype(np.float)
            idx_list = np.argsort(-changes_ar)[:self.best_assets]
            top_changes = []

            for idx in idx_list:
                top_change = detected_assets[idx]
                key = top_change["name"]
                # Calculate how many times this appeared
                if key in self.top_count:
                    self.top_count[key] += 1
                else:
                    self.top_count[key] = 1

                top_change["peaks_count"] = self.top_count[key]
                top_changes.append(top_change)

            await self.display(top_changes)
