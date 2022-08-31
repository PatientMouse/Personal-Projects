# imports
from datetime import date

from database import *


def printError(e, task):
    print("Failed to complete task: {}. Created error log".format(task))
    fileName = "ErrorLog_" + str(date.today())
    file = open(fileName, "w")
    error = "Error code: {},\nSQLState val: {},\nError MSG: {},\nError: {}".format(e.errno, e.sqlstate, e.msg, e)
    file.write(error)
    file.close()


def extractLastDatabase():
    with open('settings.json') as file:
        jason = json.load(file)
        return jason['lastUsed']


def setLastUsed(database_name):
    with open('settings.json', 'r+') as file:
        jason = json.load(file)
        jason['lastUsed'] = database_name
        file.seek(0)
        json.dump(jason, file, indent=4)


def printMenu(db):
    print("""\nMENU:
    DATABASE IN USE: {}
    A - ADD ELEMENT
    D - DELETE ELEMENT
    R - READ DATA
    Y - ANALYZE DATA
    B - DATABASE SELECTION
    H - HELP
    Q - QUIT""".format(db))


def creation_full_q_and_a(databases, s) -> Database:
    responseVar = input("Would you like to use a previously constructed database?(y/n)").lower()
    if not responseVar:
        responseVar = input("Invalid response! Would you like to use a previously constructed database?(y/n)").lower()
    db = None
    while responseVar not in ['y', 'n']:
        responseVar = input("Invalid response! Would you like to use a previously constructed database?(y/n)").lower()
        if not responseVar:
            responseVar = input(
                "Invalid response! Would you like to use a previously constructed database?(y/n)").lower()
    if responseVar == "n":
        n = input("\tPlease enter desired new database name:    ")
        if not n:
            n = input(
                "Invalid response! Please enter new database name:  ").lower()
        db = Database(n, s, databases)
        setLastUsed(n)
    elif responseVar == "y":
        print("Databases available: ", end=" ")
        print(databases)
        responseVar = input("Which database would you like to use?(enter name):")
        if not responseVar:
            responseVar = input(
                "Invalid response! Which database would you like to use?(enter name):   ")
        setLastUsed(responseVar)
        db = Database(responseVar, s, databases)
    return db


def select_database(s) -> Database:
    s.cursor.execute("SHOW DATABASES")
    databases = cursor_to_str_subscript(s.cursor)
    lastDB = extractLastDatabase()
    if not lastDB or lastDB not in databases:
        lastDB = None

    if lastDB is None and databases is None:
        print("********** DATABASE SELECTION ********\n" +
              "No databases found. Please create a new database:")
        nameDB = input("Please enter desired database name: ").lower()
        if not nameDB:
            nameDB = input("Invalid response! Please enter desired database name:   ")
        setLastUsed(nameDB)
        return Database(nameDB, s, databases)

    elif lastDB is not None and databases is None:
        # case there is no databases and a previously used one, should not ever logically flag
        print("********** DATABASE SELECTION ********\n" +
              "Last Database used: ", end='')
        print(lastDB)
        response = input("Would you like to use this Database?(y/n)").lower()
        while response not in ['y', 'n']:
            response = input("Invalid response! Would you like to use this Database?(y/n)").lower()
        if response == "y":
            return Database(lastDB, s, databases)
        else:
            nameDB = input("\tPlease enter desired database name:").lower()
            setLastUsed(nameDB)
            return Database(nameDB, s, databases)

    else:  # case there is a last used db and db's in system
        print("********** DATABASE SELECTION ********\n" +
              "Last Database used: ", end='')
        print(lastDB)
        if lastDB is not None:
            response = input("Would you like to use this Database?(y/n)").lower()
            while response not in ['y', 'n']:
                response = input("Invalid response! Would you like to use this Database?(y/n)").lower()
            if response == "y":
                return Database(lastDB, s, databases)
            else:
                return creation_full_q_and_a(databases, s)
        else:
            return creation_full_q_and_a(databases, s)


def add_item(database):
    print("\nAdd new item...")
    itemName = input("Input item name:")
    if not itemName:
        itemName = input(
            "Invalid response! Input item name:")
    price = input("Input item price (2 decimal):")
    if not price:
        price = input(
            "Invalid response! Input item price (2 decimal):")
    database.create_item(itemName, price)


def analyze_data(database):
    responseName = input("Would you like to analyze all data? (y/n)").lower()
    while responseName not in ['y', 'n']:
        responseName = input("Invalid response! Would you like to analyze all data?(y/n)")
    if responseName == "y":
        database.analyze_all()
    else:
        responseName = input("Enter name of item to analyze data of:")
        if not responseName:
            responseName = input(
                "Invalid response! Enter name of item to analyze data of:")
        database.analyze_one(responseName)


