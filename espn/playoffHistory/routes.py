from flask import Blueprint, jsonify


mod = Blueprint('playoffHistory', __name__)

@mod.route('/test')
def test():
   return {'result': 'Hitting playoff blueprint'}

