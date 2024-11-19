# gloal file for constants. we can add more specific constant files later on - e.g. exchnage_constants.py

from binance import Client
from enum import Enum

# Candle enum: igy tudni fogjuk, hogy a lista melyik eleme micsoda. volume, timestamp is mehetne majd vele
# ezt kene hasznalni majd mindenhol. ez azert jo, mert ha veletlen valtozna a sorrend, akkor csak itt kell atirni, nem pedig a teljes kodban
class Candle(Enum):
    OPEN = 1
    HIGH = 2
    LOW = 3
    CLOSE = 4

SYM = 'BTCUSDT'
CANDLE_INTERVAL = Client.KLINE_INTERVAL_15MINUTE
HISTORICAL_DATA_RELATIVE_START_DATE = '24 hour ago'
