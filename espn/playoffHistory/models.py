import requests
from flask import jsonify 

def get_years_with_league_id(league_id):
   url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id)  + "?seasonId=2018"
   teamView_json = requests.get(url, params={"view": "mTeam"}).json()[0]
   years = teamView_json['status']['previousSeasons']
   years.append(2018)
   return years

def get_owners_with_league_id(league_id, years=None):
   league_owners =  {}
   if years is None:
      years = get_years_with_league_id(league_id)
   for year in years:
        url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + "?seasonId=" + str(year)
        r = requests.get(url, params={"view": "mTeam"})
        json = r.json()[0]
        members = json['members']
        for member in members:
           owner_id = member['id']
           name = member['firstName'] + ' ' + member['lastName']
           if owner_id not in league_owners:
                league_owners[owner_id] = name
   return league_owners

def get_teams_with_league_id(league_id, years=None):
   team_ids =  {}
   if years is None:
      years = get_years_with_league_id(league_id)
   for year in years:
        url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + "?seasonId=" + str(year)
        r = requests.get(url, params={"view": "mTeam"})
        json = r.json()[0]
        teams = json['teams']
        for team in teams:
           owner_id = team['primaryOwner']
           team_id = team['id']
           if owner_id not in team_ids:
                team_ids[team_id] = owner_id
   return team_ids

def get_count_regular_season_games(league_id, year):
   url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + "?seasonId=" + str(year)
   r = requests.get(url, params={"view": "mTeam"})
   json = r.json()[0]
   record_json = json['teams'][0]['record']['overall']
   wins = record_json['wins']
   losses = record_json['losses']
   ties = record_json['ties']
   return (wins + losses + ties)

def get_playoff_performance(league_id):
   years = get_years_with_league_id(league_id)   
   team_ids = get_teams_with_league_id(league_id, years)
   owners = get_owners_with_league_id(league_id, years)
   regular_season_games = get_count_regular_season_games(league_id, years[0])
   playoff_record = {}
   total_postseason_games = 0
   for year in years:
      url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + "?seasonId=" + str(year)
      r = requests.get(url, params={"view": "mMatchup"})
      json = r.json()[0]
      games = json['schedule']
      for game in games:
         if game['matchupPeriodId'] >= regular_season_games:
            total_postseason_games += 1
            if game['winner'] == 'HOME':
                winner_team_id = game['home']['teamId']
                loser_team_id = game['away']['teamId']
            elif game['winner'] == 'AWAY':
                winner_team_id = game['away']['teamId']
                loser_team_id = game['home']['teamId']
            winner_owner_id = team_ids[winner_team_id]
            loser_owner_id = team_ids[loser_team_id]
            if winner_owner_id not in playoff_record:
                playoff_record[winner_owner_id] = {
                    "name": owners[winner_owner_id],
                    "wins": 1,
                    "losses": 0
                }
            else:
               playoff_record[winner_owner_id]["wins"] += 1
            if loser_owner_id not in playoff_record:
                playoff_record[loser_owner_id] = {
                    "name": owners[loser_owner_id],
                    "wins": 1,
                    "losses": 0
                }
            else:
               playoff_record[loser_owner_id]["losses"] += 1
      print(total_postseason_games)
      return playoff_record









