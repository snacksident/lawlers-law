import requests
from dotenv import load_dotenv
import os
import json
import random
from datetime import datetime
import time

load_dotenv() # loads environmental vars

def get_todays_games():
    todays_date = str(datetime.today())[:10]

    url = 'https://api-nba-v1.p.rapidapi.com/games'
    querystring = {"date":todays_date}
    headers = {
        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY')
        }
    todays_schedule = requests.request("GET", url, headers=headers, params=querystring)
    todays_games = open("rapid_api_todaysgames.txt","w")
    todays_json = json.dumps(todays_schedule.json())
    todays_games.write(todays_json)

get_todays_games()