from bs4 import BeautifulSoup
import urllib2
import datetime
from collections import namedtuple
import re
import random
import pandas as pd

leaderboard = namedtuple("leaderboard", [
    'POS', 'BLANK', 'PLAYER','TOPAR','TODAY','THRU','R1','R2','R3','R4','TOT','EARNINGS',
    'FEDEXPTS','TEETIME'])


def get_content(s, p=False):
    n = s.text
    if p:
        if n[0] == 'T':
            return int(n[1:])
    return n


def kr(x):
    for i in x:
        if i != "F" and i != "CUT":
            return True
    return False


def scrape_leaderboard(url):
    request = urllib2.Request(url)
    page = urllib2.urlopen(request)
    content = page.read()
    soup = BeautifulSoup(content)
    soupTable = soup.findChildren('table',{'class':"leaderboard-table"})
    headers = soupTable[0].findChildren('th')
    rows = soupTable[0].findChildren('tr')
    rows = filter(lambda r: len(r) > 5, rows)
    tableheaders = [i.text.replace(' ','') for i in headers]
    cutplace = 1000
    cutcheck = True

    row_details = []
    for i, row in enumerate(rows):
        tt = [j.find("a", {"class":"full-name"}).text if j.get("class")[0] == "playerName" else j.text for j in row.findAll('td')]
        if len(tt) > 5:
            if cutcheck and tt[tableheaders.index("POS")] == "-":
                cutplace = i + 5
                cutcheck = False
                tt[tableheaders.index("POS")] = cutplace
            elif tt[tableheaders.index("POS")] == "-":
                tt[tableheaders.index("POS")] = cutplace
            if "T" in str(tt[tableheaders.index("POS")]):
                tt[tableheaders.index("POS")] = tt[tableheaders.index("POS")][1:]
            try:
                tt[tableheaders.index("POS")] = int(tt[tableheaders.index("POS")])
            except ValueError:
                tt[tableheaders.index("POS")] = cutplace
            try:
                row_details.append(leaderboard(*tt))
            except:
                continue
    return pd.DataFrame(row_details)


def load_scores():
    update_time = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(hours=4), '%Y-%m-%d %I:%M %p')

    standings = {
        "Kellert":[
            "Dustin Johnson",
            "Patrick Reed",
            "Matt Kuchar",
            "Gary Woodland",
            "J.B. Holmes",
            "Kevin Chappell"
        ],
        "Keesee":[
            "Adam Scott",
            "Rickie Fowler",
            "Branden Grace",
            "Russell Knox",
            "Rafael Cabrera Bello",
            "Emiliano Grillo"
        ],
        "Shane":[
            "Hideki Matsuyama",
            "Jon Rahm",
            "Louis Oosthuizen",
            "Thomas Pieters",
            "Bill Haas",
            "Jason Dufner"
        ],
        "Rankin":[
            "Henrik Stenson",
            "Tyrrell Hatton",
            "Alex Noren",
            "Charley Hoffman",
            "Tommy Fleetwood",
            "Soren Kjeldsen"
        ],
        "Trent":[
            "Rory McIlroy",
            "Phil Mickelson",
            "Paul Casey",
            "Marc Leishman",
            "Lee Westwood",
            "Shane Lowry"
        ],
        "Bergman":[
            "Jason Day",
            "Bubba Watson",
            "Sergio Garcia",
            "Zach Johnson",
            "Martin Kaymer",
            "Ryan Moore"
        ],
        "Moops":[
            "Justin Thomas",
            "Justin Rose",
            "Jimmy Walker",
            "Matthew Fitzpatrick",
            "Charl Schwartzel",
            "Hideto Tanihara"
        ],
        "Day":[
            "Jordan Spieth",
            "Brandt Snedeker",
            "Danny Willett",
            "Francesco Molinari",
            "Brooks Koepka",
            "Daniel Berger"
        ]
    }

    leaderboard_pd = scrape_leaderboard("http://www.espn.com/golf/leaderboard")
    places = dict(map(lambda y: (y.PLAYER, y), leaderboard_pd.itertuples()))

    standing_tuple = namedtuple("standing_tuple", ["name","total_pos","total_score"])
    players_tuple = namedtuple("players_tuple", ["PLAYER","THRU","TOPAR","POS"])

    individual_standings = {}
    total_standings = []

    for name, players in standings.items():
        individual_standings[name] = []
        for player in players:
            x = []
            for field in players_tuple._fields:
                if field == "PLAYER":
                    x.append(player)
                else:
                    try:
                        x.append(getattr(places[player], field))
                    except:
                        x.append("")
            individual_standings[name].append(players_tuple(*x))
        all_places = [int(v.POS) if (v.POS not in ('', '-')) else 0 for v in individual_standings[name]]
        all_scores = [int(v.TOPAR) if v.TOPAR not in ('E','MDF','WD','CUT','') else 0 for v in individual_standings[name]]
        total_pos = sum(all_places) - max(all_places)
        total_score = sum(all_scores)
        total_standings.append(standing_tuple(name, total_pos, total_score))

    total_standings = sorted(total_standings, key=lambda x: x.total_pos,reverse=False)
    t = [datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(hours=4), '%Y-%m-%d %H:%M')]
    write_line = ",".join(t + [str(i.total_pos) for i in sorted(total_standings, key=lambda r: r.name)])
    if datetime.datetime.now().day >= 7 and datetime.datetime.now().minute % 10 == 0:
        try:
            with open("static/score_graph.csv", 'a') as outfile:
                outfile.write(write_line+'\n')
        except:
            pass
    return update_time, individual_standings, total_standings, places
