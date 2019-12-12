import requests
from flask import jsonify

def get_years_with_league_id(league_id):
   url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id)  + "?seasonId=2018"
   teamView_json = requests.get(url, params={"view": "mTeam"}).json()[0]
   years = teamView_json['status']['previousSeasons']
   years.append(2018)
   return years

def get_owners_with_league_id(league_id):
   league_owners =  {}
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

def get_season_data(league_id, year):
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

def get_all_time_data(league_id):
   years = get_years_with_league_id(league_id)
   alltime_data = {}
   for year in years:
      print("Getting data for: ", str(year))
      season_data = get_season_data(league_id, year)
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

def get_records(league_id):
  years = get_years_with_league_id(league_id)
  records = {}
  most_wins = {"team_name": "null", "wins": 0}
  most_points = {"team_name": "null", "points": 0}
  least_wins = {"team_name": "null", "wins": 0}
  least_points = {"team_name": "null", "points": 0}
  for year in years:
     season_data = get_season_data(league_id, year)
     for team in season_data:
        wins = team["record"]["wins"]
        points = team["record"]["pointsFor"]
        if ( wins > most_wins["wins"] ):
            most_wins = {"team_name": team["name"], "wins": wins}
        if ( points > most_points["points"] ):
            most_points = {"team_name": team["name"], "points": points}
        if ( wins < least_wins["wins"] or least_wins["team_name"] == "null" ):
            least_wins = {"team_name": team["name"], "wins": wins} 
        if ( points < least_points["points"] or least_points["team_name"] == "null" ):
            least_points = {"team_name": team["name"], "points": points}
  records = {"most_wins": most_wins, "least_wins": least_wins, "most_points": most_points, "least_points": least_points}
  return records







