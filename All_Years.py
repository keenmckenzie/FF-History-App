import requests

print 'Enter League ID'

input_id = input()

league_id = input_id
year = 2010

url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + \
      str(league_id) + "?seasonId=" + str(year)

# Basic League Info
league_r = requests.get(url)

# Match-up view
matchup_r = requests.get(url, params={"view": "mMatchup"})

past_years = []
while year<2019:
    url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + \
          str(league_id) + "?seasonId=" + str(year)
    league_r = requests.get(url)
    try:
        json = league_r.json()[0]
        past_years.append(year)
        year += 1
    except:
        year += 1
