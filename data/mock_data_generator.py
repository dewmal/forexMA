import random

from data.price_data import MarketStatus


def gen_market_status():
    status = MarketStatus(
        asset_name="EURUSD",
        open=random.random(),
        high=random.random(),
        low=random.random(),
        close=random.random(),
        time_stamp=round(random.random() * 10e5),
        volume=round(random.random() * 10e2),
    )
    return status
