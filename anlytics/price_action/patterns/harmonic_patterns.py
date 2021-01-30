from scipy.signal import argrelextrema
import numpy as np

from anlytics.price_action.patterns import PatternTypes


def peak_detection(prices, order=10):
    max_idx = list(argrelextrema(prices, np.greater, order=1)[0])
    min_idx = list(argrelextrema(prices, np.less, order=1)[0])

    idx = max_idx + min_idx + [len(prices) - 1]
    idx.sort()
    idx = idx[-5:]

    return idx, prices[idx]


def is_gartly_pattern(moves, error_allowed=10 / 100):
    XA, AB, BC, CD = moves
    AB_range = np.array([0.618 - error_allowed, 0.618 + error_allowed]) * abs(XA)
    BC_range = np.array([0.382 - error_allowed, 0.886 + error_allowed]) * abs(AB)
    CD_range = np.array([1.27 - error_allowed, 1.618 + error_allowed]) * abs(BC)
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return PatternTypes.BULLISH_GARTLEY

    elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(CD) < \
                CD_range[1]:
            return PatternTypes.BEARISH_GARTLEY


def is_butterfly_pattern(moves, error_allowed=10 / 100):
    XA, AB, BC, CD = moves
    AB_range = np.array([0.786 - error_allowed, 0.786 + error_allowed]) * abs(XA)
    BC_range = np.array([0.382 - error_allowed, 0.886 + error_allowed]) * abs(AB)
    CD_range = np.array([1.618 - error_allowed, 2.618 + error_allowed]) * abs(BC)
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(
                CD) < \
                CD_range[1]:
            return PatternTypes.BULLISH_GARTLEY

    elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(
                CD) < \
                CD_range[1]:
            return PatternTypes.BEARISH_GARTLEY


def is_bat_pattern(moves, error_allowed):
    XA, AB, BC, CD = moves
    AB_range = np.array([0.382 - error_allowed, 0.5 + error_allowed]) * abs(XA)
    BC_range = np.array([0.382 - error_allowed, 0.886 + error_allowed]) * abs(AB)
    CD_range = np.array([1.618 - error_allowed, 2.618 + error_allowed]) * abs(BC)
    if XA > 0 > AB and BC > 0 and CD < 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(
                CD) < \
                CD_range[1]:
            return PatternTypes.BULLISH_BAT

    elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(
                CD) < \
                CD_range[1]:
            return PatternTypes.BEARISH_BAT


def is_cab_pattern(moves, error_allowed):
    XA, AB, BC, CD = moves
    AB_range = np.array([0.382 - error_allowed, 0.618 + error_allowed]) * abs(XA)
    BC_range = np.array([0.382 - error_allowed, 0.886 + error_allowed]) * abs(AB)
    CD_range = np.array([2.24 - error_allowed, 3.618 + error_allowed]) * abs(BC)
    if XA > 0 and AB < 0 and BC > 0 and CD < 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(
                CD) < \
                CD_range[1]:
            return PatternTypes.BULLISH_CAB

    elif XA < 0 and AB > 0 and BC < 0 and CD > 0:
        if AB_range[0] < abs(AB) < AB_range[1] and BC_range[0] < abs(BC) < BC_range[1] and CD_range[0] < abs(
                CD) < \
                CD_range[1]:
            return PatternTypes.BEARISH_CAB
