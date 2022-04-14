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

def get_score_by_game_id(game_id):
    API_KEY = os.getenv('RAPID_API_KEY')
    url = "https://api-nba-v1.p.rapidapi.com/games"
    querystring = {"id": game_id}
    headers = {
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
	"X-RapidAPI-Key": API_KEY
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    current_score_info = open("nba_api.txt","w")
    current_score_json = json.dumps(response.json())
    current_score_info.write(current_score_json)

with open("rapid_api_todaysgames.txt") as todays_games:
    todays_docket = todays_games.read()
json_docket = json.loads(todays_docket)

def assign_game_data():
    #check if any games on the menu today
    #if no games, set 24h timer to check for games again?
    #if games today
        #log games info (id,start_time,home{name, score},away{home,score})
    pass
