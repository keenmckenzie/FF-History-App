from flask import Blueprint, jsonify

mod = Blueprint('setupLeague', __name__)

@mod.route('/test')
def getStuff():
   return '{"result": "hitting settup blueprin"}'
