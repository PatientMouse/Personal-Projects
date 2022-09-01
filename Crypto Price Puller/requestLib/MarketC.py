import requests


class Market():
    def __init__(self, inmarketname):
        self.baseApiURL = None
        self.fetchURL = None
        self.marketName = inmarketname
        self.cryptoPairDefs = {}

    def fetchCoin(self, coin):
        pass

    def defaultRequest(self, coin):
        url = self.fetchURL.format(coin)
        raw = requests.get(url)
        return raw.json()
