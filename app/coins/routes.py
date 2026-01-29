from flask import Blueprint, jsonify, request
from app.coins.models import Coins
from app.duties.models import Duties
from app.coin_duties.models import CoinDuties
import uuid 
from peewee import JOIN
import peewee

coins_bp = Blueprint("coins", __name__)

# COINS

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
        }), 404
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
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
            'error': "Duplication error",
            'message': f"{data['name']} already exists"
        }), 409

@coins_bp.delete('/<id>')
def delete_a_coin(id):
    try:
        coin_to_delete = Coins.get_by_id(id)
        coin_to_delete.delete_instance()
        return jsonify({
            'status': "Success",
            'deleted': {
                'id': coin_to_delete.id,
                'name': coin_to_delete.name
            },
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"Coin with ID = {id} does not exist"
        }), 404
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
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
        }), 404
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400

# COIN AND DUTY RELATIONSHIPS

@coins_bp.get('/<coin_id>/duties')
def get_all_duties_for_coin(coin_id):
    try:
        query = (Duties
            .select(Duties.name)
            .join(CoinDuties, JOIN.INNER)
            .where(CoinDuties.coin_id == coin_id))
        return jsonify({
                'Coin': Coins.get_by_id(coin_id).name,
                'linked_to': [duty.name for duty in query]
            }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"A coin with ID = {coin_id} does not exist"
        }), 404
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided coin ID must be a valid UUID"
        }), 400

@coins_bp.post('/<coin_id>/duties/<duty_id>')
def add_duty_to_coin(coin_id, duty_id):
    try:
        coin = Coins.get_by_id(coin_id)
        duty = Duties.get_by_id(duty_id)
        record = CoinDuties.create(
                id=uuid.uuid4(),
                coin_id = coin_id,
                duty_id = duty_id,
            )
        return jsonify({
            'id': record.id,
            'coin_id': record.coin_id.id,
            'duty_id': record.duty_id.id,
        }), 201
    except peewee.IntegrityError as err:
        if "already exists" in err.args[0]:
            return jsonify({
                'error': "Duplication error",
                'message': f"{duty.name} is already associated with {coin.name}"
            }), 409
    except peewee.DoesNotExist as err:
        if "Model: Coins" in err.args[0]:
            return jsonify({
                'error': "Invalid ID",
                'message': f"A coin with ID = {coin_id} does not exist"
            }), 404
        if "Model: Duties" in err.args[0]:
            return jsonify({
                'error': "Invalid ID",
                'message': f"A duty with ID = {duty_id} does not exist"
            }), 404
        return jsonify({
                'error': "Unknown error",
            }), 400
    except peewee.DataError as err:
        return jsonify({
            'error': "Invalid ID format",
            'message': "IDs must be a valid UUID"
        }), 400

@coins_bp.delete('/<coin_id>/duties/<duty_id>')
def remove_duty_from_coin(coin_id, duty_id):
    try:
        Coins.get_by_id(coin_id)
        coin_name = Coins.get_by_id(coin_id).name
        Duties.get_by_id(duty_id)
        duty_name = Duties.get_by_id(duty_id).name

        record = CoinDuties.get(CoinDuties.coin_id == coin_id, CoinDuties.duty_id == duty_id)
        record.delete_instance()
        return jsonify({
                'status': "Success",
                'message': f"Removed {duty_name} from {coin_name}",
            }), 200
    except peewee.DoesNotExist as err:
        if "Model: Coins" in err.args[0]:
            return jsonify({
                'error': "Invalid ID",
                'message': f"A coin with ID = {coin_id} does not exist"
            }), 404
        if "Model: Duties" in err.args[0]:
            return jsonify({
                'error': "Invalid ID",
                'message': f"A duty with ID = {duty_id} does not exist"
            }), 404
        return jsonify({
                'error': "Record does not exist",
                'message': f"{duty_name} is not associated with {coin_name}"
            }), 404
    except peewee.DataError as err:
        return jsonify({
            'error': "Invalid ID format",
            'message': "IDs must be a valid UUID"
        }), 400