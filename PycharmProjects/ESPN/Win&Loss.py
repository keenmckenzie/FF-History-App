import requests
import All_Years
import Owner_Names
import pandas as pd

league_id = All_Years.input_id
## league_id = 1107328, 103635

past_years = All_Years.past_years


season_wins = {}

for eachyear in past_years:
    url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + \
          str(league_id) + "?seasonId=" + str(eachyear)
    win_loss_r = requests.get(url, params={"view": "mTeam"})
    d = win_loss_r.json()[0]
    for team in d['teams']:
        owner_id = team['owners'][0]
        owner_id = owner_id.encode('ascii')
        win_count = team['record']['overall']['wins']
        loss_count = team['record']['overall']['losses']
        ties = 0
        record = str(win_count) + " - " + str(loss_count)
        if owner_id not in season_wins:
            season_wins[owner_id] = {}
            season_wins[owner_id]['name'] = Owner_Names.owners[owner_id]
            season_wins[owner_id][eachyear] = {}
            season_wins[owner_id][eachyear]['wins'] = win_count
            season_wins[owner_id][eachyear]['losses'] = loss_count
            season_wins[owner_id]['totalWins'] = win_count
            season_wins[owner_id]['totalLosses'] = loss_count
        else:
            season_wins[owner_id][eachyear] = {}
            season_wins[owner_id][eachyear]['wins'] = win_count
            season_wins[owner_id][eachyear]['losses'] = loss_count
            season_wins[owner_id]['totalWins'] = season_wins[owner_id]['totalWins'] + win_count
            season_wins[owner_id]['totalLosses'] = season_wins[owner_id]['totalLosses'] + loss_count

print season_wins


df = []


for owner in Owner_Names.owners:
    try:
        df_ind = [season_wins[owner]['name']]
    except KeyError:
        print "No season found"
        continue
    win_perc = float(season_wins[owner]['totalWins'])/(season_wins[owner]['totalLosses']+season_wins[owner]['totalWins'])
    for year in past_years:
        try:
            df_ind.extend([season_wins[owner][year]['wins'],season_wins[owner][year]['losses']])
        except KeyError:
            df_ind.extend([0,0])
    df_ind.extend([season_wins[owner]['totalWins'],season_wins[owner]['totalLosses'],win_perc])
    df.append(df_ind)

columns = ['Name']

for year in past_years:
    columns.extend([str(year)+" Wins",str(year)+" Losses"])
columns.extend(['Total Wins', 'Total Losses', 'Win %'])

df = pd.DataFrame(df, columns=columns)

df.to_csv('/Users/keenan/PycharmProjects/Dump/Season_Wins_'+str(league_id)+'.csv')