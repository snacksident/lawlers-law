import json

with open('todaysgames.txt') as f:
    the_api_data = f.read()
#convert cached and stringified api data back to json for parsing
json_object = json.loads(the_api_data)

game_ids = {

}

if json_object["games"]: # if there's any games today
    print('todays matchups:')
    for game in json_object["games"]: # list out the matchups and time, save gameid to dict for later use
        print(f'{game["title"]} @ {game["scheduled"]}')
        print(game["id"])