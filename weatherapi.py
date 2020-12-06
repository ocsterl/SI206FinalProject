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
    for i in range(0, 151):
        d = d + datetime.timedelta(days = 1)
        url = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=5a9833b5e89c46039c8184642200212&q=Vail,co&date=" + str(d) + "&tp=3&format=json"
        response = requests.get(url).json()

        dates.append(str(d))
        

        r = response["data"]["weather"][0]["avgtempF"]
        temps.append(r)
        combined  = list(zip(dates, temps))
    print(combined)

    return combined  

def create_table(cur, conn):

    data = get_temp_and_day()
    count = 0
    cur.execute("DROP TABLE IF EXISTS Weather")
    cur.execute("CREATE TABLE Weather (Date TEXT PRIMARY KEY, Temperature INTEGER)")
    for tup in range(len(data)):
        if count > 24:
            break
        day = data[tup][0]
        temperature = data[tup][1]
        cur.execute("INSERT INTO Weather (Date, Temperature) VALUES (?, ?)", (day, temperature,))
        count += 1
    conn.commit()

def main():
    combo = get_temp_and_day()
    cur, conn = SetUpDatabase()
    create_table(cur, conn)




if __name__ == "__main__":
    main()


         
    # for i in range(len(category_list)):
    #     cur.execute("INSERT INTO Weather (date,temp) VALUES (?,?)",(i,category_list[i]))
    # conn.commit()
#     #create db file and cur and con -- modify name of file from assignments 
#     #DONT DO DROP TABLE 
#     #date PRIMARY KEY -- across ALL DATABASE (makes joins easier)
#     cur.execute("CREATE TABLE ")
#     temps = get_temp_and_day() 
#     count = 0
#     for x in temps:
#         #check count var 
#         if count < 24:
#             break
#         #select statement 
#         if cur.execute("SELECT ") == None:
#             cur.execute("INSERT date, temp = ? ?",
#             count += 1

#     con.commit()

