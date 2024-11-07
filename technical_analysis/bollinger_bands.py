import numpy as np
from technical_analysis.sma import get_sma

def get_bollinger_bands(ohlc_array, window, band_width=2):
    sma = get_sma(ohlc_array, window)
    closes = ohlc_array[:, 3]
    std = np.std([closes[i:i+window] for i in range(len(closes)-window+1)], axis=1)
    bb_up = sma + band_width*std
    bb_down = sma - band_width*std
    return [bb_up, sma, bb_down]
