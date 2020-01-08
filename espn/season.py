import requests


class Season:
    def __init__(self, league, year):
        self.id = league.id
        self.year = year


        url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(self.id) + "?seasonId=" + str(year)
        r = requests.get(url, params={"view": "mSettings"})
        json = r.json()[0]
        schedule_settings = json['settings']['scheduleSettings']
        self.regularSeasonLength = schedule_settings['matchupPeriodCount']
        self.playoffTeamCount = schedule_settings['playoffTeamCount']
        self.playoffMatchupLength = schedule_settings['playoffMatchupPeriodLength']

        url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(self.id) + "?seasonId=" + str(year)
        r = requests.get(url, params={"view": "mTeam"})
        json = r.json()[0]

        members = json['members']
        owners = {}
        for member in members:
            owner_id = member['id']
            name = member['firstName'] + ' ' + member['lastName']
            if owner_id not in owners:
                owners[owner_id] = name
        self.owners = owners

        teams = json['teams']
        playoff_teams = {}
        for team in teams:
            final_rank = team['rankCalculatedFinal']
            if final_rank <= self.playoffTeamCount:
                owner_id = team['owners'][0]
                playoff_teams[owner_id] = self.owners[owner_id]

        self.playoffTeams = playoff_teams

