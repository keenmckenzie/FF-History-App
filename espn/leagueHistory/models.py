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



