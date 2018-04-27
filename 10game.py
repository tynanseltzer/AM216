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
for i in range(1100,1231):
    # Generate games, they are 0001 to 1230
    print ("ITERS", i)
    path = '/Users/tynanseltzer/ap216/project/pics/10/'
    gamestr = '002100'
    gamestr += str(i).zfill(4)
    # Home players
    summary = game.BoxscoreSummary(game_id=gamestr).game_summary()
    homeTeam = summary['HOME_TEAM_ID']
    awayTeam = summary['VISITOR_TEAM_ID']
    ids = game.Boxscore(game_id=gamestr).player_stats()['PLAYER_ID']
    # Go through players
    appended_data = []
    for an_id in ids:
        shot_df = ShotChart(player_id=an_id, game_id = gamestr, season='2010-11')
        shot_df = shot_df.shot_chart()
        appended_data.append(shot_df)
    shot_df = pd.concat(appended_data, axis=0)
    plt.scatter(shot_df.LOC_X, shot_df.LOC_Y)
    homePath = path + gamestr + ".jpg"
    plt.savefig(homePath, dpi=100, frameon='false', aspect = 'normal', bbox_inches='tight', pad_inches=0)
    plt.clf()
   