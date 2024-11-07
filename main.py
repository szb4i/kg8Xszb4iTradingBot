from exchange.exchange_websocket import ExchangeWebsocket 
from strategy.strategy import Strategy
from exchange.exchange_rest import ExchangeRest
from technical_analysis.bollinger_bands import get_bollinger_bands

def on_message(message):
    print(message)

if __name__ == "__main__":
    exchange_rest = ExchangeRest()
    print(get_bollinger_bands(exchange_rest.get_historical_ohlc(), 20)[2])
    # strategy = Strategy(exchange_rest.get_historical_ohlc())
    # exchange_websocket = ExchangeWebsocket(strategy.on_exchange_ws_message)
