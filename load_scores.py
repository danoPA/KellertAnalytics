from bs4 import BeautifulSoup
import urllib2
import re
import html5lib
import os
import time
import random
import csv
import sys
import datetime
import matplotlib.pyplot as plt
import matplotlib
from collections import namedtuple


def getContent(s,p = False):
    check = False
    n = ''
    for i in str(s):
        if i == '<' or i == ']':
            check = False
        if check:
            n += i
        if i == '>':
            check = True
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
    update_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    url = 'http://scores.espn.go.com/golf/leaderboard'
    request = urllib2.Request(url)
    page = urllib2.urlopen(request)
    content = page.read()
    soup = BeautifulSoup(content, 'html5lib')

    #print soup.prettify()
    soupTable = soup.findChildren('table',{'class':"tablehead leaderboard during"})
    rows = soupTable[0].findChildren(['th', 'tr'])

    standings = {
        "Kellert":[
            "Jason Day",
            "Henrik Stenson",
            "Kevin Chappell",
            "Justin Rose",
            "Jamie Lovemark",
            "Troy Merritt"
        ],
        "Keesee":[
            "Jason Day",
            "Paul Casey",
            "Kevin Chappell",
            "Justin Rose",
            "Jamie Lovemark",
            "Troy Merritt"
        ],
        "Shane":[
            "Jason Day",
            "Chris Wood",
            "Kevin Chappell",
            "Justin Rose",
            "Jamie Lovemark",
            "Troy Merritt"
        ],
        "Rankin":[
            "Jason Day",
            "Henrik Stenson",
            "Kevin Chappell",
            "Justin Rose",
            "Brian Harman",
            "Troy Merritt"
        ],
        "Trent":[
            "Jason Day",
            "Henrik Stenson",
            "Kevin Chappell",
            "Justin Rose",
            "Jamie Lovemark",
            "Troy Merritt"
        ],
        "Bergman":[
            "Jason Day",
            "Henrik Stenson",
            "Keegan Bradley",
            "Justin Rose",
            "Jamie Lovemark",
            "Troy Merritt"
        ],
        "Paul":[
            "Jason Day",
            "Henrik Stenson",
            "Kevin Chappell",
            "Billy Horschel",
            "Jamie Lovemark",
            "Troy Merritt"
        ],
        "Moops":[
            "Jason Day",
            "Henrik Stenson",
            "Kevin Chappell",
            "Justin Rose",
            "Kyle Reifers",
            "Troy Merritt"
        ],
        "Sample":[
            "Jason Day",
            "Will Wilcox",
            "Kevin Chappell",
            "Justin Rose",
            "Jamie Lovemark",
            "Troy Merritt"
        ],
        "Day":[
            "Jason Day",
            "Henrik Stenson",
            "Kevin Chappell",
            "Justin Rose",
            "Zac Blair",
            "Ernie Els"
        ]
    }

    places = {}
    cut = soupTable[0].find("tr",{"class":"cut-line"})

    for i, row in enumerate(rows):
        if row == cut:
            print i, "cut"
            cutPlace = int(place)
        try:
            place = getContent(row.find_all("td",{"class":"textcenter"})[0], p = True)
            name = row.find_all("a")
            score = getContent(row.find_all("td",{"class":"textcenter"})[3], p = True)
            try:
                hole = int(getContent(row.find_all("td",{"class":"textcenter"})[5], p = True))
            except:
                hole = getContent(row.find_all("td",{"class":"textcenter"})[5], p = True)
            if place == "-" or hole == "N/A":
                place = cutPlace + 5
            places[getContent(name)] = {"place":int(place),"score":score,"hole":hole}
        except:
            pass

    standing_tuple = namedtuple("standing_tuple", ["name","score"])
    players_tuple = namedtuple("players_tuple", ["player","hole","score","place"])

    individual_standings = {}
    total_standings = []

    for name, players in standings.items():
        individual_standings[name] = []
        score = 0
        for player in players:
            x = [player]+places[player].values()
            individual_standings[name].append(players_tuple(*x))
            score += int(places[player]["place"])
        total_standings.append(standing_tuple(name,score))

    total_standings = sorted(total_standings, key=lambda x: x.score,reverse=False)

    return update_time, individual_standings, total_standings