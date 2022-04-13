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

home_team = { # set these vars from the api for quick reference
    "score": 0,
    "name": None, 
}
away_team = {
    "score": 0,
    "name": None,
}
# while (either teams score) < 100:
    #if (either teams score) > 90:
        #do a call in 3 mins
    #elif (either teams score) > 80:
        #do a call in 7 mins
    #else:
        #call in 10 mins
# if (either team score) > 100:
    #tweet out that we have a team over 100 (a 'winner' in lawlers eyes)
    #save gameID
    #follow up when game ends to determine if law was t/f
