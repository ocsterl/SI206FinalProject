#courtney
#courtney

import requests
import json
import datetime


def get_temp_and_day():
    
    d = datetime.date(2018, 11, 30)
    date = str(d)
    dates = []
    temps = []
    for i in range(0, 101):
        d = d + datetime.timedelta(days = 1)
        url = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=5a9833b5e89c46039c8184642200212&q=Vail,co&date=" + str(d) + "&tp=3&format=json"
        response = requests.get(url).json()

        dates.append(str(d))

        r = response["data"]["weather"][0]["avgtempF"]
        temps.append(r)

    return dates, temps

print(get_temp_and_day())

