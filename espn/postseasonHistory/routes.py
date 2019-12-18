from flask import Blueprint, jsonify
from .models import get_owners_with_league_id, get_teams_with_league_id, get_postseason_performance

mod = Blueprint('postseasonHistory', __name__)

@mod.route('/test')
def test():
   return {'result': 'Hitting postseason blueprint'}

@mod.route('/owners/<int:league_id>')
def owners(league_id):
   owners = get_owners_with_league_id(league_id)
   return owners

@mod.route('/teams/<int:league_id>')
def teams(league_id):
   teams = get_teams_with_league_id(league_id)
   return teams

@mod.route('/performance/<int:league_id>')
def perform(league_id):
   test = get_postseason_performance(league_id)
   return test

