import requests
from flask import jsonify
from espn.league import League


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









