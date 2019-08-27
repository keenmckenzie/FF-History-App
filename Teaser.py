import requests
import pandas as pd



league_id = 1107328
year = 2017
url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + \
      str(league_id) + "?seasonId=" + str(year)

# Basic League Info
league_r = requests.get(url)

# Match-up view
matchup_r = requests.get(url, params={"view": "mMatchup"})


d = matchup_r.json()[0]

df = []


for game in d['schedule']:
  if game['winner'] != "UNDECIDED":
        df_ind = \
              [
              game['matchupPeriodId'],
              game['home']['teamId'], game['home']['totalPoints'],
              game['away']['teamId'], game['away']['totalPoints']
              ]
        df.append(df_ind)

df = pd.DataFrame(df, columns=['Week', 'Team1', 'Score1', 'Team2', 'Score2'])
df['Type'] = ['Regular' if w<=14 else 'Playoff' for w in df['Week']]
df.head()

print df

df3 = df.assign(Margin1 = df['Score1'] - df['Score2'],
                Margin2 = df['Score2'] - df['Score1'])
df3 = (df3[['Week', 'Team1', 'Margin1', 'Type']]
 .rename(columns={'Team1': 'Team', 'Margin1': 'Margin'})
 .append(df3[['Week', 'Team2', 'Margin2', 'Type']]
 .rename(columns={'Team2': 'Team', 'Margin2': 'Margin'}))
)
df3.head()

print df3
df3.to_csv('/Users/keenan/PycharmProjects/test.csv')
df = pd.read_csv('/Users/keenan/PycharmProjects/test.csv', usecols=[0,1], parse_dates=True, dayfirst=True, index_col=0)

print(df)

