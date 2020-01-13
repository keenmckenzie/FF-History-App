from flask import Blueprint, jsonify, render_template, request
from requests_oauthlib import OAuth2Session
from .oauth import login, auth
import requests

mod = Blueprint('yahoo', __name__)


@mod.route('/login')
def yahoo_login():
    return login()

@mod.route('/login/redirect')
def redirect():
    redirect_response = request.url
    r =  auth(redirect_response)
    return r.content
