import json

with open('apidata.txt') as f:
    the_api_data = f.read()
#convert cached and stringified api data back to json for parsing
json_object = json.loads(the_api_data)


# print(f'matchups for: {json_object["parameters"]["date"]}')
# for matchups in json_object["response"]:
#     print(f'{matchups["teams"]["home"]["name"]} vs {matchups["teams"]["visitors"]["name"]}')
#     print(f'{matchups["scores"]["home"]["points"]} vs {matchups["scores"]["visitors"]["points"]}')



home_team = json_object["response"][0]["teams"]["home"]["name"]
home_score = json_object["response"][0]["scores"]["home"]["points"]
away_team = json_object["response"][0]["teams"]["visitors"]["name"]
away_score = json_object["response"][0]["scores"]["visitors"]["points"]
lawler_score = 100
lawler_event = False
# print(f'the final score is: {home_team}:{home_score}, {away_team}:{away_score}')
with open('sportradar.txt') as g:
    sportradar_data = g.read()
sportradar_json = json.loads(sportradar_data)
if sportradar_json["status"] == "closed": #if the game is over
    print('game over')
    print(f'{sportradar_json["home"]["name"]} had {sportradar_json["home"]["points"]}' )
    print(f'{sportradar_json["away"]["name"]} had {sportradar_json["away"]["points"]}' )
# if sportradar_json["status"] == "scheduled"
# print(sportradar_json["games"])
# for games in sportradar_json["games"]:
#     print(f'games start at {games["scheduled"]}, this games id is {games["id"]}')
#     print(f'matchup is: {games["home"]["name"]} vs {games["away"]["name"]}')

#this file should run every time new data arrives
