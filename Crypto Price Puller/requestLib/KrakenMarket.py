import requests
from model.MarketCryptoPair import MarketCryptoPair
from requestLib.MarketC import Market

class KrakenMarket(Market):
    def __init__(self):
        Market.__init__(self, "Kraken")
        self.fetchURL = "https://api.kraken.com/0/public/Ticker?pair={}"
        self.cryptoPairDefs = {'ripple_eth': 'XRPETH'}

    def fetchCoin(self, coin):
        coin = self.cryptoPairDefs.get(coin)
        data = self.defaultRequest(coin)

        checkTMP = data.get('result').get(coin)
        if(checkTMP == None):
            print("Coin name not found")
            return

        askPrice = float(data.get('result').get(coin).get('a')[0])
        bidPrice = float(data.get('result').get(coin).get('b')[0])
        returnPair = MarketCryptoPair(market=self, cryptoPair=coin,askPrice=askPrice, bidPrice=bidPrice)
        return returnPair