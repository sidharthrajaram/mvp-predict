#forecast top 20 players' stats for next season
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import urllib.request
from urllib.request import urlopen



def getPlayerStats(name, advanced=True):
    player_name = name.lower()
    ln_fi = player_name.find(' ') + 1  # index of first initial of last name
    first = player_name[:2]
    last = player_name[ln_fi:ln_fi + 5]

    url = "https://www.basketball-reference.com/players/" + player_name[ln_fi] + "/" + last + first + "01.html"

    # res = requests.get(link)

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

adv_df = getPlayerStats('Kevin Durant')
vorp = adv_df['VORP']
print(vorp)