import logging

from agent import Agent
from agent_helpers import message_filter
from data.data_formats import FactPattern, MarketStatus, Action, MarketDirection
from data.mock_data_generator import gen_action

log = logging.getLogger(Agent.Decision_Agent)


def print(*args, **kwargs):
    log.info(f"{args=}")


class DecisionAgent:
    publish = None
    display = None

    decisions_history = {}
    market_data = {}

    open_decision = False

    def __init__(self, *args, **kwargs):
        log.info(f"{self} Start")

    async def start(self):
        # await self.publish("AgentTwo", "Hi Agent 2")
        pass

    async def accept_message(self, agent, message):
        await self.market_status(agent=agent, status=message)
        await self.pattern_analysis(agent=agent, pattern=message)

    async def stop(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        pass

    @message_filter(message_type=MarketStatus, param_name="status")
    async def market_status(self, agent, status: MarketStatus):
        self.market_data[f"{status.time_stamp}"] = status
        select_time = f"{status.time_stamp}"
        if select_time in self.decisions_history:
            action: Action = self.decisions_history[select_time]
            action_end_time = f"{action.time_stamp}"
            if action_end_time in self.market_data:
                start_status: MarketStatus = self.market_data[action_end_time]
                apv = round((status.close - start_status.close) * 10e4)
                ppv = action.predicted_price_variation
                pa = action.predicted_action

                ##Driection
                aa = MarketDirection.BUY if apv > 0 else MarketDirection.STAY if apv == 0 else MarketDirection.SELL
                if aa == pa:
                    ## Reward Calculation
                    reward = 1 - abs(apv - ppv) / ((apv + ppv) / 2)
                    reward = 0 if reward < 0 else reward
                else:
                    reward = 0

                print(f"{apv=},{ppv=} , {reward=}")

                action.reward = reward
                action.actual_price = status.close

                await self.publish(Agent.Performance_Analysing_Agent, action)
                self.open_decision = False

    @message_filter(message_type=MarketStatus, param_name="pattern")
    async def pattern_analysis(self, agent, pattern: FactPattern):
        action = gen_action(time_stamp=pattern.time_stamp, asset_name=pattern.asset_name)
        if action and action.accuracy > 75:
            print(f"{action.to_dict()=}")
            self.decisions_history[f"{action.action_end_time}"] = action
            await self.display(action.to_dict())
            await self.publish(Agent.Performance_Analysing_Agent, action.to_dict())
            self.open_decision = True
