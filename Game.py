import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
from tweet import send_tweet
from dateutil import parser

class Game():
    def __init__(self, start_time, game_id, home_name, home_score, away_name, away_score):
        self.winner = None
        self.start_time = start_time
        self.game_id = game_id
        self.home_name = home_name
        self.home_score = home_score
        self.away_name = away_name
        self.away_score = away_score
        self.next_check_time = start_time #+ timedelta(minutes = 90)
        self.status = None

    def __str__(self):
        return f'{self.home_name} vs {self.away_name} @ {self.start_time}, {self.game_id} - score is {self.home_score} to {self.away_score}'

    def __repr__(self):
        return f'{self.home_name} vs {self.away_name} @ {self.start_time}, {self.game_id} - score is {self.home_score} to {self.away_score}'

    def check_score_time(self):
        current_time = time.time()
        print(f'current time is: {current_time}, and check time is: {self.next_check_time}')
        #convert next_check_time to time shape here
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(current_time))
        # test_time = datetime.utcnow().isoformat()
        # print(f'test time is {test_time}')
        print(f'current time AFTER is: {current_time}, and check time AFTER is: {self.next_check_time}')
        if current_time > self.next_check_time:
            self.check_score()
            print(f'checking scores. currently {self.home_name} @ {self.home_score} vs {self.away_name} @ {self.away_score}')
            if self.home_score > 100 or self.away_score > 100:
                if self.home_score > 100:
                    self.winner = self.home_name
                elif self.away_score > 100:
                    self.winner = self.away_name
            elif self.home_score > 90 or self.away_score > 90:
                self.next_check_time = current_time + timedelta(seconds = 20)
            elif self.home_score > 80 or self.away_score > 80:
                self.next_check_time = current_time + timedelta(seconds = 90)
            else:
                print('checking scores again in 120 seconds!')
                self.next_check_time = current_time + timedelta(seconds = 120)

    def check_score(self):
        '''
        checks score on rapidAPI - updates home_score and away_score
        '''
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
        self.home_score = response["response"][0]["scores"]["home"]["points"]
        self.away_score = response["response"][0]["scores"]["visitors"]["points"]
        #maybe recursively call check_score (on a timer depending on current score) until a team hits 100?
        


    def watch_game(self):
        while self.winner == None:
            self.check_score_time()

# test_game = Game("2022-04-17T17:00:00.000Z",10914,"Miami Heat",50,"Atlanta Hawks",50)
# print(test_game)
# test_game.check_score() #seems to work, scores updating correctly
# print(f'after check_score(): {test_game}')

#while there is a game that is not "Finished"
    #check scores on this game
