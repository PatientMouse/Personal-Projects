import requests
import json
import coinbase
from coinbase.wallet.client import Client

if __name__ == '__main__':
    krakenBTCRequest = requests.get('https://api.kraken.com/0/public/Ticker?pair=XBTUSD')
    # coinBaseBTC = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy')

    # note:  from crypto.com can omite the instrument for all
    cryptoBTCRequest = requests.get('https://api.crypto.com/v2/public/get-ticker?instrument_name=BTC_USDT')
    # for crypto b is bid and k is ask
    # cryptoLEORequest = requests.get('https://api.crypto.com/v2/public/get-ticker?')


    #            CONVER TO JSON FROM REQUEST
    krakenBTCJson = krakenBTCRequest.json()
    #   coinBaseBTCJson = coinBaseBTC.json()
    cryptoBTCJson = cryptoBTCRequest.json()
    # cryptoLEOJson = cryptoLEORequest.json()

    ######              CONVERT FROM JSON TO SINGLE DIGIT VALUE
    krakenBTCAsk = float(krakenBTCJson.get('result').get('XXBTZUSD').get('a')[0])
    krakenBTCBid = float(krakenBTCJson.get('result').get('XXBTZUSD').get('b')[0])
    # coinBaseBTCBuyPrice = coinBaseBTCJson.get('data').get('amount')
    cryptoBTCBid = cryptoBTCJson.get('result').get('data').get('b')  # bid
    cryptoBTCAsk = cryptoBTCJson.get('result').get('data').get('k')  # ask

    ######              FIND THE DIFFRENCES
    bidDiff = abs(max(krakenBTCBid, cryptoBTCBid) - min(krakenBTCBid, cryptoBTCBid))
    askDiff = abs(max(krakenBTCAsk, cryptoBTCAsk) - min(krakenBTCAsk, cryptoBTCAsk))
    cAsk2KBid = abs(cryptoBTCAsk - krakenBTCBid)
    kAsk2CBid = abs(krakenBTCAsk - cryptoBTCBid)

    # is is ask to bid

    ######              calc loan and how much it aave take\
    loanUnits = .1 #in units
    aaveCut = 0.0009
    loanValue = loanUnits * krakenBTCAsk
    rawGain = kAsk2CBid * loanUnits
    cutValue = loanValue * aaveCut


    # Prints the
    # print(krakenBTCJson)
    # print(cryptoBTCJson)
    # print(cryptoLEOJson)
    print("Kraken BTC 'Ask' price is: " + str(krakenBTCAsk))
    print("Kraken BTC 'Bid' price is: " + str(krakenBTCBid))
    # print("coinbase BTC 'buy amount is: " + coinBaseBTCBuyPrice)

    print("crypto.com BTC 'Ask' price is: " + str(cryptoBTCAsk))
    print("crypto.com 'Bid' price is: " + str(cryptoBTCBid))

    print("Bid diffrence: $" + str(bidDiff) + " USD")
    print("Ask diffrence: $" + str(askDiff) + " USD")
    print("Crypto.com ask to Kraken bid diffrence: $" + str(cAsk2KBid) + " USD")
    print("Kraken ask to Crypto.com bid diffrence: $" + str(kAsk2CBid) + " USD")
    print("Using Kraken")
    print(loanValue)
    print(rawGain)
    print(cutValue)
    print("Cut Value:" + str(cutValue) + " needs to be lower than rawGain:"+ str(rawGain))

