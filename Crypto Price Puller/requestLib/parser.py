import requests
import json


def toArr(curr,quote):
    key = '36ebdc8e7cd2f0bf649256abb051583cc9e368b91fe0338b8e9141b4de1ea1fa'
    url = "https://min-api.cryptocompare.com/data/v2/pair/mapping/fsym?fsym={}&api_key={}".format(curr,key)
    dataJ = requests.get(url).json()
    dataJ = dataJ.get('Data').get('current')
    arr = []
    for key in dataJ:
        if (key.get('fsym')==curr and key.get('tsym')==quote):
            arr.append(key.get('exchange'))
    return arr


arr = toArr("DOGE","ETH")
print(arr)