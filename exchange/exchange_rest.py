# our "broker" who is responsible for making the transactions on the exchange
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from credentials import getBinanceKey, getBinanceSecretKey
from constants import SYM, CANDLE_INTERVAL, HISTORICAL_DATA_RELATIVE_START_DATE
import numpy as np
from constants import SYM
from binance.enums import SIDE_BUY, FUTURE_ORDER_TYPE_MARKET

class ExchangeRest:
    def __init__(self) -> None:
        self.client=Client(getBinanceKey(), getBinanceSecretKey())

    def get_historical_ohlc(self):
        historical_klines = self.client.get_historical_klines(symbol = SYM, interval = CANDLE_INTERVAL, start_str=HISTORICAL_DATA_RELATIVE_START_DATE)
        historical_klines = [[float(x) for x in kline[1:6]] for kline in historical_klines]
        return np.array(historical_klines)
    
    def open_long(self, quantity):
        self.client.futures_create_order(symbol=SYM, side=SIDE_BUY, type=FUTURE_ORDER_TYPE_MARKET, quantity=quantity, isIsolated=True)

