#courtney

import requests
import json
import datetime
import os
import sqlite3
import matplotlib.pyplot as plt


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
    temp = []
    dates = []
    total = 0
    average = 0
    cur.execute("CREATE TABLE IF NOT EXISTS Weather (DateID INTEGER PRIMARY KEY, Date TEXT, Temperature INTEGER, HoursOfSun INTEGER)")
    
    # for tup in range(len(data)):
    #     if count > 24:
    #         break
    #     day = data[tup][0]
    #     temperature = data[tup][1]
    #     hours = data[tup][2]
    #     cur.execute("INSERT INTO Weather (Date, Temperature, HoursOfSun) VALUES (?, ?, ?)", (day, temperature,hours,))
    #     count += 1
    cur.execute("SELECT Date FROM Weather")
    datelist = cur.fetchall()
    count = len(datelist)
    for x in range(25):
        DateID = count + 1
        day = data[count][0]
        temperature = data[count][1]
        hours = data[count][2]
        count = count + 1
        cur.execute("INSERT OR IGNORE INTO Weather (DateID, Date, Temperature, HoursOfSun) VALUES (?, ?, ?, ?)", (DateID, day, temperature,hours,))

    conn.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Averages (Months TEXT PRIMARY KEY, AverageTemp FLOAT)")
    months = []
    tempD = []
    tempJ = []
    tempF = []
    tempM = []
    tempA = []
    tempMay = []
    avgj = 0
    avgd = 0
    avgf = 0
    avgm = 0
    avgmay = 0
    avga = 0
    averages = []
    countD  = 0
    countJ = 0
    countF = 0
    countM = 0
    countA = 0
    countMay = 0

    for x in range(len(data)):
        day = data[x][0]
        dates.append(day)
        temperature = data[x][1]
        temp.append(temperature)
    daytemp = list(zip(dates, temp))
    for d in range(len(daytemp)):
        if daytemp[d][0][5:7] == "12":
            if countD < 1:
                months.append("December")
                countD += 1
            tempD.append(int(daytemp[d][1][-2:]))

        if daytemp[d][0][5:7] == "01":
            if countJ  < 1:
                months.append("January")
                countJ += 1
            tempJ.append(daytemp[d][1][-2:])


        if daytemp[d][0][5:7] == "02":
            if countF < 1:
                months.append("Feburary")
                countF +=  1
            tempF.append(daytemp[d][1][-2:])

    
        if daytemp[d][0][5:7] == "03":
            if  countM < 1:
                months.append("March")
                countM += 1
            tempM.append(daytemp[d][1][-2:])
        
            
        if daytemp[d][0][5:7] == "04":
            if countA < 1:
                months.append("April")
                countA += 1
            tempA.append(daytemp[d][1][-2:])

            
        if daytemp[d][0][5:7] == "05":
            if countMay < 1:
                months.append("May")
                countMay += 1
            tempMay.append(daytemp[d][1][-2:])

    if len(tempD) > 1:
        for x in tempD:
            avgd += int(x)
        avd = float(avgd/len(tempD))
        averages.append(avd)

    if len(tempJ) > 1:
        for x in tempJ:
            avgj += int(x)
        avj = float(avgj/len(tempJ))
        averages.append(avj)

    if len(tempF) > 1:
        for x in tempF:
            avgf += int(x)
        avf = float(avgf/len(tempF))
        averages.append(avf) 

    if len(tempM)  > 1:
        for x in tempM:
            avgm += int(x)
        avm = float(avgm/len(tempM))
        averages.append(avm)

    if len(tempA) > 1:

        for x in tempA:
            avga += int(x)
        ava = float(avga/len(tempA))
        averages.append(ava)

    if len(tempMay) > 1:

        for x in tempMay:
            avgmay += int(x)
        avmay = float(avgmay/len(tempMay))
        averages.append(avmay)
   
   

    for i in range(0, len(months)):       
        cur.execute("INSERT OR IGNORE INTO Averages (Months, AverageTemp) VALUES (?, ?)", (months[i], averages[i],))
    conn.commit()
    newm = []
    for x in months:
        newm.append(str(x))
    newa = []
    for x in averages:
        newa.append(str(x))


    with open('Average_Temp_Per_Month.txt', 'w') as f:
        f.write("Average Temperature Per Month" + '\n')
        f.write("Average Temperature in " + str(months[0]) + " was " + str(averages[0])+ ". \n")
        f.write("Average Temperature in " + str(months[1]) + " was " + str(averages[1])+ ". \n")
        f.write("Average Temperature in " + str(months[2]) + " was " + str(averages[2]) +". \n")
        f.write("Average Temperature in " + str(months[3]) + " was " + str(averages[3]) +". \n")


