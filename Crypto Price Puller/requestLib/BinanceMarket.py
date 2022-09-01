import requests
from model.MarketCryptoPair import MarketCryptoPair
from requestLib.MarketC import Market

class BinanceMarket(Market):
    def __init__(self):
        Market.__init__(self, "Binance")
        self.fetchURL = "https://api.binance.com/api/v3/ticker/bookTicker?symbol={}"
        self.cryptoPairDefs = {'ripple_eth': 'XRPETH'}

    def fetchCoin(self, coin):
        coin = self.cryptoPairDefs.get(coin)
        data = self.defaultRequest(coin)

        checkTMP = data.get('symbol')
        if(checkTMP == None):
            print("Coin name not found")
            return

        askPrice = float(data.get('askPrice'))
        bidPrice = float(data.get('bidPrice'))
        returnPair = MarketCryptoPair(market=self, cryptoPair=coin, askPrice=askPrice, bidPrice=bidPrice)
        return returnPair
