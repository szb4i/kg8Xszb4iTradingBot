from exchange.exchange_websocket import ExchangeWebsocket 
from strategy.strategy import Strategy

if __name__ == "__main__":
    strategy = Strategy()
    exchange_websocket = ExchangeWebsocket(strategy.on_exchange_ws_message)
