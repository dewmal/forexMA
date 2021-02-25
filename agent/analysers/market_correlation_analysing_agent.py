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
            max_val_index = np.argwhere(p_changes_corr == max_corr)

            y_asset = values_list[max_val_index[0, 0]]
            x_asset = values_list[max_val_index[0, 1]]

            log.info(f"{max_corr=}")
            log.info(f"{y_asset['s']=} {x_asset['s']=}")
            log.info(f"{y_asset['P']=} {x_asset['P']=}")


        except Exception as e:
            log.error(e)
