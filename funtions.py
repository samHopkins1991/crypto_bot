import csv
from datetime import date
import test
from ast import literal_eval
import json
import logging

logging.basicConfig(filename='wealth.log', encoding='utf-8', level=logging.INFO)


today = date.today()
cash =10000
investing_increments = 1000
value = 0

PANIC_SELL_THRESH = 0.71
FOMO_BUY_THRESH = 1.19
AV_BUY_THRESH = 1.1
AV_SELL_THRESH = 0.9
SPOT_BUY_THRESH = 0.95
SPOT_SELL_THRESH = 1.05




btc = {
    "ticker": "btc",
    "my_amount": 0,
    "price": 0,
    "week": []


}

ltc = {
    "ticker": "LTC",
    "my_amount": 0,
    "price": 0,
    "week": []
}

dogecoin = {
    "ticker": "DOGE",
    "my_amount": 0,
    "price": 0,
    "week": []
}


coins = [btc,  ltc, dogecoin]

def update_price ():

    for coin in coins:

        bytes = test.quotebuy(coin["ticker"], 1)
        coin['price'] = bytes_to_json(bytes)





def bytes_to_json(bytes):
    data = literal_eval(bytes.decode('utf8'))
    # print(data)
    s = json.dumps(data)
    resp = json.loads(s)

    return resp['quote']

def buy(coin):
    global cash

    bytes = test.quotebuy(coin["ticker"], 1)
    buy_price = bytes_to_json(bytes)
    amount = calc_buy(buy_price, investing_increments)


    with open("transactions.csv", 'a') as file:
        writer = csv.writer(file)
        line = [coin["ticker"], "buy", buy_price, amount]
        writer.writerow(line)

    cash = cash - amount * buy_price
    print(amount)
    coin['my_amount'] += amount
    coin["price"] = buy_price



def sell (coin):
    global cash

    bytes = test.quotesell(coin["ticker"], 1)
    buy_price = bytes_to_json(bytes)
    amount = calc_buy(buy_price, investing_increments)


    with open("transactions.csv", 'a') as file:
        writer = csv.writer(file)
        line = [coin["ticker"], "sell", buy_price, amount]
        writer.writerow(line)

    cash = cash + amount * buy_price
    coin['my_amount'] -= amount
    coin['price'] = buy_price



def calc_buy(price, cash):
    return cash/price

def buy_price(coin):
    bytes = test.quotebuy(coin["ticker"], 1)
    buy_price = bytes_to_json(bytes)
    return buy_price

def panic_sell(coin):
    global PANIC_SELL_THRESH
    if buy_price(coin)/coin["price"] < PANIC_SELL_THRESH:
        print('Panic sold! : ', coin['ticker'])
        print (buy_price(coin)/coin['price'])
        sell(coin)

def fomo_buy(coin):
    global FOMO_BUY_THRESH
    if buy_price(coin)/coin["price"] > FOMO_BUY_THRESH:
        print("FOMO'd into: ", coin['ticker'])
        buy(coin)

def my_wealth():
    wealth = 0.00
    for coin in coins:
        wealth += (coin['my_amount'] * coin['price'])


    wealth += cash

    return wealth


def daily_price():
    global today
    if date.today().toordinal() > today.toordinal():
        for coin in coins:
            bytes = test.quotebuy(coin["ticker"], 1)
            buy_price = bytes_to_json(bytes)

            coin['price'] = buy_price
            coin['week'].append(buy_price)

            if len(coin['week']) == 8:
                coin['week'].pop(0)
        today = date.today()
        logging.info(str(today) + "current Balance: " + str(my_wealth()))
    else:
        update_price()




def get_average(coin):
    average = 0.00
    for x in range(len(coin['week'])):
        average += coin['week'][x]
    average = average/len(coin['week'])
    return average

def av_buy_sell(coin):
    global AV_SELL_THRESH, AV_SELL_THRESH

    if len(coin['week']) > 0:

        if coin['price']/get_average(coin) > AV_BUY_THRESH:
            print('average buy executed')
            buy(coin)
        if coin['price']/get_average(coin) < AV_SELL_THRESH:
            print('Average sell executed')
            sell(coin)


def spot (coin):
    if buy_price(coin)/coin['price'] >= SPOT_SELL_THRESH:
        sell(coin)
        logging.info ("spot sell: " + coin['ticker'])
    if  buy_price(coin)/coin['price'] <= SPOT_BUY_THRESH:
        logging.info("spot buy: " + coin['ticker'])
        buy(coin)
def init():
    buy(btc)
    buy(ltc)
    buy(dogecoin)
    logging.info("Date: %s Current Balance: %s", today, str(my_wealth()))

