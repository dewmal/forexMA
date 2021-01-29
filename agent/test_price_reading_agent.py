import asyncio
import logging
import pandas as pd
import numpy as np
from agent import Agent
from data.data_formats import MarketStatus
from utils.binary_api_helpers import convert_message_to_environment
from utils.test_data_helpers import convert_data_frame_to_market_status

log = logging.getLogger(Agent.Price_Reading_Agent)

input_column_names = ["DATE", "TIME", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
output_column_names = ["timestamp", "pac", "ppv", "aac", "apv", "reward"]


def print(*args, **kwargs):
    log.info(f"{args=}")


class PriceReadingAgent:
    publish = None
    display = None
    last_candle: MarketStatus = None

    def __init__(self, *args, **kwargs):
        self.data_path_prefix = "_data_/data/eur_usd/5m/EURUSD5"

    async def start(self):
        pass

    async def process_message(self, message):
        price_status_list = convert_message_to_environment(message)
        for status in price_status_list:
            if not self.last_candle:
                self.last_candle = status

            if self.last_candle.time_stamp < status.time_stamp:
                await self.publish(Agent.Quantitative_FAAgent, self.last_candle)
                await self.publish(Agent.Performance_Analysing_Agent, self.last_candle)
                await self.publish(Agent.Decision_Agent, self.last_candle)
                await self.display(self.last_candle.to_dict())

            self.last_candle = status

    async def accept_message(self, agent, message):
        pass

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        col_names = input_column_names
        df = pd.read_csv(f"{self.data_path_prefix}.csv", names=col_names)
        df_pre = pd.DataFrame()
        df_pre["timestamp"] = pd.to_datetime(df.DATE + " " + df.TIME)
        df_pre["timestamp"] = df_pre.timestamp.values.astype(np.int64) // 10 ** 9
        df_pre["open"] = df.OPEN.astype(np.float)
        df_pre["high"] = df.HIGH.astype(np.float)
        df_pre["low"] = df.LOW.astype(np.float)
        df_pre["close"] = df.CLOSE.astype(np.float)
        df_pre["vol"] = df.VOLUME.astype(np.int64)
        log.info(df_pre.head())
        log.info(df_pre.tail())
        for value in df_pre.values:
            market_status = convert_data_frame_to_market_status(value, "EUR_USD")
            await self.publish(Agent.Quantitative_FAAgent, market_status)
            await self.publish(Agent.Performance_Analysing_Agent, market_status)
            await self.publish(Agent.Decision_Agent, market_status)
            await self.display(market_status.to_dict())
            await asyncio.sleep(1)

        # await self.exit()
