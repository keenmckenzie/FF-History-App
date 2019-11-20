from flask import Blueprint, jsonify
from .models import getYearsWithLeagueId, getOwnersWithLeagueId

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



