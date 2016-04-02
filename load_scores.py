from bs4 import BeautifulSoup
import urllib2
import datetime
from collections import namedtuple
import re


def getContent(s,p = False):
    n = s.text
    if p:
        if n[0] == 'T':
            return int(n[1:])
    return n


def kr(x):
    for i in x:
        if i <> "F" and i <> "CUT":
            return True
    return False


def load_scores():
    update_time = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(hours=4), '%Y-%m-%d %I:%M %p')
    url =  'http://scores.espn.go.com/golf/leaderboard'
    request = urllib2.Request(url)
    page = urllib2.urlopen(request)
    content = page.read()
    soup = BeautifulSoup(content, 'html5lib')

    standings = {
        "Kellert":[
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "Keesee":[
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "Shane":[
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "Rankin":[
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "Trent":[
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "Bergman":[
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "Grayhack":[
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "Moops":[
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "Sample":[
            "",
            "",
            "",
            "",
            "",
            ""
        ],
        "Day":[
            "",
            "",
            "",
            "",
            "",
            ""
        ]
    }

    #print soup.prettify()

    if len(soup.findChildren('table',{'class':"tablehead leaderboard before"})) == 1:

        soupTable = soup.findChildren('table',{'class':"tablehead leaderboard before"})
        headers = soupTable[0].findChildren('th')
        rows = soupTable[0].findChildren('tr', {'class':re.compile(r"^(evenrow|oddrow)$")})
        tableheaders = [header.text.replace(' ','') for header in headers]

        places = {}
        table_tuple = namedtuple("table_tuple", tableheaders)
        for i, row in enumerate(rows):
            tt = [j.text for j in row.findAll('td')]
            tt = table_tuple(*tt)
            places[tt.PLAYER] = tt

    if len(soup.findChildren('table',{'class':"tablehead leaderboard during"})) == 1:

        soupTable = soup.findChildren('table',{'class':"tablehead leaderboard during"})
        headers = soupTable[0].findChildren('th')
        rows = soupTable[0].findChildren('tr', {'class':re.compile(r"^(evenrow|oddrow)$")})
        tableheaders = [header.text.replace(' ','') for header in headers]
        cutplace = 1000
        cutcheck = True

        places = {}
        table_tuple = namedtuple("table_tuple", tableheaders)
        for i, row in enumerate(rows):
            tt = [j.text for j in row.findAll('td')]
            if cutcheck and tt[tableheaders.index("POS")] == "CUT":
                cutplace = i + 5
                cutcheck = False
                tt[tableheaders.index("POS")] = cutplace
            if "T" in tt[tableheaders.index("POS")]:
                tt[tableheaders.index("POS")] = tt[tableheaders.index("POS")][1:]
            try:
                tt[tableheaders.index("POS")] = int(tt[tableheaders.index("POS")])
            except ValueError:
                tt[tableheaders.index("POS")] = "WD"
            tt = table_tuple(*tt)
            places[tt.PLAYER] = tt

    if len(soup.findChildren('table',{'class':"tablehead leaderboard after"})) == 1:

        soupTable = soup.findChildren('table',{'class':"tablehead leaderboard after"})
        headers = soupTable[0].findChildren('th')
        rows = soupTable[0].findChildren('tr', {'class':re.compile(r"^(evenrow|oddrow)$")})
        tableheaders = [header.text.replace(' ','') for header in headers]
        cutplace = 1000
        cutcheck = True

        places = {}
        table_tuple = namedtuple("table_tuple", tableheaders)
        for i, row in enumerate(rows):
            tt = [j.text for j in row.findAll('td')]
            if cutcheck and tt[tableheaders.index("POS")] == "CUT":
                cutplace = i + 5
                cutcheck = False
                tt[tableheaders.index("POS")] = cutplace
            if "T" in tt[tableheaders.index("POS")]:
                tt[tableheaders.index("POS")] = tt[tableheaders.index("POS")][1:]
            try:
                tt[tableheaders.index("POS")] = int(tt[tableheaders.index("POS")])
            except ValueError:
                tt[tableheaders.index("POS")] = "WD"
            tt = table_tuple(*tt)
            places[tt.PLAYER] = tt

    standing_tuple = namedtuple("standing_tuple", ["name","total_pos","total_score"])
    players_tuple = namedtuple("players_tuple", ["PLAYER","THRU","TOPAR","POS"])

    individual_standings = {}
    total_standings = []

    for name, players in standings.items():
        individual_standings[name] = []
        for player in players:
            x = []
            for field in players_tuple._fields:
                try:
                    x.append(getattr(places[player], field))
                except:
                    x.append("")
            individual_standings[name].append(players_tuple(*x))
        all_places = [int(v.POS) if v.POS != '' else 0 for v in individual_standings[name]]
        all_scores = [int(v.TOPAR) if v.TOPAR not in ('E','') else 0 for v in individual_standings[name]]
        total_pos = sum(all_places) - max(all_places)
        total_score = sum(all_scores)
        total_standings.append(standing_tuple(name, total_pos, total_score))


    total_standings = sorted(total_standings, key=lambda x: x.total_pos,reverse=False)

    return update_time, individual_standings, total_standings, places
