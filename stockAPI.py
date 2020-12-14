import pandas as pd
from pandas import DataFrame
from iexfinance.stocks import Stock
from datetime import datetime
from iexfinance.stocks import get_historical_data
import json
import sqlite3
import os
import time
import plotly.graph_objects as go
import plotly.express as px


def getHistoricalPrices(stock, start, end):
    return get_historical_data(stock, start, end, close_only = True, token="pk_b293d53490f44d968784fbd2107a0ecb")

#Date Range
start = datetime(2018, 12, 15)
end = datetime(2019, 5, 24)

#Connecting to Database
def SetUpDatabase():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + "finaldatabase.db")
    cur = conn.cursor()
    return cur, conn


#DataFrame date/price
s = getHistoricalPrices('MTN', start, end)


#List of Prices
prices = s['close'].to_list()

#List of Volume
volume = s['volume'].to_list()


index = s.index
a_list = list(index)

#List of Dates
dates = []
for i in range(0, len(a_list)):
    date_time = a_list[i].strftime("%Y-%m-%d")
    dates.append(date_time)

lst1 = list(zip(dates, prices))
lst2 = list(zip(dates, volume))

dprice = []
jprice = []
fprice =[]
mprice = []
for x in lst1:
    if '2018-12' in x[0]:
        dprice.append(x[1])
    elif '2019-01' in x[0]:
        jprice.append(x[1])
    elif '2019-02' in x[0]:
        fprice.append(x[1])
    elif '2019-03' in x[0]:
        mprice.append(x[1]) 

#calculate monthly average price
def monthavg (monthlst):
    total = 0
    for i in monthlst:
        total += i
    avg = total/(len(monthlst))
    return avg

#write txt file
with open('Average_Monthly_Stock_Price.txt', 'w') as output:
    output.write('Monthly Average Price of MTN For December, January, February, and March' + '\n')
    dp = monthavg(dprice)
    jp = monthavg(jprice)
    fp = monthavg(fprice)
    mp = monthavg(mprice)
    s1 = f"The average price of MTN in December was ${dp}."
    s2 = f"The average price of MTN in January was ${jp}."
    s3 = f"The average price of MTN in February was ${fp}."
    s4 = f"The average price of MTN in March was ${mp}."
    s = []
    s.append(s1)
    s.append(s2)
    s.append(s3)
    s.append(s4)
    for i in s:
        output.write(str(i) + '\n')


#Create Price Table
def create_price_table(lst1, cur, conn):
    data = lst1
    cur.execute("CREATE TABLE IF NOT EXISTS Price (Date TEXT PRIMARY KEY, Price INTEGER)")
    cur.execute("SELECT Date FROM Price")
    lst= cur.fetchall()
    length = len(lst) + 25
    for i in range(length):
        day = data[i][0]
        price = data[i][1]
        cur.execute("INSERT OR IGNORE INTO Price (Date, Price) VALUES (?, ?)", (day, price,))
    conn.commit()


#Create Volume Table
def create_volume_table(lst2, cur, conn):
    data = lst2
    cur.execute("CREATE TABLE IF NOT EXISTS Volume (Date TEXT PRIMARY KEY, Volume INTEGER)")
    cur.execute("SELECT Date FROM Volume")
    lst = cur.fetchall()
    length = len(lst) + 25
    for i in range(length):
        day = data[i][0]
        volume = data[i][1]
        cur.execute("INSERT OR IGNORE INTO Volume (Date, Volume) VALUES (?, ?)", (day, volume,))
    conn.commit()

#crete avg price graph
def creategraph():
    months = ['December', 'January', 'February', 'March']
    price = [214.314, 195.498, 204.774, 212.648]
    df = pd.DataFrame(dict(price=price, month= months))

    img = px.line(df, x = "month", y="price", title="Average Price of MTN Stock Over Ski Season")
    img.show()




def main():
    #DataFrame date/price
    s = getHistoricalPrices('MTN', start, end)


    #List of Prices
    prices = s['close'].to_list()

    #List of Volume
    volume = s['volume'].to_list()


    index = s.index
    a_list = list(index)

    #List of Dates
    dates = []
    for i in range(0, len(a_list)):
        date_time = a_list[i].strftime("%Y-%m-%d")
        dates.append(date_time)

    lst1 = list(zip(dates, prices))
    lst2 = list(zip(dates, volume))

    cur, conn = SetUpDatabase()
    creategraph()
    create_price_table(lst1, cur, conn)
    create_volume_table(lst2, cur, conn)





if __name__ == "__main__":
    main()