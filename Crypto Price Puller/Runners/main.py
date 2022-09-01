import requests
from requestLib.CryptoComMarket import CryptoComMarket
from requestLib.KrakenMarket import KrakenMarket
from requestLib.BinanceMarket import BinanceMarket
from requestLib.ftxMarket import FTXMarket
from requestLib.KucoinMarket import KucoinMarket


# https://min-api.cryptocompare.com/data/v2/pair/mapping/fsym?fsym=BTC&extraParams=YourSite
# https://min-api.cryptocompare.com/data/v2/pair/mapping/fsym?fsym=XRP
# https://min-api.cryptocompare.com/data/pricemultifull?e=Kraken&fsyms=DUSK&tsyms=ETH

def getCoins2File(url, filename):
    print(url)
    print(filename)
    urlRequest = requests.get(url)
    details = urlRequest.json()
    fileLoc = 'Data/List of markets Currencys/{}'
    with open(fileLoc.format(filename), 'w') as data:
        data.write(str(details))

if __name__ == '__main__':
    # coin = "ripple_eth"
    # KRAKEN = KrakenMarket()
    # tmpk = KRAKEN.fetchCoin(coin)
    # print(tmpk)

    # binm = BinanceMarket()
    # tmpb = binm.fetchCoin(coin)
    # print(tmpb)
    #
    # coin = "XRP_CRO"
    # cryptocom = CryptoComMarket()
    # tmpc = cryptocom.fetchCoin(coin)
    # print(tmpc)

    # coin = "XRP-ETH"
    # KuMarket = KucoinMarket()
    # tmpP = KuMarket.fetchCoin(coin)
    # print(tmpP)

    # urlCheckKra = requests.get("https://api.kraken.com/0/public/Ticker?pair=XRPETH").json()
    # urlCheckBin = requests.get("https://ftx.com/api/markets/BTC/USD").json()
    # print(urlCheckKra)
    # print(urlCheckBin)


    # urlCheckBin = requests.get("https://api.uphold.com/v0/ticker").json()
    # print(urlCheckBin)
    # coin = "1incheth"
    # tmpM = KucoinMarket()
    # tmpP = tmpM.fetchCoin(coin)
    # print(tmpP)


    # inchKRAKEN.printAllValues()

    # coin = "1INCH_USDT"
    # x = CryptoComMarket()
    # x.setCurrency(coin)
    # x.fetchcoin()
    # # x.fetchAllData()
    # # x.printAllValues()
    # x.printAsk()
    # inchKRAKEN.printAsk()
    # x.printBid()
    # inchKRAKEN.printBid()

    import requests

    url = "https://crypto-arbitrage.p.rapidapi.com/crypto-arb"

    querystring = {"pair": "XRP/ETH", "consider_fees": "False", "selected_exchanges": "exmo cex bitstamp hitbtc kraken coinbasebv "}

    headers = {
        'x-rapidapi-host': "crypto-arbitrage.p.rapidapi.com",
        #'x-rapidapi-key': "x"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

