from dataclasses import dataclass
from typing import List
from requestLib.MarketC import Market


@dataclass
class MarketCryptoPair:
    marketName: str
    cryptoCurr: str
    cryptoSYM: str
    price: float
    # askPrice: float
    # bidPrice: float
    # volume: int
    # address:?


@dataclass
class AggregateMarketCryptoPair:
    commonCryptoPairName: str
    marketCryptoPairs: List[MarketCryptoPair]
