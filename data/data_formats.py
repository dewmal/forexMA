import enum
import math
from dataclasses import dataclass


@dataclass
class MarketStatus:
    time_stamp: int
    asset_name: str
    open: float
    high: float
    low: float
    close: float
    volume: int = 0
    _id: str = ""

    def to_dict(self):
        dt = {
            "_id": self._id,
            "time_stamp": self.time_stamp,
            "asset_name": self.asset_name,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
        }
        if self._id or self._id == "":
            del dt["_id"]
        return dt

    @staticmethod
    def from_dict(data):
        dt = MarketStatus(
            _id=data["_id"],
            time_stamp=int(data["time_stamp"]),
            asset_name=data["asset_name"],
            open=data["open"],
            high=data["high"],
            low=data["low"],
            close=data["close"],
            volume=data["volume"],
        )
        return dt


@dataclass
class TextData:
    time_stamp: int
    text: str
    _id: str = ""

    def to_dict(self):
        dt = {
            "_id": self._id,
            "time_stamp": self.time_stamp,
            "text": self.text
        }
        if self._id or self._id == "":
            del dt["_id"]
        return dt

    @staticmethod
    def from_dict(data):
        dt = TextData(
            _id=data["_id"],
            time_stamp=int(data["time_stamp"]),
            text=data["text"]
        )
        return dt


class MarketDirection(enum.Enum):
    BUY = "UP"
    SELL = "DOWN"
    STAY = "NULL"

    @staticmethod
    def value_of(value):
        for m, mm in MarketDirection.__members__.items():
            if m == value.upper():
                return mm


@dataclass
class FactPattern:
    time_stamp: int
    asset_name: str
    expected_change: float
    direction: MarketDirection
    accuracy: float
    _id: str = ""

    def to_dict(self):
        dt = {
            "_id": self._id,
            "time_stamp": self.time_stamp,
            "asset_name": self.asset_name,
            "expected_change": self.expected_change,
            "direction": self.direction.value,
            "accuracy": self.accuracy,
        }
        if self._id or self._id == "":
            del dt["_id"]
        return dt

    @staticmethod
    def from_dict(data):
        dt = FactPattern(
            _id=data["_id"],
            time_stamp=int(data["time_stamp"]),
            asset_name=data["asset_name"],
            expected_change=data["expected_change"],
            direction=MarketDirection.value_of(data["direction"]),
            accuracy=data["accuracy"],
        )
        return dt


@dataclass
class Action:
    time_stamp: int
    action_end_time: int
    asset_name: str
    predicted_action: MarketDirection
    predicted_price_variation: float
    accuracy: float
    _id: str = ""
    actual_price: float = 0
    reward: float = -math.inf

    def to_dict(self):
        dt = {
            "_id": self._id,
            "time_stamp": self.time_stamp,
            "action_end_time": self.action_end_time,
            "asset_name": self.asset_name,
            "predicted_action": self.predicted_action.value,
            "predicted_price_variation": self.predicted_price_variation,
            "accuracy": self.accuracy,
            "reward": self.reward,
            "actual_price": self.actual_price,
        }
        if self._id or self._id == "":
            del dt["_id"]
        return dt

    @staticmethod
    def from_dict(data):
        dt = Action(
            _id=data["_id"],
            time_stamp=int(data["time_stamp"]),
            action_end_time=int(data["action_end_time"]),
            asset_name=data["asset_name"],
            predicted_action=MarketDirection.value_of(data["predicted_action"]),
            predicted_price_variation=data["predicted_price_variation"],
            accuracy=data["accuracy"],
            reward=data["reward"],
            actual_price=data["actual_price"],
        )
        return dt


@dataclass
class AgentPerformance:
    name: str
    performance: float
    time_stamp: int
    _id: str = ""

    def to_dict(self):
        dt = {
            "_id": self._id,
            "time_stamp": self.time_stamp,
            "name": self.name,
            "performance": self.performance,
        }
        if self._id or self._id == "":
            del dt["_id"]
        return dt

    @staticmethod
    def from_dict(data):
        dt = AgentPerformance(
            _id=data["_id"],
            time_stamp=int(data["time_stamp"]),
            performance=data["performance"],
            name=data["name"]
        )
        return dt
