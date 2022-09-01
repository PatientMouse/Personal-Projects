import requests
from model.MarketCryptoPair import MarketCryptoPair
from requestLib.MarketC import Market

class KrakenMarket(Market):
    def __init__(self):
        Market.__init__(self, "Kraken")
        self.fetchURL = "https://api.kraken.com/0/public/Ticker?pair={}"

    def fetchcoin(self, coin):
        url = self.fetchURL.format(coin)
        raw = requests.get(url)
        data = raw.json()

        checkTMP = data.get('result').get(coin)
        if(checkTMP == None):
            print("Coin name not found")
            return

        askPrice = data.get('result').get(coin).get('a')[0]
        bidPrice = float(data.get('result').get(coin).get('b')[0])
        returnPair = MarketCryptoPair(market=self, cryptoPair=coin,askPrice=askPrice, bidPrice=bidPrice)
        return returnPair