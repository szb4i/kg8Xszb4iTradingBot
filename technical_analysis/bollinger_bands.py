import numpy as np
from technical_analysis.sma import get_sma
from constants import Candle

def get_bollinger_bands(ohlc_array, window=20, band_width=2):
    sma = get_sma(ohlc_array, window)
    closes = ohlc_array[:, Candle.CLOSE]
    std = np.std([closes[i:i+window] for i in range(len(closes)-window+1)], axis=1)
    bb_top = sma + band_width*std
    bb_bottom = sma - band_width*std
    return [bb_top, sma, bb_bottom]
