#By @ImA1ex_ twitter
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os

api_key = os.environ["SOME_SECRET"]

r=requests.get("https://liga.dust2.dk/hold/?hold=61239a41191993590c361e9d")
soup=BeautifulSoup(r.text, "html.parser")

ids = re.findall(r'id=(\d+)', str(soup.find_all("img", class_="players--player-img")))
nickname_divs = soup.find_all("div", class_="players--player--nickname text-ellipsis")
nicknames = [div.text.strip() for div in nickname_divs]
teamname_divs = soup.find_all("div", class_="menu--teamName")
teamnames = [div.text.strip() for div in teamname_divs]
teamlogo_divs = soup.find_all("img", class_="menu--team--img")
teamlogos = [div["src"] for div in teamlogo_divs]
team_ids = []
value_ids = []
league_ids = []
divs = soup.find_all("div", class_="players--player")
for div in divs:
    team_id = div.get("teamid")
    if team_id:
        team_ids.append(team_id)
for div in divs:
    value_id = div.get("value")
    if value_id:
        value_ids.append(value_id)
for div in divs:
    league_id = div.get("leagueid")
    if league_id:
        league_ids.append(league_id)

dic={}
id=0
team=0
n=len(nicknames)
for i in range(n):
    if nicknames[i]=="TBA":
        dic[("TBA")+str(i)]=((str(nicknames[i])+str(i)), 0, 0, teamnames[team], teamlogos[team])
        id = id-1
        print("TBA")
    else:
        url = f'https://open.faceit.com/data/v4/players?game=cs2&game_player_id={ids[id]}'

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + api_key
        }
        response = requests.get(url, headers=headers)
        faceitdata = response.json()

        try: dic[faceitdata["nickname"]]=(nicknames[i], faceitdata["games"]["cs2"]["skill_level"], faceitdata["games"]["cs2"]["faceit_elo"], teamnames[team], teamlogos[team])
        except: dic["Ingen Faceit"]=(nicknames[i], 0, 0, teamnames[team], teamlogos[team])
    id = id + 1
    if (i+1) % 5 == 0:
        team += 1
df = pd.DataFrame(dic)
try:
    os.remove("dic30.csv")
except FileNotFoundError:
    pass

for i in range(29, -1, -1):
    try:
        os.rename(f"dic{i}", f"dic{i+1}")
    except FileNotFoundError:
        print(f"Failed to rename {i}")
df.to_csv("dic0.csv")
