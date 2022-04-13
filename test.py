import requests
import os
from dotenv import load_dotenv
import json

#get dotenv vars available for api call
load_dotenv()
#using games endpoint for score data
url = "https://api-nba-v1.p.rapidapi.com/games"
#querystring will need interpolation to change dates/games based on what games are being played that day/night
querystring = {"date":"2022-04-09","season":"2021"}
testquery = {"live": "1"}
#headers provided by rapidAPI
headers = {
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
	"X-RapidAPI-Key": os.getenv('RAPID_API_KEY')
}
#make api call to url with selected headers and params
response = requests.request("GET", url, headers=headers, params=querystring)
#print response json object
print(response.json())

#write data to text file to prevent need for further api calls
test_file = open("apidata.txt","w")
json_dumps = json.dumps(response.json())
test_file.write(json_dumps)

#pull data early in the AM to see if/when any games are on that day - log to txt file (schedule cron job to fire off at like... 4AM?)
#if any games are happening that day, check start times. (save start times as vars to reference later - when to ping API)
#start pinging API again for score updates starting ~30 min after halftime (not likely the score hits 100 before half)
#if a team hits 100, save that team as "lawler winner" var (call tweet.py to fire off announcement of lawler situation)
    #no need to further check scores on that game, until the game ends (verify lawler true/false)
    #check API after game ends (on a timer?) - call tweet.py verifying lawler t/f
