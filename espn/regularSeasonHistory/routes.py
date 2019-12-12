from flask import Blueprint, jsonify
from .models import get_years_with_league_id, get_owners_with_league_id, get_season_data, get_all_time_data, get_records

mod = Blueprint('regularSeasonHistory', __name__)

@mod.route('/test')
def getStuff():
   return '{"result": "Hitting regularSeasonHistory Blueprint"}'

@mod.route('/years/<int:league_id>', methods=['GET'])
def getYearsLeagueId(league_id):
  years = get_years_with_league_id(league_id)
  return jsonify({'years': years})

@mod.route('/owners/<int:league_id>', methods=['GET'])
def leagueOwners(league_id):
  league_owners = get_owners_with_league_id(league_id)
  return jsonify({'owners': league_owners})

@mod.route('/season/<int:league_id>/<int:year>', methods=['GET'])
def getSeason(league_id, year):
  season_data = get_season_data(league_id, year)
  return jsonify({'owners': season_data})

@mod.route('/alltime/<int:league_id>', methods=['GET'])
def getAlltime(league_id):
  alltime_data = get_all_time_data(league_id)
  return jsonify({'owners': alltime_data})

@mod.route('/records/<int:league_id>', methods=['GET'])
def getLeagueRecords(league_id):
  records = get_records(league_id)
  return records


