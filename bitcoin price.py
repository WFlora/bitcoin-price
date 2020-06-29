# VERSION 1.0 19/3/2020

import requests
import sqlite3
from bs4 import BeautifulSoup

cnx = sqlite3.connect("bc-history.db")

# color table
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


# make database and table if not exist
def initialize():
    cursor = cnx.cursor()
    # USA Dollar Table
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS us (id INTEGER PRIMARY KEY AUTOINCREMENT, update_date VARCHAR(50) NOT NULL,"
        "currency_type VARCHAR(20) NOT NULL, last_rate VARCHAR(30)NOT NULL , currency_description "
        "VARCHAR(50) NOT NULL )")
    # UK Pound
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS uk (id INTEGER PRIMARY KEY AUTOINCREMENT, update_date VARCHAR(50) NOT NULL,"
        "currency_type VARCHAR(20) NOT NULL, last_rate VARCHAR(30)NOT NULL , currency_description"
        " VARCHAR(50) NOT NULL )")
    # EU Euro
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS eu (id INTEGER PRIMARY KEY AUTOINCREMENT, update_date VARCHAR(50) NOT NULL,"
        "currency_type VARCHAR(20) NOT NULL, last_rate VARCHAR(30)NOT NULL , currency_description"
        " VARCHAR(50) NOT NULL )")
    # IR Rial
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS ir (id INTEGER PRIMARY KEY AUTOINCREMENT, update_date VARCHAR(50) NOT NULL,"
        "currency_type VARCHAR(20) NOT NULL, last_rate VARCHAR(30)NOT NULL , currency_description"
        " VARCHAR(50) NOT NULL )")
    cnx.commit()


def main_menu():
    initialize()
    history_db()
    try:
        while True:
            main_input = int(input(f"{OKBLUE}\n--------------------------------------------------\n{ENDC}"
                                   "1.Bitcoin current price\n2.Bitcoin history prices\n3.dollar to rial\n4.EXIT\n: "))
            if main_input == 1:
                current_price()
            elif main_input == 2:
                bitcoin_history()
            elif main_input == 3:
                doll_ir()
            elif main_input == 4:
                print(f"{OKBLUE}bye{ENDC}")
                exit()
            else:
                print(f"{FAIL}invalid entry !!{ENDC}")
                main_menu()
    except ValueError:
        print(f"{FAIL}\ninvalid entry !!{ENDC}")
        main_menu()


def current_price():
    price_currency = int(input(f"{OKBLUE}\n--------------------------------------------------\n{ENDC}"
                               f"1.BTC/USD(United States)\n2.BTC/EUR(Europe)\n3.BTC/GBP(United Kingdom)"
                               f"\n4.BTC/RIAL(Iran)\n5.main menu\n:"))
    try:
        if price_currency == 1:
            bit_usd()
        elif price_currency == 2:
            bit_euro()
        elif price_currency == 3:
            bit_uk()
        elif price_currency == 4:
            bit_ir()
        elif price_currency == 5:
            main_menu()
        else:
            print(f"{FAIL}invalid entry !!{ENDC}")
    except ValueError:
        print(f"{FAIL}\ninvalid entry !!{ENDC}")
        current_price()


def bit_usd():
    try:
        usd_updated = requests.get('https://api.livecoin.net/exchange/ticker?currencyPair=BTC/USD')
        usd_json = usd_updated.json()
        usd_last = usd_json['last']
        usd_high = usd_json['high']
        usd_low = usd_json['low']
        print(f"{OKBLUE}\n--------------------------------------------------{ENDC}")
        print("last price : {0:24.6f} DOLLAR\nhighest price this week : {1:8.6f} DOLLAR\nlowest price this week : "
              "{2:12.6f} DOLLAR\n".format(usd_last, usd_high, usd_low))

    except requests.exceptions.ConnectionError:
        print(f"{FAIL}\nERROR: BAD CONNECTION. CHECK YOUR INTERNET !!{ENDC}")

    finally:
        main_menu()


