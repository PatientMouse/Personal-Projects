import requests
from model.MarketCryptoPair import MarketCryptoPair
from requestLib.MarketC import Market

class KucoinMarket(Market):
    def __init__(self):
        Market.__init__(self, "Kucoin")
        self.fetchURL = "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={}"
        self.allTickersURL = "https://api.kucoin.com/api/v1/market/allTickers"
        self.cryptoPairDefs = {'ripple_eth': 'XRP-ETH'}

    def fetchCoin(self, coin):
        coin = self.cryptoPairDefs.get(coin)
        data = self.defaultRequest(coin)

        checkTMP = data.get('code')
        if(checkTMP != '200000'):
            print("Coin name not found")
            return

        askPrice = float(data.get('data').get('bestAsk'))
        bidPrice = float(data.get('data').get('bestBid'))
        returnPair = MarketCryptoPair(market=self, cryptoPair=coin,askPrice=askPrice, bidPrice=bidPrice)
        return returnPair