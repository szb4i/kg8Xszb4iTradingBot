from exchange.exchange_websocket import ExchangeWebsocket 
from strategy.strategy import Strategy
from exchange.exchange_rest import ExchangeRest

if __name__ == "__main__":
    exchange_rest = ExchangeRest()
    strategy = Strategy(exchange_rest.get_historical_ohlc())
    exchange_websocket = ExchangeWebsocket(strategy.on_exchange_ws_message)
