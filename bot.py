#while True:
#(automated, early AM) get days games (via sportradar.py check_todays_games())
#store games in dict/list var for reference later (teams playing, game id, scores, game time (local))
#API call at halftime just to check scores (45 min after game start?) (via sportradar.py, check_score_by_game_id() )
 # should update sportradar.txt with new current game data
    #if scores are below threshold, do not call API for another 15 mins
    #if scores are above threshold, begin API pining via time.py
        #if we get a result that both teams crossed the 100 mark since the last API call, check the "who_was_100_first.py" file to check who was first
        #save first-to-100 in var for checking after the game
        #fire off tweet announcing "winner"
        #check how much time is left in the game
            #do next API call after ~that amount of time to get final score
                #fire followup tweet if my "winning team" had lost


#app will need overhaul for new API once sportradar trial expires :(