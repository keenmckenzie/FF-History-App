import requests
from fantasy.league import League
from fantasy.espn.playoffs import get_postseason_performance
from fantasy.espn.regularSeason import get_all_season_data


def get_alltime(league_id):
    league = League(league_id)
    alltime_performance = {}
    regular_season = get_all_season_data(league)
    postseason = get_postseason_performance(league)
    for owner in regular_season:
        try:
            wins = regular_season[owner]['wins'] + postseason[owner]['wins']
            losses = regular_season[owner]['losses'] + postseason[owner]['losses']
            alltime_performance[owner] = {
                "name": regular_season[owner]['name'],
                "wins": wins,
                "losses": losses,
                "yearsActive": regular_season[owner]['yearsActive']
            }

        except KeyError:
            alltime_performance[owner] = {
               "name": regular_season[owner]['name'],
               "wins": regular_season[owner]['wins'],
               "losses":regular_season[owner]['losses'],
               "yearsActive": regular_season[owner]['yearsActive']
            }
            print("No postseason data for: " + regular_season[owner]['name'])

    return {'owners': alltime_performance}

