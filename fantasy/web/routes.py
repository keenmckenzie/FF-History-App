from flask import Blueprint, jsonify, render_template, request

mod = Blueprint('web', __name__)


@mod.route('/')
def home():
    return render_template('index.html')


@mod.route('/index')
def index():
    return render_template('index.html')


@mod.route('/contact')
def contact():
    return render_template('contact.html')


@mod.route('/history')
def leagueHistoryForm():
    return render_template('league_history_form.html')


@mod.route('/league-info')
def get_league_info():
    return render_template('history.html')
