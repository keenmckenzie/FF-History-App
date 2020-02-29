from flask import Flask
from flask_cors import CORS

#from fantasy import yahoo, espn
from fantasy import espn

app = Flask(__name__)
cors=CORS(app, resources={r"/*": {"origins": ["https://localhost*"]}})

#from fantasy.yahoo.routes import mod
from fantasy.espn.routes import mod

#app.register_blueprint(yahoo.routes.mod, url_prefix='/yahoo')
app.register_blueprint(espn.routes.mod, url_prefix='/espn')
