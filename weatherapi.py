#courtney

import requests
import json
import datetime
import os
import sqlite3


def SetUpDatabase():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+ "finaldatabase.db")
    cur = conn.cursor()
    return cur, conn

def get_temp_and_day():
    d = datetime.date(2018, 11, 30)
    date = str(d)
    dates = []
    temps = []
    sun = []

    for i in range(0, 151):
        d = d + datetime.timedelta(days = 1)
        url = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=5a9833b5e89c46039c8184642200212&q=Vail,co&date=" + str(d) + "&tp=3&format=json"
        response = requests.get(url).json()

        dates.append(str(d))
        

        r = response["data"]["weather"][0]["avgtempF"]
        temps.append(r)

        s = response["data"]["weather"][0]["sunHour"]
        sun.append(s)
        combined  = list(zip(dates, temps, sun))
    return combined  

def create_table(cur, conn):

    data = get_temp_and_day()
    count = 0
    temp = []
    days = []
    total = 0
    average = 0
    cur.execute("DROP TABLE IF EXISTS Weather")
    cur.execute("CREATE TABLE Weather (Date TEXT PRIMARY KEY, Temperature INTEGER, HoursOfSun INTEGER)")
    for tup in range(len(data)):
        if count > 24:
            break
        day = data[tup][0]
        days.append(day)
        temperature = data[tup][1]
        temp.append(temperature)
        hours = data[tup][2]
        cur.execute("INSERT INTO Weather (Date, Temperature, HoursOfSun) VALUES (?, ?, ?)", (day, temperature,hours,))
        count += 1
    conn.commit()

    cur.execute("DROP TABLE IF EXISTS Averages")
    cur.execute("CREATE TABLE Averages (Days TEXT PRIMARY KEY, AverageTemp INTEGER)")
    for t in temp:
        total = total + int(t)
    average = total / len(temp)

    dayrange = days[0] + " to " + days[-1]

    print(dayrange)

    cur.execute("INSERT INTO Averages (Days, AverageTemp) VALUES (?, ?)", (dayrange, average,))
    conn.commit()

        
        


    

# def jointables(cur, conn):
#     cur.execute("SELECT Weather.Date, Weather.Temperature FROM Weather JOIN ConditioninVail WHERE Weather.Date = ConditioninVail.Date, PercipitationinVail.Date")
#     conn.commit()

def main():
    combo = get_temp_and_day()
    cur, conn = SetUpDatabase()
    create_table(cur, conn)




if __name__ == "__main__":
    main()
