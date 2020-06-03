# Twitter Trading Analyst Bot
# Author: deathlyface
# TESTED for BTCUSD

from tradingview_ta import TA_Handler
from sys import argv
from binance.client import Client
import tweepy
import datetime
from time import sleep

if len(argv) != 7:
    print("Usage: {} symbol webdriver c_key c_secret a_token a_secret".format(argv[0]))
    print("Symbol: Trading pair/symbol (ex: BTCUSDT).")
    print("Webdriver: Selenium webdriver (ex: chrome, firefox, edge).")
    print("c_key: Twitter consumer key.")
    print("c_secret: Twitter consumer secret.")
    print("a_token: Twitter access token.")
    print("a_secret: Twitter access token secret.")
    exit(1)

# Tradingview Settings
handler = TA_Handler()
handler.symbol = argv[1]
handler.interval = "1h"
handler.driver = argv[2]
handler.start_driver()

# Tweepy and Twitter Settings
auth = tweepy.OAuthHandler(argv[3], argv[4])
auth.set_access_token(argv[5], argv[6])

up = "📈"
down = "📉"
last_price = 0

# Create API object
api = tweepy.API(auth)

# Binance Settings
client = Client()

# Get Price Function
def get_price():
    klines = client.get_klines(symbol=handler.symbol.upper(), interval=handler.interval)
    price = klines[-1][4]
    return price

# Repeat Forever
while True:
    # Get current time
    now = datetime.datetime.now()

    # Tweet every time the minute is 00
    if now.minute == 00:
        price = get_price()
        analysis = handler.get_analysis()

        # Emoji
        if float(price) >= last_price:
            emoji = up
        else:
            emoji = down

        last_price = float(price)

        # You can change #btc to other crypto if you like to.
        tweet = "Hourly #btc Analysis (BETA) \n\nPrice {}: ${}\n\nAnalysis: {}\nSell: {}\nNeutral: {}\nBuy: {}\n\nSource: Tradingview and Binance\n**TRADE AT YOUR OWN RISK**\n\nOpen-source crypto analysis bot (github deathlyface/twitter-btc-bot)".format(emoji, float(price), analysis[0], analysis[1], analysis[2], analysis[3])
        api.update_status(tweet)

        # Make sure it doesn't tweet again that same minute
        sleep(60) # 1 minute
    else:
        sleep(30)

        

    




