import pandas as pd
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt


def conf_m(confusion_matrix):
    confusion_matrix_normalized = confusion_matrix.astype('float') / confusion_matrix.sum(axis=1)[:, np.newaxis] * 100.0
    plt.matshow(confusion_matrix_normalized)
    width = len(confusion_matrix)
    height = len(confusion_matrix[0])
    for x in xrange(width):
        for y in xrange(height):
            plt.gca().annotate("{:5.2f} %".format(confusion_matrix_normalized[x][y]), xy=(y, x),
                               horizontalalignment='center',
                               verticalalignment='center')

    tick_labels = ['Run', 'Pass']
    plt.xticks(range(width), tick_labels)
    plt.yticks(range(height), tick_labels)
    plt.title('Normalized confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return plt

def getAllFeatures():
    all_features = []
    isPass = []
    season = []
    passProp = defaultdict(list)

    for idx, play in data.iterrows():
        features = defaultdict(float)
        if(isinstance(play['DESCRIPTION'],int)): continue
        if (' punt' not in play['DESCRIPTION']) \
        				and (play['DOWN'] != 0) \
                        and ('END ' != play['DESCRIPTION'][:4]) \
                        and ('End ' != play['DESCRIPTION'][:4]) \
                        and ('Two-Minute Warning' not in play['DESCRIPTION']) \
                        and ('spiked the ball to stop the clock' not in play['DESCRIPTION']) \
                        and ('kneels to ' not in play['DESCRIPTION']) \
                        and ('Delay of Game' not in play['DESCRIPTION']) \
                        and ('Penalty on' not in play['DESCRIPTION']) \
                        and ('Delay of Game' not in play['DESCRIPTION']) \
                        and ('sacked at' not in play['DESCRIPTION']) \
                        and ('Punt formation' not in play['DESCRIPTION']) \
                        and ('Direct snap to' not in play['DESCRIPTION']) \
                        and ('Aborted' not in play['DESCRIPTION']) \
                        and ('temporary suspension of play' not in play['DESCRIPTION']) \
                        and ('TWO-POINT CONVERSION ATTEMPT' not in play['DESCRIPTION']) \
                        and ('warned for substitution infraction' not in play['DESCRIPTION']) \
                        and ('no play run - clock started' not in play['DESCRIPTION']) \
                        and ('challenged the first down ruling' not in play['DESCRIPTION']) \
                        and ('*** play under review ***' not in play['DESCRIPTION']) \
                        and ('Direct Snap' not in play['DESCRIPTION']) \
                        and ('Direct snap' not in play['DESCRIPTION']): 

            features['team'] = play['OFF']
            features['season'] = play['SEASON']
            features['isHome'] = (play['HOME_TEAM'] == play['OFF'])
            features['opponent'] = play['DEF']


            #features['position'] = 50 - play.yardline.offset
            features['down'] = play['DOWN']
            features['togo'] = play['YARDS_TO_FIRST']
            features['togoal'] = play['YARDS_TO_GOAL']
            features['ptdiff'] = play['OFF_SCORE']-play['DEF_SCORE']
            features['quarter'] = play['QTR']

            if 'Shotgun' in play['DESCRIPTION']:
                features['shotgun'] = 1
            else:
                features['shotgun'] = 0

            if 'incomplete' in play['DESCRIPTION'] or ' pass ' in play['DESCRIPTION']:
                isPass.append(1)
                passProp[play['OFF']].append(1)
            else:
                isPass.append(0)
                passProp[play['OFF']].append(0)

            all_features.append(features)

    return all_features, isPass
