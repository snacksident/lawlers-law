import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
def check_todays_games():
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

# check if there's any games happening today
    # if there are games, grab and save game ID's to use in the game url
    # if no games, do not make any more API calls until next day


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
    # if a team is "close to" 100, do another ping shortly after 
    
    # if a team is AT OR PAST 100, we can stop pinging until the game is over. save teams ID
    # send tweet (f'we have a winner!  {team who hit 100} bested {other team} with {time left in the game} to spare!!!')
    # at game end, check winning team ID vs first_team_to100 ID

test_file = open("sportradar.txt","w")
json_dumps = json.dumps(current_game.json())
test_file.write(json_dumps)