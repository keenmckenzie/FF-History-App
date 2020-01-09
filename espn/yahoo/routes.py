from flask import Blueprint, jsonify, render_template, request
from requests_oauthlib import OAuth2Session
from .oauth import login
import requests

mod = Blueprint('yahoo', __name__)


@mod.route('/test', methods=['GET'])
def test_route():
    return {'result': 'Hitting the yahoo blueprint'}


@mod.route('/login')
def yahoo_login():
    return login()
