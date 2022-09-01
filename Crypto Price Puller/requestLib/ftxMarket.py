import requests
from model.MarketCryptoPair import MarketCryptoPair
from requestLib.MarketC import Market

class FTXMarket(Market):
    def __init__(self):
        Market.__init__(self, "FTX")
        self.fetchURL = "https://ftx.com/api/markets/{}" #base/conver eg. BTC/USD
        self.allMarketsURL = "https://ftx.com/api/markets"

    def fetchCoin(self, coin):
        coin = self.cryptoPairDefs.get(coin)
        data = self.defaultRequest(coin)

        checkTMP = data.get('success')
        if(checkTMP == False):
            print("Coin name not found")
            return

        askPrice = data.get('result').get('ask')
        bidPrice = data.get('result').get('bid')
        returnPair = MarketCryptoPair(market=self, cryptoPair=coin, askPrice=askPrice, bidPrice=bidPrice)
        return returnPair
