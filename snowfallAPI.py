import os
import requests
import http.client
import json
import sqlite3


# Create the Cache and Path
path = os.path.dirname(os.path.realpath(__file__))
snow_cache = path + '/' + "season_snowfall.json"
key = "195dc45ef9c74ffcb81195700200212"

#Read the Cache
def read_cache(CACHE_FNAME):
    try:
        fhand = open(CACHE_FNAME, 'r')
        cache_dict = json.loads(fhand.read())
        fhand.close()
        return cache_dict
    except:
        cache_dict = {}
        return cache_dict

#Write into the Cache
def write_cache(CACHE_FNAME, cache_dict):
    fpath = os.path.join(os.path.dirname(__file__), CACHE_FNAME)
    fhand = open(fpath, 'w')
    fhand.write(json.dumps(cache_dict))

#Create the URL
def get_url(area_id):
    curl = f"http://api.weatherapi.com/v1/history.json?key=195dc45ef9c74ffcb81195700200212&q=81657&dt=2019-02-15"
    return curl

#Get the Data
def get_data(curl, CACHE_FNAME):
    cache_dict = read_cache(CACHE_FNAME)
    if curl in cache_dict:
        return cache_dict[curl]
    else:
        request = requests.get(curl)
        cache_dict[curl] = json.loads(request.text)
        write_cache(CACHE_FNAME, cache_dict)
        return cache_dict[curl]


#Create the Database
path = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(path + '/' + "finaldatabase.db")
cur = conn.cursor()

#Create the Chance of Snowfall
def SnowfallTable():
    chance_lst = []
    for info in data['forecast']['forecastday']
        
    cur.execute("DROP TABLE IF EXISTS ChanceofSnowfall")
    cur.execute("CREATE TABLE IF NOT EXISTS SnowfallInVail (date TEXT PRIMARY KEY, chance_of_snow TEXT")
    for info in data['forecast']:
        cur.execute("INSERT INTO ChanceofSnow (Date, Chance of Snow) VALUES (?, ?)", ChanceofSnowfall.date, ChanceofSnowfall.chance_of_snow ")

#Create the Precipitation 





