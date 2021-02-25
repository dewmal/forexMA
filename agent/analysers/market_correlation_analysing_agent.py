import datetime
import logging

from agent import Agent
import numpy as np

from utils.timeit import log_time

log = logging.getLogger(Agent.Market_Correlation_Analysing_Agent)


class MarketCorrelationAnalysingAgent:
    def __init__(self, *args, **kwargs):
        pass

    @log_time(logger=log, log_off=False)
    async def accept_message(self, agent, message):
        log.info(f"{agent=}")
        try:
            values_list = message['data']
            p_changes = np.array([d["P"] for d in values_list]).astype(np.float32)
            p_changes_2d = np.vstack([p_changes for i in range(len(p_changes))])
            p_changes_corr = p_changes_2d / p_changes_2d.T
            p_changes_corr = np.nan_to_num(p_changes_corr, neginf=0, posinf=0)
            max_corr = p_changes_corr.max()
            min_corr = p_changes_corr.min()
            max_val_indexes = np.argwhere((p_changes_corr == max_corr) | (p_changes_corr == min_corr))

            for val_index in max_val_indexes:
                x, y = val_index[0], val_index[1]
                corr = p_changes_corr[x, y]
                y_asset = values_list[y]
                x_asset = values_list[x]
                log.info(f"{corr=} {y_asset['s']=} {x_asset['s']=}")


        except Exception as e:
            log.error(e)
