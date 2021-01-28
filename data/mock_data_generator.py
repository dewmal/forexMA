import random

from data.data_formats import MarketStatus, TextData, FactPattern


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


def gen_market_text_data():
    status = TextData(
        time_stamp=round(random.random() * 10e5),
        text=f"this kind of thing before {random.random()}",
    )
    return status


def gen_fact_pattern():
    status = FactPattern(
        time_stamp=round(random.random() * 10e5),
        asset_name="EURUSD",
        accuracy=random.random(),
        expected_change=random.random(),
        direction=random.choice(("UP", "DOWN", "NULL"))
    )
    return status
