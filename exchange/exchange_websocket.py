# websocket for receiving current prices from exchange. on each new message, tick strategy
from binance import ThreadedWebsocketManager
from credentials import getBinanceKey, getBinanceSecretKey
from typing import Callable
 
class ExchangeWebsocket:
    def __init__(self, on_exchange_ws_message: Callable) -> None:
        twm = ThreadedWebsocketManager(api_key=getBinanceKey(), api_secret=getBinanceSecretKey())
        twm.start()
        twm.start_kline_socket(symbol="BTCUSDT", callback=on_exchange_ws_message)
        twm.join()