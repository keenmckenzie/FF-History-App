import requests
from flask import jsonify

def getYearsWithLeagueId(league_id):
   url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id)  + "?seasonId=2018"
   teamView_json = requests.get(url, params={"view": "mTeam"}).json()[0]
   years = teamView_json['status']['previousSeasons']
   years.append(2018)
   return years

def getOwnersWithLeagueId(league_id):
   league_owners =  {}
   years = getYearsWithLeagueId(league_id)
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

def getSeasonData(league_id,year):
   league_owners = getOwnersWithLeagueId(league_id)
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
      team_data = {'abbrev': abbrev, 'name': name, 'owner_id': owner_id, 'record': overall}
      ##team_data = {'abbrev': abbrev, 'owner_id': owner_id, 'record': overall}
      if owner_id not in season_data:
          season_data.append(team_data)
   return season_data

def getAllTimeData(league_id):
   years = getYearsWithLeagueId(league_id)
   alltime_data = {}
   for year in years:
      print("Getting data for: ", str(year))
      season_data = getSeasonData(league_id, year)
      for team in season_data:
          owner_id = team["owner_id"]
          if owner_id not in alltime_data:
              alltime_data[owner_id] = {"name": team["name"], "wins": team["record"]["wins"], "losses": team["record"]["losses"], "ties": team["record"]["ties"], "points": team["record"]["pointsFor"]}
              print("Added an owner: ", team["name"])
          else: 
              alltime_data[owner_id]["wins"] +=  team["record"]["wins"]
              alltime_data[owner_id]["losses"] +=  team["record"]["losses"]
              alltime_data[owner_id]["ties"] +=  team["record"]["ties"]
              alltime_data[owner_id]["points"] +=  team["record"]["pointsFor"]
   return alltime_data







