import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
def check_todays_games():
    '''
    checks sportradar api for any games happening today.  for now, adds them to text file for further viewing
    '''
    API_KEY = os.getenv('SPORTRADAR_API_KEY')
    #gonna need to change dates in URL with a var
    url = f'http://api.sportradar.us/nba/trial/v7/en/games/2022/04/12/schedule.json?api_key={API_KEY}'
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
    game_url = f'http://api.sportradar.us/nba/trial/v7/en/games/{game_id}/pbp.json?api_key={API_KEY}'
    headers = {
        "X-Originating-IP": "104.182.70.32"
    }
    current_game = requests.request('GET',game_url,headers=headers)
    test_file = open("sportradar.txt","w")
    json_dumps = json.dumps(current_game.json())
    test_file.write(json_dumps)
    return current_game

current_game_tracker = {
    "home": {
        "name": "home test",
        "score": 60
    },
    "away": {
        "name": "away test",
        "score": 75
    }
}
#  do this loop for home and away. stopping if either team reaches 100.
# while (gameid_game["home"]["score"]) < 100:
    #if (gameid_game["home"]["score"]) > 90:
        #do a new call in 3 mins
        #reassign both team scores
        #gameid_game["home"]["score"] = api_result["home"]["score"]
    #elif (either teams score) > 80:
        #do a call in 7 mins
        #reassign both team scores
        #gameid_game["home"]["score"] = api_result["home"]["score"]
    #else:
        #call in 10 mins
        #reassign both team scores
        ##gameid_game["home"]["score"] = api_result["home"]["score"]
# if (either team score) > 100:
    #tweet out that we have a team over 100 (a 'winner' in lawlers eyes)
    #save gameID
    #follow up when game ends to determine if law was t/f

def check_scores():
    while current_game_tracker["home"]["score"] < 100:
        if current_game_tracker["home"]["score"] > 90:
            pass
            #do a new call in 3 mins
            #reassign  team scores
            print(f'current score is {current_game_tracker["home"]["score"]}')
            current_game_tracker["home"]["score"] += 3
        elif current_game_tracker["home"]["score"] > 80:
            pass
            #do a call in 7 mins
            print(f'current score is {current_game_tracker["home"]["score"]}')
            current_game_tracker["home"]["score"] += 5
        else:
            pass
            #call in 10 mins
            #reassign both team scores
            print(f'current score is {current_game_tracker["home"]["score"]}')
            current_game_tracker["home"]["score"] += 5
    if current_game_tracker["home"]["score"] > 100:
        print('we have a winner!!')

check_scores()