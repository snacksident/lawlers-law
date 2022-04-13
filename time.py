import time

sleep_for_checking_games = 60 * 60 * 24 #daily
sleep_for_checking_scores = 60 * 60 #hourly
sleep_loop = 60
last_game_check_time = last_score_check_time = 0 #initialize both as 0 so it runs on the first loop
while True:
    now = time.time()
    if now - last_game_check_time > sleep_for_checking_games:
        last_game_check_time = now
        #check for games
    if now - last_score_check_time > sleep_for_checking_scores:
        last_score_check_time = now
        #check scores
    time.sleep(sleep_loop)

# example of time within python
# def foo():
#     print(time.ctime())
# while True:
#     foo()
#     time.sleep(1)