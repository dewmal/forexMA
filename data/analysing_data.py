from dataclasses import dataclass


@dataclass
class MarketTrendAsset:
    asset_name: str
    time_stamp: float
    price: float
    change: float
    count: int
    _id: str = ""

    def to_dict(self):
        dt = {
            "_id": self._id,
            "time_stamp": self.time_stamp,
            "asset_name": self.asset_name,
            "change": self.change,
            "price": self.price,
            "count": self.count,
        }
        if self._id or self._id == "":
            del dt["_id"]
        return dt

    @staticmethod
    def from_dict(data):
        dt = MarketTrendAsset(
            _id=data["_id"],
            time_stamp=int(data["time_stamp"]),
            asset_name=data["asset_name"],
            price=data["price"],
            change=data["change"],
            count=data["count"],
        )
        return dt
