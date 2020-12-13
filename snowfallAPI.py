#Olivia
import json
import requests
import os
import sqlite3
import datetime
import plotly.graph_objects as go

# Define the Key
key = "195dc45ef9c74ffcb81195700200212"

#Create the Database, URL, and Get the Data
def SetUp():
    #Build API url..and insert into request, make a for loop to go through dates,append all to a list
    path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(path + '/' + "finaldatabase.db")
    cur = conn.cursor()
    return cur, conn


def get_data():
    condition_lst = []
    precip_lst = []

    date = datetime.date(2018, 11, 30)
    d = str(date)
    dates = []
    for item in range(0, 151):
        d = date + datetime.timedelta(days = item)
        url = "http://api.weatherapi.com/v1/history.json?key=195dc45ef9c74ffcb81195700200212&q=81657&dt=" + str(d)
        dates.append(str(d))
        request = requests.get(url)
        data = json.loads(request.text)
        conditions = data['forecast']['forecastday'][0]['day']['condition']['text']
        condition_lst.append(conditions)
        precip = data['forecast']['forecastday'][0]['day']['totalprecip_in']
        precip_lst.append(precip)
    c_results = list(zip(dates, condition_lst))
    p_results = list(zip(dates, precip_lst))
    print(c_results)
    return c_results, p_results


#Create the Chance of Snowfall
def ConditionTable(conn, cur):
    c_results, p_results = get_data()
    cur.execute("CREATE TABLE IF NOT EXISTS ConditionInVail (dateid INTEGER PRIMARY KEY, date TEXT, condition TEXT)")
    cur.execute("SELECT Date FROM ConditionInVail")
    datelst = cur.fetchall()
    counter = len(datelst)
    counting = counter + 25
    for num in range(counting):
        dateid = num
        date = c_results[num][0]
        condition = c_results[num][1]
        print(dateid, date, condition)
        cur.execute("INSERT OR IGNORE INTO ConditionInVail (dateid, date, condition) VALUES (?, ?, ?)", (dateid, date, condition,))
    conn.commit()

# Create the Precipitation 
def PrecipitationTable(conn, cur):
    c_results, p_results = get_data()
    counter = 0
    cur.execute("CREATE TABLE IF NOT EXISTS PrecipitationInVail (dateid TEXT PRIMARY KEY, date TEXT, precipitation INTEGER)")
    cur.execute("SELECT date From PrecipitationInVail")
    datelst = cur.fetchall()
    counter = len(datelst)
    counting = counter + 25
    for num in range(counting):
        dateid = num
        date = p_results[num][0]
        precipitation = p_results[num][1]
        cur.execute("INSERT OR IGNORE INTO PrecipitationInVail (dateid, date, precipitation) VALUES (?, ?, ?)", (dateid, date, precipitation))
    conn.commit()

