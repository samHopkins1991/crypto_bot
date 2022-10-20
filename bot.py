from funtions import *
from time import sleep


init()

while True:
    daily_price()

    for coin in coins:
        av_buy_sell(coin)
        panic_sell(coin)
        fomo_buy(coin)
        spot(coin)


    sleep(6)