#courtney

import requests
import json
import datetime
import os
import sqlite3


def get_temp_and_day():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ "weather.db")
    cur = conn.cursor()
    
    d = datetime.date(2018, 11, 30)
    date = str(d)
    dates = []
    temps = []
    for i in range(0, 151):
        d = d + datetime.timedelta(days = 1)
        url = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=5a9833b5e89c46039c8184642200212&q=Vail,co&date=" + str(d) + "&tp=3&format=json"
        response = requests.get(url).json()

        dates.append(str(d))
        

        r = response["data"]["weather"][0]["avgtempF"]
        temps.append(r)
        combined  = list(zip(dates, temps))  

    cur.execute("CREATE TABLE Weather (Date TEXT PRIMARY KEY, Temperature INTEGER)")
    count = 0
    for combo in range(len(combined)):
        if count < 24:
            break
        if cur.execute("SELECT") == None:
            day = combined[combo][0]
            temperature = combined[combo][1]
            cur.execute("INSERT INTO Weather (Date, Temperature) VALUES (?, ?)", day, temperature,)
            count += 1
    conn.commit()






