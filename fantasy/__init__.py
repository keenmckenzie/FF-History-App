from flask import Flask
from flask_cors import CORS

from fantasy import api, web

app = Flask(__name__)
cors=CORS(app, resources={r"/*": {"origins": ["https://localhost*"]}})

from fantasy.api.routes import mod
from fantasy.web.routes import mod

app.register_blueprint(api.routes.mod, url_prefix='/api')
app.register_blueprint(web.routes.mod)
