import json

with open('testergame.txt') as file:
    test_data = file.read()
test_json = json.loads(test_data)

def who_hit_100_first():
    '''
    in case of 'tie' situation due to non-polling API, check who actually hit 100 first.
    will return the team name of the 'winner'
    '''
    if int(test_json["home"]["points"]) > 100 and int(test_json["away"]["points"]) > 100:
        print('both teams hit 100, now gotta find who did it first!')
        for periods in test_json["periods"]:
            for events in periods["events"]:
                if events["home_points"] >= 100 and events["away_points"] < 100:
                    print('home team hit 100, we have a lawler event')
                    print(events["id"])
                    break
                    #return home team
                if events["away_points"] >= 100 and events["home_points"] < 100:
                    print('away team hit 100, we have a lawler event')
                    print(events["id"])
                    break
                    #return away team
        # print(periods["events"][0]["home_points"])
