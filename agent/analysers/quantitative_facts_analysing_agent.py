import logging
import queue

import numpy as np
from agent import Agent
from agent_helpers import message_filter
from anlytics.price_action.patterns import PatternTypes
from anlytics.price_action.patterns.harmonic_patterns import peak_detection, is_gartly_pattern, is_butterfly_pattern, \
    is_bat_pattern, is_cab_pattern
from anlytics.price_action.price_action_pattern_analyser import PriceActionPatternAnalyser
from data.data_formats import MarketStatus, MarketDirection
from data.mock_data_generator import gen_fact_pattern, gen_fact_pattern_mock

log = logging.getLogger(Agent.Quantitative_FAAgent)


def print(*args, **kwargs):
    log.info(f"{args=}")


class QuantitativeFAAgent:
    publish = None
    display = None
    history_records = []
    max_history_records = 100

    def __init__(self, *args, **kwargs):
        self.max_size = 50
        self.__buffer = queue.Queue(maxsize=self.max_size)
        self.error_rate = 0.0001
        self.pattern_id = 0
        self.selected_pattern = {}

    async def start(self):
        # await self.publish("AgentTwo", "Hi Agent 2")
        pass

    async def accept_message(self, agent, message):
        res = await self.quantitative_facts_analysis(agent=agent, data=message)

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        pass

    @message_filter(message_type=MarketStatus, param_name="data")
    async def quantitative_facts_analysis(self, agent, data: MarketStatus):
        # self.__buffer.put((data.time_stamp, data.close))
        self.__buffer.put((data.time_stamp, data.close))
        if self.__buffer.qsize() >= self.max_size:
            data_values = np.array(list(self.__buffer.queue))
            price_values = data_values[:, 1]
            time_stamp_values = data_values[:, 0]

            idx, pattern = peak_detection(price_values, order=45)

            if len(idx) >= 5:
                XA = pattern[1] - pattern[0]
                AB = pattern[2] - pattern[1]
                BC = pattern[3] - pattern[2]
                CD = pattern[4] - pattern[3]
                moves = [XA, AB, BC, CD]

                pattern_gartly = is_gartly_pattern(moves=moves, error_allowed=self.error_rate)
                pattern_butterfly = is_butterfly_pattern(moves=moves, error_allowed=self.error_rate)
                pattern_bat = is_bat_pattern(moves=moves, error_allowed=self.error_rate)
                pattern_cab = is_cab_pattern(moves=moves, error_allowed=self.error_rate)
                patterns, direction = [], None
                if pattern_cab or pattern_butterfly or pattern_bat or pattern_gartly:
                    log.info(f"Pattern {pattern_bat=},{pattern_cab=},{pattern_gartly=},{pattern_butterfly=}")
                    pattern_points = [tuple(data_values[id]) for id in idx]
                    # print(f"{pattern_points=}")
                    pattern_diff = pattern_points[0][1] - pattern_points[-1][1]
                    expected_change = abs(round(pattern_diff * 10e5) * 10 / 100)
                    if pattern_cab:
                        direction = MarketDirection.SELL if pattern_cab == PatternTypes.BEARISH_CAB else MarketDirection.BUY
                    if pattern_gartly:
                        direction = MarketDirection.SELL if pattern_cab == PatternTypes.BEARISH_GARTLEY else MarketDirection.BUY
                    if pattern_bat:
                        direction = MarketDirection.SELL if pattern_cab == PatternTypes.BEARISH_BAT else MarketDirection.BUY
                    if pattern_butterfly:
                        direction = MarketDirection.SELL if pattern_cab == PatternTypes.BEARISH_BUTTERFLY else MarketDirection.BUY

                    if direction:
                        pattern = gen_fact_pattern(time_stamp=data.time_stamp,
                                                   asset_name=data.asset_name,
                                                   expected_change=expected_change,
                                                   accuracy=90,
                                                   direction=direction)
                        await self.display(pattern.to_dict())
                        await self.publish(Agent.Decision_Agent, pattern)

            self.__buffer.get()

        # pattern = gen_fact_pattern_mock(time_stamp=data.time_stamp,
        #                                 asset_name=data.asset_name)
        # await self.display(pattern.to_dict())
        # await self.publish(Agent.Decision_Agent, pattern)
