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
