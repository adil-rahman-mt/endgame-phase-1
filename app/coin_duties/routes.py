from flask import Blueprint, jsonify, request
from app.coin_duties.models import CoinDuties
import uuid 
import peewee

coin_duties_bp = Blueprint("coin_duties", __name__)

@coin_duties_bp.get("")
def get_all():
    coin_duties = [coin_duty for coin_duty in CoinDuties.select().dicts()]
    return jsonify(coin_duties), 200

@coin_duties_bp.get('/<id>')
def get_by_id(id):
    try:
        record = CoinDuties.get_by_id(id)
        return jsonify({
            'id': record.id,
            'coin_id': record.coin_id.id,
            'duty_id': record.duty_id.id,
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"A record with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400

@coin_duties_bp.post('')
def create():
    data = request.get_json()

    if not data or 'coin_id' not in data or 'duty_id' not in data:
        return jsonify({'error': 'Invalid json input'}), 400
    
    try:
        record = CoinDuties.create(
            id=uuid.uuid4(),
            coin_id=data['coin_id'],
            duty_id=data['duty_id']
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
                'message': "This record already exists"
            }), 400
        if "not present in table" in err.args[0]:
            return jsonify({
                'error': "Input error",
                'message': f"{err.args[0].split('DETAIL:')[-1][2:-1]}"
            }), 400
        return jsonify({
                'error': "Unknown error",
            }), 400
    except peewee.DataError as err:
        return jsonify({
            'error': "Invalid ID format",
            'message': "IDs must be a valid UUID"
        }), 400

@coin_duties_bp.delete('/<id>')
def delete(id):
    try:
        record = CoinDuties.get_by_id(id)
        record.delete_instance()
        return jsonify({
            'status': "Success",
            'deleted': {
                'id': record.id,
                'coin_id': record.coin_id.id,
                'duty_id': record.duty_id.id
            },
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"A record with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400

@coin_duties_bp.patch('/<id>')
def update(id):
    try:
        data = request.get_json()
        record = CoinDuties.get_by_id(id)

        if 'coin_id' in data:
            record.coin_id = data["coin_id"]
        if 'duty_id' in data:
            record.duty_id = data["duty_id"]
        
        record.save()
        updated_record = CoinDuties.get_by_id(id)

        return jsonify({
            "id": updated_record.id,
            "coin_id": updated_record.coin_id.id,
            "duty_id": updated_record.duty_id.id
        }), 200
    except peewee.DoesNotExist:
        return jsonify({
            'error': "Database error",
            'message': f"A record with ID = {id} does not exist"
        }), 400
    except peewee.DataError:
        return jsonify({
            'error': "Invalid ID format",
            'message': "The provided ID must be a valid UUID"
        }), 400
