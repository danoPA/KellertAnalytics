import pandas as pd
import json
from collections import namedtuple
from itertools import chain

ranking = namedtuple("team_stats", [
    "rank",
    'team',
    'score',
    'Offense',
    'Defense',
    'Pace',
    'Threes',
    'DefRebounds',
    'OffRebounds',
    'Blocks',
    'Turnovers',
    'Assists',
    'Steals',
    'FreeThrows',
    'FreeThrowsGiven'
])


def load_power_rankings(filepath):

    data = pd.read_csv(filepath, header = 0)
    data = data.sort("PtDiff", ascending = False)
    data = data.reset_index(drop=True)
    rankings = [ranking(*i) for i in data.to_records()]

    return rankings

team_stats = namedtuple("team_stats", [
    'Team',
    'PtDiff',
    'Offense',
    'Defense',
    'Pace',
    'Threes',
    'DefRebounds',
    'OffRebounds',
    'Blocks',
    'Turnovers',
    'Assists',
    'Steals',
    'FreeThrows',
    'FreeThrowsGiven'
])

def load_team_stats(filepath):

    data = pd.read_csv(filepath, header = 0)
    data = data.sort("Offense", ascending = False)
    team_statistics = [team_stats(*i) for i in data.to_records(index=False)]

    return team_statistics


def load_teams(filepath):

    teams = pd.read_csv(filepath, header = 0)
    unique_teams = list(set(chain(*[[x[2],x[3]] for x in teams.to_records(index=False)])))

    return unique_teams