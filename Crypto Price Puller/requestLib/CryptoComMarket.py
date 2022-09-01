import requests

from requestLib.MarketC import Market

class CryptoComMarket(Market):
    def __init__(self):
        Market.__init__(self, "Crypto.com")
        self.fetchURL = "https://api.crypto.com/v2/public/get-ticker?instrument_name={}"
        self.cryptoPairDefs = {'ripple_eth': 'XRPETH'}

    def fetchCoin(self, coin):
        coin = self.cryptoPairDefs.get(coin)
        data = self.defaultRequest(coin)

        checkTMP = data.get('result').get(coin)
        if (checkTMP == None):
            print("Coin name not found")
            return

        self.askPrice = data.get('result').get('data').get('a')
        self.bidPrice = data.get('result').get('data').get('b')
        self.volume = data.get('result').get('data').get('v')