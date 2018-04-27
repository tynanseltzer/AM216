import numpy as np
import pandas as pd
import string
import csv
import requests
import matplotlib.pyplot as plt
import pandas as pd
from nba_py.shotchart import ShotChart
from nba_py import game
import requests_cache
from xgboost import XGBClassifier
import random
import sklearn
 
zones = [
    ['Center(C)', 'Less Than 8 ft.'],
    ['Center(C)', '8-16 ft.'],
    ['Center(C)', '16-24 ft.'],
    ['Center(C)', '24+ ft.'],
    ['Left Side(L)', '8-16 ft.'],
    ['Left Side(L)', '16-24 ft.'],
    ['Left Side(L)', '24+ ft.'],
    ['Right Side(R)', '8-16 ft.'],
    ['Right Side(R)', '16-24 ft.'],
    ['Right Side(R)', '24+ ft.'],
    ['Left Side Center(LC)', '16-24 ft.'],
    ['Left Side Center(LC)', '24+ ft.'],
    ['Right Side Center(RC)', '16-24 ft.'],
    ['Right Side Center(RC)', '24+ ft.'],
]
 
def gen_shot_chart_features(shot_df, homeTeam, awayTeam, winTeam):
    home_features = []
    away_features = []
   
    home_zones = shot_df[shot_df['TEAM_ID'] == int(homeTeam)]
    away_zones = shot_df[shot_df['TEAM_ID'] == int(awayTeam)]
    num_home = (shot_df.where(shot_df['TEAM_ID'] == int(homeTeam)).dropna().shape[0])
    num_away = (shot_df.where(shot_df['TEAM_ID'] == int(awayTeam)).dropna().shape[0])
    for zone in zones:
        home_zone = home_zones[(home_zones['SHOT_ZONE_AREA'] == zone[0]) & (home_zones['SHOT_ZONE_RANGE'] == zone[1])]
        away_zone = away_zones[(away_zones['SHOT_ZONE_AREA'] == zone[0]) & (away_zones['SHOT_ZONE_RANGE'] == zone[1])]
       
        total = len(home_zone) + len(away_zone)
        if total == 0:
            home_features.append(0)
            away_features.append(0)
        else:
            home_features.append(len(home_zone) / num_home)
            away_features.append(len(away_zone) / num_away)
       
    if random.uniform(0, 1) < 0.5:
        features = home_features + away_features
        features.append(int(winTeam != homeTeam))
    else:
        features = away_features + home_features
        features.append(int(winTeam == homeTeam))
    
    
    return features
 
final = []
for i in range(1,1231):
    gamestr = '002160'
    gamestr += str(i).zfill(4)
    # Home players
    summary = game.BoxscoreSummary(game_id=gamestr).game_summary()
    homeTeam = summary['HOME_TEAM_ID']
    awayTeam = summary['VISITOR_TEAM_ID']
    ids = game.Boxscore(game_id=gamestr).player_stats()['PLAYER_ID']
    # Go through players
    appended_data = []
    for an_id in ids:
        shot_df = ShotChart(player_id=an_id, game_id = gamestr, season='2016-17')
        shot_df = shot_df.shot_chart()
        appended_data.append(shot_df)
    shot_df = pd.concat(appended_data, axis=0)
    team_box = game.Boxscore(game_id= gamestr).team_stats()
    winTeam = team_box[team_box['PLUS_MINUS'] > 0.0]['TEAM_ID']
    winTeam = int(winTeam)
    final.append(gen_shot_chart_features(shot_df, homeTeam, awayTeam, winTeam))
    
final_df = np.vstack(final)
np.random.shuffle(final_df)
train = final_df[:1000,:]
test = final_df[1000:, :]
train_x = train[:, :-1]
train_y = train[:, -1]
test_x = test[:, :-1]
test_y = test[:, -1]




print (train[267])
print("SIZE OF TRAIN", train.shape)
print("SIZE OF TEST", test.shape)

# Run XGBoost
clf = XGBClassifier(n_estimators=3000, n_jobs=8, silent = False)
print ("Sepaeate")
clf.fit(train_x, train_y, verbose= True)
print ("FITTED")
print("SCORE",clf.score(test_x, test_y))

from sklearn.ensemble import RandomForestClassifier
cl2 = RandomForestClassifier(max_depth= 5)
cl2.fit(train_x, train_y)
print("RF SCORE",cl2.score(test_x, test_y))


