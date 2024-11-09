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
        self.capital_at_risk=0.03
        self.leverage = 6

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
            self.__set_stop_loss()
            self.__set_quantity()
            # TODO
            # 3. pozi megnyitasa
            # 4. nyitott pozicio managelese. on_message-ben ha poziban vagy, akkor minden message-re csekkolod, hogy le kell-e zarni. vagy trailing stop loss, ha jo iranyba megy
            # 5. logolas, email kuldes
            # 6. backtest

    def __set_stop_loss(self):
        threshold_bottom = self.ohlc[-1, Candle.CLOSE] * (1 - 0.05)
        threshold_top = self.ohlc[-1, Candle.CLOSE] * (1 - 0.005)
        bollinger_bands_last_bottom_price = get_bollinger_bands(self.ohlc)[2,-1]

        # if in position, check if SL can be modified
        if self.stop_loss is not None:
            if bollinger_bands_last_bottom_price > self.stop_loss:
                self.stop_loss = bollinger_bands_last_bottom_price
        else:
            if bollinger_bands_last_bottom_price > threshold_top:
                self.stop_loss = threshold_top
            elif bollinger_bands_last_bottom_price < threshold_bottom:
                self.stop_loss = threshold_bottom
            else:
                self.stop_loss = bollinger_bands_last_bottom_price

    def __set_quantity(self):
        # a toke hany szazalekaval nyitunk poziciot, 0 es (100*leverage) % kozotti ertek
        position_size_pct_of_capital = self.capital_at_risk / (1 - self.stop_loss / self.ohlc[-1, Candle.CLOSE])
        usdc_capital = ExchangeRest.futures_usdc_balance 
        # ezt nem tudom honnan kéne, elkezdtem az ExchangeRest classban egy új attribútumot (?), 
        # de nem vagyok benne biztos h igy kéne, pls gondold már át te is.
        # vagy behivni a get_futures_usdc_balance fuggvenyt csak az kicsit lassithat a pozinyitásunkon
        position_size = position_size_pct_of_capital * usdc_capital
        return position_size