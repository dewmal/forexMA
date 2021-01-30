import random

from data.data_formats import MarketStatus, TextData, FactPattern, Action, MarketDirection


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


def gen_fact_pattern_mock(time_stamp, asset_name):
    status = FactPattern(
        time_stamp=time_stamp,
        asset_name=asset_name,
        accuracy=random.random() * 100,
        expected_change=random.random(),
        direction=random.choice((MarketDirection.SELL, MarketDirection.BUY, MarketDirection.STAY)),
    )
    return status


def gen_fact_pattern(time_stamp, asset_name, direction, expected_change, accuracy):
    status = FactPattern(
        time_stamp=time_stamp,
        asset_name=asset_name,
        accuracy=accuracy,
        expected_change=expected_change,
        direction=direction,
    )
    return status


def gen_action_mock(time_stamp, asset_name):
    duration = round(random.random() * 10)
    if duration > 0:
        status = Action(
            time_stamp=time_stamp,
            asset_name=asset_name,
            accuracy=random.random() * 100,
            action_end_time=(duration * 60) + time_stamp,
            predicted_action=random.choice((MarketDirection.SELL, MarketDirection.BUY)),
            predicted_price_variation=round(random.random() * 10),
        )
        return status


def gen_action(time_stamp, asset_name, accuracy, direction, price_change, duration=5):
    status = Action(
        time_stamp=time_stamp,
        asset_name=asset_name,
        accuracy=accuracy,
        action_end_time=(duration * 60) + time_stamp,
        predicted_action=direction,
        predicted_price_variation=price_change,
    )
    return status
