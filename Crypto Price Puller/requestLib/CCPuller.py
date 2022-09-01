import requests
from model.MarketCryptoPair import MarketCryptoPair

XRP_ETH = ['ABCC', 'Bibox', 'Binance', 'BitTrex', 'Exmo', 'LiveCoin', 'bkex', 'coinsuper', 'ataix', 'aax', 'sistemkoin', 'Yobit', 'OKEX', 'Kucoin', 'TradeSatoshi', 'Upbit', 'BitMart', 'RightBTC', 'OKCoin', 'OpenLedger', 'FCoin', 'HitBTC', 'Gatecoin', 'IDAX', 'Nexchange', 'CoinHub', 'Bitsane', 'CoinPulse', 'xbtpro', 'Bitforex', 'CoinTiger', 'DigiFinex', 'Catex', 'CBX', 'bw', 'bitmax', 'Ironex', 'coss', 'gopax', 'crex24', 'coinzest', 'etoro', 'bequant', 'bhex', 'DSX', 'Kraken', 'LBank', 'LAToken', 'tokok', 'bitcoincom', 'btse', 'BitBay', 'nominex']
DOGE_ETH = ['HuobiPro', 'Bleutrade', 'Tidex', 'Bibox', 'oex', 'Yobit', 'CCEX', 'BitZ', 'TradeSatoshi', 'Graviex', 'OKEX', 'FCoin', 'HitBTC', 'Hikenex', 'Nexchange', 'P2PB2B', 'BitTrex', 'Bitforex', 'Zecoex', 'Coinsbit', 'Catex', 'CryptoExchangeWS', 'altilly', 'Bgogo', 'huobikorea', 'crex24', 'hbus', 'DigiFinex', 'coinall', 'unnamed', 'ataix', 'Cryptopia', 'Novaexchange', 'bitcoincom', 'betconix', 'coineal', 'Gemini']


def fetchPairData(curr, symbolic, e):

    key = '36ebdc8e7cd2f0bf649256abb051583cc9e368b91fe0338b8e9141b4de1ea1fa'
    getPriceurl = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}&e={}".format(curr,symbolic,e)
    url = "https://min-api.cryptocompare.com/data/ob/l1/top?&api_key={}fsyms={}&tsyms={}&e={}".format(key, e, curr, symbolic)
    tmp = 'https://min-api.cryptocompare.com/data/ob/l1/top?fsyms=XRP&tsyms=USD&e=Kraken'
    print(getPriceurl)
    data = requests.get(getPriceurl).json()
    print(data)
    # mar = data.get('RAW').get(curr).get(symbolic).get('MARKET')
    currency = data.get('Data').get('RAW').get(curr)
    symb = data.get('Data').get('RAW').get(curr).get(symbolic)
    ask = data.get('Data').get('RAW').get(curr).get(symbolic).get('ASK')
    bid = data.get('Data').get('RAW').get(curr).get(symbolic).get('BID')
    market = MarketCryptoPair(e,currency, symb, ask, bid)


def fetchPriceData(curr, symbolic, e,showErr):

    key = '36ebdc8e7cd2f0bf649256abb051583cc9e368b91fe0338b8e9141b4de1ea1fa'
    getPriceurl = "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}&e={}".format(curr, symbolic,e)
    data = requests.get(getPriceurl).json()
    # print(getPriceurl)
    try:
        mar = data.get('RAW').get(curr).get(symbolic).get('MARKET')
        price = data.get('RAW').get(curr).get(symbolic).get('PRICE')
        return MarketCryptoPair(mar, curr, symbolic, price)
    except AttributeError:
        if(showErr == True):
            print("ERROR: Exchange does not have pair {}/{} on market {}".format(curr, symbolic, e))


markets = XRP_ETH
coin = "ATOM"
SYM = "ETH"
arr = []
minValue = 100000000000000
minMarket = "yuuu"
maxValue = 0
maxMarket = "yeee"




for x in markets:

    yeet = fetchPriceData(coin, SYM, x, False)
    if(yeet != None):
        print(yeet)
    try:
        if yeet.price > maxValue:
            maxValue = yeet.price
            maxMarket = yeet.marketName
        if yeet.price < minValue:
            minValue = yeet.price
            minMarket = yeet.marketName
        arr.append(yeet)
    except:
        pass


print(arr)

print("The lowest price is: {}, on {}\n The Highest Price is {}, on {}".format(minValue,minMarket,maxValue,maxMarket))
diff= maxValue-minValue
print("Diffrence max-min:{}".format(diff))
worth = minValue/diff
print("Worth is: {}".format(worth))
if(worth >= .1):
    print("This is worth a flashloan")
else:
    print("This is not viable flashloan")
