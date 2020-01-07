from flask import Blueprint, jsonify
from .models import get_postseason_performance
from espn.league import League

mod = Blueprint('postseasonHistory', __name__)


@mod.route('/performance/<int:league_id>')
def perform(league_id):
    league = League(league_id)
    test = get_postseason_performance(league)
    return test

