from flask import Flask, jsonify, request
from models import Coins
from database import db
import uuid 
import peewee

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
    return jsonify(coins), 200

@app.get('/coins/<id>')
def get_coin_by_id(id):
    try:
        coin = Coins.get_by_id(id)
        return jsonify({
            'id': coin.id,
            'name': coin.name
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"Coin with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Input syntax error",
            'message': "Invalid input"
        }), 400

@app.post('/coins')
def create_new_coin():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    
    try:
        new_coin = Coins.create(
            id=uuid.uuid4(),
            name=data['name'],
        )
        return jsonify({
            'id': new_coin.id,
            'name': new_coin.name,
        }), 201
    except peewee.IntegrityError:
        return jsonify({
            'error': "Integrity error",
            'message': f"{data["name"]} already exists"
        }), 400

@app.delete('/coins/<id>')
def delete_a_coin(id):
    try:
        coin_to_delete = Coins.get(Coins.id == f"{id}")
        coin_to_delete.delete_instance()
        return jsonify({
            'status': "Success",
            'message': f"Coin with ID = {id} has been deleted",
        }), 200
    except Coins.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"Coin with ID = {id} does not exist"
        }), 400

