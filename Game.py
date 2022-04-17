import requests
import os
from dotenv import load_dotenv
import json

class Game():
    def __init__(self, start_time, game_id, home_name, home_score, away_name, away_score):
        self.winner = None
        self.start_time = start_time
        self.game_id = game_id
        self.home_team = {home_name,home_score}
        self.away_team = {away_name,away_score}

    def __str__(self):
        return f'{self.home_team} vs {self.away_team} @ {self.start_time}, {self.game_id}'

    def check_score(self):
        load_dotenv()
        #ping api to check for any score differences, reassign updated scores
        url = "https://api-nba-v1.p.rapidapi.com/games"
        querystring = {"id":self.game_id}
        headers = {
	        "X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
	        "X-RapidAPI-Key": os.getenv('RAPID_API_KEY')
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json() #convert to json object for further parsing
        print(response["response"])
        print(self.home_team["home_score"])
        # self.home_team["home_score"] = response["response"]["scores"]["home"]["points"]
        # self.away_team["home_score"] = response["response"]["scores"]["visitors"]["points"]
        

    def check_winner():
        pass

test_game = Game("2022-04-17T17:00:00.000Z",10914,"Miami Heat",50,"Atlanta Hawks",50)
print(test_game)
test_game.check_score()
print(f'after score check: {test_game}')