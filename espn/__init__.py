from flask import Flask

app = Flask(__name__)

from espn.regularSeasonHistory.routes import mod
from espn.playoffHistory.routes import mod

app.register_blueprint(regularSeasonHistory.routes.mod, url_prefix = '/regularSeason')
app.register_blueprint(playoffHistory.routes.mod, url_prefix = '/playoff')
