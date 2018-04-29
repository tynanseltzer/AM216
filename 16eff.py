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
top = [1610612744, 1610612745, 1610612739, 1610612746, 1610612743, 1610612761, 1610612759, 1610612738, 1610612764,
    1610612750, 1610612757, 1610612762, 1610612749, 1610612766]
for i in range(1,1231):
    # Generate games, they are 0001 to 1230
    path = '/home/tynan/am216/picseff/'
    gamestr = '002160'
    gamestr += str(i).zfill(4)
    # Home players
    summary = game.BoxscoreSummary(game_id=gamestr).game_summary()
    homeTeam = summary['HOME_TEAM_ID']
    awayTeam = summary['VISITOR_TEAM_ID']
    ids = game.Boxscore(game_id=gamestr).player_stats()['PLAYER_ID']
    homeIds = ids.where(game.Boxscore(game_id=gamestr).player_stats()['TEAM_ID'] == int(homeTeam))
    homeIds = homeIds.dropna().astype('int')
    # Go through players
    appended_data = []
    for an_id in homeIds:
        shot_df = ShotChart(player_id=an_id, game_id = gamestr, season='2016-17')
        shot_df = shot_df.shot_chart()
        appended_data.append(shot_df)
    shot_df = pd.concat(appended_data, axis=0)
    plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
    if int(homeTeam) in top:
        homePath = path + 'top/'
    else:
        homePath = path + 'bot/'
    homePath += gamestr + ".jpg"
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
    if int(awayTeam) in top:
        awayPath = path + 'top/'
    else:
        awayPath = path + 'bot/'
    awayPath += gamestr + "away.jpg"
    plt.savefig(awayPath, dpi=100, frameon='false', aspect = 'normal', bbox_inches='tight', pad_inches=0)
    plt.clf()
