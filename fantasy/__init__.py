from flask import Flask

from fantasy import yahoo, espn

app = Flask(__name__)

from fantasy.yahoo.routes import mod
from fantasy.espn.routes import mod

app.register_blueprint(yahoo.routes.mod, url_prefix='/yahoo')
app.register_blueprint(espn.routes.mod, url_prefix='/espn')
