# roty stategy comes here
import numpy as np
from technical_analysis.ema import get_ema
from technical_analysis.bollinger_bands import get_bollinger_bands
from constants import Candle
from exchange.exchange_rest import ExchangeRest

CAPITAL_RISK = 0.03
STOPLOSS_THRESHOLD_BOTTOM_RATIO = 0.05
STOPLOSS_THRESHOLD_TOP_RATIO = 0.005

class Strategy:
    def __init__(self, historical_ohlc) -> None:
        self.ohlc = historical_ohlc
        self.__set_technical_indicators()
        self.exchange_rest = ExchangeRest()
        self.balance = self.exchange_rest.get_futures_usdc_balance()
        self.leverage = 6

    def __set_variables_to_default(self):
        self.is_in_long = False
        self.stop_loss = None
        self.is_trailing_stop_loss = False
        self.trailing_stop_loss_step_ratio = None
        self.take_profit_virtual = None
        self.quantity = None

    def on_exchange_ws_message(self, message):
        is_candle_closing = message['x']
        if is_candle_closing:
            self.__set_ohlc(message)
            self.__set_technical_indicators()
            if not self.is_in_long:
                self.__open_long_position()
        if self.is_in_long:
            current_price = message['k']['c']
            self.__manage_long_position(current_price, is_candle_closing)

    def __set_ohlc(self, message):
        np.append([message['k']['o'], message['k']['h'], message['k']['l'], message['k']['c'], message['k']['v']])

    def __set_technical_indicators(self):
        self.ema_5 = get_ema(self.ohlc, 5)
        self.ema_21 = get_ema(self.ohlc, 21)
        self.ema_55 = get_ema(self.ohlc, 55)
        self.bollinger_bands = get_bollinger_bands(self.ohlc)

    def __open_long_position(self):
        if self.ema_21[-2] < self.ema_55[-2] and self.ema_21[-1] > self.ema_55[-1]:
            self.__set_stop_loss_init()
            self.__set_take_profit_virtual()
            self.__set_trailing_stop_loss_step_ratio()
            self.__set_quantity()
            self.exchange_rest.open_long(self.quantity)
            self.is_in_long = True
            # TODO
            # 5. logolas, email kuldes
            # 6. backtest

    def __set_stop_loss_init(self):
        threshold_bottom = self.ohlc[-1, Candle.CLOSE] * (1 - STOPLOSS_THRESHOLD_BOTTOM_RATIO)
        threshold_top = self.ohlc[-1, Candle.CLOSE] * (1 - STOPLOSS_THRESHOLD_TOP_RATIO)
        bollinger_bands_last_bottom_price = self.bollinger_bands[2,-1]
        if bollinger_bands_last_bottom_price > threshold_top:
            self.stop_loss = threshold_top
        elif bollinger_bands_last_bottom_price < threshold_bottom:
            self.stop_loss = threshold_bottom
        else:
            self.stop_loss = bollinger_bands_last_bottom_price

    def __set_take_profit_virtual(self):
        self.take_profit_virtual = self.ohlc[-1, Candle.CLOSE] + (self.ohlc[-1, Candle.CLOSE] - self.stop_loss)

    def __set_trailing_stop_loss_step_ratio(self):
        self.trailing_stop_loss_step_ratio = (1 - (self.stop_loss / self.ohlc[-1, Candle.CLOSE])) / 4

    def __set_quantity(self):
        # a toke hany szazalekaval nyitunk poziciot, 0 es (100*leverage) % kozotti ertek
        position_size_pct_of_capital = CAPITAL_RISK / (1 - self.stop_loss / self.ohlc[-1, Candle.CLOSE])
        usdc_capital = ExchangeRest.futures_usdc_balance 
        # ezt nem tudom honnan kéne, elkezdtem az ExchangeRest classban egy új attribútumot (?), 
        # de nem vagyok benne biztos h igy kéne, pls gondold már át te is.
        # vagy behivni a get_futures_usdc_balance fuggvenyt csak az kicsit lassithat a pozinyitásunkon
        position_size = position_size_pct_of_capital * usdc_capital
        return position_size
    
    def __manage_long_position(self, current_price, is_candle_closing):
        self.__close_long_position()
        if self.is_in_long:
            self.__set_stop_loss_live(current_price, is_candle_closing)

    def __close_long_position(self, current_price):
        if current_price < self.stop_loss:
            # TODO
            # close_long fuggveny implementalasa az ExchangeRestben
            self.__set_variables_to_default()

    def __set_stop_loss_live(self, current_price, is_candle_closing):
        # TODO
        # ha valtozik a stop_loss, azt az exchange-en is kezelni kell
        if current_price > self.take_profit_virtual:
            self.stop_loss = self.take_profit_virtual * (1 - self.trailing_stop_loss_step_ratio)
            self.take_profit_virtual = self.take_profit_virtual * (1 + self.trailing_stop_loss_step_ratio)
            self.is_trailing_stop_loss = True
        elif is_candle_closing and not self.is_trailing_stop_loss:
            bollinger_bands_last_bottom_price = self.bollinger_bands[2,-1]
            if bollinger_bands_last_bottom_price > self.stop_loss:
                self.stop_loss = bollinger_bands_last_bottom_price


