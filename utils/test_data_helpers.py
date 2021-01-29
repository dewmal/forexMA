from data.data_formats import MarketStatus


def convert_data_frame_to_market_status(values, asset_name) -> MarketStatus:
    time_stamp = values[0]
    open, high, low, close = values[1], values[2], values[3], values[4]
    market_status = MarketStatus(
        time_stamp=int(time_stamp),
        asset_name=asset_name,
        open=open,
        high=high,
        low=low,
        close=close
    )
    return market_status
