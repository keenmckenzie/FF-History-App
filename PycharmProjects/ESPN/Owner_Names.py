import requests
import All_Years

league_id = All_Years.league_id
multi_year = All_Years.past_years

owners = {}

for year in multi_year:
    url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + \
          str(league_id) + "?seasonId=" + str(year)
    r = requests.get(url, params={"view": "mTeam"})
    json = r.json()[0]
    members = json['members']
    for member in members:
        owner_id = member['id']
        name = member['firstName'] + ' ' + member['lastName']
        if owner_id not in owners:
            owners[owner_id] = name