def createvisual(cur, conn):
    data = get_temp_and_day()
    temp = []
    dates = []
    total = 0
    average = 0

    datelist = cur.fetchall()
    count = len(datelist)
    for x in range(25):
        DateID = count + 1
        day = data[count][0]
        temperature = data[count][1]
        hours = data[count][2]
        count = count + 1

    months = []
    tempD = []
    tempJ = []
    tempF = []
    tempM = []
    tempA = []
    tempMay = []
    avgj = 0
    avgd = 0
    avgf = 0
    avgm = 0
    avgmay = 0
    avga = 0
    averages = []
    countD  = 0
    countJ = 0
    countF = 0
    countM = 0
    countA = 0
    countMay = 0
    i = []

    for x in range(len(data)):
        day = data[x][0]
        dates.append(day)
        temperature = data[x][1]
        temp.append(temperature)
    daytemp = list(zip(dates, temp))
    for d in range(len(daytemp)):
        if daytemp[d][0][5:7] == "12":
            i.append(daytemp[d][0][8:])
            if countD < 1:
                months.append("December")
                countD += 1
            tempD.append(daytemp[d][1][-2:])

        if daytemp[d][0][5:7] == "01":
            if countJ  < 1:
                months.append("January")
                countJ += 1
            tempJ.append(daytemp[d][1][-2:])


        if daytemp[d][0][5:7] == "02":
            if countF < 1:
                months.append("Feburary")
                countF +=  1
            tempF.append(daytemp[d][1][-2:])

    
        if daytemp[d][0][5:7] == "03":
            if  countM < 1:
                months.append("March")
                countM += 1
            tempM.append(daytemp[d][1][-2:])
        
            
        if daytemp[d][0][5:7] == "04":
            if countA < 1:
                months.append("April")
                countA += 1
            tempA.append(daytemp[d][1][-2:])

            
        if daytemp[d][0][5:7] == "05":
            if countMay < 1:
                months.append("May")
                countMay += 1
            tempMay.append(daytemp[d][1][-2:])

    if len(tempD) > 1:
        for x in tempD:
            avgd += int(x)
        avd = float(avgd/len(tempD))
        averages.append(avd)

    if len(tempJ) > 1:
        for x in tempJ:
            avgj += int(x)
        avj = float(avgj/len(tempJ))
        averages.append(avj)

    if len(tempF) > 1:
        for x in tempF:
            avgf += int(x)
        avf = float(avgf/len(tempF))
        averages.append(avf) 

    if len(tempM)  > 1:
        for x in tempM:
            avgm += int(x)
        avm = float(avgm/len(tempM))
        averages.append(avm)

    if len(tempA) > 1:

        for x in tempA:
            avga += int(x)
        ava = float(avga/len(tempA))
        averages.append(ava)

    if len(tempMay) > 1:

        for x in tempMay:
            avgmay += int(x)
        avmay = float(avgmay/len(tempMay))
        averages.append(avmay)
   
   
    mon = []
    for m in months:
        mon.append(m[0:3])

    newtemps = []
    for temp in tempD:
        newtemps.append(int(temp))
    
    print(i)
    print(newtemps)

    

    fig, ax = plt.subplots()
    ax.plot(mon, averages)
    ax.set_xlabel("Months")
    ax.set_ylabel("Temperature (F)")
    ax.set_title("Average Temperature Per Month")

    fig.savefig("Average-Temperature.png")
    plt.show()

    figure, axi = plt.subplots()
    axi.plot(i, newtemps)
    axi.set_xlabel("December Dates")
    axi.set_ylabel("Temperature (F)")
    axi.set_title("Temperature in December")

    figure.savefig("December-Temp.png")
    plt.show()



def main():
    combo = get_temp_and_day()
    cur, conn = SetUpDatabase()
    create_table(cur, conn)
    createvisual(cur, conn)




if __name__ == "__main__":
    main()



