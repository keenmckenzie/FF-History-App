import requests
from espn.league import League
from espn.postseasonHistory.models import get_postseason_performance
from espn.regularSeasonHistory.models import get_all_season_data


def get_alltime(league_id):
    league = League(league_id)
    alltime_performance = {}
    regular_season = get_all_season_data(league)
    postseason = get_postseason_performance(league)
    for owner in regular_season:
        try:
            wins = regular_season[owner]['wins'] + postseason[owner]['wins']
            losses = regular_season[owner]['losses'] + postseason[owner]['losses']
        except KeyError:
            print("No postseason data for: " + regular_season[owner]['name'])
        alltime_performance[owner] = {
            "name": regular_season[owner]['name'],
            "wins": wins,
            "losses": losses,
            "yearsActive": regular_season[owner]['yearsActive']
        }
    return {'owners': alltime_performance}
