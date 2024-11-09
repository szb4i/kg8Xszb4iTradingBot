# roty stategy comes here
import numpy as np
from technical_analysis.ema import get_ema
from technical_analysis.bollinger_bands import get_bollinger_bands
from constants import Candle

class Strategy:
    def __init__(self, historical_ohlc) -> None:
        self.ohlc = historical_ohlc
        self.__set_technical_indicators()
        self.is_in_long = False
        self.stop_loss = None
        self.quantity = None
        self.margin = None

    def on_exchange_ws_message(self, message):
        if message['x']:
            self.__set_ohlc(message)
            self.__set_technical_indicators()


    def __set_ohlc(self, message):
        np.append([message['k']['o'], message['k']['h'], message['k']['l'], message['k']['c'], message['k']['v']])

    def __set_technical_indicators(self):
        self.ema_5 = get_ema(self.ohlc, 5)
        self.ema_21 = get_ema(self.ohlc, 21)
        self.ema_55 = get_ema(self.ohlc, 55)

    def __open_long_position(self):
        if self.ema_21[-2] < self.ema_55[-2] and self.ema_21[-1] > self.ema_55[-1]:
            # TODO
            # 1. stoploss meghatarozasa: bollinger bands also
            self.__set_stop_loss()
            # 2. quantity es margin szamitasa
            self.__set_quantity()
            # 3. pozi megnyitasa
            # 4. nyitott pozicio managelese. on_message-ben ha poziban vagy, akkor minden message-re csekkolod, hogy le kell-e zarni. vagy trailing stop loss, ha jo iranyba megy
            # 5. logolas, email kuldes
            # 6. backtest

    def __set_stop_loss(self):
        threshold_bottom = 0.01
        threshold_top = 0.05
        bollinger_bands_last_bottom_price = get_bollinger_bands(self.ohlc)[2,-1]
        diff_relative = self.ohlc[-1, Candle.CLOSE]/bollinger_bands_last_bottom_price - 1
        if diff_relative > threshold_top:
            self.stop_loss = threshold_top
        elif diff_relative < threshold_bottom:
            self.stop_loss = threshold_bottom
        else:
            self.stop_loss = diff_relative

    def __set_quantity(self):
        # TODO
        # quantity es margin szamitasa
        # ennek a fuggvenynek lehetne generikusabb neve, mivel mindket valtozot allitja. set_trade_parameters? nemtom
        1


            
