import asyncio
import logging
import pandas as pd
from click import open_file

from agent import Agent
from data.data_formats import TextData

log = logging.getLogger(Agent.News_Reading_Agent)


def print(*args, **kwargs):
    log.info(f"{args=}")


class NewsReadingAgent:
    publish = None
    display = None

    def __init__(self, *args, **kwargs):
        log.info(f"{self} Start")

    async def start(self):
        self.df = pd.read_csv("_data_/data/news/USD-EUR_16-17.csv")

    async def accept_message(self, agent, message):
        pass

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        print("Reading news")
        for news_dt in self.df.News.values:
            status = TextData(
                time_stamp=-1,
                text=f"{str(news_dt)}"
            )
            await self.publish(Agent.Qualitative_FAAgent, status.to_dict())
            await self.display(status.to_dict())
            await asyncio.sleep(2)

        # news = df.News[0]
        # print(f"{news=}")

        # while True:
        #     status = gen_market_text_data()
        #     await self.publish(Agent.Qualitative_FAAgent, status.to_dict())
        #     await self.display(status.to_dict())
        #     await asyncio.sleep(50)
