import requests
import pandas as pd
from nba_py.shotchart import ShotChart
from nba_py import game
import requests_cache
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from multiprocessing import Pool
import numpy as np
for i in range(1,1231):
    # Generate games, they are 0001 to 1230
    path = '/Users/tynanseltzer/ap216/project/pics/'
    if np.random.randint(10) < 8:
        path += 'train'
    else:
        path += 'validation'
    gamestr = '002160'
    gamestr += str(i).zfill(4)
    # Home players
    print ("got here")
    summary = game.BoxscoreSummary(game_id=gamestr).game_summary()
    homeTeam = summary['HOME_TEAM_ID']
    awayTeam = summary['VISITOR_TEAM_ID']
    print ("here")
    ids = game.Boxscore(game_id=gamestr).player_stats()['PLAYER_ID']
    homeIds = ids.where(game.Boxscore(game_id=gamestr).player_stats()['TEAM_ID'] == int(homeTeam))
    homeIds = homeIds.dropna().astype('int')
    # Go through players
    appended_data = []
    for an_id in homeIds:
        print ("here actually")
        shot_df = ShotChart(player_id=an_id, game_id = gamestr, season='2016-17')
        shot_df = shot_df.shot_chart()
        appended_data.append(shot_df)
        print ("alive")
    shot_df = pd.concat(appended_data, axis=0)
    plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
    homePath = path + '/' + str(homeTeam[0]) + '/' + gamestr
    plt.savefig(homePath, dpi=100, frameon='false', aspect = 'normal', bbox_inches='tight', pad_inches=0)
    print ("SAVED A PIC")
    plt.clf()
    
    awayIds = ids.where(game.Boxscore(game_id=gamestr).player_stats()['TEAM_ID'] == int(awayTeam))
    awayIds = homeIds.dropna().astype('int')
    # Go through players
    appended_data = []
    for an_id in awayIds:
        shot_df = ShotChart(player_id=an_id, game_id = gamestr, season='2016-17')
        shot_df = shot_df.shot_chart()
        appended_data.append(shot_df)
    shot_df = pd.concat(appended_data, axis=0)
    plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
    awayPath = path + '/' + str(awayTeam[0]) + '/' + gamestr
    plt.savefig(awayPath, dpi=100, frameon='false', aspect = 'normal', bbox_inches='tight', pad_inches=0)
    plt.clf()
