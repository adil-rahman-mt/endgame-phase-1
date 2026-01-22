from flask import Flask, jsonify
from models import Coins
from database import db

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to Endgame: Phase 1'

@app.before_request
def _db_connect():
    if db.is_closed():
        db.connect()

@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()

@app.get('/coins')
def get_all_coins():
    coins = [coin for coin in Coins.select().dicts()]
    return jsonify(coins)