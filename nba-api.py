import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time
from tweet import send_tweet

load_dotenv() # loads environmental vars

def scheduler():
    game_on = False
    for games in games_to_track:
        while not game_on:
            utc_clock = datetime.utcnow().strftime("%H:%M:%S")
            game_start = games["start"][11:19]
            if utc_clock >= game_start: #check utc time (HH:MM:SS) vs game start time in utc (HH:MM:SS)
                print(f'now watching the {games["home"]["name"]} vs {games["visitor"]["name"]} game')
                tweet_content = f'now watching the {games["home"]["name"]} vs {games["visitor"]["name"]} game'
                send_tweet(tweet_content)
                watch_game() #start the game-watching loop
                game_on = True #break out of loop

def watch_game():
    time.sleep(60 * 60) #wait an hour before checking scores
    check_live_scores() #start checking scores an hour into the game
    pass

def get_todays_games():
    '''
    gets a list of games happening on a specifi day, writes results into rapid_api_todaysgames.txt for further usage
    '''
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
    '''
    gets live data from rapid_api nba-api based on the game_id passed in.  updates nba_api.txt with results for further usage
    '''
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
with open("nba_api.txt") as f:
    current_game = f.read()
json_current = json.loads(current_game)
    

games_to_track = []
#only call this func if there are games on todays schedule
def assign_game_data():
    '''
    takes data from rapid_api_todaysgames.txt and shapes them into a dictionary for further usage during live games
    '''
    for games in json_docket["response"]:
        game = {
            "id": games["id"],
            "start": games["date"]["start"],
            "home": {
                "name": games["teams"]["home"]["name"],
                "score": 0
            },
            "visitor": {
                "name": games["teams"]["visitors"]["name"],
                "score": 0
            }
        }
        games_to_track.append(game)
    
def update_scores():
    '''
    updates scores via live API calls
    calls get_score_by_game_id on current game, checks currently logged scores vs most recently received data from API
    '''
    for games in games_to_track:
        get_score_by_game_id(games["id"])
        #if the score saved locally is less than the score received on the recent API call, reassign the score.
        if games["home"]["score"] < json_current["response"][0]["scores"]["home"]["points"]:
            games["home"]["score"] = json_current["response"][0]["scores"]["home"]["points"]
        if games["visitor"]["score"] < json_current["response"][0]["scores"]["visitors"]["points"]:
            games["visitor"]["score"] = json_current["response"][0]["scores"]["visitors"]["points"]


def check_winner():
    '''
    checks to see if a team has hit 100 points.  if conditions are met, winner is assigned to the first team to 100
    returns a winning team if there is one, otherwise returns None
    '''
    for games in games_to_track:
        winner = None
        if winner == None:
            if games["home"]["score"] >= 100:
                winner = games["home"]["name"]
            elif games["visitor"]["score"] >= 100:
                winner = games["visitor"]["name"]
            else: 
                winner = None
        #maybe just fire off the tweet when a winner has been determined?
        #log what part of the game we're currently in, set timer to ping game at 'end'?
        return winner
    
        
    print(f'and the winner is: {winner}')

def check_live_scores():
    winner = None
    while winner == None:
        winner = check_winner()
        for games in games_to_track:
            if games["home"]["score"] > 90 or games["visitor"]["score"] > 90:
                #api call 3x per minute
                time.sleep(20)
                update_scores()
            elif games["home"]["score"] > 80 or games["visitor"]["score"] > 80:
                #api call every minute
                time.sleep(60)
                update_scores()
            elif games["home"]["score"] > 70 or games["visitor"]["score"] > 70:
                #api call every 2 minutes
                time.sleep(120)
                update_scores()
            else: #if score is below 70
                time.sleep(60 * 10) #wait 10 mins
                update_scores()
            
                
def reset_data():
    '''
    resets the games_to_track list so we can start with a fresh slate every day
    '''
    global games_to_track
    games_to_track = []

get_todays_games() #todo: set to happen at midnight UTC
assign_game_data()  #this is working 
# update_scores() #this appears to be working - test during live games tonight
# check_winner()
# check_live_scores()
scheduler()