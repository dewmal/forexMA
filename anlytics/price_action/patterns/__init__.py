import enum


class PatternTypes(str, enum.Enum):
    BEARISH_GARTLEY = "0"
    BULLISH_GARTLEY = "1"
    BEARISH_BUTTERFLY = "2"
    BULLISH_BUTTERFLY = "3"
    BEARISH_BAT = "4"
    BULLISH_BAT = "5"
    BEARISH_CAB = "6"
    BULLISH_CAB = "7"

    # Candle Patterns
    BEARISH_EVENING_STAR = "8"
    BEARISH_TWO_BLACK_GAPING = "9"
    BULLISH_ENGULFING = "10"
    BEARISH_ENGULFING = "11"
    BULLISH_HAMMER = "12"
