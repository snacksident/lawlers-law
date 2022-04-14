import requests
from dotenv import load_dotenv
import os
import json
import random
from datetime import datetime
import time

load_dotenv() # load env vars

def check_todays_games():
    '''
    checks sportradar api for any games happening today.  adds them to text file for further viewing
    '''
    # python datetime defaults to YYYY-MM-DD, need to change shape to YYYY/MM/DD
    todays_date = str(datetime.today()).replace('-','/')[:10] #convert datetime to string, replace -'s with /'s, take first 10 chars (for format: YYYY/MM/DD instead of python date type)
    API_KEY = os.getenv('SPORTRADAR_API_KEY')
    #gonna need to change dates in URL with a var
    url = f'http://api.sportradar.us/nba/trial/v7/en/games/{todays_date}/schedule.json?api_key={API_KEY}'
    # print(url)
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
    writes found data to sportradar.txt
    '''
    API_KEY = os.getenv('SPORTRADAR_API_KEY')
    game_url = f'http://api.sportradar.us/nba/trial/v7/en/games/{game_id}/pbp.json?api_key={API_KEY}'
    headers = {
        "X-Originating-IP": "104.182.70.32"
    }
    current_game = requests.request('GET',game_url,headers=headers)
    #the block below should write json data into "sportsradar.txt"
    current_game_info = open("sportradar.txt","w")
    current_game_json = json.dumps(current_game.json())
    current_game_info.write(current_game_json)

#for testing live scoring / changing data
def get_random_score():
    return random.randrange(1,4)


with open("todaysgames.txt") as file:
    todays_docket = file.read()
json_docket = json.loads(todays_docket)

current_game_tracker = []
def assign_game_data():
    '''
    assigns game data to a list of dictionaries for any games happening that day
    currently only supports 1 game per day
    '''
    global current_game_tracker
    if json_docket["games"] == []:
        print('no games today')
    else:
        current_game_tracker = [{
            "id": json_docket["games"][0]["id"],
            "game-start": json_docket["games"][0]["scheduled"],
            "home": {
                "name": json_docket["games"][0]["home"]["name"], # assign team name here from API
                "score": 0 # score will likely start at 0, changing the first time we call the API
            },
            "away": {
                "name": json_docket["games"][0]["away"]["name"], # assign team name here from API
                "score": 0 # start at 0, changing when API is called
            }
        }]
    print(current_game_tracker)

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

# check_todays_games() ##THIS WORKS
# assign_game_data() ## THIS WORKS
check_score_by_game_id("4353138d-4c22-4396-95d8-5f587d2df25c") #why is this so broken????