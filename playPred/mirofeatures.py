import nflgame
from collections import defaultdict
import numpy as np

#Start year and end year inclusive
def getFeatures(start, end):

    all_features = []
    isPass = []
    
    for year in range(start, end + 1):
        for week in range(1,18):
            games = nflgame.games(year = year, week = week) #Get games by year/week

            for play in nflgame.combine_plays(games): #Iterate through all plays

                features = defaultdict(float)

                # TODO: Change the conditions, spikes might be interesting to add to play prediction

                if (play.note == None or play.note == 'TD' or play.note == 'INT') \
                        and (' punt' not in play.desc) \
                        and ('END ' != play.desc[:4]) \
                        and ('End ' != play.desc[:4]) \
                        and ('Two-Minute Warning' not in play.desc) \
                        and ('spiked the ball to stop the clock' not in play.desc) \
                        and ('kneels to ' not in play.desc) \
                        and ('Delay of Game' not in play.desc) \
                        and (play.time is not None) \
                        and ('Penalty on' not in play.desc) \
                        and ('Delay of Game' not in play.desc) \
                        and ('sacked at' not in play.desc) \
                        and ('Punt formation' not in play.desc) \
                        and ('Direct snap to' not in play.desc) \
                        and ('Aborted' not in play.desc) \
                        and ('temporary suspension of play' not in play.desc) \
                        and ('TWO-POINT CONVERSION ATTEMPT' not in play.desc) \
                        and ('warned for substitution infraction' not in play.desc) \
                        and ('no play run - clock started' not in play.desc) \
                        and ('challenged the first down ruling' not in play.desc) \
                        and ('*** play under review ***' not in play.desc) \
                        and ('Direct Snap' not in play.desc) \
                        and ('Direct snap' not in play.desc): 


                    # Features: team, opponent, time of play, 

                    features['team'] = play.team
                    features['isHome'] = (play.home)
                    if play.drive.game.away == play.team:
                        features['opponent'] = play.drive.game.home
                    else:
                        features['opponent'] = play.drive.game.away
                    timeclock = play.time.clock.split(':')
                    features['time'] = float(timeclock[0]) * 60 + float(timeclock[1])
                    if (play.time.qtr == 1) or (play.time.qtr == 3):
                        features['time'] += 15 * 60

                    features['position'] = 50 - play.yardline.offset
                    features['down'] = play.down
                    features['togo'] = play.yards_togo

                    if 'Shotgun' in play.desc:
                        features['shotgun'] = 1
                    else:
                        features['shotgun'] = 0

                    if 'incomplete' in play.desc or ' pass ' in play.desc:
                        isPass.append(1)
                    else:
                        isPass.append(0)

                    all_features.append(features)

    return all_features, isPass