def bit_euro():
    try:
        eur_updated = requests.get('https://api.livecoin.net/exchange/ticker?currencyPair=BTC/EUR')
        eur_json = eur_updated.json()
        eur_last = eur_json['last']
        eur_high = eur_json['high']
        eur_low = eur_json['low']
        print(f"{OKBLUE}\n--------------------------------------------------{ENDC}")
        print("last price : {0:24.6f} EURO\nhighest price this week : {1:8.6f} EURO\nlowest price this week : {2:12.6f}"
              " EURO\n".format(eur_last, eur_high, eur_low))
    except requests.exceptions.ConnectionError:
        print(f"{FAIL}\nERROR: BAD CONNECTION. CHECK YOUR INTERNET !!{ENDC}")

    finally:
        main_menu()


def bit_uk():
    try:
        uk_updated = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        uk_json = uk_updated.json()
        uk_rate = uk_json['bpi']['GBP']['rate']
        print(f"{OKBLUE}\n--------------------------------------------------{ENDC}")
        print("last price : {0:5s} POUND\nno other information\n".format(uk_rate))
        current_price()
    except requests.exceptions.ConnectionError:
        print(f"{FAIL}\nERROR: BAD CONNECTION. CHECK YOUR INTERNET !!{ENDC}")
        main_menu()


def bit_ir():
    try:
        usd_updated = requests.get('https://api.livecoin.net/exchange/ticker?currencyPair=BTC/USD')
        dollar_price = requests.get('https://www.tgju.org/%D9%82%DB%8C%D9%85%D8%AA-%D8%AF%D9%84%D8%A7%D8%B1')
        dollar_price_txt = dollar_price.text
        # print(dollar_price_txt)
        soup = BeautifulSoup(dollar_price_txt, 'html.parser')
        val = soup.find_all('td', attrs={'class': 'nf'})
        val1 = val[0]
        val2 = val1.text
        global final_price
        final_price = val2.replace(',', '')
        final_price = float(final_price)
        usd_json = usd_updated.json()
        usd_last = float(usd_json['last'])
        rial_last = usd_last * final_price
        usd_high = float(usd_json['high'])
        rial_high = usd_high * final_price
        usd_low = float(usd_json['low'])
        rial_low = usd_low * final_price
        print(f"{OKBLUE}\n--------------------------------------------------{ENDC}")
        print("last price : {0:24.3f} RIAL\nhighest price today : {1:8.3f} RIAL\nlowest price today : "
              "{2:12.3f} RIAL\n".format(rial_last, rial_high, rial_low))
        current_price()
    except requests.exceptions.ConnectionError:
        print(f"{FAIL}\nERROR: BAD CONNECTION. CHECK YOUR INTERNET !!{ENDC}")
        main_menu()


def doll_ir():
    try:
        dollar_price = requests.get('https://www.tgju.org/%D9%82%DB%8C%D9%85%D8%AA-%D8%AF%D9%84%D8%A7%D8%B1')
        dollar_price_txt = dollar_price.text
        # print(dollar_price_txt)
        soup = BeautifulSoup(dollar_price_txt, 'html.parser')
        val = soup.find_all('td', attrs={'class': 'nf'})
        val1 = val[0]
        val2 = val1.text
        final_price_dollar = val2.replace(',', '')
        final_price_dollar = float(final_price_dollar)
        print("dollar price is : ", final_price_dollar)
    except Exception:
        print("something goes wrong try again later !!")
        doll_ir()


