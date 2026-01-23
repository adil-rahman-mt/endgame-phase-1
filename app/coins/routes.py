from flask import Blueprint, jsonify, request
from app.coins.models import Coins
import uuid 
import peewee

coins_bp = Blueprint("coins", __name__)

@coins_bp.get("")
def get_all_coins():
    coins = [coin for coin in Coins.select().dicts()]
    return jsonify(coins), 200

@coins_bp.get('/<id>')
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
            'message': "Invalid input for type uuid"
        }), 400

@coins_bp.post('')
def create_new_coin():
    data = request.get_json()

    if not data or 'name' not in data:
        return jsonify({'error': 'Invalid json input'}), 400
    
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
            'message': f"{data['name']} already exists"
        }), 400

@coins_bp.delete('/<id>')
def delete_a_coin(id):
    try:
        coin_to_delete = Coins.get(Coins.id == f"{id}")
        coin_to_delete.delete_instance()
        return jsonify({
            'status': "Success",
            'message': f"Coin with ID = {id} has been deleted",
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"Coin with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Input syntax error",
            'message': "Invalid input for type uuid"
        }), 400

@coins_bp.patch('/<id>')
def update_a_coin(id):
    try:
        data = request.get_json()
        coin = Coins.get(Coins.id == f"{id}")
        coin.name = data["name"]
        coin.save()
        updated_coin = Coins.get(Coins.id == f"{id}")
        return jsonify({
            "id": updated_coin.id,
            "name": updated_coin.name
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"Coin with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Input syntax error",
            'message': "Invalid input for type uuid"
        }), 400
