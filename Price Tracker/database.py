# imports
import json

import mysql.connector


def cursor_to_str_subscript(cursor):
    result = []
    for x in cursor:
        result.append(x[0])
    return result


def extract_ignore_list():
    with open('settings.json') as file:
        jason = json.load(file)
        return jason['ignore_databases']


def print_rows(rows, n, opt):
    if opt == 0:
        print("\nPrices for '{}':".format(n))
        for x in rows:
            print("Price: ${}   Date: {}".format(x[2], x[3]))
    elif opt == 1:
        print("\nPrices for '{}':".format(n))
        for x in rows:
            print("ItemID: {}   PriceID: {}    Price: ${}   Date: {}".format(x[1], x[0], x[2], x[3]))


class Server:
    password = 'guest'
    user = "root"
    host = "localhost"

    def __init__(self):
        self.connection = self.connect_server(self.host, self.user, self.password, True)
        self.cursor = self.connection.cursor(buffered=True)

    @staticmethod
    def connect_server(h, u, p, b):
        return mysql.connector.connect(host=h,
                                       user=u,
                                       password=p,
                                       buffered=b)

    def wipe_server(self, password):
        if password != self.password:
            exit("INCORRECT SERVER PASSWORD...how did you get this far?")
        self.cursor.execute("SHOW DATABASES")
        dbs = cursor_to_str_subscript(self.cursor)
        ignoreList = extract_ignore_list()
        for x in dbs:
            if x not in ignoreList:
                self.cursor.execute("DROP DATABASE {}".format(x))
                # self.connection.commit()


