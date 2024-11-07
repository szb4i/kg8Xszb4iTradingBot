# gloal file for constants. we can add more specific constant files later on - e.g. exchnage_constants.py

from binance import Client

SYM = 'BTCUSDT'
CANDLE_INTERVAL = Client.KLINE_INTERVAL_1HOUR
HISTORICAL_DATA_RELATIVE_START_DATE = '100 hour ago'

RISK = 0.03
