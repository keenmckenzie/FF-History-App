from flask import Blueprint, jsonify
from .models import get_one_season_data, get_all_season_data, get_records
from espn.league import League

mod = Blueprint('regularSeasonHistory', __name__)


@mod.route('/season/<int:league_id>/<int:year>', methods=['GET'])
def getSeason(league_id, year):
    league = League(league_id)
    season_data = get_one_season_data(year, league)
    return jsonify({'owners': season_data})


@mod.route('/performance/<int:league_id>', methods=['GET'])
def getAlltime(league_id):
    league = League(league_id)
    alltime_data = get_all_season_data(league)
    return jsonify({'owners': alltime_data})


@mod.route('/records/<int:league_id>', methods=['GET'])
def getLeagueRecords(league_id):
    league = League(league_id)
    records = get_records(league)
    return records
