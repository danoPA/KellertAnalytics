from bottle import route, run, template, get, debug
from bottle import static_file, url
import json
import os
import pandas as pd
import numpy as np
from power_rankings_load import load_power_rankings, load_team_stats, load_teams
# from load_scores import load_scores


def check_login(username, password):
	with open("login.json", 'r') as infile:
		logins = json.load(infile)
		try:
			return logins[username] == password
		except KeyError:
			return False

@route('/')
def home():
	return template("index.html", url = url)


@route('/powerrankings')
def powerrank():
    rankings = load_power_rankings("adjustedStats_2016_finalish.csv")

    return template("index_powerrankings.html", url = url, rankings = rankings)

@route('/stats')
def stats():
    stats = load_team_stats("adjustedStats_2016_finalish.csv")
    teams = load_teams("bracket_guide_2016_final.csv")
    return template("index_stats.html", url = url, stats = stats, teams=teams)

@route('/projections')
def projections():
    teams = [""] + load_teams("bracket_guide_2016_final.csv")
    return template("index_projections.html", url=url, teams=teams)

@route('/bracket')
def bracket():
    return template("bracket.html", url=url)

@route('/team_stats/<team>')
def team_stats(team):
    team = team.replace("_"," ")
    stats = load_team_stats("adjustedStats_2016_finalish.csv")
    stats = stats.loc[stats.Team == team, :]
    with open("team_images.JSON") as infile:
        team_images = json.load(infile)
        return template("team_stats.html", url=url, stats=stats, teams=team_images, team=team)

# @route('/master')
# def masters():
#     return "Come back next year, 2017"
#     update_time, individual_standings, total_standings, places = load_scores()
#     return template("index_masters.html", url=url, update_time=update_time,
#                     individual_standings=individual_standings,
#                     total_standings=total_standings,
#                     places=places)


@route('/static/<filename>', name = 'static')
def send_static(filename):
    return static_file(filename, root='static')



from bottle import get, post, request # or route


if __name__ == "__main__":

    port = int(os.environ.get('PORT', 8000))
    debug(True)
    run(host='localhost', port=port, reloader=True)
