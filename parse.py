import json

with open('apidata.txt') as f:
    the_api_data = f.read()
#convert cached and stringified api data back to json for parsing
json_object = json.loads(the_api_data)
home_team = json_object["response"][0]["teams"]["home"]["name"]
home_score = json_object["response"][0]["scores"]["home"]["points"]
away_team = json_object["response"][0]["teams"]["visitors"]["name"]
away_score = json_object["response"][0]["scores"]["visitors"]["points"]

print(f'the visiting team for sample data is: {away_team}')
print(f'the home team for sample data is: {home_team}')
print(f'the visitors score for sample data is: {away_score}')
print(f'the home score for sample data is {home_score}')
print(f'the final score is: {home_team}:{home_score}, {away_team}:{away_score}')
