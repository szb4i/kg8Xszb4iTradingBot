import numpy as np
from constants import Candle

def get_ema(ohlc_array, window):
    closes = ohlc_array[:, Candle.CLOSE]

    alpha = 2 /(window + 1.0)
    alpha_rev = 1-alpha
    n = closes.shape[0]

    pows = alpha_rev**(np.arange(n+1))

    scale_arr = 1/pows[:-1]
    offset = closes[0]*pows[1:]
    pw0 = alpha*alpha_rev**(n-1)

    mult = closes*pw0*scale_arr
    cumsums = mult.cumsum()
    out = offset + cumsums*scale_arr[::-1]
    return out
