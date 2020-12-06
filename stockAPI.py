import pandas as pd
from pandas import DataFrame
from iexfinance.stocks import Stock
from datetime import datetime
import matplotlib.pyplot as plt
from iexfinance.stocks import get_historical_data
import json
import sqlite3
import os
import time


def getHistoricalPrices(stock, start, end):
    return get_historical_data(stock, start, end, close_only = True, token="pk_b293d53490f44d968784fbd2107a0ecb")

#Date Range
start = datetime(2018, 12, 15)
end = datetime(2019, 3, 24)

#Connecting to Database
def SetUpDatabase():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + "finaldatabase.db")
    cur = conn.cursor()


#DataFrame date/price
s = getHistoricalPrices('MTN', start, end)
price = s.drop(columns = ['volume'])

#List of Prices
prices = s['close'].to_list()



index = s.index
a_list = list(index)

#List of Dates
dates = []
for i in range(0, len(a_list)):
    date_time = a_list[i].strftime("%Y-%m-%d")
    dates.append(date_time)
