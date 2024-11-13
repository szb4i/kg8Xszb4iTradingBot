# our "broker" who is responsible for making the transactions on the exchange
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from credentials import getBinanceKey, getBinanceSecretKey
from constants import SYM, CANDLE_INTERVAL, HISTORICAL_DATA_RELATIVE_START_DATE
import numpy as np
from constants import SYM
from binance.enums import SIDE_BUY, SIDE_SELL, FUTURE_ORDER_TYPE_MARKET, FUTURE_ORDER_TYPE_STOP_MARKET, TIME_IN_FORCE_GTC

class ExchangeRest:
    def __init__(self) -> None:
        self.client=Client(getBinanceKey(), getBinanceSecretKey())

    def get_historical_ohlc(self):
        historical_klines = self.client.get_historical_klines(symbol = SYM, interval = CANDLE_INTERVAL, start_str=HISTORICAL_DATA_RELATIVE_START_DATE)
        historical_klines = [[float(x) for x in kline[1:6]] for kline in historical_klines]
        return np.array(historical_klines)
    
    def open_long(self, quantity, stop_loss):
        self.client.futures_create_order(symbol=SYM, side=SIDE_BUY, type=FUTURE_ORDER_TYPE_MARKET, quantity=quantity, isIsolated=True)
        # TODO
        # stop_loss-t folyamatosna frissiteni kellene. eloszor bollinger miatt, aztan a trailing sl miatt. megoldhato az, hogy toroljuk az elozo ordert, es helyette ujat hozunk letre? tehat frissitjuk a stop pricet?

        self.client.futures_create_order(symbol=SYM,side=SIDE_SELL,type=FUTURE_ORDER_TYPE_STOP_MARKET,timeInForce=TIME_IN_FORCE_GTC,quantity=quantity,stopPrice=stop_loss, isIsolated=True)

    def update_long(self, stop_loss):
        # TODO
        # ezt a fuggvenyt kene hivni, amikor csak a stoplosson valtoztatunk mar pozi kozben
        1

    def get_futures_usdc_balance(self):
        futures_usdc_balance = float(next((item['availableBalance'] for item in self.client.futures_account_balance() if item['asset'] == 'USDC'), 0))
        return futures_usdc_balance