def read_data(database):
    responseName = input("Would you like to read all data? (y/n)").lower()
    while responseName not in ['y', 'n']:
        responseName = input("Invalid response! Would you like to read all data?(y/n)").lower()
    if responseName == "y":
        database.read_all_data(0)
    else:
        responseName = input("Enter name of item to read data of:")
        if not responseName:
            responseName = input(
                "Invalid response! Enter name of item to read data of:")
        database.read_one_data(responseName, 0)


if __name__ == "__main__":
    print(
        "**********PRICE TRACKER**********\nBuilt with Python and mysql\nAuthor: Andrew Gerber, "
        "andrewtgerber@gmail.com\n\n")
    server = None
    try:
        server = Server()
    except mysql.connector.Error as err:
        printError(err, "Server Connection")
        exit(1)
    print("Boot-up database selection...")
    current_database = None
    try:
        current_database = select_database(server)
    except mysql.connector.Error as err:
        printError(err, "Select Database")
        exit(1)

    appState = None
    while appState != 'q':
        printMenu(current_database.name)
        appState = input("Enter option:").lower()
        match appState:
            case 'q':
                exit(0)
            case 'h':
                print(
                    "\nHELP:\nThis program is a simple database python application. \nTo use it enter a menu option "
                    "below and "
                    "the computer will prompt you with choices for your option, such as items names and prices. "
                    "\nYou can read the data in the database with the read data option and view a brief analysis of "
                    "the "
                    "items with he analyze option.\nWhen you are done you can quit and the database will save over "
                    "sessions.")

            case 'b':
                try:
                    current_database = select_database(server)
                    current_database.reconnect()
                except mysql.connector.Error as err:
                    printError(err, "select database")
            case 'admin_wipe':
                decision = None
                p = input("!!!!!!!!!!! WARNING THIS WILL WIPE ALL DATABASES OFF THE SERVER!!!!!!!!!!!!\n Enter admin "
                          "password:")
                if server.password == p:
                    decision = input("Are you sure? type host name to confirm:")
                if decision == server.host:
                    server.wipe_server(p)
            case 'a':
                try:
                    add_item(current_database)
                except mysql.connector.Error as err:
                    printError(err, "Add item")
            case 'd':
                res = input("Delete Item entirely or price entry of item? Options: I - Item, P, price:      ").lower()
                while res not in ['i', 'p', 'I', 'P']:
                    res = input("Invalid response! Delete Item entirely or price entry of item? Options: I - "
                                "Item, P - price:       ").lower()
                match res:
                    case 'i':
                        res = input(
                            "Enter name of item you would like to delete (Enter 'list' for list of names in "
                            "database):   ")

                        if res in ['list', 'List']:
                            try:
                                current_database.print_names()
                            except mysql.connector.Error as err:
                                printError(err, "Print names")
                            res = input(
                                "Enter name of item you would like to delete (Enter 'list' for list of names in "
                                "database):   ")
                        try:
                            current_database.delete_item(res)
                        except mysql.connector.Error as err:
                            printError(err, "Delete Item:{}".format(res))
                        else:
                            print("Item: {}, successfully deleted!".format(res))
                    case 'p':
                        name = input("Enter name of item you would like to delete: (Enter 'list' for list of names in "
                                     "database):     ")
                        if not name:
                            name = input(
                                "Invalid response! Enter name of item you would like to delete: (Enter 'list' for list of names in "
                                "database):")
                        if name in ['list', 'List']:
                            try:
                                current_database.print_names()
                            except mysql.connector.Error as err:
                                printError(err, "Print names")

                            name = input(
                                "Enter name of item you would like to delete: (Enter 'list' for list of names in "
                                "database):      ")
                            if not name:
                                name = input(
                                    "Invalid response! Enter name of item you would like to delete: (Enter 'list' for list of names in "
                                    "database):")

                        print("Item Prices for '{}'".format(name))
                        try:
                            current_database.read_one_data(name, 1)
                        except mysql.connector.Error as err:
                            printError(err, "Read one data")
                        price_id = input("Enter PriceID of entry to delete:")
                        if not price_id:
                            price_id = input(
                                "Invalid response! Enter PriceID of entry to delete:")
                        try:
                            current_database.delete_price(name, price_id)
                        except mysql.connector.Error as err:
                            printError(err, "Delete Price")
                            # print("Failed to delete item {} with id {}".format(name, price_id))
                        else:
                            print("Item {} with id {}, successfully deleted!".format(name, price_id))

            case 'r':
                try:
                    read_data(current_database)
                except mysql.connector.Error as err:
                    printError(err, "Read Data")

            case 'y':
                try:
                    analyze_data(current_database)
                except mysql.connector.Error as err:
                    printError(err, "Analyze data")