def history_db():
    try:
        cursor = cnx.cursor()
        db_updated = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
        db_json = db_updated.json()
        time = db_json['time']['updateduk']
        curr_type = db_json['chartName']
        us_last_rate = db_json['bpi']['USD']['rate']
        us_curr_desc = db_json['bpi']['USD']['description']
        us_sql = 'INSERT INTO us (update_date, currency_type, last_rate, currency_description) VALUES(?, ?, ?, ?)'
        us_val = (time, curr_type, us_last_rate, us_curr_desc)
        cursor.execute(us_sql, us_val)
        cnx.commit()

        curr_type = db_json['chartName']
        uk_last_rate = db_json['bpi']['GBP']['rate']
        uk_curr_desc = db_json['bpi']['GBP']['description']
        uk_sql = 'INSERT INTO uk (update_date, currency_type, last_rate, currency_description) VALUES(?, ?, ?, ?)'
        uk_val = (time, curr_type, uk_last_rate, uk_curr_desc)
        cursor.execute(uk_sql, uk_val)
        cnx.commit()

        curr_type = db_json['chartName']
        eu_last_rate = db_json['bpi']['EUR']['rate']
        eu_curr_desc = db_json['bpi']['EUR']['description']
        eu_sql = 'INSERT INTO eu (update_date, currency_type, last_rate, currency_description) VALUES(?, ?, ?, ?)'
        eu_val = (time, curr_type, eu_last_rate, eu_curr_desc)
        cursor.execute(eu_sql, eu_val)
        cnx.commit()

        usd_updated = requests.get('https://api.livecoin.net/exchange/ticker?currencyPair=BTC/USD')
        dollar_price = requests.get('https://www.tgju.org/%D9%82%DB%8C%D9%85%D8%AA-%D8%AF%D9%84%D8%A7%D8%B1')
        dollar_price_txt = dollar_price.text
        # print(dollar_price_txt)
        soup = BeautifulSoup(dollar_price_txt, 'html.parser')
        val = soup.find_all('td', attrs={'class': 'nf'})
        val1 = val[0]
        val2 = val1.text
        final_price = val2.replace(',', '')
        final_price = float(final_price)
        usd_json = usd_updated.json()
        usd_last = float(usd_json['last'])
        rial_last = usd_last * final_price

        ir_curr_desc = "Rial ,Iran"
        ir_sql = 'INSERT INTO ir (update_date, currency_type, last_rate, currency_description) VALUES(?, ?, ?, ?)'
        ir_val = (time, curr_type, rial_last, ir_curr_desc)
        cursor.execute(ir_sql, ir_val)
        cnx.commit()
    except requests.exceptions.ConnectionError:
        print(f"{FAIL}\nERROR: BAD CONNECTION. CHECK YOUR INTERNET !!{ENDC}")
        main_menu()


def bitcoin_history():
    cursor = cnx.cursor()
    while True:
        his_input = int(input("1.BTC/USD\n2.BTC/GBP\n3.BTC/EUR\n4.BTC/IRA\n5.main menu\n:"))
        if his_input == 1:
            cursor.execute('SELECT * FROM us ')
            a = cursor.fetchall()
            for i in a:
                print('---------------------------\nid : {0}\ndate and time : {1}\ntype : {2}\nrate : {3}\n'
                      'currency type : {4}\n---------------------------'.format(i[0], i[1], i[2], i[3], i[4]))

        elif his_input == 2:
            cursor.execute('SELECT * FROM uk ')
            b = cursor.fetchall()
            for i in b:
                print('---------------------------\nid : {0}\ndate and time : {1}\ntype : {2}\nrate : {3}\n'
                      'currency type : {4}\n---------------------------'.format(i[0], i[1], i[2], i[3], i[4]))

        elif his_input == 3:
            cursor.execute('SELECT * FROM eu ')
            c = cursor.fetchall()
            for i in c:
                print('---------------------------\nid : {0}\ndate and time : {1}\ntype : {2}\nrate : {3}\n'
                      'currency type : {4}\n---------------------------'.format(i[0], i[1], i[2], i[3], i[4]))

        elif his_input == 4:
            cursor.execute('SELECT * FROM ir ')
            d = cursor.fetchall()
            for i in d:
                print('---------------------------\nid : {0}\ndate and time : {1}\ntype : {2}\nrate : {3}\n'
                      'currency type : {4}\n---------------------------'.format(i[0], i[1], i[2], i[3], i[4]))

        elif his_input == 5:
            main_menu()
        else:
            print(f"{FAIL}invalid entry!!{ENDC}")
            bitcoin_history()


main_menu()
# 268 line
