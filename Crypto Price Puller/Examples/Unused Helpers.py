import requests



# Name: setMarketNameOveride
# Descripton: overides to init market name to a new market name. Used for readable purposes rather than api usage
# Paramaters: self, newName(String)
# Return: void
def setMarketNameOveride(self, newname, op):
    self.marketName = newname
    if op == "p":
        print("Market Name changed to: " + self.marketName) #optional

# Name: getMarketName
# Descripton: Returns or prints the market name based on option arg
# Paramaters: self, op_returnType: option arg to print if needed
# Return: marketName(String)
def getMarketName(self,op_returntype = "r"):
    if op_returntype == "p":
        print(self.marketName)
    else:
        return self.marketName

# Name:setCurrencyOveride
# Descripton: overisdes the inits intance varible asign
# Paramaters:self, newcurr: string most likely of currency name, op: option flag for print
# Return: void
def setCurrencyOveride(self,newcurr,op = ""):
    self.currency = newcurr
    if op == "p":
        print("Currency for " + self.marketName + " is now: " + self.currency)#optional

# Name:getCurrency
# Descripton: gets the currency for given market
# Paramaters:self, op:optional print flag
# Return: self.currency string
def getCurrency(self, op="r"):
    if op == "p":
        print(self.currency)
    else:
        return self.currency

def getCoins2File(url, filename):
    print(url)
    print(filename)
    urlRequest = requests.get(url)
    details = urlRequest.json()
    fileLoc = 'Data/List of markets Currencys/{}'
    with open(fileLoc.format(filename), 'w') as data:
        data.write(str(details))

    def printAll(self):
        print("Name: " + str(self.marketName))
        print("Sell URL: " + str(self.sellURL))
        print("Currency: "+ str(self.currency))
        print("Buy URL: " + str(self.buyURL))
        print("Home URL: " + str(self.homeURL))
        print("Base API URL: " + str(self.baseApiURL))


    def setHomeURL(self,url):
        self.homeURL = url

    def getHomeURL(self):
        return self.homeURL

    def setBaseApiURL(self,url):
        self.baseApiURL = url

    def getBaseApiURL(self):
        return self.baseApiURL

    def setBuyURL(self, url):
        self.buyURL = url

    def getBuyRUL(self):
        return self.buyURL

    def setSellURL(self, url):
        self.sellURL = url

    def getSellURL(self):
        return self.sellURL


    def setMarketNameOveride(self, newname, op):
        self.marketName = newname
        if op == "p":
            print("Market Name changed to: " + self.marketName)

    def getMarketName(self,op_returntype = "r"):
        if op_returntype == "p":
            print(self.marketName)
        else:
            return self.marketName

    def setCurrency(self, newcurr, op=""):
        self.currency = newcurr
        if op == "p":
            print("Currency for " + self.marketName + " is now: " + self.currency)

    def getCurrency(self):
        return self.currency
    def printAllValues(self):
        values = vars(self)
        print(values)
    def printBid(self):
        print("Bid price for {} in {} is in USD: ${}".format(self.currency,self.marketName,self.bidPrice))

    def printAsk(self):
        print("Ask price for {} in {} is in USD: ${}".format(self.currency,self.marketName,self.askPrice))