def Get_Most_Common_Condition():
    c_results, p_results = get_data()
    for num in range(0,5):
        if num == 1:
            clear_lst1 = []
            cloudy_lst1 = []
            rain_lst1 = []
            snow_lst1 = []
            for item in c_results[0:32]:
                if item[1] == "Sunny" or item[1] == "Clear":
                    clear_lst1.append(item[1])
                elif item[1] == "Partly cloudy" or item[1] == "Overcast" or item[1] == "Fog" or item[1] == "Freezing fog":
                    cloudy_lst1.append(item[1])
                elif item[1] == "Patchy rain possible" or item[1] == "Patchy freezing drizzle possible" or item[1] == "Thundery outbreaks possible" or item[1] == "Patchy sleet possible" or item[1] == "Pathcy light drizzle" or item[1] == "Light drizzle" or item[1] == "Freezing drizzle" or item[1] == "Heavy freezing drizzle" or item[1] == "Patchy light rain" or item[1] == "Moderate rain at times" or item[1] == "Moderate rain" or item[1] == "Heavy rain at times" or item[1] == "Heavy rain" or item[1] == "Light freezing rain" or item[1] == "Moderate or heavy freezing rain" or item[1] == "Light sleet" or item[1] == "Moderate or heavy sleet" or item[1] == "Light rain shower" or item[1] == "Moderate or heavy rain shower" or item[1] == "Torrential rain showers" or item[1] == "Light sleet showers" or item[1] == "Moderate or heavy sleet showers" or item[1] == "Light showers of ice pellets" or item[1] == "Moderate or heavy showers of ice pellets" or item[1] == "Patchy light rain with thunder" or item[1] == "Moderate or heavy rain with thunder":
                    rain_lst1.append(item)
                elif item[1] == "Patchy snow possible" or item[1] == "Blowing snnow" or item[1] == "Blizzard" or item[1] == "Patchy light snow" or item[1] == "Light snow" or item[1] == "Patchy moderate snow" or item[1] == "Moderate snow" or item[1] == "Patchy heavy snow" or item[1] == "Heavy snow" or item[1] == "Light snow showers" or item[1] == "Moderate or heavy snow showers" or item[1] == "Patchy light snow with thunder" or item[1] == "Moderate or heavy snow with thunder":
                    snow_lst1.append(item)
                clear_len1 = len(clear_lst1)
                c_len1 = len(cloudy_lst1)
                r_len1 = len(rain_lst1)
                s_len1 = len(snow_lst1)
        if num == 2:
            clear_lst2 = []
            cloudy_lst2 = []
            rain_lst2 = []
            snow_lst2 = []
            for item in c_results[32:63]:
                if item[1] == "Sunny" or item[1] == "Clear":
                    clear_lst2.append(item)
                elif item[1] == "Partly cloudy" or item[1] == "Overcast" or item[1] == "Fog" or item[1] == "Freezing fog":
                    cloudy_lst2.append(item)
                elif item[1] == "Patchy rain possible" or item[1] == "Patchy freezing drizzle possible" or item[1] == "Thundery outbreaks possible" or item[1] == "Patchy sleet possible" or item[1] == "Pathcy light drizzle" or item[1] == "Light drizzle" or item[1] == "Freezing drizzle" or item[1] == "Heavy freezing drizzle" or item[1] == "Patchy light rain" or item[1] == "Moderate rain at times" or item[1] == "Moderate rain" or item[1] == "Heavy rain at times" or item[1] == "Heavy rain" or item[1] == "Light freezing rain" or item[1] == "Moderate or heavy freezing rain" or item[1] == "Light sleet" or item[1] == "Moderate or heavy sleet" or item[1] == "Light rain shower" or item[1] == "Moderate or heavy rain shower" or item[1] == "Torrential rain showers" or item[1] == "Light sleet showers" or item[1] == "Moderate or heavy sleet showers" or item[1] == "Light showers of ice pellets" or item[1] == "Moderate or heavy showers of ice pellets" or item[1] == "Patchy light rain with thunder" or item[1] == "Moderate or heavy rain with thunder":
                    rain_lst2.append(item)
                elif item[1] == "Patchy snow possible" or item[1] == "Blowing snnow" or item[1] == "Blizzard" or item[1] == "Patchy light snow" or item[1] == "Light snow" or item[1] == "Patchy moderate snow" or item[1] == "Moderate snow" or item[1] == "Patchy heavy snow" or item[1] == "Heavy snow" or item[1] == "Light snow showers" or item[1] == "Moderate or heavy snow showers" or item[1] == "Patchy light snow with thunder" or item[1] == "Moderate or heavy snow with thunder":
                    snow_lst2.append(item)
                clear_len2 = len(clear_lst2)
                c_len2 = len(cloudy_lst2)
                r_len2 = len(rain_lst2)
                s_len2 = len(snow_lst2)
        if num == 3:
            clear_lst3 = []
            cloudy_lst3 = []
            rain_lst3 = []
            snow_lst3 = []
            for item in c_results[62:91]:
                if item[1] == "Sunny" or item[1] == "Clear":
                    clear_lst3.append(item)
                elif item[1] == "Partly cloudy" or item[1] == "Overcast" or item[1] == "Fog" or item[1] == "Freezing fog":
                    cloudy_lst3.append(item)
                elif item[1] == "Patchy rain possible" or item[1] == "Patchy freezing drizzle possible" or item[1] == "Thundery outbreaks possible" or item[1] == "Patchy sleet possible" or item[1] == "Pathcy light drizzle" or item[1] == "Light drizzle" or item[1] == "Freezing drizzle" or item[1] == "Heavy freezing drizzle" or item[1] == "Patchy light rain" or item[1] == "Moderate rain at times" or item[1] == "Moderate rain" or item[1] == "Heavy rain at times" or item[1] == "Heavy rain" or item[1] == "Light freezing rain" or item[1] == "Moderate or heavy freezing rain" or item[1] == "Light sleet" or item[1] == "Moderate or heavy sleet" or item[1] == "Light rain shower" or item[1] == "Moderate or heavy rain shower" or item[1] == "Torrential rain showers" or item[1] == "Light sleet showers" or item[1] == "Moderate or heavy sleet showers" or item[1] == "Light showers of ice pellets" or item[1] == "Moderate or heavy showers of ice pellets" or item[1] == "Patchy light rain with thunder" or item[1] == "Moderate or heavy rain with thunder":
                    rain_lst3.append(item)
                elif item[1] == "Patchy snow possible" or item[1] == "Blowing snnow" or item[1] == "Blizzard" or item[1] == "Patchy light snow" or item[1] == "Light snow" or item[1] == "Patchy moderate snow" or item[1] == "Moderate snow" or item[1] == "Patchy heavy snow" or item[1] == "Heavy snow" or item[1] == "Light snow showers" or item[1] == "Moderate or heavy snow showers" or item[1] == "Patchy light snow with thunder" or item[1] == "Moderate or heavy snow with thunder":
                    snow_lst3.append(item)
                clear_len3 = len(clear_lst3)
                c_len3 = len(cloudy_lst3)
                r_len3 = len(rain_lst3)
                s_len3 = len(snow_lst3)
        if num == 4:
            clear_lst4 = []
            cloudy_lst4 = []
            rain_lst4 = []
            snow_lst4 = []
            for item in c_results[90:121]:
                if item[1] == "Sunny" or item[1] == "Clear":
                    clear_lst4.append(item)
                elif item[1] == "Partly cloudy" or item[1] == "Overcast" or item[1] == "Fog" or item[1] == "Freezing fog":
                    cloudy_lst4.append(item)
                elif item[1] == "Patchy rain possible" or item[1] == "Patchy freezing drizzle possible" or item[1] == "Thundery outbreaks possible" or item[1] == "Patchy sleet possible" or item[1] == "Pathcy light drizzle" or item[1] == "Light drizzle" or item[1] == "Freezing drizzle" or item[1] == "Heavy freezing drizzle" or item[1] == "Patchy light rain" or item[1] == "Moderate rain at times" or item[1] == "Moderate rain" or item[1] == "Heavy rain at times" or item[1] == "Heavy rain" or item[1] == "Light freezing rain" or item[1] == "Moderate or heavy freezing rain" or item[1] == "Light sleet" or item[1] == "Moderate or heavy sleet" or item[1] == "Light rain shower" or item[1] == "Moderate or heavy rain shower" or item[1] == "Torrential rain showers" or item[1] == "Light sleet showers" or item[1] == "Moderate or heavy sleet showers" or item[1] == "Light showers of ice pellets" or item[1] == "Moderate or heavy showers of ice pellets" or item[1] == "Patchy light rain with thunder" or item[1] == "Moderate or heavy rain with thunder":
                    rain_lst4.append(item)
                elif item[1] == "Patchy snow possible" or item[1] == "Blowing snnow" or item[1] == "Blizzard" or item[1] == "Patchy light snow" or item[1] == "Light snow" or item[1] == "Patchy moderate snow" or item[1] == "Moderate snow" or item[1] == "Patchy heavy snow" or item[1] == "Heavy snow" or item[1] == "Light snow showers" or item[1] == "Moderate or heavy snow showers" or item[1] == "Patchy light snow with thunder" or item[1] == "Moderate or heavy snow with thunder":
                    snow_lst4.append(item)
                clear_len4 = len(clear_lst4)
                c_len4 = len(cloudy_lst4)
                r_len4 = len(rain_lst4)
                s_len4 = len(snow_lst4)
    
    with open("Conditions_Per_Month.txt", "w") as filer:
        filer.write("Conditions in Vail Per Month" + "\n")
        filer.write("There were " + str(clear_len1) + " clear days, " + str(c_len1) + " cloudy days, " + str(r_len1) + " rainy days, " + str(s_len1) + " snowy days in Vail during the month of December." + "\n") 
        filer.write("There were " + str(clear_len2) + " clear days, " + str(c_len2) + " cloudy days, " + str(r_len2) + " rainy days, " + str(s_len2) + " snowy days in Vail during the month of January." + "\n") 
        filer.write("There were " + str(clear_len3) + " clear days, " + str(c_len3) + " cloudy days, " + str(r_len3) + " rainy days, " + str(s_len3) + " snowy days in Vail during the month of February." + "\n") 
        filer.write("There were " + str(clear_len4) +  " clear days, " + str(c_len4) + " cloudy days, " + str(r_len4) + " rainy days, " + str(s_len4) + " snowy days in Vail during the month of March. " + "\n") 