class Database:
    password = 'guest'
    user = "root"
    host = "localhost"

    def __init__(self, n, s, dbs) -> None:
        self.name = n
        self.server = s
        self.cursor = None
        self.connection = None

        if self.name in dbs:
            self.connection = self.loadDB()
            self.cursor = self.connection.cursor(buffered=True)
            self.cursor.execute("SHOW TABLES")
            tables = cursor_to_str_subscript(self.cursor)
            if ("Item" not in tables) and ("ItemPriceHistory" not in tables):
                self.init_tables()
                self.reconnect()
            elif ("Item" in tables) and ("ItemPriceHistory" not in tables):
                self.create_item_table()
                self.reconnect()
            elif ("Item" not in tables) and ("ItemPriceHistory" in tables):
                self.create_item_price_history_table()
                self.reconnect()
        else:
            self.add_database()
            self.connection = self.loadDB()
            self.cursor = self.connection.cursor(buffered=True)
            self.init_tables()
            self.reconnect()

    def reconnect(self):
        self.cursor.close()
        self.connection.close()
        self.connection = self.loadDB()
        self.cursor = self.connection.cursor(buffered=True)

    def add_database(self):
        self.server.cursor.execute("CREATE DATABASE " + self.name)

    def load_databases(self):
        return self.cursor.execute("SHOW DATABASES")

    def create_item_table(self):
        self.cursor.execute("""CREATE TABLE Item(
                ItemID int NOT NULL AUTO_INCREMENT,
                Name varchar(128) NOT NULL,
                PRIMARY KEY (ItemID)
                );""")

    def create_item_price_history_table(self):
        self.cursor.execute("""CREATE TABLE ItemPriceHistory(
        ItemPriceID int NOT NULL AUTO_INCREMENT,
        ItemID int NOT NULL,
        Price decimal(15,2),
        Date datetime NOT NULL,
        PRIMARY KEY (ItemPriceID),
        FOREIGN KEY (ItemID) REFERENCES Item(ItemID) ON DELETE CASCADE
        );
        
        CREATE INDEX idx_ItemPriceHistory_ItemDate
        ON ItemPriceHistory (ItemID,Date);
        """)

    def init_tables(self):
        self.create_item_table()
        self.create_item_price_history_table()

    def loadDB(self):
        return mysql.connector.connect(host=self.host,
                                       user=self.user,
                                       password=self.password,
                                       database=self.name,
                                       buffered=True)

    def create_item(self, n, p):
        statementName = "SELECT ItemID from Item WHERE Name = (%s)"
        values = (n,)
        self.cursor.execute(statementName, values)
        self.connection.commit()
        items = cursor_to_str_subscript(self.cursor)
        if len(items) == 0:
            statementName = "INSERT INTO Item (Name) VALUE (%s)"
            self.cursor.execute(statementName, values)
            self.connection.commit()

        statementPrice = "INSERT INTO ItemPriceHistory (Price,Date,ItemId) SELECT %s, NOW(), ItemId FROM Item WHERE Name = %s"
        values = (p, n)
        self.cursor.execute(statementPrice, values)
        self.connection.commit()

    def delete_item(self, n):
        statementName = "SELECT ItemID from Item WHERE Name = (%s)"
        values = (n,)
        self.cursor.execute(statementName, values)
        self.connection.commit()
        items = self.cursor.fetchall()
        if len(items) > 0:
            statementName = "DELETE FROM Item WHERE name = %s"
            self.cursor.execute(statementName, values)
            self.connection.commit()

    def delete_price(self, n, itemid):
        statementName = "SELECT ItemID from Item WHERE Name = (%s)"
        self.cursor.execute(statementName, (n,))
        self.connection.commit()
        items = self.cursor.fetchall()
        if len(items) > 0:
            statementName = "DELETE FROM ItemPriceHistory WHERE ItemPriceID = %s"
            self.cursor.execute(statementName, (itemid,))
            self.connection.commit()

    def print_names(self):
        statement = "SELECT Name FROM Item"
        self.cursor.execute(statement)
        rows = self.cursor.fetchall()
        names = ""
        ignoreList = extract_ignore_list()
        for x in rows:
            if x not in ignoreList:
                names = names + x[0] + ", "
        print(names)

    def read_all_data(self, opt):
        statement = "SELECT Name FROM Item"
        self.cursor.execute(statement)
        rows = self.cursor.fetchall()
        for x in rows:
            self.read_one_data(x[0], opt)

    def read_one_data(self, n, opt):
        statement = "SELECT * FROM ItemPriceHistory WHERE ItemID = (SELECT ItemID FROM Item WHERE Name = (%s))"
        self.cursor.execute(statement, (n,))
        rows = self.cursor.fetchall()
        print_rows(rows, n, opt)

    def analyze_one(self, n):
        statement = "SELECT * FROM ItemPriceHistory WHERE ItemID = (SELECT ItemID FROM Item WHERE Name = (%s)) ORDER BY Date"
        self.cursor.execute(statement, (n,))
        rowsAll = self.cursor.fetchall()
        print("\nData for item: {}".format(n))

        if rowsAll:
            statement = """SELECT * FROM Item i
                            join ItemPriceHistory iph on iph.ItemID = i.ItemID
                            where i.Name = (%s)
                            order by iph.Price ASC
                            limit 1;"""
            self.cursor.execute(statement, (n,))
            smallest = self.cursor.fetchall()
            statement = """SELECT * FROM Item i
            join ItemPriceHistory iph on iph.ItemID = i.ItemID
            where i.Name = (%s)
            order by iph.Price DESC 
            limit 1;"""
            self.cursor.execute(statement, (n,))
            largest = self.cursor.fetchall()

            first = rowsAll[0]
            last = rowsAll[len(rowsAll) - 1]
            change = last[2] - first[2]
            print("Overall The price of Item '{}' has changed ${} from {} to {}".format(n, change, first[3], last[3]))
            print("With the highest price for Item '{}': ${} on: {}".format(n, smallest[0][4], smallest[0][5]))
            print("and the Lowest price for Item   '{}': ${} on: {}".format(n, largest[0][4], largest[0][5]))

        else:
            print("No price data for item: '{}'".format(n))

    def analyze_all(self):
        statement = "SELECT Name FROM Item"
        self.cursor.execute(statement)
        rows = self.cursor.fetchall()
        print("\nAnalyze of data:")
        for x in rows:
            self.analyze_one(x[0])
