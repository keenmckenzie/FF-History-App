from flask import Flask

app = Flask(__name__)

from espn.leagueHistory.routes import mod
from espn.setupLeague.routes import mod

app.register_blueprint(leagueHistory.routes.mod, url_prefix = '/leagueHistory')
app.register_blueprint(setupLeague.routes.mod, url_prefix = '/setup')

