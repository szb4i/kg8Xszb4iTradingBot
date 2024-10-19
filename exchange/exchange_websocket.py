# websocket for receiving current prices from exchange. on each new message, tick strategy
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager

client=Client(credentials.getBinanceKey(), credentials.getBinanceSecretKey())
twm = ThreadedWebsocketManager(api_key=credentials.getBinanceKey(), api_secret=credentials.getBinanceSecretKey())
twm.start()

twm.start_symbol_ticker_socket(symbol="BTCUSDT", callback=handle_socket_message)