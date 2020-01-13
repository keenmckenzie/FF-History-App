import requests
from fantasy.season import Season


class League:
    def __init__(self, league_id):
        self.id = league_id
        self.regularSeasonLength = 0
        self.playoffTeamCount = 0
        self.playoffMatchupLength = 0
        self.playoffTeams = {}
        self.seasons = {}

        def get_years_active():
            url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + "?seasonId=2018"
            team_view_json = requests.get(url, params={"view": "mTeam"}).json()[0]
            years = team_view_json['status']['previousSeasons']
            years.append(2018)
            return years

        self.years = get_years_active()

        def get_owners():
            owners = {}
            for year in self.years:
                url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + "?seasonId=" + str(
                    year)
                r = requests.get(url, params={"view": "mTeam"})
                json = r.json()[0]
                members = json['members']
                for member in members:
                    owner_id = member['id']
                    name = member['firstName'] + ' ' + member['lastName']
                    if owner_id not in owners:
                        owners[owner_id] = name
            return owners

        self.owners = get_owners()

        def get_team_ids():
            team_ids = {}
            for year in self.years:
                url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(league_id) + "?seasonId=" + str(
                    year)
                r = requests.get(url, params={"view": "mTeam"})
                json = r.json()[0]
                teams = json['teams']
                for team in teams:
                    owner_id = team['primaryOwner']
                    team_id = team['id']
                    if owner_id not in team_ids:
                        team_ids[team_id] = owner_id
            return team_ids

        self.teamIds = get_team_ids()

    def set_schedule_settings(self, year):
        url = "https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/" + str(self.id) + "?seasonId=" + str(
            year)
        r = requests.get(url, params={"view": "mSettings"})
        json = r.json()[0]
        schedule_settings = json['settings']['scheduleSettings']
        self.regularSeasonLength = schedule_settings['matchupPeriodCount']
        self.playoffTeamCount = schedule_settings['playoffTeamCount']
        self.playoffMatchupLength = schedule_settings['playoffMatchupPeriodLength']

    def set_season(self, year):
        if year not in self.seasons:
            season_class = Season(self, year)
            self.seasons[year] = season_class
