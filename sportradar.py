import requests
from dotenv import load_dotenv
import os
import json
import random
from datetime import datetime
import time

load_dotenv() # load env vars

# python datetime defaults to YYYY-MM-DD, need to change shape to YYYY/MM/DD
todays_date = str(datetime.today()).replace('-','/')[:10] #convert datetime to string, replace -'s with /'s, take first 10 chars (for format: YYYY/MM/DD instead of python date type)
print(todays_date)

def check_todays_games():
    '''
    checks sportradar api for any games happening today.  for now, adds them to text file for further viewing
    '''
    global todays_date
    API_KEY = os.getenv('SPORTRADAR_API_KEY')
    #gonna need to change dates in URL with a var
    url = f'http://api.sportradar.us/nba/trial/v7/en/games/{todays_date}/schedule.json?api_key={API_KEY}'
    print(url)
    headers = {
        "X-Originating-IP": "104.182.70.32"
    }
    todays_schedule = requests.request('GET', url, headers=headers)
    todays_games = open("todaysgames.txt","w")
    todays_json = json.dumps(todays_schedule.json())
    todays_games.write(todays_json)


# hit game url endpoint (60 mins?) after game start to check scores.
def check_score_by_game_id(game_id):
    '''
    gets live game data about a specific game from param game_id
    returns json result of api call
    '''
    API_KEY = os.getenv('SPORTRADAR_API_KEY')
    game_url = f'http://api.sportradar.us/nba/trial/v7/en/games/{game_id}/pbp.json?api_key={API_KEY}'
    headers = {
        "X-Originating-IP": "104.182.70.32"
    }
    current_game = requests.request('GET',game_url,headers=headers)
    test_file = open("sportradar.txt","w")
    json_dumps = json.dumps(current_game.json())
    test_file.write(json_dumps)
    return current_game

def get_random_score():
    return random.randrange(1,4)

current_game_tracker = {
    "home": {
        "name": "home test", # assign team name here from API
        "score": 60 # score will likely start at 0, changing the first time we call the API
    },
    "away": {
        "name": "away test", # assign team name here from API
        "score": 60 # start at 0, changing when API is called
    }
}

#need game id in this def, to determine which game we're checking scores of
def check_scores():
    while current_game_tracker["home"]["score"] < 100 and current_game_tracker["away"]["score"] < 100:
        print(f'current score is {current_game_tracker["home"]["score"]} to {current_game_tracker["away"]["score"]}')
        if current_game_tracker["home"]["score"] or current_game_tracker["away"]["score"] > 90:
            #do a new api call in 3 mins - assign team scores rather than incrementing dummy code
            current_game_tracker["home"]["score"] += get_random_score()
            current_game_tracker["away"]["score"] += get_random_score()
            time.sleep(1) # adjust as needed. 5 set as dummy value
            #fire off a tweet that we're close to having a winner
        elif current_game_tracker["home"]["score"] or current_game_tracker["away"]["score"] > 80:
            #do a call in 7 mins
            current_game_tracker["home"]["score"] += get_random_score()
            current_game_tracker["away"]["score"] += get_random_score()
            time.sleep(3)# adjust as needed. 5 set as dummy value
        else:
            #call in 10 mins
            #reassign both team scores
            current_game_tracker["home"]["score"] += get_random_score()
            current_game_tracker["away"]["score"] += get_random_score()
            time.sleep(5)
    if current_game_tracker["home"]["score"] >= 100:
        #fire off a tweet announcing the winner
        print(f'we have a winner: {current_game_tracker["home"]["name"]}')
        print(f'final score: {current_game_tracker["home"]["score"]} to {current_game_tracker["away"]["score"]}')
    elif current_game_tracker["away"]["score"] >= 100:
        print(f'we have a winner: {current_game_tracker["away"]["name"]}')
        print(f'final score: {current_game_tracker["home"]["score"]} to {current_game_tracker["away"]["score"]}')

# check_scores()