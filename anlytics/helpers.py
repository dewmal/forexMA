import numpy as np
from scipy.signal import argrelextrema


def peak_detection(prices, order=10):
    max_idx = list(argrelextrema(prices, np.greater, order=1)[0])
    min_idx = list(argrelextrema(prices, np.less, order=1)[0])

    idx = max_idx + min_idx + [len(prices) - 1]
    idx.sort()
    idx = idx[-5:]

    return idx, prices[idx]
