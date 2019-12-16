import requests
from flask import jsonify

def get_years(league_id):
   url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id)  + "?seasonId=2018"
   teamView_json = requests.get(url, params={"view": "mTeam"}).json()[0]
   years = teamView_json['status']['previousSeasons']
   years.append(2018)
   return years

def get_owners_with_league_id(league_id, years=None):
   league_owners =  {}
   if years is None:
      years = get_years(league_id)
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
      years = get_years(league_id)
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
   return wins + losses + ties

def get_playoff_performance(league_id, years=None):
   if years is None:
     years = get_years(league_id)
   team_ids = get_teams_with_league_id(league_id, years)
   owners = get_owners_with_league_id(league_id, years)
   playoff_record = {}
   total_postseason_games = 0
   for year in years:
      regular_season_games = get_count_regular_season_games(league_id, year)
      url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + "?seasonId=" + str(year)
      r = requests.get(url, params={"view": "mMatchup"})
      json = r.json()[0]
      games = json['schedule']
      for game in games:
         if game['matchupPeriodId'] > regular_season_games:
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
                    "wins": 0,
                    "losses": 1
                }
            else:
                playoff_record[loser_owner_id]["losses"] += 1
   return playoff_record

def get_one_season_data(league_id, year):
   league_owners = get_owners_with_league_id(league_id)
   season_data = []
   url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + "?seasonId=" + str(year)
   r = requests.get(url, params={"view": "mTeam"})
   json = r.json()[0]
   teams = json['teams']
   for team in teams:
      record = team['record']
      overall = record['overall']
      abbrev = team['abbrev']
      owner_id = team['owners'][0]
      name = league_owners[owner_id]
      final_rank = team['rankCalculatedFinal']
      team_data = {'abbrev': abbrev, 'name': name, 'owner_id': owner_id, 'record': overall, "final rank": final_rank}
      ##team_data = {'abbrev': abbrev, 'owner_id': owner_id, 'record': overall}
      if owner_id not in season_data:
          season_data.append(team_data)
   return season_data

def get_all_season_data(league_id, years=None):
   if years is None:
     years = get_years(league_id)
   alltime_data = {}
   for year in years:
      season_data = get_one_season_data(league_id, year)
      for team in season_data:
          owner_id = team["owner_id"]
          champ_boolean = 0
          rank = team["final rank"]
          if(rank == 1):
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
              ##print("Added an owner: ", team["name"])
          else:
              alltime_data[owner_id]["wins"] +=  team["record"]["wins"]
              alltime_data[owner_id]["losses"] +=  team["record"]["losses"]
              alltime_data[owner_id]["ties"] +=  team["record"]["ties"]
              alltime_data[owner_id]["points"] +=  team["record"]["pointsFor"]
              alltime_data[owner_id]["yearsActive"] += 1
              alltime_data[owner_id]["championships"] += champ_boolean
   return alltime_data

def get_alltime(league_id):
   years = get_years(league_id)
   alltime_performance = {}
   regular_season = get_all_season_data(league_id, years)
   playoffs = get_playoff_performance(league_id, years)
   for owner in regular_season:
      try:
        wins = regular_season[owner]['wins'] + playoffs[owner]['wins']
        losses = regular_season[owner]['losses'] + playoffs[owner]['losses']
      except KeyError:
        print("No playoff data for: " + regular_season[owner]['name'])
      alltime_performance[owner] = {
        "name": regular_season[owner]['name'],
        "wins": wins,
        "losses": losses,
        "yearsActive": regular_season[owner]['yearsActive']
      }
   return {'owners': alltime_performance}





