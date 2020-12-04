#Olivia

import os
import requests
import http.client
import json
import sqlite3
import pandas as pd
from datetime import datetime

# Define the Key
key = "195dc45ef9c74ffcb81195700200212"

#Create the Database, URL, and Get the Data
def get_data():
    #Build API url..and insert into request, make a for loop to go through dates,append all to a list
    path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connnnect(path + '/' + "finaldatabase.db")
    cur = conn.cursor

    start = datetime.datetime.strptime("15-12-2018", "%d-%m-%Y")
    end = datetime.datetime.strptime("24-03-2014", "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    dates = []
    for date in date_generated:
        dates.append(date.strftime("%d-%m-%Y"))

    condition_lst = []
    for num in range (0, 101):
        for date in dates:
            url = f"http://api.weatherapi.com/v1/history.json?key=195dc45ef9c74ffcb81195700200212&q=81657&dt=" + str(date) 
            request = requests.get(url)
            data = json.loads(request.text)

            conditions = data['forecast']['forecastday'][0]['day']['condition']['text']
            condition_lst.append(conditions)
    results = list(zip(dates, conditions))
    return results

#Create the Chance of Snowfall
def ConditionTable(cur,conn):
    info = get_data()
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS ConditionInVail (Date TEXT PRIMARY KEY, Condition TEXT")
    for item in range(len(info)):
        if counter < 24:
            break
        if cur.execute("SELECT") == None:
            date = info[item][0]
            condition = info[item][1]
            cur.execute("INSERT INTO ConditioninVail (Date, Condition) VALUES (?, ?)", (date, condition))
            counter += 1
    conn.commit()

#Create the Precipitation 
def PrecipitationTable(cur, conn):
    precip_lst = []
    for info in data['forecast']['forecastday'][0]['day']['totalprecip_in']:
        precip_lst.append(info)
    cur.execute("DROP TABLE IF IT EXISTS PrecipitationinVail")
    cur.execute("CREATE TABLE IF NOT EXISTS PrecipitationinVail (Date TEXT PRIMARY KEY, TotalPrecipitation TEXT")
    for item in range(len(dates)):
        cur.execute("INSERT INTO PrecipitationinVail (Date, TotalPrecipitation) VALUES (?,?)", (dates[item], precip_lst[item]))
    conn.commit()

def main():
    #Creating Filename
    path = os.path.dirname(os.path.realpath(__file__))
    key = "195dc45ef9c74ffcb81195700200212"

    #Initiliazing dates
    start = datetime.datetime.strptime("15-12-2018", "%d-%m-%Y")
    end = datetime.datetime.strptime("24-03-2014", "%d-%m-%Y")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]
    dates = []
    for date in date_generated:
        dates.append(date.strftime("%d-%m-%Y"))


