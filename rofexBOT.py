#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 11:37:34 2021

@author: lorenzo

Rofex-BOT
"""

import pyRofex
import pandas as pd
import numpy as np
from datetime import datetime

pyRofex.initialize(user="MD_REYES", 
                   password="Lorenzo6+", 
                   account="88406",
                   environment=pyRofex.Environment.LIVE)

instruments = [str(input("Enter instrument to operate: "))]

prices = pd.DataFrame(columns=["Time", "Bid", "Offer", "Last"])
prices.set_index('Time', inplace=True)

def market_data_handler(message):
    global prices
    last = None if not message["marketData"]["LA"] else message["marketData"]["LA"]["price"]
    prices.loc[datetime.fromtimestamp(message["timestamp"]/1000)] = [
        message["marketData"]["BI"][0]["price"],
        message["marketData"]["OF"][0]["price"],
        last
    ]
    chartboard()

entries=[pyRofex.MarketDataEntry.BIDS,
        pyRofex.MarketDataEntry.OFFERS,
        pyRofex.MarketDataEntry.LAST]

# 3-Initialize Websocket Connection with the handlers
pyRofex.init_websocket_connection(market_data_handler=market_data_handler)
pyRofex.market_data_subscription(tickers=instruments,
                                 entries=entries)

prices = prices.append(prices)

response = pyRofex.get_all_instruments()


for inst in response['instruments']:
    instruments.append(inst['instrumentId']['symbol'])

instrument = instruments[0] # reformat list to string
validate = instrument in instruments
print(f'Is {instrument} a valid instrument? {validate}')

if validate==True:
    def chartboard():
        bot = pd.DataFrame(prices['Last'].values, columns=['Last'], index=prices.index)
        bot['SMA'] = prices['Last'].rolling(round(len(bot.index)*0.05), min_periods=1).mean()
        bot['signal'] = 0.0
        bot['signal'] = np.where(bot['Last'] > bot['SMA'], 1.0, 0.0)  # use a conditional
        bot['positions'] = bot['signal'].diff()
        print(bot.tail(1))
        
        
