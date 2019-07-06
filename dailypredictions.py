import pandas as pd
from bs4 import BeautifulSoup
import re
import urllib.request
import numpy as np

from mvp_statline import blueprint
mvp_bp = blueprint()

test_indices = [2,3,5,16,20,21,24,45]
test_labels = ['PER','TS%','FTr','WS','BPM','VORP','FG','PPG']

#this is what needs to be updated as the days go by
player_names = ['Kevin Durant','Joel Embiid',
'James Harden','Kawhi Leonard','Nikola Jokic','Anthony Davis',
'Karl-Anthony Towns','Giannis Antetokounmpo','LeBron James', 'Stephen Curry']

player_tensors = []

#returns player advanced and regular dataframes
# return reg_df, reg_header, adv_df, adv_header
def getPlayerDataFrames(name):
    player_name = name.lower()
    ln_fi = player_name.find(' ') + 1  # index of first initial of last name
    first = player_name[:2]
    last = player_name[ln_fi:ln_fi + 5]

    url = "https://www.basketball-reference.com/players/" + player_name[ln_fi] + "/" + last + first + "01.html"
    if(name=='Anthony Davis'):
        url = "https://www.basketball-reference.com/players/d/davisan02.html"

    with urllib.request.urlopen(url) as response:
        # UTF-8 doesn't support some initial character on the websites for some reason!
        r = response.read().decode('latin-1')

    content = re.sub(r'(?m)^\<!--.*\n?', '', r)
    content = re.sub(r'(?m)^\-->.*\n?', '', content)

    soup = BeautifulSoup(content, 'html.parser')
    tables = soup.findAll('table')

    #change dep on website format
    reg_table = tables[0]
    adv_table = tables[4]

    reg_df = pd.read_html(str(reg_table))[0]
    adv_df = pd.read_html(str(adv_table))[0]

    reg_header = reg_df.columns.values.tolist()
    adv_header = adv_df.columns.values.tolist()
    return reg_df, adv_df

def cleanedUpTensor(reg_df, adv_df):
    current_reg = np.array(list(filter(lambda a: str(a) != 'nan', reg_df.iloc[-2])))
    current_adv = np.array(list(filter(lambda a: str(a) != 'nan', adv_df.iloc[-2])))

    current_reg = current_reg[6:].tolist()
    current_adv = current_adv[5:].tolist()
    tensor = np.array(current_adv + current_reg)
    tensor_final = []
    for a in tensor:
        if(a=='0.0'):
            tensor_final.append(0.0)
        else:
            tensor_final.append(float(a))
    return tensor_final

def compareStat(mvp_stat, player_stat):
    return player_stat-mvp_stat

def getAllPlayers():
    for player in player_names:
        dfs = getPlayerDataFrames(player)
        tensor = cleanedUpTensor(dfs[0], dfs[1])
        player_tensors.append(tensor)

def findClosest():
    closest_folks = []
    #test -> stat
    for stat in test_indices:
        # print(stat)

        closest_diff = 100000.0
        closest_player_index = 0

        mvp_stat = mvp_bp[stat]
        # print(mvp_stat)

        for player in player_tensors:
            # print(player_names[player_tensors.index(player)])
            # print(player)
            # print()
            player_stat = player[stat]
            # print(player_stat)

            closest_test_diff = abs(compareStat(mvp_stat, player_stat))

            if(closest_test_diff < closest_diff):
                closest_diff = closest_test_diff
                closest_player_index = player_tensors.index(player)

        #to change
        name = player_names[closest_player_index]
        closest_folks.append([stat, name])

    return closest_folks

def findBiggest():
    biggest_folks = []
    for stat in test_indices:
        # print(stat)

        biggest_stat = 0.0
        biggest_player_index = 0

        mvp_stat = mvp_bp[stat]
        # print(mvp_stat)

        for player in player_tensors:
            # print(player_names[player_tensors.index(player)])
            # print(player)
            # print()
            player_stat = player[stat]
            # print(player_stat)

            if(biggest_stat < player_stat):
                biggest_stat = player_stat
                biggest_player_index = player_tensors.index(player)

        #to change
        name = player_names[biggest_player_index]
        biggest_folks.append([stat, name])

    return biggest_folks


print(mvp_bp)
print()
getAllPlayers()
closest_people = findClosest()
for pl in closest_people:
    print("{} was closest to the MVP line for {} with {}".format(pl[1], test_labels[test_indices.index(pl[0])], player_tensors[ player_names.index( pl[1] ) ][ pl[0] ] ))

print()
biggest_people = findBiggest()
for pl in biggest_people:
    print("{} was most above the MVP line for {} with {}".format(pl[1], test_labels[test_indices.index(pl[0])], player_tensors[ player_names.index( pl[1] ) ][ pl[0] ] ))
