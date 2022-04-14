import json

with open('testergame.txt') as file:
    test_data = file.read()
test_json = json.loads(test_data)

if int(test_json["home"]["points"]) > 100 and int(test_json["away"]["points"]) > 100:
    print('both teams hit 100, now gotta find who did it first!')
    for periods in test_json["periods"]:
        for events in periods["events"]:
            if events["home_points"] >= 100 and events["away_points"] < 100:
                print('home team hit 100, we have a lawler event')
                break
            if events["away_points"] >= 100 and events["home_points"] < 100:
                print('away team hit 100, we have a lawler event')
                break
        # print(periods["events"][0]["home_points"])

#loop through game events
    #compare both teams scores against eachother
    #check to see if the leading team has reached 100