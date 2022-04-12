import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY = os.getenv('SPORTRADAR_API_KEY')
url = f'http://api.sportradar.us/nba/trial/v7/en/games/2022/04/12/schedule.json?api_key={API_KEY}'
print(url)
headers = {
    "X-Originating-IP": "104.182.70.32"
}
response = requests.request('GET', url, headers=headers)

print(response.json())

todays_games = {}
test_file = open("sportradar.txt","w")
json_dumps = json.dumps(response.json())
test_file.write(json_dumps)