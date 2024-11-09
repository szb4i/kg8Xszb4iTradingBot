import numpy as np
from constants import Candle

def get_sma(ohlc_array, window):
    closes = ohlc_array[:, Candle.CLOSE]
    return np.convolve(closes, np.ones(window), 'valid') / window