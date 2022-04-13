import time
from datetime import datetime

sleep_for_checking_games = 60 * 60 * 24 #daily
sleep_for_checking_scores = 60 * 60 #hourly
sleep_loop = 60
last_game_check_time = last_score_check_time = 0 #initialize both as 0 so it runs on the first loop
while True:
    now = time.time()
    shaped_time = datetime.fromtimestamp(now) #convert to datetime shape
    print(now)
    print(shaped_time)
    if now - last_game_check_time > sleep_for_checking_games:
        last_game_check_time = now
        #check for games
    if now - last_score_check_time > sleep_for_checking_scores:
        last_score_check_time = now
        #check scores
    time.sleep(10)

# example of time within python
# def foo():
#     print(time.ctime())
# while True:
#     foo()
#     time.sleep(1)

# while (either teams score) < 100:
    #if (either teams score) > 90:
        #do a call in 3 mins
    #elif (either teams score) > 80:
        #do a call in 7 mins
    #else:
        #call in 10 mins
# if (either team score) > 100:
    #tweet out that we have a team over 100 (a 'winner' in lawlers eyes)
    #save gameID
    #follow up when game ends to determine if law was t/f