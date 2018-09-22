import math
import numpy as np
import pandas as pd
from scipy import stats
from mvp_model import zscore_model, stats_of_interest

global num_players
field_zscores = []
players = []

MVP_MODEL = zscore_model()
FILE_PATH = 'mvp2014'

def eucliddist(a,b):
    sum = 0.0
    for i in range(len(a)):
        sum += (a[i]-b[i])**2
    return math.sqrt(sum)

def produceZs(file_path):
    global num_players

    field_df = pd.read_csv('data/'+file_path+'.csv')
    num_players = len(field_df.index)

    for stat in stats_of_interest:
        stat_for_t20 = field_df[stat].tolist()
        math_ready = np.array(stat_for_t20)
        one_stat_zscores = np.array(stats.zscore(math_ready))
        field_zscores.append(one_stat_zscores)

        # print()
        # print(stat)
        # print(one_stat_zscores)

def compilePlayerZ():
    for i in range(num_players):
        player_stats = []
        for zscores in field_zscores:
            player_stats.append(zscores[i])
        players.append(player_stats)

def findClosest():
    distances = list(map(lambda player: eucliddist(player, MVP_MODEL), players))
    # for dist in distances:
    #     print(dist)
    # print()
    return distances.index(min(distances))

def getName(index, file_path):
    field_df = pd.read_csv('data/' + file_path + '.csv')
    return field_df.iloc[index][field_df.columns.get_loc('Player')]


print("mvp z-score compared to top 20 PER players")
print(stats_of_interest)
print(MVP_MODEL)
print()

produceZs(FILE_PATH)
compilePlayerZ()
closest_match = findClosest()
print(getName(closest_match, FILE_PATH))
