from flask import Blueprint, jsonify

from fantasy.espn.alltime import get_alltime
from fantasy.espn.playoffs import get_postseason_performance
from fantasy.espn.regularSeason import get_all_season_data, get_records, get_one_season_data
from fantasy.league import League

mod = Blueprint('espn', __name__)

@mod.route('/test')
def test():
    return {'result': 'Test'}

@mod.route('/regular-season/<int:league_id>', methods=['GET'])
def getAlltime(league_id):
    league = League(league_id)
    alltime_data = get_all_season_data(league)
    return jsonify({'owners': alltime_data})


@mod.route('/season/<int:league_id>/<int:year>', methods=['GET'])
def getSeason(league_id, year):
    league = League(league_id)
    season_data = get_one_season_data(year, league)
    return jsonify({'owners': season_data})


@mod.route('/records/<int:league_id>', methods=['GET'])
def getLeagueRecords(league_id):
    league = League(league_id)
    records = get_records(league)
    return records


@mod.route('/playoffs/<int:league_id>')
def perform(league_id):
    league = League(league_id)
    test = get_postseason_performance(league)
    return test


@mod.route('/performance/<int:league_id>')
def get_alltime_performance(league_id):
   alltime_data = get_alltime(league_id)
   return alltime_data
