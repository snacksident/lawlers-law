import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import time

load_dotenv() # loads environmental vars

def scheduler():
    game_on = False
    for games in games_to_track:
        while not game_on:
            utc_clock = datetime.utcnow().strftime("%H:%M:%S")
            # fake_game_start = "22:31:00"
            # if utc_clock == fake_game_start:
            #     print('its time to ball')
            #     game_on = True
            if utc_clock != games["date"]["start"][11:19]: #check utc time (HH:MM:SS) vs game start time in utc (HH:MM:SS)
                print(f'now watching the {games["home"]["name"]} vs {games["visitors"]["name"]} game')
                game_on = True #break out of loop
        #fire off tweet saying you're watching the broadcast

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
    #if no games, set 24h timer to check for games again?
    #if games today
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
        #log games info (id,start_time,home{name, score},away{home,score})
    pass
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
    '''
    for games in games_to_track:
        winner = None
        if winner == None:
            if games["home"]["score"] >= 100:
                winner = games["home"]["name"]
            if games["visitor"]["score"] >= 100:
                winner = games["visitor"]["name"]
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
                #update_scores() ?
            elif games["home"]["score"] > 80 or games["visitor"]["score"] > 80:
                #api call every minute
                time.sleep(60)
                update_scores()
            elif games["home"]["score"] > 70 or games["visitor"]["score"] > 70:
                #api call every 2 minutes
                time.sleep(120)
                update_scores()
            
                
        

def reset_data():
    '''
    resets the games_to_track list so we can start with a fresh slate every day
    '''
    global games_to_track
    games_to_track = []

# get_todays_games()
assign_game_data()  #this is working 
# update_scores() #this appears to be working - test during live games tonight
# # check_winner()
# check_live_scores()
scheduler()