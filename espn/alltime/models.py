import requests
from flask import jsonify
from .league import League


def get_postseason_performance(league):
    postseason_record = {}
    total_postseason_games = 0
    for year in league.years:
        league.get_schedule_settings(year)
        url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league.id) + "?seasonId=" + str(year)
        r = requests.get(url, params={"view": "mMatchup"})
        json = r.json()[0]
        games = json['schedule']
        for game in games:
            if game['matchupPeriodId'] > league.regularSeasonLength:
                total_postseason_games += 1
                if game['winner'] == 'HOME':
                    winner_team_id = game['home']['teamId']
                    loser_team_id = game['away']['teamId']
                elif game['winner'] == 'AWAY':
                    winner_team_id = game['away']['teamId']
                    loser_team_id = game['home']['teamId']
                winner_owner_id = league.teamIds[winner_team_id]
                loser_owner_id = league.teamIds[loser_team_id]
                if winner_owner_id not in postseason_record:
                    postseason_record[winner_owner_id] = {
                        "name": league.owners[winner_owner_id],
                        "wins": 1,
                        "losses": 0
                    }
                else:
                    postseason_record[winner_owner_id]["wins"] += 1
                if loser_owner_id not in postseason_record:
                    postseason_record[loser_owner_id] = {
                        "name": league.owners[loser_owner_id],
                        "wins": 0,
                        "losses": 1
                    }
                else:
                    postseason_record[loser_owner_id]["losses"] += 1
    return postseason_record


def get_one_season_data(year, league):
    season_data = []
    url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league.id) + "?seasonId=" + str(year)
    r = requests.get(url, params={"view": "mTeam"})
    json = r.json()[0]
    teams = json['teams']
    for team in teams:
        record = team['record']
        overall = record['overall']
        abbrev = team['abbrev']
        owner_id = team['owners'][0]
        name = league.owners[owner_id]
        final_rank = team['rankCalculatedFinal']
        team_data = {'abbrev': abbrev, 'name': name, 'owner_id': owner_id, 'record': overall, "final rank": final_rank}
        if owner_id not in season_data:
            season_data.append(team_data)
    return season_data


def get_all_season_data(league):
    alltime_data = {}
    for year in league.years:
        season_data = get_one_season_data(year, league)
        for team in season_data:
            owner_id = team["owner_id"]
            champ_boolean = 0
            rank = team["final rank"]
            if (rank == 1):
                champ_boolean = 1
            if owner_id not in alltime_data:
                alltime_data[owner_id] = {
                    "name": team["name"],
                    "wins": team["record"]["wins"],
                    "losses": team["record"]["losses"],
                    "ties": team["record"]["ties"],
                    "championships": champ_boolean,
                    "points": team["record"]["pointsFor"],
                    "yearsActive": 1}
            else:
                alltime_data[owner_id]["wins"] += team["record"]["wins"]
                alltime_data[owner_id]["losses"] += team["record"]["losses"]
                alltime_data[owner_id]["ties"] += team["record"]["ties"]
                alltime_data[owner_id]["points"] += team["record"]["pointsFor"]
                alltime_data[owner_id]["yearsActive"] += 1
                alltime_data[owner_id]["championships"] += champ_boolean
    return alltime_data


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
