from flask import Flask

app = Flask(__name__)

from espn.leagueHistory.routes import mod

app.register_blueprint(leagueHistory.routes.mod, url_prefix = '/leagueHistory')

