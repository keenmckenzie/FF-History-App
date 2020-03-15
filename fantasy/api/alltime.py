import requests
from fantasy.league import League
from fantasy.api.playoffs import get_postseason_performance
from fantasy.api.regularSeason import get_all_season_data


def get_alltime_map(league_id):
    league = League(league_id)
    alltime_performance = {}
    alltime_list = []
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
                "losses": regular_season[owner]['losses'],
                "yearsActive": regular_season[owner]['yearsActive']
            }
            ##print("No postseason data for: " + regular_season[owner]['name'])

    for owner in alltime_performance:
        alltime_list.append(alltime_performance[owner])
    return {'owners': alltime_performance}


def get_alltime_list(league_id):
    league = League(league_id)
    alltime_performance = {}
    alltime_list = []
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
                "championships": regular_season[owner]['championships'],
                "yearsActive": regular_season[owner]['yearsActive']
            }

        except KeyError:
            alltime_performance[owner] = {
                "name": regular_season[owner]['name'],
                "wins": regular_season[owner]['wins'],
                "losses": regular_season[owner]['losses'],
                "yearsActive": regular_season[owner]['yearsActive'],
                "championships": regular_season[owner]['championships']
            }
            ##print("No postseason data for: " + regular_season[owner]['name'])

    for owner in alltime_performance:
        alltime_list.append(alltime_performance[owner])
    return {'owners': alltime_list}
