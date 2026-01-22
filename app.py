from flask import Flask, jsonify, request
from models import Coins
from database import db
import uuid 

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

@app.post('/coins')
def create_new_coin():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    new_coin = Coins.create(
        id=uuid.uuid4(),
        name=data['name'],
    )
    return jsonify({
        'id': new_coin.id,
        'name': new_coin.name,
    }), 201