#Creating Plot for Conditions Per Month:'
def ConditionsGraph():
    months = ["December", "January", "February", "March"]
    title_lbl = "Conditions in Vail Per Month"
    fig = go.Figure(data = [
        go.Bar(name = "Clear Days", x = months, y = [18, 0, 0, 0]),
        go.Bar(name = "Cloudy Days", x = months, y = [9, 11, 8 ,6]),
        go.Bar(name = "Rainy Days", x = months, y = [0, 0, 0, 1]),
        go.Bar(name = "Snowy Days", x = months, y = [3, 21, 21, 24]),
    ])
    fig.update_layout(
        title = {'text': title_lbl},
        font_family = "Sans Serif",
        barmode='group')
    fig.show()

def jointables(cur, conn):
    cur.execute("SELECT PrecipitationInVail.date, PrecipitationInVail.precipitation FROM PrecipitationInVail JOIN Weather WHERE PrecipitationInVail.date = Weather.Date")
    return cur.fetchall()



def main():
    # #Creating Filename
    path = os.path.dirname(os.path.realpath(__file__))
    key = "195dc45ef9c74ffcb81195700200212"
    # commons = Get_Most_Common_Condition()
    cur, conn = SetUp()
    # lists = get_data()
    # c_table= ConditionTable(conn,cur)
    # p_table = PrecipitationTable(conn, cur)
    joins = jointables(cur, conn)
    print(joins)
    # # graph1 = ConditionsGraph()


if __name__ == "__main__":
    main()

