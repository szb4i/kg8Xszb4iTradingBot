# roty stategy comes here
import numpy as np
from technical_analysis.ema import get_ema

class Strategy:
    def __init__(self, historical_ohlc) -> None:
        self.ohlc = historical_ohlc
        self.set_technical_indicators()
        self.is_in_long = False

    def on_exchange_ws_message(self, message):
        if message['x']:
            self.set_ohlc(message)
            self.set_technical_indicators()


    def set_ohlc(self, message):
        np.append([message['k']['o'], message['k']['h'], message['k']['l'], message['k']['c'], message['k']['v']])

    def set_technical_indicators(self):
        self.ema_5 = get_ema(self.historical_ohlc, 5)
        self.ema_21 = get_ema(self.historical_ohlc, 21)
        self.ema_55 = get_ema(self.historical_ohlc, 55)

    def open_long_position(self):
        if self.ema_21[-2] < self.ema_55[-2] and self.ema_21[-1] > self.ema_55[-1]:
            # TODO
            # 1. stoploss meghatarozasa: bollinger bands also -> trade_quantity szamitasa
            # 2. pozi megnyitasa
            # 3. nyitott pozicio managelese. on_message-ben ha poziban vagy, akkor minden message-re csekkolod, hogy le kell-e zarni. vagy trailing stop loss, ha jo iranyba megy
            # 4. logolas, email kuldes
            # 5. backtest
            
