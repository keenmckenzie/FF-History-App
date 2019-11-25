from flask import Blueprint, jsonify
from .models import getYearsWithLeagueId, getOwnersWithLeagueId, getSeasonData

mod = Blueprint('leagueHistory', __name__)

@mod.route('/test')
def getStuff():
   return '{"result": "Hitting leagueHistory Blueprint"}'

@mod.route('/years/<int:league_id>', methods=['GET'])
def getYearsLeagueId(league_id):
  years = getYearsWithLeagueId(league_id)
  return jsonify({'years': years})

@mod.route('/owners/<int:league_id>', methods=['GET'])
def leagueOwners(league_id):
  league_owners = getOwnersWithLeagueId(league_id)
  return jsonify({'owners': league_owners})

@mod.route('/season/<int:league_id>/<int:year>', methods=['GET'])
def getSeason(league_id, year):
  season_data = getSeasonData(league_id, year)
  return jsonify({'owners': season_data})
