import requests
import os
from dotenv import load_dotenv
import json

# search 'games happening today' at the beginning of every day to view what games are happening. save gameid's, start times
# schedule api call for 2 hours after game start to check score
# if either team is at 90 points, log both teams scores to compare against eachother post-game
# if score is within tweet threshold, fire off tweet with necessary data (save game ID for follow up post-game)
# if no score within threshold, carry on. check again in another hour

#get dotenv vars available for api call
load_dotenv()
#using games endpoint for score data
url = "https://api-nba-v1.p.rapidapi.com/games"
#querystring will need interpolation to change dates/games based on what games are being played that day/night
querystring = {"date":"2022-04-09","season":"2021"}
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