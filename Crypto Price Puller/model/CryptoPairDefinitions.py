from dataclasses import dataclass
from typing import Dict


# Used to track different markets name for Crypto Pairs
@dataclass
class CryptoPairDefinition:
    commonCryptoPairName: str
    marketCryptoPairNames: Dict[str, str]  # Where first str is market name, second is market's crypto pair name

#Format: var name = CryptoPairDefinition('genName', {'kraken': '', 'coinbase': '', 'binance': ''})
# BTC_ETH is bitcoin IN ETH
btc_eth = CryptoPairDefinition('BTC_ETH', {'kraken': '?'})
ripple_ETH = CryptoPairDefinition('RIP_ETH', {'kraken': 'XRPETH', 'coinbase': None, 'binance': 'XRPETH'})