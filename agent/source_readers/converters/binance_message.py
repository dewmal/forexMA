from data.data_formats import MarketStatus


def get_market_status(dms) -> MarketStatus:
    asset_name = dms["s"]
    time_stamp = dms["C"]
    open, close, high, low = dms["o"], dms["c"], dms["h"], dms["l"]
    status = MarketStatus(
        time_stamp=int(time_stamp),
        open=float(open),
        close=float(close),
        high=float(high),
        low=float(low),
        asset_name=asset_name
    )
    return status


def get_market_status_from_kline(kline) -> MarketStatus:
    kline = kline["k"]
    asset_name = kline["s"]
    time_stamp = kline["T"]
    open, close, high, low = kline["o"], kline["c"], kline["h"], kline["l"]
    volume = kline["v"]
    status = MarketStatus(
        time_stamp=int(time_stamp),
        open=float(open),
        close=float(close),
        high=float(high),
        low=float(low),
        asset_name=asset_name,
        volume=volume
    )
    return status
