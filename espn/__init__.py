from flask import Flask

app = Flask(__name__)

from espn.regularSeasonHistory.routes import mod
from espn.postseasonHistory.routes import mod
from espn.alltime.routes import mod
from espn.yahoo.routes import mod

app.register_blueprint(regularSeasonHistory.routes.mod, url_prefix = '/regularSeason')
app.register_blueprint(postseasonHistory.routes.mod, url_prefix = '/playoff')
app.register_blueprint(alltime.routes.mod, url_prefix = '/alltime')
app.register_blueprint(yahoo.routes.mod, url_prefix = '/yahoo')
