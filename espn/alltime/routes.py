from flask import Blueprint, jsonify
from .models import get_alltime

mod = Blueprint('alltime', __name__)

@mod.route('performance/<int:league_id>')
def get_alltime_performance(league_id):
   alltime_data = get_alltime(league_id)
   return alltime_data

