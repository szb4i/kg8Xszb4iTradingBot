import numpy as np

def get_sma(ohlc_array, window):
    closes = ohlc_array[:, 3]
    return np.convolve(closes, np.ones(window), 'valid') / window