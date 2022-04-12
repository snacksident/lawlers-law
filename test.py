import requests
import os
from dotenv import load_dotenv
# search 'games happening today' at the beginning of every day to view what games are happening. save gameid's, start times
# schedule api call for 2 hours after game start to check score
# if either team is at 90 points, log both teams scores to compare against eachother post-game
# if score is within tweet threshold, fire off tweet with necessary data (save game ID for follow up post-game)
# if no score within threshold, carry on. check again in another hour

#parse through api data for scores

url = "https://api-nba-v1.p.rapidapi.com/games"
querystring = {"date":"2022-02-12"}
rapid_api_key = os.getenv('RAPID_API_KEY')
headers = {
	"X-RapidAPI-Host": "api-nba-v1.p.rapidapi.com",
	"X-RapidAPI-Key": rapid_api_key
}

response = requests.request("GET", url, headers=headers, params=querystring)
print(response.json())

