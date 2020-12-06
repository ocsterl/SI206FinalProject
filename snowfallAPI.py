#Olivia

import os
import requests
import http.client
import json
import sqlite3
import pandas as pd
import datetime

# Define the Key
key = "195dc45ef9c74ffcb81195700200212"

#Create the Database, URL, and Get the Data
def get_data():
    #Build API url..and insert into request, make a for loop to go through dates,append all to a list
    path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(path + '/' + "finaldatabase.db")
    cur = conn.cursor

    condition_lst = []
    precip_lst = []

    date = datetime.date(2018, 11, 30)
    d = str(date)
    dates = []
    for item in range(0, 101):
        d = date + datetime.timedelta(days = item)
        url = f"http://api.weatherapi.com/v1/history.json?key=195dc45ef9c74ffcb81195700200212&q=81657&dt=" + str(d) 
        dates.append(str(d))
        request = requests.get(url)
        data = json.loads(request.text)
        conditions = data['forecast']['forecastday'][0]['day']['condition']['text']
        condition_lst.append(conditions)
        precip = data['forecast']['forecastday'][0]['day']['totalprecip_in']
        precip_lst.append(precip)
    c_results = list(zip(dates, condition_lst))
    p_results = list(zip(dates, precip_lst))
    return c_results, p_results, conn, cur


#Create the Chance of Snowfall
def ConditionTable(cur,conn):
    info = get_data()
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS ConditionInVail (Date TEXT PRIMARY KEY, Condition TEXT")
    for item in range(len(info)):
        if counter > 24:
            break
        if cur.execute("SELECT") == None:
            date = info[item][0]
            condition = info[item][1]
            cur.execute("INSERT INTO ConditioninVail (Date, Condition) VALUES (?, ?)", (date, condition))
            counter += 1
    conn.commit()

#Create the Precipitation 
def PrecipitationTable(cur, conn):
    info = get_data()
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS PrecipitationinVail (Date TEXT PRIMARY KEY, Precipitation INTEGER")
    for item in range(len(info)):
        if counter > 24:
            break
        if cur.execute("SELECT") == None:
            date = info[item][0]
            precip = info[item][1]
            cur.execute("INSERT INTO ConditioninVail (Date, Precipiation) VALUES (?, ?)", (date, precip))
            counter += 1
    conn.commit()



def main():
    #Creating Filename
    path = os.path.dirname(os.path.realpath(__file__))
    key = "195dc45ef9c74ffcb81195700200212"

    lists = get_data()

if __name__ == "__main__":
    main()

