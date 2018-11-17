#forecast top 20 players' stats for next season
import pandas as pd
from bs4 import BeautifulSoup
import re
import urllib.request
import numpy as np
import csv
from mvp_model import zscore_model, stats_of_interest

FORECAST_FILE = 'data/mvpForecast.csv'
field_df = pd.read_csv('data/mvpForecast.csv')
player_names = field_df['Player']
player_names = player_names.tolist()
print(field_df)

start_ind = 7 #PER

def getPlayerStats(name, advanced=True):
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

    if advanced:
        table = tables[4]
    else:
        table = tables[0]

    df = pd.read_html(str(table))[0]
    return df

def getLatest(df):

    latest_stats = df.iloc[-2].tolist()
    age = latest_stats[df.columns.get_loc('Age')]+1

    if len(df['VORP']) > 2:
        latest_stats = np.array(list(filter(lambda a: str(a) != 'nan', df.iloc[-2].tolist()[start_ind:] )))
        next_latest_stats = np.array(list(filter(lambda a: str(a) != 'nan', df.iloc[-3].tolist()[start_ind:] )))

        return [latest_stats, next_latest_stats, age]

    else:
        latest_stats = np.array(list(filter(lambda a: str(a) != 'nan', df.iloc[-2].tolist()[start_ind:] )))
        return [latest_stats, age]

def getDelta(stats_tuple):
    mip_candidate = False

    if len(stats_tuple) > 2 :

        #progress cap for massive improvement players (e.g. Oladipo)
        delta_PER = float(stats_tuple[0][0]-stats_tuple[1][0])
        proportion = delta_PER/float(stats_tuple[0][0])
        if proportion > 0.2:
            mip_candidate = True

        return [stats_tuple[0]-stats_tuple[1], stats_tuple[2], True, mip_candidate]
    else:
        return [stats_tuple[0], stats_tuple[1], False, mip_candidate]

def getChange(delta_tuple):
    age = delta_tuple[1]
    stat_delta = delta_tuple[0]

    if delta_tuple[2] == True:

        weight = (28-age)*0.15

        #mip candidate
        if delta_tuple[3] == True:
            weight = 0.075

        return weight*stat_delta

    # only one year of exp
    else:
        weight = (28-age)*0.015
        return weight*stat_delta

def updatedStatRow(df, change):

    latest_stats = np.array(list(filter(lambda a: str(a) != 'nan', df.iloc[-2].tolist() )))

    for i in range(len(latest_stats)-start_ind):
        np.put(latest_stats, i+start_ind, float(latest_stats[i+start_ind])+float(change[i]))

    return latest_stats


# ****************************************************************************
# EXPERIMENT **************************************
def adjustment(delta_tuple):
    age = delta_tuple[1]
    adjustment = 0.0

    if age <= 28:
        adjustment = (28 - age) * 0.025
    else:
        adjustment = (28 - age) * 0.01

    weight = 1 + adjustment
    return weight

def newUpdatedStatRow(df, adjustment):
    latest_stats = np.array(list(filter(lambda a: str(a) != 'nan', df.iloc[-2].tolist())))

    for i in range(len(latest_stats)-start_ind):
        np.put(latest_stats, i+start_ind, adjustment*float(latest_stats[i+start_ind]))

    return latest_stats


def newWriteCSV():
    the_full_thang = []
    header_row = field_df.columns.values.tolist()
    the_full_thang.append(header_row)

    for name in player_names:
        df = getPlayerStats(name)
        latest_szns = getLatest(df)
        delta_tuple = getDelta(latest_szns)
        change = adjustment(delta_tuple)

        new_stat_row = newUpdatedStatRow(df, change).tolist()
        new_stat_row.insert(0, name)
        the_full_thang.append(new_stat_row)

    print(the_full_thang)

    with open(FORECAST_FILE, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(the_full_thang)

# EXPERIMENT **************************************
# ****************************************************************************



def writeCSV():
    the_full_thang = []
    header_row = field_df.columns.values.tolist()
    the_full_thang.append(header_row)

    for name in player_names:
        df = getPlayerStats(name)
        latest_szns = getLatest(df)
        delta_tuple = getDelta(latest_szns)
        change = getChange(delta_tuple)

        new_stat_row = updatedStatRow(df, change).tolist()
        new_stat_row.insert(0, name)
        the_full_thang.append(new_stat_row)

    print(the_full_thang)

    with open(FORECAST_FILE, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(the_full_thang)

# writeCSV()
newWriteCSV()
