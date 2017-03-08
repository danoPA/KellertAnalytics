from bottle import route, run, template, get, debug
from bottle import static_file, url
import json
import os
import pandas as pd
import numpy as np
from power_rankings_load import load_power_rankings, load_team_stats, load_teams

adjusted_stats_file = "adjustedStats_2017_prelim_all_years.csv"

@route('/')
def home():
    return template("index.html", url=url)


@route('/details')
def details():
    return template("index_details.html", url=url)


@route('/powerrankings')
def powerrank():
    rankings = load_power_rankings(adjusted_stats_file)
    teams = [""] + load_teams("bracket_guide_2016_2017.csv")
    return template("index_powerrankings.html", url=url, rankings=rankings, teams=teams)


@route('/stats')
def stats():
    stats = load_team_stats(adjusted_stats_file)
    teams = load_teams("bracket_guide_2016_2017.csv")
    return template("index_stats.html", url=url, stats=stats, teams=teams)


@route('/projections')
def projections():
    teams = [""] + load_teams("bracket_guide_2016_2017.csv")
    stats = load_team_stats(adjusted_stats_file)
    return template("index_projections.html", url=url, teams=teams, stats=stats)


@route('/bracket')
def bracket():
    return template("bracket.html", url=url)


@route('/team_stats/<team>')
def team_stats(team):
    team = team.replace("_"," ")
    stats = load_team_stats(adjusted_stats_file)
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

    port = int(os.environ.get('PORT', 80))
    debug(True)
    run(host='0.0.0.0', port=port, reloader=True)
